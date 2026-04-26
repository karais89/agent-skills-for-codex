#!/usr/bin/env python3
import json
import re
import shlex
import sys


PROTECTED_MARKERS = re.compile(r"simplify-ignore-(?:start|end)|\bBLOCK_[0-9A-Fa-f]{8,}\b")


def emit_ok():
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse"}}))


def block(reason: str):
    print(reason, file=sys.stderr)
    raise SystemExit(2)


def stringify_command(value):
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return " ".join(shlex.quote(str(part)) for part in value)
    return ""


def extract_command(tool_input):
    if isinstance(tool_input, str):
        return tool_input
    if not isinstance(tool_input, dict):
        return ""
    for key in ("command", "cmd", "shell_command"):
        command = stringify_command(tool_input.get(key))
        if command:
            return command
    params = tool_input.get("params")
    if isinstance(params, dict):
        for key in ("command", "cmd", "shell_command"):
            command = stringify_command(params.get(key))
            if command:
                return command
    return ""


def has_dangerous_shell_command(command: str) -> str | None:
    compact = " ".join(command.split())
    lowered = compact.lower()
    checks = [
        (r"\brm\s+-[^\n;]*[rf][^\n;]*\s+(/|~|\.{1,2}|\*|\.codex|\.agents|agents\.md|docs/(?:references|product-specs|exec-plans)|tmp/upstream)(\s|$)", "refusing broad destructive rm against workspace, policy, or harness-reference paths"),
        (r"\bgit\s+reset\s+--hard\b", "refusing git reset --hard"),
        (r"\bgit\s+clean\s+-[^\n;]*[fdx][^\n;]*\b", "refusing git clean that deletes untracked files"),
        (r"\bgit\s+checkout\s+--\s+", "refusing git checkout -- because it can discard local edits"),
        (r"\bgit\s+restore\s+(\.|\*|:\/|--source)\b", "refusing git restore that can discard local edits"),
        (r"\bchmod\s+-r\s+777\s+(/|~|\.)(\s|$)", "refusing recursive chmod 777 on broad paths"),
        (r"\bmkfs(\.|)\b|\bdd\s+if=", "refusing disk formatting or raw disk write command"),
    ]
    for pattern, reason in checks:
        if re.search(pattern, lowered):
            return reason
    return None


def text_fields(tool_input):
    if isinstance(tool_input, dict):
        for key in ("content", "old_string", "new_string", "input", "patch"):
            value = tool_input.get(key)
            if isinstance(value, str):
                yield key, value
        params = tool_input.get("params")
        if isinstance(params, dict):
            yield from text_fields(params)


try:
    payload = json.load(sys.stdin)
except Exception:
    emit_ok()
    raise SystemExit(0)

tool_input = payload.get("tool_input")
command = extract_command(tool_input)

if command:
    reason = has_dangerous_shell_command(command)
    if reason:
        block(f"agent-skills PreToolUse blocked command: {reason}. Ask the user before running destructive operations.")
    if PROTECTED_MARKERS.search(command):
        block("agent-skills PreToolUse blocked command: do not modify simplify-ignore protected blocks.")

for key, value in text_fields(tool_input):
    if PROTECTED_MARKERS.search(value):
        block(f"agent-skills PreToolUse blocked edit field `{key}`: do not modify simplify-ignore protected blocks.")

emit_ok()
