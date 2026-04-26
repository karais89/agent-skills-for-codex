# 하네스 템플릿 Git 기반 시뮬레이션 실행 결과

## 목적

full 하네스 템플릿을 실제 Git 저장소 형태의 대상 프로젝트에 적용하고 `spec -> plan -> build -> build` 흐름이 Git 상태를 인식한 채 이어지는지 확인한다.

## 실행 대상

- fixture: `/tmp/harness-git-sim.GwoaGA/project`
- 템플릿 적용 명령: `python3 harness/scripts/build-template.py --generate /tmp/harness-git-sim.GwoaGA/project`
- fixture Git 브랜치: `main`
- 최종 fixture 상태: clean

## 범위

- `/tmp` 아래에 새 대상 프로젝트 fixture를 만들었다.
- `build-template.py --generate`로 full 템플릿을 적용했다.
- fixture에서 `git init`과 초기 커밋을 수행했다.
- `codex exec "spec: ..."`를 실행했다.
- `codex exec "plan: ..."`를 실행했다.
- `codex exec "build"`를 두 번 실행했다.
- 생성 파일, Git 상태, legacy/reference 경로 부재를 확인했다.
- 원 저장소 템플릿 정적 검증을 다시 실행했다.

## 제외 항목

- full 템플릿 내용 변경.
- `$harness-apply` 스킬 작성.
- 모든 ExecPlan 항목 완료.
- 로컬 서버 browser smoke 강제 실행. 현재 sandbox에서 TCP socket bind가 차단되어 한계로 기록했다.

## 진행 체크리스트

- [x] Git fixture를 만들고 템플릿을 적용한다.
- [x] 초기 Git 커밋을 만들어 깨끗한 대상 프로젝트 상태를 준비한다.
- [x] `spec` 시뮬레이션을 실행하고 product spec 생성을 확인한다.
- [x] `plan` 시뮬레이션을 실행하고 active ExecPlan 생성을 확인한다.
- [x] 첫 번째 `build`가 첫 미완료 체크박스를 처리하는지 확인한다.
- [x] 두 번째 `build`가 다음 미완료 체크박스로 넘어가는지 확인한다.
- [x] legacy/reference 경로가 생성되지 않았는지 확인한다.
- [x] 검증 결과를 기록하고 커밋한다.

## 검증 기록

| 날짜 | 항목 | 실행한 검증 | 결과 |
| --- | --- | --- | --- |
| 2026-04-26 | 템플릿 적용 | `python3 harness/scripts/build-template.py --generate /tmp/harness-git-sim.GwoaGA/project` | 통과: full 템플릿이 fixture root에 생성되었다. |
| 2026-04-26 | fixture 초기화 | `git init`, `git add .`, `git commit -m "Initial harness template"` | 통과: 초기 커밋 `ee4141b` 생성. |
| 2026-04-26 | `spec` smoke | `codex exec --sandbox workspace-write "spec: ..."` | 통과: `docs/product-specs/personal-counter-app.md`와 색인이 생성되고 root `SPEC.md`는 생성되지 않았다. fixture 커밋 `2c6d40d`. |
| 2026-04-26 | `plan` smoke | `codex exec --sandbox workspace-write "plan: ..."` | 통과: `docs/exec-plans/active/personal-counter-app.md`가 생성되고 product spec이 갱신되었다. fixture 커밋 `e30b8b3`. |
| 2026-04-26 | `build` smoke 1 | `codex exec --sandbox workspace-write "build"` | 통과: 첫 번째 체크박스가 완료되고 정적 앱 골격, 검증 스크립트, 검증 기록이 추가되었다. fixture 커밋 `98a66e9`. |
| 2026-04-26 | 작업 1 재검증 | `npm run verify` | 통과: lint와 3개 smoke test가 통과했다. |
| 2026-04-26 | `build` smoke 2 | `codex exec --sandbox workspace-write "build"` | 통과: 두 번째 체크박스가 완료되고 `createCounter` 저장 로직과 TDD 검증 기록이 추가되었다. fixture 커밋 `5e2aa6a`. |
| 2026-04-26 | 작업 2 재검증 | `npm run verify` | 통과: lint와 11개 counter/storage test가 통과했다. |
| 2026-04-26 | 작업 2 diff 검증 | `git diff --check` | 통과. |
| 2026-04-26 | forbidden path | `find . \( -name SPEC.md -o -path './tasks/plan.md' -o -path './tasks/todo.md' -o -path './docs/references' \) -print` | 통과: 출력 없음. |
| 2026-04-26 | fixture 최종 상태 | `git status --short`, `git log --oneline --max-count=6` | 통과: status clean, 최종 커밋 `5e2aa6a`. |
| 2026-04-26 | 템플릿 drift 확인 | `python3 harness/scripts/build-template.py --check` | 통과: `harness/source/full/root`와 `harness/templates`가 일치한다. |
| 2026-04-26 | 템플릿 정적 검증 | `python3 harness/scripts/validate-template.py` | 통과: template validation ok. |
| 2026-04-26 | 원 저장소 diff 검증 | `git diff --check` | 통과. |

## fixture 커밋 로그

| 커밋 | 내용 |
| --- | --- |
| `5e2aa6a` | 작업 2: 카운터 상태와 `localStorage` 저장 로직 구현 |
| `98a66e9` | 작업 1: 정적 앱 골격과 검증 명령 추가 |
| `e30b8b3` | 개인용 카운터 ExecPlan 추가 |
| `2c6d40d` | 개인용 카운터 product spec 추가 |
| `ee4141b` | full 하네스 템플릿 초기 적용 |

## 확인한 동작

- `spec` alias는 `$harness-product-spec`로 라우팅되어 `docs/product-specs/` 아래 산출물을 만들었다.
- `plan` alias는 `$harness-exec-plan`로 라우팅되어 `docs/exec-plans/active/` 아래 산출물을 만들었다.
- 첫 번째 `build`는 active ExecPlan의 첫 번째 미완료 체크박스만 구현했다.
- 두 번째 `build`는 다음 미완료 체크박스인 작업 2로 넘어갔다.
- 각 `build`는 같은 ExecPlan에 검증 기록과 결정 로그를 남겼다.
- 새 target 프로젝트에서 `docs/references`, root `SPEC.md`, `tasks/plan.md`, `tasks/todo.md`는 생성되지 않았다.

## 발견 사항

- full 템플릿은 Git 저장소로 초기화된 대상 프로젝트에서 `spec -> plan -> build -> build` 흐름을 유지한다.
- `build`는 직전 작업을 fixture Git 커밋으로 고정한 뒤 실행하면 다음 체크박스를 안정적으로 선택한다.
- 첫 번째 `build`에서 `npm run serve` 확인을 시도했지만 현재 Codex sandbox가 TCP socket bind를 `PermissionError: [Errno 1] Operation not permitted`로 차단했다. 이는 템플릿 실패가 아니라 실행 환경 제한으로 기록했다.
- `codex exec` 종료 시 session rollout 기록 경고가 출력됐지만 명령 exit code는 0이고 대상 파일 변경과 fixture 커밋은 정상적으로 완료되었다.

## 완료 조건

- [x] Git repo fixture에서 `spec`, `plan`, `build` alias가 정상 라우팅된다.
- [x] 첫 번째 `build`가 첫 미완료 체크박스를 처리한다.
- [x] 두 번째 `build`가 다음 미완료 체크박스를 처리하거나 한계를 명확히 기록한다.
- [x] legacy/reference 경로가 생성되지 않는다.
- [x] 원 저장소 템플릿 정적 검증이 통과한다.
- [x] 결과가 문서화되고 커밋되어 있다.

## 결론

현재 full 하네스 템플릿은 다른 프로젝트에 복제한 뒤 Git 기반으로 사용하는 목적에 적합하다. 최소한의 실제 시뮬레이션에서 템플릿 적용, 제품 요구사항 작성, 실행 계획 작성, 순차 build 2회, 검증 기록 갱신, legacy/reference 경로 미생성이 모두 확인되었다.
