---
name: agent-skills-test
description: Runs the original test command workflow as a Codex skill. Use when the user types test or test:, invokes $agent-skills-test, asks for TDD, bug reproduction, or coverage analysis.
---

# Agent Skills Test

Use this skill when the user types `test`, `test:`, invokes `$agent-skills-test`, asks for TDD, needs a failing reproduction, or wants coverage gaps identified. Bare `/test` is not supported by Codex TUI; it is rejected before hooks run.

Workflow:
1. Invoke and follow the `test-driven-development` skill.
2. For new features: write tests that describe the expected behavior and confirm they fail, implement the code to make them pass, then refactor while keeping tests green.
3. For bug fixes, use the Prove-It pattern: write a test that reproduces the bug, confirm the test fails, implement the fix, confirm the test passes, then run the full test suite for regressions.
4. For browser-related issues, also invoke `browser-testing-with-devtools` to verify behavior with a real browser runtime when applicable.
5. Report exactly what was run and what remains unverified.
