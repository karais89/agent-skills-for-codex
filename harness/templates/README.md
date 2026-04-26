# 프로젝트 README

이 문서는 프로젝트의 짧은 시작점이다. 프로젝트의 목적, 실행 방법, 검증 방법을 이곳에 요약하고, 상세 요구사항과 실행 계획은 `docs/` 아래에 보관한다.

## 프로젝트 개요

- 목적: TBD
- 주요 사용자: TBD
- 실행 환경: TBD
- 주요 진입점: TBD

## 로컬 하네스

이 프로젝트는 repo-local Codex 하네스를 사용한다. 하네스 설정은 프로젝트 안의 `.agents/`, `.codex/`, `AGENTS.md`, `docs/`에 들어 있으며 전역 Codex 설정을 바꾸지 않는다.

## 문서 구조

```text
.
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
    validation.md
```

- `AGENTS.md`: Codex가 이 프로젝트에서 따라야 할 짧은 작업 지침.
- `ARCHITECTURE.md`: 장기 구조, 주요 구성요소, 설계 결정.
- `docs/product-specs/`: 기능 요구사항과 수용 기준.
- `docs/exec-plans/`: 장시간 작업과 여러 단계 구현의 진행 상태.
- `docs/validation.md`: 자주 쓰는 검증 명령과 수동 확인 기준.

## Alias 계약

Codex TUI는 알 수 없는 `/spec` 같은 입력을 prompt가 아니라 slash command로 먼저 해석할 수 있다. 이 프로젝트는 slash command 대신 텍스트 alias와 직접 스킬 호출을 사용한다.

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

## 시작 흐름

1. 프로젝트 목적과 실행 환경을 이 README와 `ARCHITECTURE.md`에 간단히 적는다.
2. 새 기능이나 제품 목표는 `spec:`으로 `docs/product-specs/`에 정리한다.
3. 구현이 여러 단계라면 `plan:`으로 active ExecPlan을 만든다.
4. `build`로 active ExecPlan의 첫 미완료 항목을 구현하고 검증 기록을 남긴다.
5. 검증 명령이 정해지면 `docs/validation.md`의 기본 명령 표를 갱신한다.

## 개발 명령

프로젝트 스택이 정해지면 아래 항목을 실제 명령으로 교체한다.

| 목적 | 명령 |
| --- | --- |
| 개발 서버 | TBD |
| 테스트 | TBD |
| 린트 | TBD |
| 빌드 | TBD |
| 타입 검사 | TBD |

## 빠른 하네스 확인

아래 명령은 로컬 Codex hook과 agent 설정이 파싱 가능한지 확인한다.

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

아래 명령은 `spec` alias가 product spec workflow로 안내되는지 확인한다.

```bash
python3 .codex/hooks/user_prompt_submit.py <<'JSON'
{
  "hook_event_name": "UserPromptSubmit",
  "prompt": "spec 새 기능 요구사항을 정리해줘"
}
JSON
```

예상 결과: 출력 JSON의 `additionalContext`에 `$harness-product-spec`와 `docs/product-specs/` 안내가 포함된다.
