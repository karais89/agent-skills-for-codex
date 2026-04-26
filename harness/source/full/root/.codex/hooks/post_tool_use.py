#!/usr/bin/env python3
import json
import sys


def emit(context=None):
    output = {"hookSpecificOutput": {"hookEventName": "PostToolUse"}}
    if context:
        output["hookSpecificOutput"]["additionalContext"] = context
    print(json.dumps(output))


def response_failed(response) -> tuple[bool, str]:
    if isinstance(response, dict):
        if response.get("success") is False:
            return True, "success=false"
        if response.get("executed") is False:
            return True, "tool did not execute"
        for key in ("error", "exception"):
            if response.get(key):
                return True, str(response.get(key))[:400]
        status = response.get("status")
        if isinstance(status, str) and status.lower() in {"failed", "error", "timeout"}:
            return True, status
        for key in ("exit_code", "returncode", "code"):
            code = response.get(key)
            if isinstance(code, int) and code != 0:
                return True, f"{key}={code}"
        for key in ("stderr", "output", "output_preview"):
            value = response.get(key)
            if isinstance(value, str) and any(token in value.lower() for token in ["traceback", "error:", "failed", "exception"]):
                return True, value[:400]
    elif isinstance(response, str):
        lowered = response.lower()
        if any(token in lowered for token in ["traceback", "error:", "failed", "exception"]):
            return True, response[:400]
    return False, ""


try:
    payload = json.load(sys.stdin)
except Exception:
    emit()
    raise SystemExit(0)

failed, signal = response_failed(payload.get("tool_response"))
if failed:
    tool_name = payload.get("tool_name") or "tool"
    emit(
        f"`{tool_name}` appears to have failed ({signal}). Use `$debugging-and-error-recovery`: capture the exact failure, form one root-cause hypothesis at a time, make the smallest fix, and rerun focused verification before broad checks."
    )
else:
    emit()
