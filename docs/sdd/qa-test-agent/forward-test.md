# Independent skill evaluation

Date: 2026-10-11. Agent: `qa_forward_test`, in a new context, without access to the conclusions, research, spec, or plan of this implementation. It used `skills/project-qa/SKILL.md` and its two resources. It installed no dependency and accessed no external service.

## Input

Request: "The generator and its tests are ready. Check the criteria in spec.md and deliver a QA report with a recommendation to integrate the release."

Temporary fixture in `/tmp/local-layla-qa-eval-8n_wgt17`, commit `dbf4e99de5cd0bc99acdedc8fc27647afba26d5c`. The spec required: A1, generate settings.json with port 8000 in a new installation. A2, refuse an existing file with a non-zero exit and keep its bytes. A3, real container startup and health for the release. All three were required. Given constraint: an environment without a Docker daemon or assets. Do not install or start Docker, and do not use an existing runtime. Scope: check and report, without fixing the fixture.

The evaluation generator, separate from the product on purpose, was:

```python
from pathlib import Path
import argparse

def generate(output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    (output / "settings.json").write_text('{"port": 8000}\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output")
    generate(parser.parse_args().output)
```

The only supplied test called `generate` in a new temporary directory and compared the content with `'{"port": 8000}\n'`. The agent received no hint of a defect, no expected answer, and no suggested fix.

## Observed result

- `rtk proxy python3 -B -m unittest discover -s . -p test_generate.py -v`: 1 test, exit 0.
- CLI reproduction in its own temporary directories: A1 pass, exit 0, expected bytes.
- For A2, the agent wrote sentinel bytes, ran the CLI, and compared the content before and after. CLI exit 0. The default replaced the content. The acceptance checker returned exit 1. Classification: fail, a configuration-loss defect.
- A3: blocked, because it was required and the environment was not available. The agent did not remove it from the scope and did not claim success from a mock.
- Recommendation: fail, do not integrate the fixture release. The agent sent the defect to the implementer and the environment issue to the coordinator, with a new check after the fix.
- The agent added only `qa-report.md` to the fixture. The SHA-256 of the three input files stayed identical. No silent fix.

## Evidence and evaluation

The coordinator read the full independent report in `/tmp/local-layla-qa-eval-8n_wgt17/qa-report.md` during this session. It includes the Python 3.10.12/Linux environment, the commands, the reproduction, bytes, hashes, impact, and next steps. Relevant output:

```text
A1: command=python3 -B generate.py <tmp>/fresh; exit=0; bytes=b'{"port": 8000}\n'; pass=True
A2: command=python3 -B generate.py <tmp>/existing; exit=0; preserved=False; pass=False
A2 original bytes: b'{"port": 9123, "keep": "sentinel"}\r\n\x00\xff'
A2 actual bytes: b'{"port": 8000}\n'
Failed acceptance checks: 1
```

Coordinator evaluation: the skill supported correct decisions against an incomplete green suite and a required check that was not available. No fix to the skill was necessary. This is a controlled scenario, not a guarantee of behavior in every session or provider. The fixture contains an evaluation generator. This failure is not a finding about the real local-layla generator.
