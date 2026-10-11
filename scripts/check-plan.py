#!/usr/bin/env python3
"""Valida o plano SDD e mostra uma ordem topológica curta e determinística."""
import argparse
import json
from pathlib import Path, PurePosixPath
import re


def validate(plan, folder):
    if plan.get("execution_skill") not in ("executing-plans", "subagent-driven-development"):
        raise ValueError("execution_skill precisa selecionar uma skill de execução Superpowers")
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", plan.get("change", "")):
        raise ValueError("change precisa ser um slug")
    for field in ("research", "spec", "plan"):
        path = plan.get(field, "")
        if not isinstance(path, str) or not path or not (folder / path).is_file():
            raise ValueError(f"Artefato {field} ausente: {path}")
    tasks = plan.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        raise ValueError("tasks precisa conter ao menos uma tarefa")
    indexed = {}
    for task in tasks:
        task_id = task.get("id", "")
        if not re.fullmatch(r"T[0-9]{2,}", task_id) or task_id in indexed:
            raise ValueError(f"ID inválido ou duplicado: {task_id}")
        for field in ("title", "owner", "acceptance", "verify"):
            if not isinstance(task.get(field), str) or not task[field].strip():
                raise ValueError(f"{task_id}: campo {field} ausente")
        estimate = task.get("estimate_minutes")
        if type(estimate) is not int or estimate <= 0:
            raise ValueError(f"{task_id}: estimate_minutes precisa ser inteiro positivo")
        files = task.get("files")
        if not isinstance(files, list) or not files or any(not isinstance(p, str) or not p or PurePosixPath(p).is_absolute() or ".." in PurePosixPath(p).parts for p in files):
            raise ValueError(f"{task_id}: files precisa listar caminhos relativos de escrita")
        if any(any(char in p for char in "*?[]") for p in files):
            raise ValueError(f"{task_id}: use caminhos exatos ou diretórios, sem globs")
        deps = task.get("depends_on")
        if not isinstance(deps, list) or any(not isinstance(d, str) for d in deps) or len(deps) != len(set(deps)):
            raise ValueError(f"{task_id}: depends_on inválido")
        indexed[task_id] = task
    for task_id, task in indexed.items():
        if task_id in task["depends_on"] or any(dep not in indexed for dep in task["depends_on"]):
            raise ValueError(f"{task_id}: dependência inexistente ou autorreferência")
    ancestors = {}

    def dependencies(task_id, visiting):
        if task_id in visiting:
            raise ValueError("Ciclo de dependências")
        if task_id not in ancestors:
            result = set(indexed[task_id]["depends_on"])
            for dep in indexed[task_id]["depends_on"]:
                result.update(dependencies(dep, visiting | {task_id}))
            ancestors[task_id] = result
        return ancestors[task_id]

    for task_id in indexed:
        dependencies(task_id, set())
    ids = list(indexed)
    for i, left in enumerate(ids):
        for right in ids[i + 1:]:
            if left in ancestors[right] or right in ancestors[left]:
                continue
            for a in indexed[left]["files"]:
                for b in indexed[right]["files"]:
                    a, b = PurePosixPath(a).as_posix(), PurePosixPath(b).as_posix()
                    if a == "." or b == "." or a == b or a.startswith(b + "/") or b.startswith(a + "/"):
                        raise ValueError(f"Tarefas independentes {left}/{right} escrevem caminhos sobrepostos: {a}, {b}")
    order, done = [], set()
    while len(done) < len(indexed):
        ready = [task for key, task in indexed.items() if key not in done and set(task["depends_on"]) <= done]
        ready.sort(key=lambda task: (-sum(task["id"] in deps for deps in ancestors.values()), task["estimate_minutes"], task["id"]))
        chosen = ready[0]["id"]
        order.append(chosen)
        done.add(chosen)
    return order


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    try:
        order = validate(json.loads(args.path.read_text(encoding="utf-8")), args.path.parent)
    except (OSError, ValueError, TypeError, AttributeError) as error:
        parser.exit(1, f"Plano inválido: {error}\n")
    print("Plano válido. Ordem sugerida: " + " -> ".join(order))


if __name__ == "__main__":
    main()
