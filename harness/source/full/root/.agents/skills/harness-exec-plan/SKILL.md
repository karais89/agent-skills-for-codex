---
name: harness-exec-plan
description: Creates or updates active execution plans under docs/exec-plans/active. Use when the user types plan or plan:, invokes $harness-exec-plan, or wants a product spec or request broken into verifiable build-sized work.
---

# Harness Exec Plan

Use this skill when the user types `plan`, `plan:`, invokes `$harness-exec-plan`, asks for task breakdown, or wants an implementable plan before coding.

Bare `/plan` is not supported by the Codex TUI; it is rejected before hooks run unless the user prefixes a leading space. Do not create `tasks/plan.md` or `tasks/todo.md`.

## Workflow

1. Read `AGENTS.md`, `ARCHITECTURE.md`, `docs/README.md`, and `docs/exec-plans/README.md` when present.
2. Look for a related product spec in `docs/product-specs/`. If one exists, reference it. If none exists, plan from the user request and repository context.
3. Inspect relevant code and documentation enough to understand current state, dependencies, and verification commands.
4. Stay in planning mode. Do not make product code changes.
5. Choose a concise lowercase hyphen-case slug. Update an existing active ExecPlan for the same goal; otherwise create `docs/exec-plans/active/<slug>.md`.
6. Write checklist items that one `build` invocation can finish and verify.
7. For each checklist item, include only these lightweight fields: files to read, change scope, verification, and completion record.
8. Include acceptance criteria and verification steps for every meaningful item.
9. Report the active ExecPlan path and any decisions or open questions.

## Required ExecPlan Sections

- Purpose
- Current state
- Scope
- Non-goals
- Progress checklist
- Execution plan
- Verification plan
- Findings
- Decision log
- Completion criteria
- Post-completion handling

## Rules

- Make the plan actionable without being a full implementation transcript.
- Keep every checklist item small enough for one focused build/test loop.
- Keep checklist item details short: `읽을 파일`, `변경 범위`, `검증`, `완료 기록`.
- Record assumptions and decisions where future builders will need them.
- Never create or update root `SPEC.md`, `tasks/plan.md`, or `tasks/todo.md` for this workflow.
