---
name: agent-skills-review
description: Runs the original review command workflow as a Codex skill. Use when the user types review or review:, invokes $agent-skills-review, or wants a five-axis code review.
---

# Agent Skills Review

Use this skill when the user types `review`, `review:`, invokes `$agent-skills-review`, asks for a code review, or wants current changes evaluated before merge. Bare `/review` is not supported by Codex TUI; it is rejected before hooks run.

Workflow:
1. Invoke and follow the `code-review-and-quality` skill.
2. Review the current changes: staged changes, recent commits, or the specified scope.
3. Check all five axes: correctness, readability, architecture, security, and performance.
4. Use `security-and-hardening` for security findings and `performance-optimization` for performance risks when those axes matter.
5. Categorize findings as Critical, Important, or Suggestion.
6. Output a structured review that leads with findings, cites specific file:line references, and includes fix recommendations.
