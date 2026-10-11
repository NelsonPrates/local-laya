#!/usr/bin/env python3
"""Cliente JSON para a API local do Layla; apenas biblioteca padrão Python."""
import argparse
import json
import math
import os
import sys
import urllib.error
import urllib.parse
import urllib.request


def local_url(value):
    try:
        parsed = urllib.parse.urlsplit(value)
        port = parsed.port
    except ValueError as error:
        raise argparse.ArgumentTypeError(str(error)) from error
    if parsed.scheme != "http" or parsed.hostname not in ("localhost", "127.0.0.1", "::1") or parsed.username or parsed.password or parsed.query or parsed.fragment or parsed.path not in ("", "/"):
        raise argparse.ArgumentTypeError("Use http://127.0.0.1:PORTA (ou localhost/::1), sem caminho ou credenciais.")
    if port is not None and not 1 <= port <= 65535:
        raise argparse.ArgumentTypeError("Porta inválida.")
    return value.rstrip("/")


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def request(base_url, path, payload=None, timeout=120):
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(base_url + path, data=data, headers={"Content-Type": "application/json", "Accept": "application/json"})
    # Não encaminhar prompts ao proxy HTTP do ambiente ou seguir redirects.
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
    with opener.open(req, timeout=timeout) as response:
        return json.load(response)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", type=local_url, default=os.environ.get("LAYLA_BASE_URL", "http://127.0.0.1:8000"))
    parser.add_argument("--timeout", type=float, default=120)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("health", "ready", "schema", "pending", "wakeup"):
        commands.add_parser(name)
    ask = commands.add_parser("ask", help="Envia uma mensagem; escrita/execução desabilitadas")
    ask.add_argument("message", help="Mensagem; use - para ler de stdin")
    ask.add_argument("--context", default="")
    ask.add_argument("--conversation-id", default="")
    args = parser.parse_args(argv)
    if not math.isfinite(args.timeout) or args.timeout <= 0:
        parser.error("--timeout deve ser positivo e finito")
    path = {"health": "/health", "ready": "/health", "schema": "/openapi.json", "pending": "/pending", "wakeup": "/wakeup"}.get(args.command)
    payload = None
    if args.command == "ask":
        message = sys.stdin.read() if args.message == "-" else args.message
        if not message.strip():
            parser.error("A mensagem não pode ser vazia")
        payload = {"message": message, "context": args.context, "conversation_id": args.conversation_id, "workspace_root": "/workspace", "allow_write": False, "allow_run": False, "stream": False}
        path = "/agent"
    try:
        result = request(args.base_url, path, payload, args.timeout)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if isinstance(result, dict) and (result.get("ok") is False or result.get("error")):
            return 1
        if args.command == "ready" and (not isinstance(result, dict) or result.get("model_loaded") is not True):
            print("API responde, mas o modelo ainda não está carregado. Verifique /ui e os logs.", file=sys.stderr)
            return 1
        return 0
    except urllib.error.HTTPError as error:
        print(f"HTTP {error.code}: {error.read(4096).decode('utf-8', errors='replace')}", file=sys.stderr)
    except (urllib.error.URLError, TimeoutError, OSError, ValueError) as error:
        print(f"Falha ao consultar Layla: {error}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
