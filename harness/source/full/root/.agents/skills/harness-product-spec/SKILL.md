---
name: harness-product-spec
description: Creates or updates repository product specs under docs/product-specs. Use when the user types spec or spec:, invokes $harness-product-spec, asks to write requirements, or wants a product specification before planning or coding.
---

# Harness Product Spec

Use this skill when the user types `spec`, `spec:`, invokes `$harness-product-spec`, asks to spec a feature, or wants structured requirements before planning or implementation.

Bare `/spec` is not supported by the Codex TUI; it is rejected before hooks run unless the user prefixes a leading space. Do not create root `SPEC.md`.

## Workflow

1. Read `AGENTS.md`, `ARCHITECTURE.md`, `docs/README.md`, and existing `docs/product-specs/` files when present.
2. Understand the user's objective, target users, core behavior, constraints, and success criteria. Ask only for information that is required to avoid a wrong spec.
3. Choose a concise slug from the goal, using lowercase hyphen-case.
4. Check `docs/product-specs/index.md` and existing specs for the same goal. Update the existing spec when it is clearly the same product intent; create a new file only for a distinct goal.
5. Write or update `docs/product-specs/<slug>.md`.
6. Update `docs/product-specs/index.md` so the spec is discoverable.
7. Report the spec path and any open questions. Do not move into planning or implementation unless the user explicitly asks.

## Required Spec Sections

- Purpose
- Users and target audience
- Core features
- Acceptance criteria
- Non-goals
- Related commands
- Verification criteria

## Rules

- Keep the spec product-focused. Implementation sequencing belongs in an ExecPlan.
- Prefer concrete acceptance criteria over vague adjectives.
- If a requirement is uncertain, mark it as an open question instead of silently deciding.
- Never create or update `tasks/plan.md`, `tasks/todo.md`, or root `SPEC.md` for this workflow.
