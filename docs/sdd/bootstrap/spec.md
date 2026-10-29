# Bootstrap spec

Deliver the public `NelsonPrates/local-layla` repository and the project in `~/Documentos/local-layla`.

- Self-contained skills that generate a CPU Docker installation of PapaKoftes/Layla and query the local API. Persist data, models, and the workspace. Publish the port only on loopback.
- The generator does not overwrite an existing installation. The client uses only localhost, disables write and execution permissions, and separates an available API from a ready model.
- The development and maintenance workflow starts with research, continues with the tech-planner, and then uses the selected Superpowers execution. Plans use the smallest sufficient order of clear tasks, with dependencies and checks.
- Codex and Claude read the same contract and can run independent tasks in different worktrees. Claim tasks, avoid shared files, and integrate one at a time.
- Download the official Superpowers skills at a fixed revision, with the license and verifiable integrity.
- Gitflow with main, develop, feature, release, and hotfix branches, CI, and publication automation that a tag validates. The bootstrap publishes no release tag.

Acceptance:

- valid skills and passing behavior tests
- a valid Compose file
- a real startup test, with the explicit limit of a missing GGUF model
- validated plans and an intact vendor copy
- worktrees and claims isolated in tests
- a synchronized remote repository
