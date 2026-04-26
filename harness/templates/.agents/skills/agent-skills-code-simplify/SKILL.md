---
name: agent-skills-code-simplify
description: Runs the original code-simplify command workflow as a Codex skill. Use when the user types code-simplify or code-simplify:, invokes $agent-skills-code-simplify, or asks to simplify code without behavior changes.
---

# Agent Skills Code Simplify

Use this skill when the user types `code-simplify`, `code-simplify:`, invokes `$agent-skills-code-simplify`, asks to simplify code, or wants clarity and maintainability without behavior changes. Bare `/code-simplify` is not supported by Codex TUI; it is rejected before hooks run.

Workflow:
1. Invoke and follow the `code-simplification` skill.
2. Read `AGENTS.md` and `CLAUDE.md` if present, then study project conventions.
3. Identify the target code: recently changed code unless the user specifies a broader scope.
4. Understand the code's purpose, callers, edge cases, and test coverage before editing.
5. Scan for simplification opportunities: deep nesting, long functions, nested ternaries, generic names, duplicated logic, and confirmed dead code.
6. Apply each simplification incrementally and run tests after each meaningful change.
7. Verify all tests pass, the build succeeds, and the diff is clean.
8. If tests fail after a simplification, revert that specific simplification and reconsider.
9. Use `code-review-and-quality` to review the result.
10. Avoid editing blocks marked with `simplify-ignore-start` and `simplify-ignore-end`.
