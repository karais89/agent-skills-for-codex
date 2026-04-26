---
name: harness-exec-build
description: Implements the next unchecked item from an active ExecPlan and updates that plan with verification results. Use when the user types build or build:, invokes $harness-exec-build, or asks to continue implementation from docs/exec-plans/active.
---

# Harness Exec Build

Use this skill when the user types `build`, `build:`, invokes `$harness-exec-build`, asks to implement the next task, or wants the active ExecPlan advanced by one verified increment.

Bare `/build` is not supported by the Codex TUI; it is rejected before hooks run unless the user prefixes a leading space.

## Workflow

1. Read `AGENTS.md`, `ARCHITECTURE.md`, `docs/README.md`, and `docs/exec-plans/README.md` when present.
2. List `docs/exec-plans/active/*.md`.
3. If there is exactly one active ExecPlan, use it. If there are none, ask the user to run `plan` first. If there are multiple, ask the user which plan to use before editing code.
4. Read the selected ExecPlan and identify the first unchecked checklist item.
5. Inspect relevant code, tests, and documentation for that item only.
6. Implement the smallest change that satisfies the item. Use `test-driven-development` when a new behavior or bug fix needs a test.
7. Run the focused verification from the ExecPlan, then broader verification when the change has shared or user-facing impact.
8. Update the same ExecPlan with:
   - the completed checkbox only after verification passes or the user explicitly accepts a documented limitation
   - commands run and results
   - findings discovered during implementation
   - decisions that changed the plan
9. If all checklist items are complete, add a completion retrospective and ask the user before moving the file to `docs/exec-plans/completed/`.
10. Report changed files, verification, and remaining unchecked items.

## Rules

- Do not skip verification silently. If a verification cannot run, record why and leave the checkbox unchecked unless the user accepts the risk.
- Do not work on a later checklist item while an earlier unchecked item remains unresolved.
- Keep unrelated refactors out of the build increment.
- Never create or update root `SPEC.md`, `tasks/plan.md`, or `tasks/todo.md` for this workflow.
