# 하네스 템플릿 v0.1 실행 계획

## 목적

이 문서는 `harness/templates/` 아래에 만들 하네스 템플릿 v0.1의 구현 범위, 진행 체크리스트, 검증 기준을 관리한다. v0.1의 목표는 다른 프로젝트에 복사해 바로 사용할 수 있는 문서 템플릿과 repo-local Codex 스킬/alias 하네스를 함께 제공하는 것이다.

이 문서는 내부 실행 계획이며, 실제 배포 산출물은 아니다. 실제 템플릿 문서와 설정은 `harness/templates/` 아래에 대상 프로젝트 루트 기준 경로를 그대로 미러링해 작성한다.

## 현재 상태

- `harness/templates/` 아래에 문서 템플릿, repo-local `.agents`, `.codex` 하네스 구성을 작성했다.
- `agent-skills-test`의 추적 가능한 repo-local 하네스 구성만 선별해 반영했고, 실험 산출물(`SPEC.md`, `tasks/`, `todo-app/`, `tmp/`)은 제외했다.
- 기존 `agent-skills-spec`, `agent-skills-plan`, `agent-skills-build` wrapper 대신 `harness-product-spec`, `harness-exec-plan`, `harness-exec-build` wrapper를 템플릿에 추가했다.
- hook과 안내 문서는 `spec`, `plan`, `build`, `test`, `review` alias 계약을 기준으로 갱신했다.

## v0.1 범위

v0.1은 다른 프로젝트에 적용할 수 있는 최소 하네스 템플릿을 만든다. 대상 프로젝트는 다음 계약을 갖는다.

| Alias | 스킬 | 산출물 |
| --- | --- | --- |
| `spec`, `spec:` | `$harness-product-spec` | `docs/product-specs/<slug>.md` |
| `plan`, `plan:` | `$harness-exec-plan` | `docs/exec-plans/active/<slug>.md` |
| `build`, `build:` | `$harness-exec-build` | active ExecPlan 기반 구현과 계획 갱신 |
| `test`, `test:` | `$agent-skills-test` | 기존 TDD/검증 workflow |
| `review`, `review:` | `$agent-skills-review` | 기존 5축 리뷰 workflow |

`harness/templates/` 아래의 하위 구조는 대상 프로젝트 루트 기준 경로를 그대로 미러링한다. 예를 들어 `harness/templates/AGENTS.md`는 대상 프로젝트의 `AGENTS.md`가 되고, `harness/templates/.codex/hooks/user_prompt_submit.py`는 대상 프로젝트의 `.codex/hooks/user_prompt_submit.py`가 된다.

v0.1에서 다루는 범위는 다음과 같다.

- 프로젝트 루트용 `AGENTS.md` 템플릿 작성
- 프로젝트 루트용 `ARCHITECTURE.md` 템플릿 작성
- 프로젝트 문서 진입점 템플릿 작성
- 제품 요구사항을 위한 `docs/product-specs/` 구조와 템플릿 작성
- 장시간 작업과 큰 변경을 위한 `docs/exec-plans/` 구조와 실행 계획 템플릿 작성
- 검증 기준을 기록하는 문서 템플릿 작성
- `agent-skills-test`의 `.agents/skills/`, `.codex/` 중 추적 가능한 하네스 구성 반영
- 기존 `agent-skills-spec`, `agent-skills-plan`, `agent-skills-build` wrapper를 새 `harness-product-spec`, `harness-exec-plan`, `harness-exec-build` wrapper로 교체
- `user_prompt_submit.py`, `session_start.py`, `AGENTS.md`, `harness/templates/README.md`의 alias 안내를 새 계약에 맞게 갱신
- 템플릿 문서 간 링크와 공통 용어 정리
- v0.1 완료 기준과 검증 절차 정리

## v0.1 진행 체크리스트

- [x] 기존 내부 문서와 `agent-skills-test`에서 템플릿으로 승격할 규칙과 제외할 규칙을 선별한다.
- [x] `harness/templates/.agents/skills/`에 추적 가능한 스킬을 반영하고 기존 `agent-skills-spec`, `agent-skills-plan`, `agent-skills-build` wrapper를 제외한다.
- [x] `harness/templates/.agents/skills/harness-product-spec/SKILL.md`를 작성한다.
- [x] `harness/templates/.agents/skills/harness-exec-plan/SKILL.md`를 작성한다.
- [x] `harness/templates/.agents/skills/harness-exec-build/SKILL.md`를 작성한다.
- [x] `harness/templates/.codex/config.toml`, `.codex/hooks.json`, `.codex/hooks/*.py`, `.codex/agents/*.toml`을 반영한다.
- [x] `harness/templates/.codex/hooks/user_prompt_submit.py`가 `spec`, `plan`, `build`를 새 harness wrapper로 라우팅하게 한다.
- [x] `harness/templates/.codex/hooks/session_start.py`가 새 alias 계약을 안내하게 한다.
- [x] `harness/templates/AGENTS.md` 초안을 새 alias 계약에 맞게 작성한다.
- [x] `harness/templates/ARCHITECTURE.md` 초안을 작성한다.
- [x] `harness/templates/docs/README.md` 초안을 작성한다.
- [x] `harness/templates/docs/product-specs/index.md`와 `template.md`를 작성한다.
- [x] `harness/templates/docs/exec-plans/README.md`와 `template.md`를 작성한다.
- [x] `harness/templates/docs/exec-plans/active/`와 `completed/`를 Git에 보존할 자리표시자를 작성한다.
- [x] `harness/templates/docs/validation.md` 초안을 작성한다.
- [x] `docs/references` 보조 체크리스트는 기본 템플릿에서 제외하고, 스킬 내부 링크는 upstream 참고 안내로 낮춘다.
- [x] `SPEC.md`, `tasks/`, `todo-app/`, `tmp/`가 템플릿에 포함되지 않았는지 확인한다.
- [x] 문서 간 상대 링크가 실제 경로와 맞는지 확인한다.
- [x] `harness/templates/README.md`가 v0.1 템플릿 목록, alias 계약, 검증 방법을 반영하게 갱신한다.
- [x] 변경 범위가 `harness/templates/`와 필요한 내부 계획 갱신에 한정되는지 확인한다.

## v0.1 산출물 목록

- `harness/templates/.agents/skills/`
- `harness/templates/.codex/config.toml`
- `harness/templates/.codex/hooks.json`
- `harness/templates/.codex/hooks/*.py`
- `harness/templates/.codex/agents/*.toml`
- `harness/templates/AGENTS.md`
- `harness/templates/ARCHITECTURE.md`
- `harness/templates/README.md`
- `harness/templates/docs/README.md`
- `harness/templates/docs/product-specs/index.md`
- `harness/templates/docs/product-specs/template.md`
- `harness/templates/docs/exec-plans/README.md`
- `harness/templates/docs/exec-plans/template.md`
- `harness/templates/docs/exec-plans/active/.gitkeep`
- `harness/templates/docs/exec-plans/completed/.gitkeep`
- `harness/templates/docs/validation.md`

## 제외 항목

다음 항목은 v0.1 실행 범위에 포함하지 않는다.

- `agent-skills-test`의 dirty 산출물인 `SPEC.md`, `tasks/plan.md`, `tasks/todo.md`
- `agent-skills-test`의 실험 앱과 임시 파일인 `todo-app/`, `tmp/`
- 대상 프로젝트 루트에 `SPEC.md`, `tasks/plan.md`, `tasks/todo.md`를 만드는 기존 workflow
- `agent-skills-spec`, `agent-skills-plan`, `agent-skills-build` wrapper 유지
- `test`, `review`, `code-simplify`, `ship` wrapper 재설계
- upstream `agent-skills`의 보조 reference 체크리스트를 `docs/references/`로 기본 vendoring
- phase/step 실행기나 큰 자동화 구조 설계
- UI 프로젝트 전용 브라우저 검증 기준 작성
- 내부 운영 문서 전체 리팩터링

## 검증 기준

v0.1 템플릿 구현이 끝나면 다음 기준으로 확인한다.

- `git diff --check`가 통과한다.
- `.codex/config.toml`, `.codex/agents/*.toml`, `.codex/hooks.json`이 파싱된다.
- 모든 `.agents/skills/*/SKILL.md` frontmatter가 유효하다.
- `skill-creator`의 `quick_validate.py`로 새 harness skill 3개가 통과한다.
- `spec 새 기능...`이 `$harness-product-spec`로 매핑된다.
- `plan ...`이 `$harness-exec-plan`으로 매핑된다.
- `build`가 `$harness-exec-build`로 매핑된다.
- destructive command 차단 hook이 기존처럼 동작한다.
- `/tmp` fixture에 `harness/templates/`를 적용한 뒤 `codex exec "spec: ..."`, `codex exec "plan: ..."`, `codex exec "build"` smoke 검증을 시도하고 결과를 기록한다.
- 템플릿 적용 결과에 루트 `SPEC.md`, `tasks/plan.md`, `tasks/todo.md`가 새로 생성되지 않는다.
- v0.1 산출물 목록의 모든 파일과 디렉터리가 존재한다.
- 문서 간 상대 링크가 실제 경로와 맞다.
- v0.1 제외 항목이 실제 산출물에 구현 범위처럼 섞이지 않는다.

## 검증 기록

| 날짜 | 항목 | 실행한 검증 | 결과 |
| --- | --- | --- | --- |
| 2026-04-26 | 공백과 패치 형식 | `git diff --check` | 통과 |
| 2026-04-26 | Codex 설정 파싱 | `.codex/hooks.json`, `.codex/config.toml`, `.codex/agents/*.toml` 파싱 스크립트 | 통과 |
| 2026-04-26 | 스킬 frontmatter | 모든 `harness/templates/.agents/skills/*/SKILL.md` frontmatter 확인 | 통과: 28개 스킬 |
| 2026-04-26 | 신규 harness 스킬 검증 | `quick_validate.py`로 `harness-product-spec`, `harness-exec-plan`, `harness-exec-build` 검증 | 통과 |
| 2026-04-26 | alias hook | `spec 새 기능 요구사항`, `plan 사용자 설정 화면`, `build` 입력을 `user_prompt_submit.py`로 실행 | 각각 `$harness-product-spec`, `$harness-exec-plan`, `$harness-exec-build`로 매핑됨 |
| 2026-04-26 | destructive command hook | `rm -rf .agents`를 `pre_tool_use.py`로 실행 | exit 2로 차단됨 |
| 2026-04-26 | session start hook | `session_start.py` 실행 | 새 alias 계약과 legacy 파일 금지 안내 출력 |
| 2026-04-26 | 제외 항목 확인 | `harness/templates`에서 `SPEC.md`, `tasks`, `todo-app`, `tmp`, 기존 spec/plan/build wrapper 검색 | 포함되지 않음 |
| 2026-04-26 | references 제외 확인 | `harness/templates`에서 `docs/references` 직접 참조 검색 | 기본 템플릿에서 `docs/references` 제외, 스킬은 upstream references 선택 참고로 정리 |
| 2026-04-26 | smoke: `spec` | `/tmp` fixture에 템플릿을 적용하고 `codex exec --skip-git-repo-check "spec: ..."` 실행 | `docs/product-specs/memo-list.md` 생성, 루트 `SPEC.md`와 `tasks/` 미생성 |
| 2026-04-26 | smoke: `plan` | 같은 fixture에서 `codex exec --skip-git-repo-check "plan: ..."` 실행 | `docs/exec-plans/active/memo-list.md` 생성, legacy 산출물 미생성 |
| 2026-04-26 | smoke: `build` | 같은 fixture에서 `codex exec --skip-git-repo-check "build"` 실행 | active ExecPlan을 읽고 작업 1 구현과 검증 기록을 추가함. Node 테스트와 문법 검사는 통과했지만 HTTP 서버, Playwright, GUI 브라우저 확인은 환경 제약으로 차단되어 체크박스는 미완료로 유지됨 |

## 완료 회고

- 완료 날짜: 2026-04-26
- 실제 작성된 산출물은 v0.1 산출물 목록과 같다.
- 계획과 달라진 점:
  - `build` smoke는 실제 브라우저 수동 검증까지 완료하지 못했다. 현재 실행 환경에서 socket bind, npm registry 접근, GUI 브라우저 실행이 차단되었기 때문이다.
  - 대신 `build` wrapper가 active ExecPlan을 선택하고, 첫 미완료 항목 구현을 진행하며, 검증 결과와 차단 사유를 같은 ExecPlan에 기록하는 계약은 확인했다.
- 남은 위험:
  - 네트워크와 브라우저 실행이 가능한 환경에서 `build` smoke의 실제 브라우저 수동 검증까지 재확인할 필요가 있다.
  - 템플릿 적용 절차는 아직 스크립트화하지 않았으므로 반복 적용 자동화는 v0.2에서 별도 검토한다.

## 완료 조건

다음 조건을 모두 만족하면 v0.1을 완료로 본다.

- [x] v0.1 진행 체크리스트의 모든 항목이 완료되어 있다.
- [x] v0.1 산출물 목록의 파일과 디렉터리가 모두 작성되어 있다.
- [x] 검증 기준을 실행하고 결과를 완료 회고에 기록했다.
- [x] 변경 범위에 v0.1과 무관한 문서, 코드, 설정 변경이 없다.
- [x] `harness/templates/README.md`가 새 템플릿 목록과 alias 계약을 반영한다.
- [x] 변경 사항이 의미 있는 작업 단위로 커밋되어 있다.

## 다음 로드맵

후속 버전은 방향만 이 문서에 남긴다. 각 버전의 세부 실행 계획은 해당 단계에서 별도 계획 문서로 작성한다.

### v0.2: 템플릿 적용 시뮬레이션 보강

- 반복 가능한 fixture 적용 스크립트가 필요한지 검토한다.
- `codex exec` 기반 행동 검증 절차를 문서화한다.
- 기대 행동과 실제 결과 차이를 기록한다.

### v0.3: 스킬 후보 조정

- 문서만으로 반복 수행이 불안정한 작업을 식별한다.
- 실행 계획 작성, 검증 결과 해석, 템플릿 적용 같은 스킬 후보를 정리한다.
- 스킬로 만들 가치가 있는 작업과 문서 지침으로 충분한 작업을 구분한다.

### v0.4: 선택적 자동화 검토

- 반복되는 적용 절차와 검증 절차만 스크립트화할지 검토한다.
- phase/step 실행기나 큰 자동화는 실제 반복 필요가 확인된 뒤 별도 계획에서 다룬다.
- 자동화가 문서 하네스의 이해 가능성을 낮추지 않는지 확인한다.

### v0.5: UI·브라우저 검증 보강

- UI 프로젝트용 검증 체크리스트를 추가한다.
- 브라우저 기반 확인 기준을 정리한다.
- 화면 확인 결과를 템플릿 문서에 기록하는 최소 형식을 검토한다.

## 완료 후 처리

- 이 문서를 `docs/project/plans/completed/`로 이동한다.
- 완료 후 변경 범위를 확인하고, v0.1 구현 단위의 커밋을 만든다.
