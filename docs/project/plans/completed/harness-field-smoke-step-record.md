# 하네스 템플릿 단계별 현장 smoke 검증 기록

## 목적

full 하네스 템플릿을 작은 기존 프로젝트 fixture에 적용한 뒤 `spec -> plan -> build` 흐름이 실제로 단계별로 작동하는지 확인한다. 이 기록은 하네스가 다른 프로젝트에 그대로 복제해 쓸 수 있는 형태인지 판단하기 위한 실행 증거다.

## 실행 대상

- fixture: `/tmp/harness-field-smoke.dMHd0p/project`
- fixture 유형: 기존 Node.js note store 프로젝트
- fixture Git 브랜치: `main`
- 최종 fixture 상태: clean
- 검증 날짜: 2026-04-27

## 범위

- `/tmp` 아래에 기존 프로젝트 형태의 fixture를 만든다.
- 원 저장소의 템플릿 source/output drift와 정적 유효성을 확인한다.
- `harness/scripts/apply-template.py`로 dry-run 후 실제 적용한다.
- 대상 프로젝트에서 기존 테스트가 유지되는지 확인한다.
- 대상 프로젝트에서 `codex exec` 기반 `spec`, `plan`, `build` 시뮬레이션을 순서대로 실행한다.
- root `SPEC.md`, `tasks/plan.md`, `tasks/todo.md`, `docs/references`가 생성되지 않는지 확인한다.
- 각 의미 있는 단계는 fixture Git 커밋으로 고정한다.

## 제외 항목

- 실제 사용자 프로젝트 변경.
- 하네스 템플릿 구조 변경.
- 모든 ExecPlan 항목 완료.
- 충돌이 있는 기존 문서 구조 병합 검증.
- browser/UI 검증.

## 단계별 실행 기록

| 단계 | 실행 | 결과 |
| --- | --- | --- |
| 1 | fixture 생성: `package.json`, `src/notes.js`, `test/notes.test.js` 작성 후 `npm test` | 기존 테스트 2개 통과. fixture 커밋 `4359060`. |
| 2 | 원 저장소 템플릿 확인: `python3 harness/scripts/build-template.py --check`, `python3 harness/scripts/validate-template.py` | 통과. source/output drift 없음, template validation 통과. |
| 3 | 적용 전 dry-run: `python3 harness/scripts/apply-template.py --target /tmp/harness-field-smoke.dMHd0p/project --dry-run` | 복사 예정 56개, 충돌 0건. |
| 4 | 실제 적용: `python3 harness/scripts/apply-template.py --target /tmp/harness-field-smoke.dMHd0p/project` | 하네스 파일 56개 복사. fixture 커밋 `8a57e23`. |
| 5 | 적용 결과 확인: `AGENTS.md`, `.codex/hooks.json`, `.agents/skills/`, `docs/product-specs/`, `docs/exec-plans/` 존재 확인 | 기대 구조 생성 확인. root `SPEC.md`, `tasks/`, `docs/references`는 생성되지 않음. |
| 6 | 적용 후 기존 프로젝트 검증: `npm test` | 기존 테스트 2개 통과. |
| 7 | spec smoke: `codex exec --cd /tmp/harness-field-smoke.dMHd0p/project --sandbox workspace-write "spec: ..."` | `$harness-product-spec`로 라우팅. `docs/product-specs/note-completion-toggle.md` 생성, 색인 갱신. fixture 커밋 `f6ba9f9`. |
| 8 | spec 산출물 검증 | product spec 필수 섹션 확인. root `SPEC.md`, `tasks/plan.md`, `tasks/todo.md` 미생성 확인. |
| 9 | plan smoke: `codex exec --cd /tmp/harness-field-smoke.dMHd0p/project --sandbox workspace-write "plan: docs/product-specs/note-completion-toggle.md ..."` | `$harness-exec-plan`으로 라우팅. `docs/exec-plans/active/note-completion-toggle.md` 생성. fixture 커밋 `966a15e`. |
| 10 | plan 산출물 검증 | 새 lightweight 체크리스트 필드인 `읽을 파일`, `변경 범위`, `검증`, `완료 기록` 포함 확인. 기준선 `npm test` 2개 통과 기록 확인. |
| 11 | build smoke: `codex exec --cd /tmp/harness-field-smoke.dMHd0p/project --sandbox workspace-write "build"` | `$harness-exec-build`로 라우팅. 첫 번째 미완료 체크박스만 구현. |
| 12 | build 구현 확인 | `src/notes.js`에 `toggleDone(id)` 추가, `test/notes.test.js`에 단일 노트 재토글 테스트 추가. TDD red는 `store.toggleDone is not a function`으로 확인. |
| 13 | build 검증 확인 | `npm test` 3개 통과, `git diff --check` 통과. active ExecPlan 작업 1 체크 완료와 완료 기록 표 갱신 확인. fixture 커밋 `155377d`. |
| 14 | 최종 forbidden path 확인 | `find . \( -path ./.git -o -path ./node_modules \) -prune -o \( -path ./SPEC.md -o -path ./tasks -o -path ./docs/references \) -print` | 출력 없음. |
| 15 | fixture 최종 상태 확인 | `git status --short`, `git log --oneline --max-count=8` | status clean. 최종 커밋 `155377d`. |

## fixture 커밋 로그

| 커밋 | 내용 |
| --- | --- |
| `155377d` | Complete first note toggle build step |
| `966a15e` | Add note completion exec plan |
| `f6ba9f9` | Add note completion spec |
| `8a57e23` | Apply harness template |
| `4359060` | Initial note store fixture |

## 확인한 동작

- `harness/scripts/apply-template.py`는 기존 Node 프로젝트에 하네스 파일을 충돌 없이 추가했고 기존 앱 파일을 변경하지 않았다.
- `spec` alias는 root `SPEC.md`가 아니라 `docs/product-specs/` 아래 product spec을 만들었다.
- `plan` alias는 `tasks/plan.md`, `tasks/todo.md`가 아니라 `docs/exec-plans/active/` 아래 active ExecPlan을 만들었다.
- `build` alias는 active ExecPlan의 첫 번째 미완료 체크박스만 처리했다.
- `build`는 구현, 테스트, ExecPlan 완료 체크, 완료 기록 표 갱신을 한 번의 작업 단위로 수행했다.
- `docs/references`는 대상 프로젝트에 생성되지 않았다.

## 관찰한 경고

- `codex exec` 종료 시 `failed to record rollout items: thread ... not found` 경고가 출력됐다.
- `codex exec` 중 `localhost:8080/mcp` 연결 실패 경고가 관찰됐다.
- 두 경고 모두 명령 exit code와 산출물 생성에는 영향을 주지 않았다. 현재 판단으로는 템플릿 동작 실패가 아니라 실행 환경 경고다.

## 결론

현재 full 하네스 템플릿은 문서 골격이 아직 충돌하지 않는 기존 프로젝트에 복제해 사용하는 기본 목적에 적합하다. 이번 smoke에서는 적용, 기존 테스트 보존, `spec -> plan -> build` alias 라우팅, lightweight ExecPlan 기록 방식, legacy/reference 경로 미생성이 모두 확인됐다.

남은 한계는 명확하다. 이 기록은 작은 Node fixture의 happy path이며, 이미 `README.md`, `AGENTS.md`, `docs/`가 있는 프로젝트의 병합 경험이나 충돌 해소까지 검증하지는 않았다. 해당 범위는 별도 적용 정책이나 충돌 fixture에서 다뤄야 한다.

## 완료 조건

- [x] 기존 프로젝트 fixture를 만들고 기준선 테스트를 통과시켰다.
- [x] 템플릿 정적 검증을 통과시켰다.
- [x] dry-run 후 실제 적용을 수행했다.
- [x] `spec`, `plan`, `build` smoke를 순서대로 실행했다.
- [x] 각 단계 결과를 fixture Git 커밋으로 고정했다.
- [x] forbidden legacy/reference 경로 미생성을 확인했다.
- [x] 결과와 한계를 문서화했다.
