#!/usr/bin/env python3
import json
import re
import sys


def emit_ok():
    print(json.dumps({}))


try:
    payload = json.load(sys.stdin)
except Exception:
    emit_ok()
    raise SystemExit(0)

message = (payload.get("last_assistant_message") or "").lower()
changed_words = re.search(
    r"\b(implemented|changed|updated|fixed|added|created|modified)\b"
    r"|구현|변경|수정|추가|생성|작성|완료",
    message,
)
verification_words = re.search(
    r"\b(test|tests|tested|verify|verified|verification|validate|validated|lint|build|ran|checked|not run|unable to run|couldn't run|could not run)\b"
    r"|테스트|검증|확인|빌드|린트|실행|통과|미실행|못함|하지 않",
    message,
)

if changed_words and not verification_words:
    print(json.dumps({
        "decision": "block",
        "reason": "Before stopping, add a verification note that states what was run, or explicitly say verification was not run."
    }))
else:
    emit_ok()
