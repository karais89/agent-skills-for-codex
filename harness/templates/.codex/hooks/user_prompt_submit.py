#!/usr/bin/env python3
import json
import sys

ALIASES = {
    "code-simplify:": "$agent-skills-code-simplify",
    "code-simplify": "$agent-skills-code-simplify",
    "spec:": "$harness-product-spec",
    "spec": "$harness-product-spec",
    "plan:": "$harness-exec-plan",
    "plan": "$harness-exec-plan",
    "build:": "$harness-exec-build",
    "build": "$harness-exec-build",
    "test:": "$agent-skills-test",
    "test": "$agent-skills-test",
    "review:": "$agent-skills-review",
    "review": "$agent-skills-review",
    "ship:": "$agent-skills-ship",
    "ship": "$agent-skills-ship",
    # Legacy aliases only work if the user prefixes a leading space, e.g.
    # " /spec ..."; bare "/spec" is rejected by the Codex TUI before hooks run.
    "/spec": "$harness-product-spec",
    "/plan": "$harness-exec-plan",
    "/build": "$harness-exec-build",
    "/test": "$agent-skills-test",
    "/review": "$agent-skills-review",
    "/code-simplify": "$agent-skills-code-simplify",
    "/ship": "$agent-skills-ship",
}

def emit(context=None):
    output = {"hookSpecificOutput": {"hookEventName": "UserPromptSubmit"}}
    if context:
        output["hookSpecificOutput"]["additionalContext"] = context
    print(json.dumps(output))

try:
    payload = json.load(sys.stdin)
except Exception:
    emit()
    raise SystemExit(0)

prompt = (payload.get("prompt") or "").lstrip()
for alias, skill in sorted(ALIASES.items(), key=lambda item: len(item[0]), reverse=True):
    if prompt == alias or prompt.startswith(alias + " "):
        skill_name = skill.removeprefix("$")
        emit(f"`{alias}` maps to the Codex wrapper skill `{skill}`. Treat this prompt as an explicit request to use that workflow. UserPromptSubmit hooks run after Codex's dollar-prefixed skill mention collection, so this is routing guidance rather than an automatic skill injection: open `.agents/skills/{skill_name}/SKILL.md` and follow it before answering. The harness contract stores product specs under `docs/product-specs/` and ExecPlans under `docs/exec-plans/`; do not create root `SPEC.md`, `tasks/plan.md`, or `tasks/todo.md` for spec/plan/build. Bare slash commands such as `/spec` are intercepted by the Codex TUI before hooks run; prefer text aliases such as `spec`/`spec:` or invoke `{skill}` directly.")
        break
else:
    emit()
