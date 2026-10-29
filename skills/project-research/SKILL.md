---
name: project-research
description: Research and record evidence before you plan local-layla development or maintenance, including upstream Layla, Docker, APIs, dependencies, and agent workflows. Use it as the first SDD step, before you propose an implementation.
---

# Research for development and maintenance

Write a `research.md` that lets the planner decide without new discovery work. Use `references/research-template.md` as the minimum format. Copy and adapt it to `docs/sdd/<change>/research.md` in the project root.

1. Read the request and the session authorization again. Identify the technical decision and the user's criteria. Limit the research to them.
2. Read `AGENTS.md`, the related files, the existing tests, the locked revisions, and the reproducible results. Search with `rg`. If no clone or upstream copy exists, read the official sources. Do not put private configuration or tokens in the public report.
3. Check version-dependent APIs and behavior in upstream code or primary documentation. Record the URL, revision or version, date of access, evidence, and implication. Keep facts, hypotheses, and technical choices separate. Run only small, reversible experiments inside the authorized scope.
4. Compare only plausible alternatives. Use the relevant criteria: simplicity, compatibility with the repository, maintenance, resources, and license. Recommend the smallest sufficient option and give its concrete cost.
5. Record the gaps that change the plan. Propose how to close each gap. Stop when the evidence is sufficient for the acceptance criteria. Do not continue the research to catalog everything.

Research does not implement the product. It does not merge, release, or download large models. Its output is evidence and a recommendation, not an approved plan. Send the output to the `docs/workflow/tech-planner.md` role when it is available. If this skill is in a different location, find that role in the target project root. Do not depend on a `../../..` path from the skill location.
