# `$harness-apply` 적용 자동화 실행 결과

## 목적

full 하네스 템플릿을 다른 프로젝트 루트에 반복 가능하고 검증 가능한 방식으로 적용한다. 대상 프로젝트가 새 디렉터리이거나 비어 있으면 템플릿을 복제하고, 기존 파일이 있는 프로젝트에서는 충돌을 먼저 보고해 사용자가 덮어쓰기 여부를 수동으로 판단할 수 있게 한다.

## 구현 결과

- `.agents/skills/harness-apply/SKILL.md`를 추가했다.
- `harness/scripts/apply-template.py`를 추가했다.
- `harness/scripts/test-apply-template.py`를 추가했다.
- `harness/README.md`의 적용 방식을 `$harness-apply`와 `apply-template.py` 기준으로 갱신했다.
- `$harness-apply`는 이 저장소의 repo-local 적용 도구로 유지하고, 대상 프로젝트 템플릿에는 번들하지 않았다.

## 정책 결정

- 적용 소스는 기본적으로 커밋된 full 산출물인 `harness/templates/`를 사용한다.
- 대상 디렉터리가 없으면 생성한다.
- 대상 디렉터리가 있으면 기존 파일과 템플릿 파일을 비교한다.
- 기존 파일이 템플릿 파일과 byte-level로 같으면 충돌로 보지 않는다.
- 기존 파일이 다르거나 파일/디렉터리 타입이 맞지 않으면 충돌로 보고 적용하지 않는다.
- 충돌이 하나라도 있으면 아무 파일도 복사하지 않는다.
- 충돌이 없을 때만 누락 파일을 복사한다.
- `--dry-run`은 파일을 쓰지 않고 복사 예정, 동일 파일, 충돌을 보고한다.
- root `SPEC.md`, `tasks/plan.md`, `tasks/todo.md`, `docs/references`는 적용 결과에 생성되면 안 된다.

## 진행 체크리스트

- [x] 실행 계획을 작성한다.
- [x] `apply-template.py`를 구현한다.
- [x] 적용 스크립트 테스트를 구현한다.
- [x] `$harness-apply` 스킬을 추가한다.
- [x] `harness/README.md`를 갱신한다.
- [x] 새/빈 대상 적용 fixture를 검증한다.
- [x] 기존 Git 프로젝트 적용 fixture를 검증한다.
- [x] 충돌 감지 fixture를 검증한다.
- [x] 템플릿 정적 검증과 skill validation을 실행한다.
- [x] 결과를 완료 문서로 이동하고 커밋한다.

## 검증 기록

| 날짜 | 항목 | 실행한 검증 | 결과 |
| --- | --- | --- | --- |
| 2026-04-26 | 적용 스크립트 테스트 | `python3 harness/scripts/test-apply-template.py` | 통과: 새 대상, 기존 Git 유사 대상, dry-run, 재적용, 충돌 중단 5개 테스트 통과. |
| 2026-04-26 | 스킬 validation | `python3 /Users/kaya/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/harness-apply` | 통과: Skill is valid. |
| 2026-04-26 | 새 대상 dry-run | `python3 harness/scripts/apply-template.py --target /tmp/harness-apply-new.VGYbqj/project --dry-run` | 통과: 56개 파일 복사 예정, 충돌 0, 파일 쓰기 없음. |
| 2026-04-26 | 새 대상 apply | `python3 harness/scripts/apply-template.py --target /tmp/harness-apply-new.VGYbqj/project` | 통과: full 템플릿 적용 완료. |
| 2026-04-26 | 새 대상 파일 확인 | 핵심 파일 `AGENTS.md`, `.codex/hooks.json`, `.agents/skills`, `docs/product-specs/template.md`, `docs/exec-plans/active/.gitkeep` 확인 | 통과. |
| 2026-04-26 | 기존 Git fixture 적용 | `/tmp/harness-apply-git.I8qiKG/project`에서 `git init`, dry-run, apply | 통과: `.git` 유지, 템플릿 파일 생성, forbidden path 없음. |
| 2026-04-26 | 충돌 fixture dry-run | 기존 `AGENTS.md`가 다른 `/tmp/harness-apply-conflict.Cm7lYI/project`에 dry-run | 통과: `content conflict: AGENTS.md` 보고, exit 1. |
| 2026-04-26 | 충돌 fixture apply | 같은 충돌 fixture에 실제 apply | 통과: exit 1, `.codex` 등 부분 복사 없음, 기존 `AGENTS.md` 유지. |
| 2026-04-26 | forbidden path 확인 | `find`로 `SPEC.md`, `tasks/plan.md`, `tasks/todo.md`, `docs/references` 검색 | 통과: 새 대상과 Git fixture 모두 출력 없음. |
| 2026-04-26 | 적용 후 `spec` smoke | Git fixture에서 `codex exec --sandbox workspace-write "spec: ..."` | 통과: `docs/product-specs/smoke-todo-app.md` 생성, 색인 갱신, forbidden path 없음. fixture 커밋 `4d323ad`. |
| 2026-04-26 | 적용 후 `plan` smoke | Git fixture에서 `codex exec --sandbox workspace-write "plan: ..."` | 통과: `docs/exec-plans/active/smoke-todo-static-app.md` 생성, spec 상태 `ready` 갱신. fixture 커밋 `dacae34`. |
| 2026-04-26 | 적용 후 `build` smoke | Git fixture에서 `codex exec --sandbox workspace-write "build"` | 부분 통과: 첫 active ExecPlan을 읽고 첫 체크박스 범위의 정적 앱 골격을 구현했다. 필수 서버 검증은 sandbox TCP bind 제한으로 실패해 체크박스는 미완료로 남겼다. fixture 커밋 `c3c16e8`. |
| 2026-04-26 | build smoke fallback 검증 | fixture에서 `node --check src/app.mjs`와 최소 DOM import check | 통과: 문법 오류 없음, `0개`와 `아직 할 일이 없습니다.` 렌더 확인. |
| 2026-04-26 | build smoke 서버 검증 | `python3 -m http.server 8000`, `python3 -m http.server 8000 --bind 127.0.0.1` | 실행 불가: `PermissionError: [Errno 1] Operation not permitted`. 환경 제한으로 ExecPlan에 기록. |
| 2026-04-26 | fixture 최종 상태 | Git fixture `git status --short`, `git log --oneline --max-count=5` | 통과: 최종 status clean, 커밋 `c3c16e8`, `dacae34`, `4d323ad`, `cb862c9`. |
| 2026-04-26 | template drift | `python3 harness/scripts/build-template.py --check` | 통과: source와 output 일치. |
| 2026-04-26 | template validation | `python3 harness/scripts/validate-template.py` | 통과: template validation ok. |
| 2026-04-26 | builder regression | `python3 harness/scripts/test-template-builder.py` | 통과: 2개 테스트 통과. |
| 2026-04-26 | diff hygiene | `git diff --check` | 통과. |

## fixture 커밋 로그

| 커밋 | 내용 |
| --- | --- |
| `c3c16e8` | `build` smoke: 첫 정적 앱 골격 구현, 서버 검증 제한 기록 |
| `dacae34` | `plan` smoke: active ExecPlan 생성 |
| `4d323ad` | `spec` smoke: product spec 생성 |
| `cb862c9` | full 하네스 템플릿 적용 |

## 발견 사항

- `apply-template.py`는 기존 프로젝트에 적용하기 전에 전체 충돌 목록을 계산하므로, 충돌 발생 시 부분 복사가 생기지 않는다.
- 동일한 템플릿을 다시 적용하면 동일 파일로 인식되어 충돌 없이 no-op에 가깝게 종료된다.
- 적용된 Git fixture에서 `spec`, `plan`, `build` alias는 정상 라우팅된다.
- 현재 Codex sandbox에서는 Python 정적 서버의 TCP bind가 차단된다. 이 제한 때문에 target project의 `build` smoke는 첫 체크박스를 완료 처리하지 않고 환경 제한을 ExecPlan에 기록하는 동작까지 확인했다.

## 완료 조건

- [x] `$harness-apply` 스킬이 repo-local skill로 추가되어 있다.
- [x] 적용 스크립트가 새/빈 대상과 기존 Git 대상에 full 템플릿을 적용한다.
- [x] 충돌이 있는 대상에는 기본적으로 쓰지 않고 실패한다.
- [x] forbidden legacy/reference 경로가 생성되지 않는다.
- [x] 관련 테스트와 템플릿 검증이 통과한다.
- [x] 결과가 문서화되고 커밋되어 있다.

## 결론

4번 적용 자동화는 완료되었다. 이제 다른 프로젝트에 full 하네스 템플릿을 적용할 때는 `$harness-apply` 스킬 또는 `python3 harness/scripts/apply-template.py --target <target>`를 사용하고, 기존 프로젝트에는 먼저 `--dry-run`으로 충돌을 확인한다.
