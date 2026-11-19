# Skill Garden

Individual, installable agent skills by V. Each directory in `skills/` is a reviewed release edition with its own instructions and supporting files. The private garden, development skills, training records and agent profiles are not distributed here.

## Take a cutting

For example, install just **brainstorm**:

| Agent | Run in your terminal |
| --- | --- |
| Hermes | `hermes skills install vrindachaa/skill-garden-skills/skills/brainstorm` |
| Claude Code | `npx skills add vrindachaa/skill-garden-skills --skill brainstorm -a claude-code` |
| Codex | `npx skills add vrindachaa/skill-garden-skills --skill brainstorm -a codex` |

For another skill, replace `brainstorm` with its directory name. Run the `npx` commands from the project you want to use the skill in. Read each skill's requirements first: installing a skill does not install external tools, configure Hermes profiles, or grant access to an API.

## Release policy

A canonical skill must explicitly opt in with the YAML boolean `metadata.published: true`. Missing, false or string values do not qualify. A public edition is reviewed separately; opting in does not automatically upload local files. Public Git history remains public even if a later release removes a skill.
