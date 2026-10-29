# Bootstrap review

Date: 2026-10-11. Scope: Docker, API, and research skills, the SDD workflow, parallel worktrees, vendored Superpowers, and Gitflow.

## Result

An independent read-only review was completed, followed by fixes and a second review. No findings remain in the reviewed scope. The checks cover scripts, the workflow, and startup. Real inference is still untested, because no GGUF model was supplied.

## Fixed findings

1. P2: literal path comparison allowed conflicts such as `src/./client.py` and `src/client.py`, or the root `.` against a file. The validator now normalizes paths, handles the root, and rejects globs. Tests cover aliases, the root, directories, and sequential tasks.
2. P3: a concurrent listing could read claim JSON that was not yet complete. The claim is now written to a temporary file and published complete through an exclusive hard link. The listing tolerates a removal after the glob. Deterministic tests cover a partial write, a concurrent removal, and a race for double ownership.

The second review confirmed both fixes and found no related regressions.

## Checks

- 24 tests passed. They cover generation and the preservation of files, configuration, and symlinks. They also cover independent skill copies, the HTTP client, local URLs, and errors. The rest cover the DAG, collisions, parallel claims, safe cleanup, and release metadata.
- The three project skills passed the `quick_validate.py` validator of skill-creator and the project checker.
- Superpowers: 76 source files with hashes and 9 executable files matched the lock. 15 skills are available to Codex and Claude through local links.
- Bash and YAML are valid. The generated Compose file is valid.
- The CPU image was built, and the container started on `127.0.0.1:18765`. `/health` returned 200, with the database available, 207 registered tools, and `model_loaded=false`. `/ui` and `/openapi.json` returned 200, with 351 routes in the schema.
- `ready` returned 1 because no GGUF model was present, as expected. No real inference response is claimed.
- On this host, `no-new-privileges` prevented process execution in Docker. A controlled test isolated this option as the cause, and the option was removed from the template. The user's daemon and host were not changed.
- The test container was stopped and removed. Local data was kept, and the runtime port was set back to 8000. Git ignores data, models, and runtime files.

## Order and authorization review

Research → tech-planner → Superpowers execution skill → review and checks → Gitflow. The library does not change this order and does not repeat authorizations that the user already gave. Independent tasks run in parallel only with different files. One coordinator integrates work and updates the plan. Claims are local to the clone and do not replace coordination between machines.

The user authorized the first publication of the repository. Future tags and releases follow the documented flow and are not published as a side effect of the bootstrap. Branch protections are described as a recommendation, with no claim that they are applied automatically.

## Publication

Public repository created at [NelsonPrates/local-layla](https://github.com/NelsonPrates/local-layla), with `main` and `develop`. The [bootstrap CI on main](https://github.com/NelsonPrates/local-layla/actions/runs/38179536407) passed, including the 24 tests and the Compose check on the GitHub runner. No tag or GitHub Release was created.
