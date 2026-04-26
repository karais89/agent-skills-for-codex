# 하네스 템플릿 README

이 디렉터리는 대상 프로젝트 루트에 복사해 사용할 repo-local Codex 하네스 템플릿이다. 문서 템플릿, 로컬 스킬, alias hook, 검증 참고 문서를 함께 제공한다.

## 구성

```text
.
  .agents/skills/
  .codex/
    agents/
    hooks/
    config.toml
    hooks.json
  AGENTS.md
  ARCHITECTURE.md
  docs/
    README.md
    product-specs/
      index.md
      template.md
    exec-plans/
      README.md
      active/
      completed/
      template.md
    references/
    validation.md
```

## Alias 계약

Codex TUI는 알 수 없는 `/spec` 같은 입력을 hook 실행 전에 slash command로 거부할 수 있다. 이 하네스는 slash command 대신 텍스트 alias와 직접 스킬 호출을 사용한다.

| 입력 alias | 사용할 Codex 스킬 | 산출물 |
| --- | --- | --- |
| `spec`, `spec:` | `$harness-product-spec` | `docs/product-specs/<slug>.md` |
| `plan`, `plan:` | `$harness-exec-plan` | `docs/exec-plans/active/<slug>.md` |
| `build`, `build:` | `$harness-exec-build` | active ExecPlan의 다음 미완료 항목 |
| `test`, `test:` | `$agent-skills-test` | TDD와 검증 workflow |
| `review`, `review:` | `$agent-skills-review` | 5축 코드 리뷰 |
| `code-simplify`, `code-simplify:` | `$agent-skills-code-simplify` | 동작 보존 단순화 |
| `ship`, `ship:` | `$agent-skills-ship` | 출시 go/no-go 검토 |

`spec`, `plan`, `build` workflow는 루트 `SPEC.md`, `tasks/plan.md`, `tasks/todo.md`를 만들지 않는다.

## 적용 방법

1. 이 디렉터리의 내용을 대상 프로젝트 루트에 복사한다.
2. `AGENTS.md`, `ARCHITECTURE.md`, `docs/README.md`, `docs/validation.md`의 자리표시자를 대상 프로젝트에 맞게 채운다.
3. 필요한 첫 요구사항을 `spec:`으로 정리하고, 이어서 `plan:`, `build` 순서로 진행한다.
4. 적용 뒤 아래 검증을 실행한다.

## 빠른 검증

```bash
python3 - <<'PY'
import json
import tomllib
from pathlib import Path

root = Path.cwd()
json.loads((root / ".codex/hooks.json").read_text())
tomllib.loads((root / ".codex/config.toml").read_text())
for path in sorted((root / ".codex/agents").glob("*.toml")):
    data = tomllib.loads(path.read_text())
    assert data["name"] == path.stem
    assert data["description"]
    assert data["developer_instructions"]
print("config ok")
PY
```

```bash
python3 .codex/hooks/user_prompt_submit.py <<'JSON'
{
  "hook_event_name": "UserPromptSubmit",
  "prompt": "spec 새 기능 요구사항을 정리해줘"
}
JSON
```

예상 결과: 출력 JSON의 `additionalContext`에 `$harness-product-spec`와 `docs/product-specs/` 안내가 포함된다.
