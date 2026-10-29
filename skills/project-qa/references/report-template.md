# QA report: <change>

Date and agent: <UTC or explicit time zone>, <identity>. Mode: <independent or self-assessment>.
Target: <full tested SHA>. Base: <SHA>. Worktree: <clean, or the identified diff and uncommitted files>.
Environment: <OS, relevant versions, simulated or real service, prerequisites>.
Scope: <criteria and changes>. Out of scope: <reason>.

| Criterion or check | Required? | Real command or procedure | Expected | Actual result and exit code | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| <ID> | <yes/no and reason> | <command that ran, or did not run> | <observable result> | <real result, or not available> | <pass/fail/blocked/not-run> | <short output or artifact without secrets> |

## Defects and blocks

For each item, record the impact, the file or input, the minimum steps, the expected and actual results, the frequency, and the evidence. Name the next owner. If you cannot reproduce it, do not invent a cause. A defect that existed before the change stays visible. Record the comparison with the base when you make one.

## Decision

<pass/fail/blocked>, because <required criteria and defects>. List the out-of-scope checks that did not run. List the relevant residual risks. Do not record pass from the report of another agent. Do not record pass from an old run unless you checked that it still applies.

## New check

After a fix or an integration: <new SHA, relevant diff, repeated checks, and result>. If only report or control files changed, identify the diff that lets you use the evidence again. The coordinator receives the recommendation and decides the integration inside the session authorization.
