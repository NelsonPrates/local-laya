# Gitflow-based releases

## Branches and integration

| Branch | Starts from | Merges into | Purpose |
| --- | --- | --- | --- |
| `main` | bootstrap | — | Stable code and public tags |
| `develop` | `main` | `release/*` | Integration of the next version |
| `feature/<change>/<task>-<agent>` | up-to-date `develop` | `develop` | One reviewable task or delivery |
| `release/X.Y.Z` | `develop` | `main`, then `develop` | Stabilization, version, notes, and fixes |
| `hotfix/X.Y.Z` | `main` | `main`, then `develop` and the active release | Urgent fix of the published line |

One coordinator integrates PRs one at a time. Use merge commits (`--no-ff`). They keep the provenance and let the worktree script confirm ancestry. If you squash, keep the merge SHA and review the equivalence before you clean up the worktree manually. `finish` refuses to run when the ancestry is missing.

Features reach `develop` with a review and a recommendation with reasons from [qa-test](qa-test.md). A failure or a blocked required check goes back to the implementer. Check the combined result again before you release dependent tasks. Reports for isolated features do not prove the combination. QA evidence applies to the tested content. To use it again, compare the diff.

## Normal release

1. Make sure that the planned PRs are merged and that CI is green on `develop`. Create `release/X.Y.Z` from an up-to-date `origin/develop`. Freeze features on this branch.
2. Update `VERSION` and `CHANGELOG.md` to the same version. Use SemVer: patch for compatible fixes, minor for compatible capabilities, and major for incompatible changes to contracts or commands.
3. Run the script and skill checks, validate Compose, and review the relevant container and inference evidence. QA checks the stabilized candidate and records the SHA, results, and limits in the `qa-report.md` of the release change. Required checks must pass. Record changes to the upstream or Superpowers revision. Open a PR from `release/X.Y.Z` to `main` and review the result.
4. After the review, and with the merge and publication authorization that applies to the session, merge into `main`. Make sure that CI is green on the final commit. Create an annotated tag **`vX.Y.Z` that points to this `main` commit** and push the tag. Do not tag the feature branch or an earlier commit.
5. The `release.yml` Action checks the tag and version, the ancestry in `main`, the notes, and the tests. Then it creates the GitHub Release with the skills archive. Pushing the tag publishes the release. It is not only a request for validation.
6. Merge `main` back into `develop` and into any active release that still needs the fixes. Run CI on the result. Then delete the completed release branch.

## Hotfix

1. Create `hotfix/X.Y.Z` from `origin/main`. Keep the research and the plan in proportion to the defect.
2. Fix the defect. Check it with a QA run of the regression scenario and the affected checks.
3. Update the version and notes, review the PR to `main`, merge it, and publish the tag as above.
4. Merge the fix into `develop` and into any active release. Check the combination again before you close the hotfix.

Do not mix pending `develop` features with the production fix.

## Automation and protection

`ci.yml` checks pushes and PRs. `release.yml` runs only on `v*` tags, and only its publish job has `contents: write`. Its check requires a SemVer version, matching notes, and a commit that is an ancestor of `main`.

Recommended GitHub settings: protect `main` and `develop`, require a PR, a review, and the `skills-and-scripts` check, block force-push and deletion, and restrict `v*` tags to the maintainer or coordinator. These settings depend on the account and repository rules. This documentation does not mean that the protection is active. The workflow cannot prevent the first push of an invalid tag. It does prevent its publication as a Release.

The bootstrap delivers `main` and `develop`, but it does not create a tag or release unless someone asks. The first publication of the repository and the publication of a version are separate actions.

## Sources

- [Gitflow, releases, and hotfixes](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)
- [Git worktree](https://git-scm.com/docs/git-worktree)
- [GitHub Actions: push and tag events](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#push)
