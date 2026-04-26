#!/usr/bin/env python3
import json
from pathlib import Path

root = Path.cwd()
meta = root / ".agents" / "skills" / "using-agent-skills" / "SKILL.md"
if meta.exists():
    meta_text = meta.read_text(encoding="utf-8")
    context = """A repo-local Codex harness is installed under `.agents/skills`.
Use `$using-agent-skills` when routing is unclear. Codex does not support project-defined slash commands, so do not use bare `/spec` or `/ship` in the TUI. Direct wrapper skill mentions such as `$harness-product-spec` are the explicit Codex skill invocation syntax; text aliases are hook-routed guidance:
spec or spec: -> use `$harness-product-spec` and write/update `docs/product-specs/<slug>.md`
plan or plan: -> use `$harness-exec-plan` and write/update `docs/exec-plans/active/<slug>.md`
build or build: -> use `$harness-exec-build` and implement the next unchecked item from an active ExecPlan
test or test: -> use `$agent-skills-test`
review or review: -> use `$agent-skills-review`
code-simplify or code-simplify: -> use `$agent-skills-code-simplify`
ship or ship: -> use `$agent-skills-ship`

The harness spec/plan/build workflow must not create root `SPEC.md`, `tasks/plan.md`, or `tasks/todo.md`.
If a legacy slash alias is pasted, it only reaches hooks when prefixed with a leading space, for example ` /spec write a spec`. UserPromptSubmit hook context is guidance for the current turn, not a second pass through skill mention collection.

Meta-skill excerpt:
""" + meta_text[:4000]
else:
    context = """Repo-local skill directory was expected at `.agents/skills`, but `$using-agent-skills` was not found.
Use the wrapper skill names in AGENTS.md if they are present."""

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": context,
    }
}))
