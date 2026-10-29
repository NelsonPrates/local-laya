#!/usr/bin/env python3
"""Check each local vendored copy against its source lock."""
import hashlib
import json
from pathlib import Path
import sys

vendor = Path(__file__).resolve().parents[1] / "vendor"
failed = False
for lock_path in sorted(vendor.glob("*/source.lock.json")):
    root = lock_path.parent
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    actual = {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.rglob("*")) if p.is_file() and p.name != "source.lock.json" and "__pycache__" not in p.parts}
    executable = [p.relative_to(root).as_posix() for p in sorted(root.rglob("*")) if p.is_file() and p.stat().st_mode & 0o111]
    if actual != lock["sha256"]:
        print(f"{root.name} changed or is incomplete. Check the source and update the lock deliberately.", file=sys.stderr)
        failed = True
    elif executable != lock.get("executable", []):
        print(f"The executable permissions of {root.name} do not match the lock.", file=sys.stderr)
        failed = True
    else:
        print(f"{root.name} is intact: {lock['revision']} ({len(actual)} files)")
sys.exit(1 if failed else 0)
