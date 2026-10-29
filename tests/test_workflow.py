import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


planner = load("check_plan", "check-plan.py")
release = load("check_release", "check-release.py")
worktrees = load("worktree_helpers", "worktree.py")


class PlanTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.folder = Path(self.temp.name)
        for name in ("research.md", "spec.md", "plan.md"):
            (self.folder / name).write_text("Test artifact")
        self.plan = {"change":"test","research":"research.md","spec":"spec.md","plan":"plan.md","execution_skill":"executing-plans","tasks":[]}

    def tearDown(self):
        self.temp.cleanup()

    def task(self, task_id, deps=(), files=None, estimate=10):
        return {"id":task_id,"title":"Deliver behavior","owner":"unassigned","depends_on":list(deps),"files":files or [f"src/{task_id}.py"],"estimate_minutes":estimate,"acceptance":"Observable result","verify":"python3 -m unittest"}

    def test_dependencies_precede_dependents_and_short_ready_task_first(self):
        self.plan["tasks"] = [self.task("T03", ("T01", "T02")), self.task("T01", estimate=20), self.task("T02", estimate=5)]
        self.assertEqual(planner.validate(self.plan, self.folder), ["T02", "T01", "T03"])

    def test_cycle_unknown_dependency_and_duplicate_rejected(self):
        cases = [
            [self.task("T01", ("T02",)), self.task("T02", ("T01",))],
            [self.task("T01", ("T99",))],
            [self.task("T01"), self.task("T01")],
        ]
        for tasks in cases:
            self.plan["tasks"] = tasks
            with self.assertRaises(ValueError):
                planner.validate(self.plan, self.folder)

    def test_parallel_write_overlap_rejected_but_sequential_allowed(self):
        self.plan["tasks"] = [self.task("T01", files=["src/"]), self.task("T02", files=["src/client.py"])]
        with self.assertRaises(ValueError):
            planner.validate(self.plan, self.folder)
        self.plan["tasks"][1]["depends_on"] = ["T01"]
        self.assertEqual(planner.validate(self.plan, self.folder), ["T01", "T02"])

    def test_missing_research_or_undefined_execution_rejected(self):
        self.plan["tasks"] = [self.task("T01")]
        self.plan["execution_skill"] = "guess-and-code"
        with self.assertRaises(ValueError):
            planner.validate(self.plan, self.folder)
        self.plan["execution_skill"] = "executing-plans"
        (self.folder / "research.md").unlink()
        with self.assertRaises(ValueError):
            planner.validate(self.plan, self.folder)

    def test_equivalent_paths_root_and_globs_cannot_hide_parallel_writes(self):
        for paths in (("src/./client.py", "src/client.py"), (".", "src/client.py"), ("src//client.py", "src/client.py"), ("src/*.py", "src/client.py")):
            self.plan["tasks"] = [self.task("T01", files=[paths[0]]), self.task("T02", files=[paths[1]])]
            with self.assertRaises(ValueError):
                planner.validate(self.plan, self.folder)


class WorktreeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name)
        self.git("init", "-b", "develop")
        self.git("config", "user.name", "Test User")
        self.git("config", "user.email", "test@example.invalid")
        (self.repo / ".gitignore").write_text(".worktrees/\n")
        folder = self.repo / "docs/sdd/test"
        folder.mkdir(parents=True)
        (folder / "plan.json").write_text(json.dumps({"tasks":[{"id":"T01","owner":"unassigned"},{"id":"T02","owner":"unassigned"}]}))
        self.git("add", ".")
        self.git("commit", "-m", "Plan test work")

    def tearDown(self):
        self.temp.cleanup()

    def git(self, *args, cwd=None):
        return subprocess.check_output(["git", *args], cwd=cwd or self.repo, text=True, stderr=subprocess.PIPE).strip()

    def command(self, action, task="T01", agent="codex-1", cwd=None):
        args = [sys.executable, str(ROOT / "scripts/worktree.py"), action]
        if action != "list":
            args += ["--change", "test", "--task", task, "--agent", agent]
        return subprocess.run(args, cwd=cwd or self.repo, capture_output=True, text=True)

    def test_parallel_agents_have_distinct_worktrees_and_shared_registry(self):
        first = self.command("start")
        self.assertEqual(first.returncode, 0, first.stderr)
        one = Path(json.loads(first.stdout)["worktree"])
        second = self.command("start", "T02", "claude-1", cwd=one)
        self.assertEqual(second.returncode, 0, second.stderr)
        two = Path(json.loads(second.stdout)["worktree"])
        self.assertNotEqual(one, two)
        records = json.loads(self.command("list", cwd=two).stdout)
        self.assertEqual({record["agent"] for record in records}, {"codex-1", "claude-1"})
        self.assertNotEqual(self.command("finish", agent="claude-1").returncode, 0)
        self.assertTrue(one.exists())
        self.assertEqual(self.command("finish").returncode, 0)
        self.assertEqual(self.command("finish", "T02", "claude-1").returncode, 0)

    def test_concurrent_claim_of_same_task_has_exactly_one_owner(self):
        processes = [subprocess.Popen([sys.executable,str(ROOT / "scripts/worktree.py"),"start","--change","test","--task","T01","--agent",agent],cwd=self.repo,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True) for agent in ("codex-1", "claude-1")]
        results = [process.communicate(timeout=30) for process in processes]
        self.assertEqual(sorted(process.returncode for process in processes), [0, 1], results)
        self.assertEqual(len(json.loads(self.command("list").stdout)), 1)

    def test_dirty_or_unintegrated_work_is_not_removed(self):
        started = self.command("start")
        path = Path(json.loads(started.stdout)["worktree"])
        (path / "unfinished.txt").write_text("work in progress")
        self.assertNotEqual(self.command("finish").returncode, 0)
        self.git("add", ".", cwd=path)
        self.git("commit", "-m", "Unintegrated work", cwd=path)
        self.assertNotEqual(self.command("finish").returncode, 0)
        self.assertTrue(path.exists())
        self.git("merge", "--no-ff", self.git("rev-parse", "HEAD", cwd=path), "-m", "Integrate")
        self.assertEqual(self.command("finish").returncode, 0)


class ReleaseTests(unittest.TestCase):
    def test_valid_tag_and_matching_notes(self):
        release.validate("v0.1.0", "0.1.0\n", "# Changelog\n\n## 0.1.0\n\n- Feature\n")

    def test_mismatch_bad_semver_and_missing_notes_fail(self):
        for tag, version, notes in (("v0.2.0", "0.1.0", "## 0.1.0"), ("v01.1.0", "01.1.0", "## 01.1.0"), ("v0.1.0", "0.1.0", "## 0.2.0")):
            with self.assertRaises(ValueError):
                release.validate(tag, version, notes)

    def test_skill_discovery_links_and_vendor_integrity(self):
        for provider in (".agents", ".claude"):
            for name in ("project-research", "project-qa", "layla-docker", "layla-local", "executing-plans", "subagent-driven-development", "asd-ste100"):
                self.assertTrue((ROOT / provider / "skills" / name / "SKILL.md").is_file())
        result = subprocess.run([sys.executable, str(ROOT / "scripts/check-vendor.py")], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_prompt_files_pass_ste_lint(self):
        result = subprocess.run([sys.executable, str(ROOT / "scripts/check-style.py")], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_changed_vendor_file_fails_integrity_check(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / "repo"
            (copy / "scripts").mkdir(parents=True)
            (copy / "scripts/check-vendor.py").write_bytes((ROOT / "scripts/check-vendor.py").read_bytes())
            subprocess.run(["cp", "-r", str(ROOT / "vendor"), str(copy / "vendor")], check=True)
            (copy / "vendor/asd-ste100/SKILL.md").write_text("changed")
            result = subprocess.run([sys.executable, str(copy / "scripts/check-vendor.py")], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("asd-ste100", result.stderr)


class AtomicClaimTests(unittest.TestCase):
    def test_listing_during_partial_write_sees_only_complete_claim(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            claim = folder / "task.json"
            halfway, proceed = threading.Event(), threading.Event()
            errors = []

            def slow_dump(record, stream, **kwargs):
                stream.write('{"task":')
                stream.flush()
                halfway.set()
                if not proceed.wait(timeout=10):
                    raise RuntimeError("Test timed out")
                stream.write('"T01"}')

            def writer():
                try:
                    worktrees.publish_claim(claim, {"task": "T01"})
                except Exception as error:
                    errors.append(error)

            with patch.object(worktrees.json, "dump", side_effect=slow_dump):
                thread = threading.Thread(target=writer)
                thread.start()
                try:
                    self.assertTrue(halfway.wait(timeout=5))
                    self.assertEqual(worktrees.read_claims(folder), [])
                finally:
                    proceed.set()
                    thread.join(timeout=10)
            self.assertFalse(errors)
            self.assertEqual(worktrees.read_claims(folder), [{"task": "T01"}])
            self.assertEqual(list(folder.glob("*.tmp")), [])

    def test_listing_tolerates_claim_removed_after_glob(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            claim = folder / "task.json"
            worktrees.publish_claim(claim, {"task": "T01"})
            original = Path.read_text

            def remove_before_read(path, *args, **kwargs):
                if path == claim:
                    path.unlink()
                return original(path, *args, **kwargs)

            with patch.object(Path, "read_text", remove_before_read):
                self.assertEqual(worktrees.read_claims(folder), [])


if __name__ == "__main__":
    unittest.main()
