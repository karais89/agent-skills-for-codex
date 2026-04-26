# 하네스 템플릿 v0.2 실행 계획

## 목적

이 문서는 `harness/templates/` v0.2의 작업 범위와 검증 기준을 관리한다. v0.2의 목표는 v0.1 템플릿을 별도 fixture 프로젝트에 반복 적용하고, `codex exec` 기반 smoke 검증 절차와 결과 기록 방식을 안정화하는 것이다.

v0.2는 새 하네스 기능을 크게 늘리는 단계가 아니다. v0.1에서 만든 템플릿이 깨끗한 대상 프로젝트에 적용될 때 어떤 파일을 만들고, 어떤 legacy 산출물을 만들지 않으며, 어떤 환경 제약에서 실패하는지를 재현 가능하게 확인하는 단계다.

## 현재 상태

- v0.1 템플릿은 `harness/templates/` 아래에 작성되어 있다.
- `docs/project/plans/completed/harness-template-v0.1.md`에는 수동 `/tmp` fixture smoke 결과가 기록되어 있다.
- v0.1 검증에서 `spec`과 `plan`은 기대 산출물을 만들었고, 루트 `SPEC.md`와 `tasks/`는 생성되지 않았다.
- v0.1 `build` smoke는 active ExecPlan을 읽고 작업을 진행했지만, HTTP 서버, Playwright, GUI 브라우저 확인은 환경 제약으로 완료하지 못했다.
- 템플릿 적용 절차는 아직 스크립트화되어 있지 않다.

## v0.2 범위

v0.2에서 다루는 범위는 다음과 같다.

- 반복 가능한 fixture 적용 절차를 정의한다.
- fixture를 수동 절차로 충분히 검증할지, 작은 스크립트가 필요한지 판단한다.
- `harness/templates/`를 `/tmp` 아래 깨끗한 테스트 프로젝트에 적용하는 절차를 정리한다.
- `codex exec --skip-git-repo-check` 기반 `spec:`, `plan:`, `build` smoke 입력과 기대 결과를 고정한다.
- 각 smoke 실행 뒤 생성 파일, 수정 파일, 금지된 legacy 산출물 부재를 확인한다.
- 실패하거나 환경에 막히는 검증은 실패 원인, 재현 조건, 후속 확인 환경을 기록한다.
- 필요한 경우 `harness/templates/README.md` 또는 별도 문서에 빠른 적용 검증 절차를 보강한다.
- v0.2 검증 기록과 남은 위험을 이 실행 계획에 남긴다.

## 제외 항목

다음 항목은 v0.2 실행 범위에 포함하지 않는다.

- `spec`, `plan`, `build` alias 계약의 재설계
- `harness-product-spec`, `harness-exec-plan`, `harness-exec-build`의 큰 workflow 변경
- `test`, `review`, `code-simplify`, `ship` wrapper 재설계
- UI 프로젝트 전용 브라우저 검증 체크리스트 작성
- phase/step 실행기나 장시간 자동 실행 프레임워크 작성
- fixture 실행 결과물 전체를 저장소에 커밋하는 방식
- 외부 참고 저장소 갱신

## 진행 체크리스트

- [x] v0.1 완료 회고에서 v0.2로 이어지는 검증 공백을 정리한다.
- [x] fixture 적용 방식을 결정한다: 문서화된 수동 절차만 둘지, 최소 스크립트를 추가할지 판단한다.
- [x] fixture 기본 구조를 정의한다.
- [x] `harness/templates/`를 fixture에 적용하는 명령과 기대 파일 목록을 정리한다.
- [x] `spec:` smoke 입력, 기대 product spec 경로, 금지 산출물 확인 기준을 정한다.
- [x] `plan:` smoke 입력, 기대 active ExecPlan 경로, 금지 산출물 확인 기준을 정한다.
- [x] `build` smoke 입력, 기대 구현 범위, 검증 한계 기록 기준을 정한다.
- [x] smoke 실행 전후 확인 명령을 정리한다.
- [x] 실제 fixture에 템플릿을 적용하고 정적 검증을 실행한다.
- [x] `codex exec --skip-git-repo-check --sandbox workspace-write "spec: ..."` smoke를 실행하고 결과를 기록한다.
- [x] `codex exec --skip-git-repo-check --sandbox workspace-write "plan: ..."` smoke를 실행하고 결과를 기록한다.
- [x] `codex exec --skip-git-repo-check --sandbox workspace-write "build"` smoke를 실행하고 결과를 기록한다.
- [x] 루트 `SPEC.md`, `tasks/plan.md`, `tasks/todo.md`가 생성되지 않았는지 확인한다.
- [x] 필요한 문서 보강을 `harness/templates/README.md` 또는 관련 문서에 반영한다.
- [x] v0.2 검증 기록과 완료 회고를 이 문서에 작성한다.
- [x] 완료 후 이 문서를 `docs/project/plans/completed/`로 이동한다.
- [x] 변경 사항을 의미 있는 작업 단위로 커밋한다.

## 실행 계획

1. v0.1 완료 회고와 현재 `harness/templates/README.md`의 빠른 검증 절차를 비교해 반복 검증에 부족한 정보를 찾는다.
2. fixture 프로젝트는 `/tmp` 아래 새 디렉터리로 만들고, 저장소에는 생성 결과물을 커밋하지 않는다.
3. 적용 절차가 3개 이하의 단순 명령으로 안정화되면 문서 절차로 유지한다. 명령 수가 많거나 실수 가능성이 높으면 작은 스크립트를 추가하는 방안을 선택한다.
4. smoke 입력은 같은 목표를 공유하게 구성한다. 예시는 간단한 메모 목록 기능처럼 product spec, ExecPlan, build가 자연스럽게 이어지는 목표로 둔다.
5. 각 smoke 뒤에는 생성된 문서 경로와 legacy 산출물 부재를 확인한다.
6. `build` smoke는 환경 제약을 명시적으로 기록한다. 서버 bind, npm registry, GUI 브라우저, Playwright 같은 외부 조건이 막히면 체크박스를 완료하지 않고 남은 위험으로 둔다.
7. 반복 가능한 절차가 확인되면 `harness/templates/README.md` 또는 별도 내부 문서에 최소 적용 검증 절차를 반영한다.
8. 검증 기록, 계획과 달라진 점, 남은 위험을 이 문서에 추가한 뒤 completed로 이동한다.

## 검증 계획

| 항목 | 명령 또는 확인 방법 | 기대 결과 |
| --- | --- | --- |
| Git 상태 | `git status --short` | 의도한 v0.2 변경만 존재한다. |
| 패치 공백 | `git diff --check` | 통과한다. |
| 템플릿 설정 파싱 | `.codex/hooks.json`, `.codex/config.toml`, `.codex/agents/*.toml` 파싱 | 모두 파싱된다. |
| 스킬 frontmatter | 모든 `harness/templates/.agents/skills/*/SKILL.md` 확인 | frontmatter가 유효하다. |
| fixture 적용 | `/tmp` fixture에 `harness/templates/` 적용 | 대상 루트에 템플릿 파일이 생성된다. |
| alias hook | fixture에서 `spec:`, `plan:`, `build` 입력을 hook으로 확인 | 각 wrapper 스킬 안내가 출력된다. |
| `spec` smoke | `codex exec --skip-git-repo-check "spec: ..."` | `docs/product-specs/<slug>.md`가 생성 또는 갱신된다. |
| `plan` smoke | `codex exec --skip-git-repo-check "plan: ..."` | `docs/exec-plans/active/<slug>.md`가 생성 또는 갱신된다. |
| `build` smoke | `codex exec --skip-git-repo-check "build"` | active ExecPlan의 첫 미완료 항목을 대상으로 작업하고 검증 기록을 남긴다. |
| legacy 산출물 부재 | fixture에서 `SPEC.md`, `tasks/plan.md`, `tasks/todo.md` 검색 | 생성되지 않는다. |

## 검증 기록

| 날짜 | 항목 | 실행한 검증 | 결과 |
| --- | --- | --- | --- |
| 2026-04-26 | 작업 전 상태 | `git status --short` | clean |
| 2026-04-26 | fixture 생성 | `mktemp -d /tmp/harness-template-v0.2-fixture.XXXXXX` | `/tmp/harness-template-v0.2-fixture.RogCmD` 생성 |
| 2026-04-26 | fixture 적용 | `cp -R harness/templates/. /tmp/harness-template-v0.2-fixture.RogCmD/` | 템플릿 파일과 dot directory 적용 |
| 2026-04-26 | fixture 파일 확인 | `find . -maxdepth 3 -type f -print` | `.codex`, `AGENTS.md`, `ARCHITECTURE.md`, `docs/` 파일 확인 |
| 2026-04-26 | Codex 설정 파싱 | fixture에서 `.codex/hooks.json`, `.codex/config.toml`, `.codex/agents/*.toml` 파싱 | 통과 |
| 2026-04-26 | 스킬 frontmatter | fixture에서 모든 `.agents/skills/*/SKILL.md` 확인 | 통과: 28개 스킬 |
| 2026-04-26 | alias hook | fixture에서 `spec:` 입력을 `user_prompt_submit.py`로 실행 | `$harness-product-spec` routing guidance 출력 |
| 2026-04-26 | `spec` smoke 1차 | `codex exec --skip-git-repo-check "spec: ..."` | 실패: Codex CLI 기본 sandbox가 read-only로 시작되어 파일 생성 차단 |
| 2026-04-26 | `spec` smoke 재시도 | `codex exec --skip-git-repo-check --sandbox workspace-write "spec: ..."` | `docs/product-specs/memo-list.md` 생성, `docs/product-specs/index.md` 갱신 |
| 2026-04-26 | `plan` smoke | `codex exec --skip-git-repo-check --sandbox workspace-write "plan: ..."` | `docs/exec-plans/active/memo-list.md` 생성 |
| 2026-04-26 | `build` smoke | `codex exec --skip-git-repo-check --sandbox workspace-write "build"` | active ExecPlan의 첫 미완료 항목을 읽고 정적 앱 골격 파일을 생성한 뒤 ExecPlan에 검증 기록 추가 |
| 2026-04-26 | `build` 구문 검사 | nested Codex에서 `node --check src/app.js`, `node --check src/memoStore.js` | 통과 |
| 2026-04-26 | `build` 로컬 서버 smoke | nested Codex에서 `python3 -m http.server 4173 --bind 127.0.0.1` | 실패: sandbox socket bind가 `PermissionError: [Errno 1] Operation not permitted`로 차단 |
| 2026-04-26 | socket 실패 원인 확인 | nested Codex에서 Python `socket.bind(('127.0.0.1', 0))` 최소 재현 | 같은 `PermissionError`; 포트 충돌이 아니라 실행 환경의 bind 차단으로 판단 |
| 2026-04-26 | legacy 산출물 부재 | fixture에서 `SPEC.md`, `tasks/plan.md`, `tasks/todo.md`, `tasks/` 검색 | 생성되지 않음 |
| 2026-04-26 | 문서 보강 | `harness/templates/README.md` fixture smoke 절차 갱신 | `codex exec` 명령에 `--sandbox workspace-write` 반영 |
| 2026-04-26 | 패치 공백 | `git diff --check` | 통과 |

## 완료 조건

다음 조건을 모두 만족하면 v0.2를 완료로 본다.

- [x] fixture 적용 절차가 문서화되었거나, 필요한 경우 최소 스크립트로 구현되었다.
- [x] `spec`, `plan`, `build` smoke 검증의 입력과 기대 결과가 기록되어 있다.
- [x] 실제 smoke 실행 결과와 실패 또는 차단 사유가 기록되어 있다.
- [x] legacy 산출물이 생성되지 않는다는 확인 결과가 기록되어 있다.
- [x] v0.2 변경 범위가 템플릿 적용 검증 보강에 한정되어 있다.
- [x] 필요한 문서 보강이 완료되어 있다.
- [x] 변경 사항이 의미 있는 작업 단위로 커밋되어 있다.

## 남은 위험 기록란

- nested `codex exec build`가 만든 정적 앱 골격은 구문과 구조 검증은 통과했지만, 현재 Codex sandbox에서 socket bind가 차단되어 HTTP 서버와 실제 브라우저 확인은 완료하지 못했다.
- fixture를 Git 저장소로 초기화하지 않았기 때문에 nested Codex의 `git status --short`는 실패했다. 실제 대상 프로젝트는 Git 저장소일 가능성이 높으므로, 향후 반복 검증에서는 fixture에 `git init`을 포함할지 검토할 수 있다.
- `codex exec` smoke에는 `--sandbox workspace-write`가 필요하다. 이 옵션이 없으면 기본 read-only sandbox에서 spec 파일 생성부터 차단된다.

## 완료 후 처리

- 완료 날짜: 2026-04-26
- 실제 변경한 파일:
  - `harness/templates/README.md`
  - `docs/project/plans/completed/harness-template-v0.2.md`
- 계획과 달라진 점:
  - fixture 적용 스크립트는 만들지 않았다. 현재 절차는 문서화된 수동 명령으로 충분히 짧고, v0.2 목적은 반복 절차와 차단 사유 기록에 더 가깝기 때문이다.
  - `codex exec` smoke 명령에는 `--sandbox workspace-write`가 필요하다는 점을 실행 중 확인해 README에 반영했다.
  - build smoke의 HTTP 서버 확인은 현재 Codex sandbox의 socket bind 차단으로 실패했다.
- 남은 위험:
  - bind 가능한 환경에서 `python3 -m http.server 4173`와 브라우저 화면 확인을 다시 실행해야 한다.
  - fixture Git 초기화 여부는 v0.3 또는 후속 검증 절차 보강에서 판단한다.
- 후속 작업:
  - v0.3에서 스킬 후보를 조정할 때 fixture 검증 절차를 별도 스킬로 만들 가치가 있는지 검토한다.
  - UI·브라우저 검증 보강 단계에서 build smoke의 브라우저 확인 공백을 다시 다룬다.
