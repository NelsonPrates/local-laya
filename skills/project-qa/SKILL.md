---
name: project-qa
description: Plan and run QA for local-layla changes, map acceptance criteria to tests, and report evidence before integration or release. Use it during plan review and after implementation, also for regressions in scripts, skills, the local API, and Docker.
---

# QA for development and maintenance

Turn acceptance criteria into reproducible evidence. Read the request, the target project contract, the research, the spec, the plan, and the assigned diff. If this skill is installed outside the repository, look for these artifacts in the root of the target project. All resources of this skill are relative to this folder. The skill does not need a checkout or an installed Superpowers copy.

## Plan the tests

After the research, and together with the technical plan, select the smallest set of tests that finds plausible failures. Read [the matrix by change type](references/test-matrix.md). For each criterion, record the scenario, the test level, the command or procedure, the expected result, the environment, and whether it is required. Cover error and limit cases when they can cause a concrete regression. Use unittest and the existing tools. Do not add a dependency, a prose test, or a step without a demonstrated benefit.

Return the matrix to the planner or the coordinator. For a small change, the matrix can stay in the plan. For a large change, write `qa-plan.md` in the assigned SDD directory. Do not change the shared spec or plan if another agent owns them. The implementation continues with the Superpowers skill that the project plan selects.

## Check the delivery

1. Before you run tests, check the SHA and base, the diff, the scope, the environment, and the matrix. Record any uncommitted changes. If uncommitted changes exist, the SHA alone does not identify the tested content. Use a stable checkout or worktree with no other writer. For parallel tasks, get exclusive files and resources from the coordinator.
2. Run the applicable required checks. Read each result and exit code. Test observable behavior: preserved data, HTTP responses, refused conflicts, and reachable services. A mock proves only the simulated contract. It does not prove inference, Docker, or a real browser.
3. For a failure, reproduce it. Record the input, the minimum steps, the expected and actual results, the evidence, and the impact. Identify the type: product defect, test problem, or environment block. Do not guess the cause. Send the failure to the implementer. Do not change the product, weaken assertions, or retry until the result is green. Record intermittent results. After the fix, run the scenario and the affected regression again.
4. Fill in [the report](references/report-template.md) in `docs/sdd/<change>/qa-report.md`, or in the assigned path. Record the real commands, results, commit, limits, and a decision for each criterion: **pass**, **fail**, **blocked**, or **not-run**. `pass` needs current evidence. A required item without an environment or evidence is `blocked`. `not-run` needs a reason and a scope class. A green check does not replace a missing required check.
5. Recommend **pass** for integration only when all applicable required criteria and checks pass and no blocking defect is open. If a required item fails, recommend **fail**. If nothing fails but a required check is not available, recommend **blocked**. An out-of-scope item can be `not-run` with a reason. Give the report to the coordinator. QA does not merge, tag, or release.

Evidence applies only to the tested content. A later change to code, tests, configuration, or dependencies requires a new run of the affected checks. Record the new SHA. A commit that changes only the report or control files does not automatically invalidate the results. Examine the diff and explain why the evidence still applies. Check the combined result of the branches again. CI or tests of one isolated feature do not prove the combination.

## Limits and continuity

Write only the report, the matrix, and the tests that the coordinator assigns to you. Each new test must find a plausible defect. If new tests are necessary, use a separate task and worktree. Make sure that the final check includes them. A diagnosis does not authorize silent product fixes. Do not download large models, approve pending Layla actions, change credentials, or publish to a remote without the related authorization. Keep existing data. Record evidence without tokens, personal data, or private content.

The QA role checks acceptance and risk. Code review checks the implementation and stays in the existing workflow. In a session without delegation, the coordinator can apply this skill in a separate pass. The coordinator records that the pass is a self-assessment.
