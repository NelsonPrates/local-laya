#!/usr/bin/env python3
"""Mede uma instância Layla: cada pergunta é enviada uma única vez e o resultado vira uma linha JSONL."""
import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

# O otimizador de prompt do upstream reescreve pedidos de "planning" neste formato; achá-lo na resposta
# diz que o pedido perdeu a forma, não que o modelo errou.
PLAN_SHAPE = re.compile(r"estimated effort|success criteria|mitigation|^\s*(step\s*\d|\d+\.\s+\*\*)", re.I | re.M)
LOG_MARKERS = re.compile(r"tool=[a-z_]+|hit runtime limit")


def local_url(value):
    parsed = urllib.parse.urlparse(value)
    if parsed.scheme != "http" or parsed.hostname not in {"127.0.0.1", "localhost", "::1"}:
        raise argparse.ArgumentTypeError("use uma URL http de loopback")
    return value.rstrip("/")


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def post(base_url, path, payload, timeout):
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(base_url + path, data=data, headers={"Content-Type": "application/json", "Accept": "application/json"})
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
    with opener.open(req, timeout=timeout) as response:
        return json.load(response)


def load_average():
    try:
        with open("/proc/loadavg", encoding="ascii") as handle:
            return [float(value) for value in handle.read().split()[:3]]
    except OSError:
        return None


def log_counts(container, since):
    if not container:
        return None
    try:
        logs = subprocess.run(["docker", "logs", "--since", since, container], capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"error": str(exc)}
    counts = {}
    for hit in LOG_MARKERS.findall(logs.stdout + logs.stderr):
        counts[hit] = counts.get(hit, 0) + 1
    return counts


def judge(question, answer):
    words = len(answer.split())
    verdict = {"words": words, "plan_shaped": bool(PLAN_SHAPE.search(answer))}
    expect = question.get("expect")
    if expect:
        verdict["expect_found"] = re.search(rf"(?<![A-Za-z]){re.escape(expect)}(?![A-Za-z])", answer) is not None
    return verdict


def read_records(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def run(args):
    with open(args.questions, encoding="utf-8") as handle:
        questions = json.load(handle)
    done = {(record["label"], record["id"]) for record in read_records(args.out)}
    status = 0
    for question in questions:
        key = (args.label, question["id"])
        if key in done:
            # Um POST que já tem registro nunca é reenviado: a instância pode tê-lo processado.
            print(f"{question['id']}: já registrado em {args.label}, não reenviado", file=sys.stderr)
            continue
        payload = {"message": question["message"], "allow_write": False, "allow_run": False, "stream": False, "workspace_root": "/workspace"}
        for field in ("aspect_id", "project_id", "conversation_id", "context"):
            if question.get(field):
                payload[field] = question[field]
        since = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        record = {"label": args.label, "id": question["id"], "started_at": since, "load_before": load_average()}
        start = time.monotonic()
        try:
            data = post(args.base_url, "/agent", payload, args.timeout)
        except (urllib.error.URLError, OSError, ValueError) as exc:
            data = {"error": str(exc)}
            status = 1
        record["seconds"] = round(time.monotonic() - start, 1)
        record["load_after"] = load_average()
        answer = data.get("response") or ""
        record.update({"aspect": data.get("aspect"), "response": answer, "error": data.get("error")})
        record.update(judge(question, answer))
        record["log"] = log_counts(args.container, since)
        with open(args.out, "a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
        print(f"{question['id']}: {record['seconds']} s, {record['words']} palavras, erro={record['error']}", file=sys.stderr)
    return status


def compare(args):
    records = read_records(args.results)
    labels = list(dict.fromkeys(record["label"] for record in records))
    by_key = {(record["label"], record["id"]): record for record in records}
    ids = list(dict.fromkeys(record["id"] for record in records))
    print("| pergunta | " + " | ".join(labels) + " |")
    print("|---|" + "---|" * len(labels))
    for qid in ids:
        cells = []
        for label in labels:
            record = by_key.get((label, qid))
            if record is None:
                cells.append("—")
                continue
            parts = [f"{record['seconds']} s", f"{record['words']} pal."]
            if "expect_found" in record:
                parts.append("certa" if record["expect_found"] else "errada")
            if record["plan_shaped"]:
                parts.append("forma de plano")
            if record.get("error"):
                parts.append("erro")
            if record.get("load_before"):
                parts.append(f"carga {record['load_before'][0]}")
            cells.append(", ".join(parts))
        print(f"| {qid} | " + " | ".join(cells) + " |")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", type=local_url, default=local_url(os.environ.get("LAYLA_BASE_URL", "http://127.0.0.1:8000")))
    sub = parser.add_subparsers(dest="command", required=True)
    runner = sub.add_parser("run", help="enviar cada pergunta uma vez e anexar o resultado")
    runner.add_argument("questions", help="JSON: lista de {id, message, expect?, aspect_id?, project_id?, context?}")
    runner.add_argument("--out", required=True, help="arquivo JSONL de resultados (anexado)")
    runner.add_argument("--label", required=True, help="nome da rodada, ex.: antes, depois-sufixo")
    runner.add_argument("--timeout", type=float, default=1000)
    runner.add_argument("--container", default="", help="nome do container para contar tool= e limites nos logs")
    table = sub.add_parser("compare", help="tabela por pergunta e rodada")
    table.add_argument("results")
    args = parser.parse_args(argv)
    return run(args) if args.command == "run" else compare(args)


if __name__ == "__main__":
    sys.exit(main())
