# 프로젝트 이름

이 README는 사람이 가장 먼저 읽는 프로젝트 시작점이다. 프로젝트의 목적, 실행 방법, 검증 방법을 짧게 유지하고, 상세 요구사항과 실행 계획은 `docs/` 아래 문서로 분리한다.

## 프로젝트 개요

| 항목 | 내용 |
| --- | --- |
| 목적 | TBD |
| 주요 사용자 | TBD |
| 핵심 기능 | TBD |
| 실행 환경 | TBD |
| 주요 진입점 | TBD |
| 배포 또는 운영 위치 | TBD |

## 빠른 시작

프로젝트 스택이 정해지면 아래 절차를 실제 명령으로 교체한다.

```bash
# 의존성 설치
TBD

# 개발 서버 또는 로컬 실행
TBD

# 검증
TBD
```

## 개발 명령

| 목적 | 명령 | 비고 |
| --- | --- | --- |
| 개발 서버 | TBD | 예: `npm run dev`, `python -m app` |
| 테스트 | TBD | 예: `npm test`, `pytest` |
| 린트 | TBD | 예: `npm run lint`, `ruff check .` |
| 빌드 | TBD | 예: `npm run build`, `go build ./...` |
| 타입 검사 | TBD | 예: `npm run typecheck`, `mypy .` |

## 프로젝트 구조

프로젝트 고유 소스 구조가 정해지면 이 표를 실제 경로로 갱신한다.

| 경로 | 역할 |
| --- | --- |
| `AGENTS.md` | Codex가 이 프로젝트에서 따라야 할 작업 지침 |
| `ARCHITECTURE.md` | 장기 구조, 주요 구성요소, 설계 결정 |
| `docs/product-specs/` | 제품 요구사항과 수용 기준 |
| `docs/exec-plans/` | 장시간 작업과 여러 단계 구현의 진행 상태 |
| `docs/validation.md` | 자주 쓰는 검증 명령과 수동 확인 기준 |
| TBD | 프로젝트 소스 또는 테스트 경로 |

## 문서 작성 기준

- 프로젝트 사용자가 바로 알아야 하는 실행, 검증, 배포 정보는 이 README에 둔다.
- 장기 구조와 모듈 경계는 `ARCHITECTURE.md`에 둔다.
- 기능 요구사항과 수용 기준은 `docs/product-specs/`에 둔다.
- 구현 순서와 진행 상태는 `docs/exec-plans/`에 둔다.
- 검증 명령과 수동 확인 기준은 `docs/validation.md`에 둔다.

## 로컬 Codex 하네스

이 프로젝트는 repo-local Codex 하네스를 사용한다. 하네스 설정은 프로젝트 안의 `.agents/`, `.codex/`, `AGENTS.md`, `docs/`에 들어 있으며 전역 Codex 설정을 바꾸지 않는다.

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

## 추천 작업 흐름

1. 프로젝트 목적, 사용자, 실행 환경을 이 README에 적는다.
2. 장기 구조와 주요 설계 결정을 `ARCHITECTURE.md`에 적는다.
3. 새 기능이나 제품 목표는 `spec:`으로 `docs/product-specs/`에 정리한다.
4. 구현이 여러 단계라면 `plan:`으로 active ExecPlan을 만든다.
5. `build`로 active ExecPlan의 첫 미완료 항목을 구현하고 검증 기록을 남긴다.
6. 검증 명령이 정해지면 `docs/validation.md`의 기본 명령 표를 갱신한다.

## 하네스 확인

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
