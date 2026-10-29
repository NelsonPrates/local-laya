#!/usr/bin/env python3
"""Claim tasks for agents in one clone and create isolated worktrees."""
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
        raise argparse.ArgumentTypeError("Use 1 to 64 letters, digits, or hyphens")
    return value


def publish_claim(path, record):
    """Publish the complete JSON through an exclusive hard link. Readers never see a partial write."""
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
            # finish or a rollback can remove the claim after the glob.
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
        # The first entry is the main worktree. All sessions use the same root.
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
            # Use only the plan committed on the base. Never use an edit that the
            # executors in other worktrees cannot see.
            plan = json.loads(git("show", f"{args.base}:{relative_plan}"))
            tasks = {task["id"]: task for task in plan["tasks"]}
            if args.task not in tasks:
                raise ValueError("The task is not in the committed plan. Plan the task before you claim it")
            # The base must contain the plan, so that the executor gets a visible plan.
            git("cat-file", "-e", f"{args.base}:{relative_plan}")
            if tasks[args.task].get("owner") not in ("unassigned", args.agent):
                raise ValueError("The plan assigns the task to a different owner. The coordinator must update the assignment")
            if not git("check-ignore", ".worktrees/probe", cwd=primary):
                raise ValueError(".worktrees/ must be in .gitignore")
            path = primary / ".worktrees" / args.change / f"{args.task}-{args.agent}"
            branch = f"feature/{args.change}/{args.task}-{args.agent}"
            if path.exists():
                raise ValueError(f"The worktree exists: {path}")
            claims.mkdir(parents=True, exist_ok=True)
            record = {"change":args.change,"task":args.task,"agent":args.agent,"branch":branch,"worktree":str(path),"base":args.base}
            try:
                publish_claim(claim, record)
            except FileExistsError as error:
                raise ValueError("The task has a claim. Run list. Do not remove the claim of a different session.") from error
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
            raise ValueError("Only the owner can finish this claim")
        path = Path(record["worktree"])
        if git("status", "--porcelain", cwd=path):
            raise ValueError("The worktree has changes. Keep or integrate them before you finish")
        git("merge-base", "--is-ancestor", git("rev-parse", "HEAD", cwd=path), args.base)
        git("worktree", "remove", str(path), cwd=primary)
        claim.unlink()
        print(f"Claim finished. Branch kept: {record['branch']}")
        return 0
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as error:
        detail = error.stderr.strip() if isinstance(error, subprocess.CalledProcessError) else str(error)
        print(f"Failed: {detail}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
