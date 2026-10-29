#!/usr/bin/env python3
"""Run the vendored ASD-STE100 linter on the skill, agent, and prompt files."""
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
linter = root / "vendor/asd-ste100/scripts/ste-lint.py"
# Strict scope from AGENTS.md. The linter reads Markdown and plain text.
# It reads a YAML file as one sentence, so review agents/openai.yaml manually.
files = [
    root / "AGENTS.md",
    root / "CLAUDE.md",
    root / "docs/workflow/tech-planner.md",
    root / "docs/workflow/qa-test.md",
    *sorted((root / ".claude/agents").glob("*.md")),
    *sorted((root / ".codex/agents").glob("*.toml")),
    *sorted((root / "skills").glob("*/SKILL.md")),
    *sorted((root / "skills").glob("*/references/*.md")),
]
result = subprocess.run([sys.executable, "-I", str(linter), *map(str, files)])
if result.returncode == 0:
    print(f"STE check passed: {len(files)} files")
sys.exit(result.returncode)
