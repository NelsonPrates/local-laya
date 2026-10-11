#!/usr/bin/env python3
"""Reserva tarefas entre agentes de um mesmo clone e cria worktrees isoladas."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile


def git(*args, cwd=None):
    return subprocess.check_output(["git", *args], cwd=cwd, text=True, stderr=subprocess.PIPE).strip()


def slug(value):
    if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9-]{0,63}", value):
        raise argparse.ArgumentTypeError("Use 1 a 64 letras, números ou hífens")
    return value


def publish_claim(path, record):
    """Publica JSON completo via hard link exclusivo; leitores nunca veem escrita parcial."""
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, prefix=".pending-", suffix=".tmp", delete=False) as stream:
            temporary = Path(stream.name)
            json.dump(record, stream, ensure_ascii=False, indent=2)
            stream.flush()
            os.fsync(stream.fileno())
        os.link(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def read_claims(folder):
    records = []
    for path in sorted(folder.glob("*.json")):
        try:
            records.append(json.loads(path.read_text(encoding="utf-8")))
        except FileNotFoundError:
            # finish/rollback pode remover a reserva depois do glob.
            continue
    return records


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("list")
    for name in ("start", "finish"):
        sub = commands.add_parser(name)
        sub.add_argument("--change", type=slug, required=True)
        sub.add_argument("--task", type=slug, required=True)
        sub.add_argument("--agent", type=slug, required=True)
        sub.add_argument("--base", default="develop")
    args = parser.parse_args(argv)
    try:
        common = Path(git("rev-parse", "--path-format=absolute", "--git-common-dir"))
        # O primeiro registro é a worktree principal; toda sessão usa a mesma raiz.
        primary = Path(git("worktree", "list", "--porcelain").splitlines()[0].removeprefix("worktree "))
        claims = common / "local-layla" / "claims"
        if args.command == "list":
            records = read_claims(claims)
            print(json.dumps(records, ensure_ascii=False, indent=2))
            return 0
        git("check-ref-format", "--branch", args.base)
        git("rev-parse", "--verify", args.base + "^{commit}")
        claim = claims / f"{args.change}--{args.task}.json"
        if args.command == "start":
            plan_path = primary / "docs" / "sdd" / args.change / "plan.json"
            relative_plan = plan_path.relative_to(primary).as_posix()
            # Somente o plano comprometido na base, nunca uma edição ainda invisível
            # aos executores das outras worktrees.
            plan = json.loads(git("show", f"{args.base}:{relative_plan}"))
            tasks = {task["id"]: task for task in plan["tasks"]}
            if args.task not in tasks:
                raise ValueError("Tarefa não existe no plano versionado; planeje antes de reservar")
            # A base deve conter o plano, para o executor não receber um plano invisível.
            git("cat-file", "-e", f"{args.base}:{relative_plan}")
            if tasks[args.task].get("owner") not in ("unassigned", args.agent):
                raise ValueError("O plano atribui a tarefa a outro dono; o coordenador precisa atualizar a atribuição")
            if not git("check-ignore", ".worktrees/probe", cwd=primary):
                raise ValueError(".worktrees/ precisa estar no .gitignore")
            path = primary / ".worktrees" / args.change / f"{args.task}-{args.agent}"
            branch = f"feature/{args.change}/{args.task}-{args.agent}"
            if path.exists():
                raise ValueError(f"Worktree já existe: {path}")
            claims.mkdir(parents=True, exist_ok=True)
            record = {"change":args.change,"task":args.task,"agent":args.agent,"branch":branch,"worktree":str(path),"base":args.base}
            try:
                publish_claim(claim, record)
            except FileExistsError as error:
                raise ValueError("Tarefa já reservada. Consulte list; não remova a reserva de outra sessão.") from error
            try:
                path.parent.mkdir(parents=True, exist_ok=True)
                git("worktree", "add", "-b", branch, str(path), args.base, cwd=primary)
            except Exception:
                claim.unlink()
                raise
            print(json.dumps(record, ensure_ascii=False, indent=2))
            return 0
        record = json.loads(claim.read_text(encoding="utf-8"))
        if record["agent"] != args.agent:
            raise ValueError("Somente o dono pode encerrar esta reserva")
        path = Path(record["worktree"])
        if git("status", "--porcelain", cwd=path):
            raise ValueError("A worktree tem alterações; preserve/integre antes de encerrar")
        git("merge-base", "--is-ancestor", git("rev-parse", "HEAD", cwd=path), args.base)
        git("worktree", "remove", str(path), cwd=primary)
        claim.unlink()
        print(f"Reserva encerrada. Branch preservada: {record['branch']}")
        return 0
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as error:
        detail = error.stderr.strip() if isinstance(error, subprocess.CalledProcessError) else str(error)
        print(f"Falha: {detail}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
