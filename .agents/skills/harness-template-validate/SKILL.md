---
name: harness-template-validate
description: Validates the full harness template source and output, including config parsing, skill frontmatter, hook aliases, forbidden legacy paths, and source/template drift. Use before committing harness template changes or after regenerating templates.
---

# Harness Template Validate

Use this skill before committing harness template changes, after running `$harness-template-build`, or whenever you need evidence that the full template remains directly reusable.

## Workflow

1. Run `python3 harness/scripts/validate-template.py`.
2. If validation fails, inspect the failing path or check named by the script.
3. Fix the source tree first when the issue is template content.
4. Re-run `$harness-template-build` if the source change should update `harness/templates/`.
5. Re-run `python3 harness/scripts/validate-template.py`.
6. Report validation commands and results.

## What Validation Covers

- `harness/source/full/manifest.toml` paths and full distribution policy.
- `.codex/hooks.json`, `.codex/config.toml`, `.codex/agents/*.toml` parsing.
- `.agents/skills/*/SKILL.md` frontmatter.
- `spec`, `plan`, `build` alias hook routing.
- destructive command hook blocking.
- forbidden legacy paths: root `SPEC.md`, `tasks/plan.md`, `tasks/todo.md`.
- excluded bundled references: `docs/references`.
- source-generated output matching `harness/templates/`.

## Rules

- Do not treat a partially passing validation as complete.
- Record environment blockers separately from template failures.
- Keep validation deterministic and local; do not require network access.
