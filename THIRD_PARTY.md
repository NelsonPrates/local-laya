# Attribution

This project supplies independent scripts and instructions to integrate
[PapaKoftes/Layla](https://github.com/PapaKoftes/Layla), by its respective authors.
This repository does not vendor upstream Layla source code. The Dockerfile gets
the project during the build and keeps its `LICENSE` file in `/opt/layla/LICENSE`.

Layla uses the **Layla Non-Commercial Source License**. The MIT license of the
local-layla scripts does not replace it. Commercial use of Layla depends on the
terms and the authorization of its rights holders. This project uses the name
only to identify the integration. It has no official affiliation.

The user supplies GGUF models, or the app configuration downloads them. Models
stay under their own licenses. Dependencies installed in the image keep their
own licenses.

## Superpowers

`vendor/superpowers/` contains the skills from [obra/superpowers](https://github.com/obra/superpowers)
at revision `bb92a77741419a4ab5f06e711a283343f1ada0c3`. The original MIT license
is in `vendor/superpowers/LICENSE`. The source and the hashes are in
`source.lock.json`. The upstream files are not adapted. The SDD contract of this
project states its order research → plan → execution. The contract has priority
over the library defaults when they differ.

## asd-ste100

`vendor/asd-ste100/` contains the skill from [danyuchn/asd-ste100-skill](https://github.com/danyuchn/asd-ste100-skill)
at revision `8da6b6340aa22faf46fd07db8efbdea010cd38d9`. The original MIT license
is in `vendor/asd-ste100/LICENSE`. The source and the hashes are in
`source.lock.json`. The upstream files are not adapted. The copy leaves out the
upstream `.claude-plugin/` packaging metadata. The skill is inspired by
ASD-STE100. It does not include the official ASD dictionary, and it is not a
certified STE authoring tool.
