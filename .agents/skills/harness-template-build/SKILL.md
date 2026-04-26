---
name: harness-template-build
description: Builds the full harness template from harness/source/full/root into harness/templates, or checks that the generated output matches the committed template. Use when changing the harness source tree, regenerating templates, or checking source/template drift.
---

# Harness Template Build

Use this skill when editing the harness template source, regenerating `harness/templates/`, or checking whether the generated full template still matches the committed output.

## Source Model

- Source of truth: `harness/source/full/root/`
- Output: `harness/templates/`
- Manifest: `harness/source/full/manifest.toml`
- Build script: `harness/scripts/build-template.py`
- Validation script: `harness/scripts/validate-template.py`

The distribution model is full. Do not introduce a minimal variant in this workflow.

## Workflow

1. Read `harness/source/full/manifest.toml`.
2. Inspect the relevant files under `harness/source/full/root/`.
3. If the user asks to change template content, edit the source tree first.
4. Run `python3 harness/scripts/build-template.py --check` to compare source-generated output with `harness/templates/`.
5. If source and output differ because the source changed intentionally, run `python3 harness/scripts/build-template.py --write` to regenerate `harness/templates/`.
6. If `harness/scripts/build-template.py` changed, run `python3 harness/scripts/test-template-builder.py`.
7. Run `python3 harness/scripts/validate-template.py`.
8. Report whether source and output match, what changed, and which validation commands passed.

## Rules

- Treat `harness/templates/` as build output.
- Do not delete `harness/templates/` manually.
- Do not create `docs/references/` in the template unless the distribution model is explicitly changed.
- Do not create root `SPEC.md`, `tasks/plan.md`, or `tasks/todo.md` in the template.
- Keep this skill focused on template source and output management; actual target-project application belongs in a future apply skill.
