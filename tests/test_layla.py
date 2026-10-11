import contextlib
import http.server
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SETUP = ROOT / "skills/layla-docker/scripts/setup.py"
CLIENT = ROOT / "skills/layla-local/scripts/layla_client.py"
spec = importlib.util.spec_from_file_location("layla_client", CLIENT)
client = importlib.util.module_from_spec(spec)
spec.loader.exec_module(client)


def run(*args, **kwargs):
    return subprocess.run([sys.executable, *map(str, args)], capture_output=True, text=True, **kwargs)


class SetupTests(unittest.TestCase):
    def test_generate_independent_runtime_with_model(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            model = root / "modelo com espaço.gguf"
            model.write_bytes(b"GGUFtest-fixture")
            output = root / "instalacao independente"
            result = run(SETUP, "--output", output, "--model", model, "--port", "8123")
            self.assertEqual(result.returncode, 0, result.stderr)
            config = json.loads((output / "data/runtime_config.json").read_text())
            self.assertEqual(config["model_filename"], model.name)
            self.assertEqual(config["models_dir"], "/data/models")
            self.assertEqual(config["sandbox_root"], "/workspace")
            self.assertEqual((output / "models" / model.name).read_bytes(), model.read_bytes())
            self.assertIn("LAYLA_PORT=8123", (output / ".env").read_text())
            self.assertTrue(os.access(output / "layla", os.X_OK))
            self.assertIn("**", (output / ".dockerignore").read_text())
            help_result = subprocess.run([str(output / "layla"), "help"], capture_output=True, text=True)
            self.assertEqual(help_result.returncode, 0)
            self.assertIn("approve ID", help_result.stdout)

    def test_second_generation_preserves_existing_configuration(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "runtime"
            self.assertEqual(run(SETUP, "--output", output).returncode, 0)
            config_path = output / "data/runtime_config.json"
            config_path.write_text('{"custom":"preserve"}')
            before = {p.relative_to(output): p.read_bytes() for p in output.rglob("*") if p.is_file()}
            result = run(SETUP, "--output", output)
            self.assertNotEqual(result.returncode, 0)
            after = {p.relative_to(output): p.read_bytes() for p in output.rglob("*") if p.is_file()}
            self.assertEqual(before, after)

    def test_invalid_model_or_revision_has_no_side_effects(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "runtime"
            model = Path(tmp) / "fake.gguf"
            model.write_bytes(b"not a GGUF")
            for extra in (("--model", model), ("--revision", "master"), ("--port", "80")):
                result = run(SETUP, "--output", output, *extra)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(output.exists())

    def test_dangling_configuration_symlink_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            output = root / "runtime"
            output.mkdir()
            external = root / "external-env"
            (output / ".env").symlink_to(external)
            self.assertNotEqual(run(SETUP, "--output", output).returncode, 0)
            self.assertTrue((output / ".env").is_symlink())
            self.assertFalse(external.exists())

    def test_installed_skills_are_self_contained_and_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "skills"
            installer = ROOT / "scripts/install-skills.py"
            self.assertEqual(run(installer, "--target", target).returncode, 0)
            copied = target / "layla-docker/scripts/setup.py"
            output = Path(tmp) / "runtime"
            self.assertEqual(run(copied, "--output", output).returncode, 0)
            self.assertTrue((target / "project-research/SKILL.md").is_file())
            qa = target / "project-qa"
            self.assertFalse(qa.is_symlink())
            for resource in ("SKILL.md", "agents/openai.yaml", "references/test-matrix.md", "references/report-template.md"):
                self.assertTrue((qa / resource).is_file(), resource)
            self.assertEqual(run(target / "layla-local/scripts/layla_client.py", "--help").returncode, 0)
            existing = target / "layla-local/SKILL.md"
            existing.write_text("preserve existing skill")
            self.assertNotEqual(run(installer, "--target", target).returncode, 0)
            self.assertEqual(existing.read_text(), "preserve existing skill")

    def test_existing_qa_skill_prevents_partial_installation(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "skills"
            existing = target / "project-qa/SKILL.md"
            existing.parent.mkdir(parents=True)
            existing.write_text("custom QA instructions")
            installer = ROOT / "scripts/install-skills.py"
            self.assertNotEqual(run(installer, "--target", target).returncode, 0)
            self.assertEqual(existing.read_text(), "custom QA instructions")
            self.assertEqual(sorted(path.name for path in target.iterdir()), ["project-qa"])


class ApiHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_GET(self):
        self.server.paths.append(self.path)
        if self.path == "/redirect":
            self.send_response(302)
            self.send_header("Location", "http://example.com/")
            self.end_headers()
            return
        self.send_response(self.server.status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(self.server.reply).encode())

    def do_POST(self):
        self.server.payload = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        self.do_GET()


class ClientTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), ApiHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.thread.join()
        cls.server.server_close()

    def setUp(self):
        self.server.reply = {"model_loaded": True}
        self.server.status = 200
        self.server.paths = []

    def invoke(self, *args):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return client.main(["--base-url", self.url, *args])

    def test_ask_preserves_unicode_and_disables_execution(self):
        text = 'Olá\n"aspas" e $(sem executar)'
        self.server.reply = {"response": "Resposta do teste", "conversation_id": "c-42"}
        with patch.dict(os.environ, {"http_proxy": "http://127.0.0.1:1", "HTTP_PROXY": "http://127.0.0.1:1"}):
            self.assertEqual(self.invoke("ask", text, "--context", "contexto", "--conversation-id", "c-42"), 0)
        payload = self.server.payload
        self.assertEqual(payload["message"], text)
        self.assertEqual(payload["conversation_id"], "c-42")
        self.assertFalse(payload["allow_write"])
        self.assertFalse(payload["allow_run"])
        self.assertFalse(payload["stream"])
        self.assertEqual(self.server.paths, ["/agent"])

    def test_health_is_distinct_from_ready(self):
        self.server.reply = {"model_loaded": False, "status": "ok"}
        self.assertEqual(self.invoke("health"), 0)
        self.assertEqual(self.invoke("ready"), 1)
        self.server.reply["model_loaded"] = True
        self.assertEqual(self.invoke("ready"), 0)

    def test_http_and_semantic_errors_fail_without_retry(self):
        self.server.status = 422
        self.assertEqual(self.invoke("ask", "test"), 1)
        self.assertEqual(self.server.paths, ["/agent"])
        self.server.status = 200
        self.server.reply = {"ok": False, "error": "model not loaded"}
        self.assertEqual(self.invoke("ask", "test"), 1)

    def test_invalid_destinations_are_rejected(self):
        for url in ("https://127.0.0.1:8000", "http://example.com", "http://user:pass@localhost", "http://localhost/a", "http://127.0.0.1:99999", "http://localhost?x=1"):
            with self.assertRaises(Exception):
                client.local_url(url)
        self.assertEqual(client.local_url("http://[::1]:8000"), "http://[::1]:8000")

    def test_redirects_are_not_followed(self):
        with self.assertRaises(Exception):
            client.request(self.url, "/redirect")
        self.assertEqual(self.server.paths, ["/redirect"])

    def test_stdin_message(self):
        with patch("sys.stdin", io.StringIO("texto\nmultilinha")):
            self.assertEqual(self.invoke("ask", "-"), 0)
        self.assertEqual(self.server.payload["message"], "texto\nmultilinha")


if __name__ == "__main__":
    unittest.main()
