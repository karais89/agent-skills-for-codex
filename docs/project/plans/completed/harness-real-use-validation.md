# 하네스 템플릿 실사용 검증 사례 축적 결과

## 목적

full 하네스 템플릿을 여러 실제형 fixture 프로젝트에 적용해 새 프로젝트와 기존 프로젝트에서의 사용성, 충돌 양상, `spec -> plan -> build` 흐름의 반복 가능성을 확인한다.

## 배경

- 로컬 브라우저 smoke에서는 새 Git fixture에 full 템플릿을 적용하고 `spec`, `plan`, `build`, 실제 브라우저 검증까지 확인했다.
- 다음 단계는 단일 happy path를 넘어 서로 다른 프로젝트 형태에서 full 템플릿이 어디까지 자연스럽게 작동하는지 사례를 축적하는 것이다.
- full 템플릿은 `README.md`, `AGENTS.md`, `docs/`를 포함하므로 기존 프로젝트에서는 충돌이 정상적으로 발생할 수 있다. 이 작업은 성공 사례뿐 아니라 적용 전 마찰도 기록한다.

## 범위

- `/tmp` 아래에 최소 3개 fixture 프로젝트를 만든다.
- 각 fixture는 Git 저장소로 초기화한다.
- `harness/scripts/apply-template.py --dry-run`과 실제 적용 가능 여부를 확인한다.
- 적용이 성공한 fixture에서는 가능한 범위에서 `codex exec --sandbox workspace-write "spec: ..."`, `plan: ...`, `build` 흐름을 실행한다.
- 각 fixture의 기존 테스트나 간단한 검증 명령을 실행한다.
- root `SPEC.md`, `tasks/plan.md`, `tasks/todo.md`, `docs/references`가 생성되지 않는지 확인한다.
- fixture 자체는 저장소에 추가하지 않고, 결과만 이 계획 문서에 기록한다.

## 제외 항목

- 하네스 템플릿 구조 변경.
- `apply-template.py` 동작 변경.
- full 템플릿 외 minimal 배포 모델 설계.
- 실제 외부 프로젝트 저장소 변경.

## 시나리오

| ID | fixture 유형 | 확인하려는 점 |
| --- | --- | --- |
| A | 새 빈 프로젝트 | full 템플릿이 새 프로젝트 초기 하네스로 바로 작동하는지 확인한다. |
| B | 기존 Node 앱 | 기존 소스와 package/test 파일이 있을 때 하네스가 비침투적으로 붙는지 확인한다. |
| C | 기존 Python CLI 프로젝트 | `README.md`가 있는 기존 프로젝트에서 dry-run 충돌이 명확히 보고되는지 확인한다. |

## 진행 체크리스트

- [x] 원 저장소의 템플릿 상태를 정적 검증한다.
- [x] 시나리오 A를 fixture에서 검증한다.
- [x] 시나리오 B를 fixture에서 검증한다.
- [x] 시나리오 C를 fixture에서 검증한다.
- [x] 각 fixture의 forbidden legacy/reference 경로 부재를 확인한다.
- [x] 결과와 한계를 이 문서에 기록한다.
- [x] 원 저장소 검증 명령을 다시 실행한다.
- [x] completed plan으로 이동하고 커밋한다.

## 검증 계획

- 원 저장소:
  - `python3 harness/scripts/build-template.py --check`
  - `python3 harness/scripts/validate-template.py`
  - `python3 harness/scripts/test-apply-template.py`
  - `git diff --check`
- 각 fixture:
  - `python3 <repo>/harness/scripts/apply-template.py --target <fixture> --dry-run`
  - 충돌이 없으면 `python3 <repo>/harness/scripts/apply-template.py --target <fixture>`
  - 적용 후 config/hook 파싱 확인
  - 가능한 경우 `codex exec --sandbox workspace-write "spec: ..."`
  - 가능한 경우 `codex exec --sandbox workspace-write "plan: ..."`
  - 가능한 경우 `codex exec --sandbox workspace-write "build"`
  - 프로젝트별 테스트 또는 구문 검증
  - forbidden path 검색

## 검증 기록

| 날짜 | 시나리오 | 실행한 검증 | 결과 |
| --- | --- | --- | --- |
| 2026-04-26 | 원 저장소 정적 검증 | `python3 harness/scripts/build-template.py --check`, `python3 harness/scripts/validate-template.py` | 통과: source/output drift 없음, template validation 통과. |
| 2026-04-26 | 원 저장소 스크립트 smoke | `python3 harness/scripts/test-apply-template.py`, `python3 harness/scripts/test-template-builder.py` | 통과: apply smoke 5개, builder smoke 2개. |
| 2026-04-26 | A: 새 빈 프로젝트 | `/tmp/harness-real-use-a-empty-project`에서 dry-run, apply, config/hook 파싱, `spec -> plan -> build`, `npm test`, `git diff --check`, forbidden path 확인 | 통과: 충돌 0건, product spec과 active ExecPlan 생성, 정적 앱 scaffold와 테스트 생성, `npm test` 3개 통과. |
| 2026-04-26 | B: 기존 Node 앱 | `/tmp/harness-real-use-b-node-app`에서 기존 앱 커밋 후 dry-run, apply, `npm test`, config/hook 파싱, `spec -> plan -> build`, forbidden path 확인 | 통과: README가 없는 기존 Node 앱에는 충돌 없이 적용됐고, 적용 커밋은 기존 `package.json`, `src/index.js`, `test/smoke.test.js`를 변경하지 않았다. 최종 `npm test` 6개 통과. |
| 2026-04-26 | C: 기존 Python CLI 프로젝트 | `/tmp/harness-real-use-c-python-cli`에서 기존 `README.md` 포함 프로젝트에 dry-run과 실제 apply 실행, `unittest`, 부분 복사 여부, forbidden path 확인 | 통과: dry-run과 실제 apply 모두 `README.md` content conflict로 exit code 1을 반환했고, `.codex`, `.agents`, `AGENTS.md`, `docs/product-specs`, `docs/exec-plans` 부분 복사는 발생하지 않았다. 기존 unittest 2개 통과. |
| 2026-04-26 | 원 저장소 최종 검증 | `python3 harness/scripts/build-template.py --check`, `python3 harness/scripts/validate-template.py`, `python3 harness/scripts/test-apply-template.py`, `python3 harness/scripts/test-template-builder.py`, `git diff --check` | 통과. |

## 발견 사항

- 새 빈 프로젝트에서는 full 하네스가 초기 프로젝트 골격으로 바로 적용됐다. `spec -> plan -> build` 흐름은 product spec, active ExecPlan, 첫 구현 단위와 검증 기록까지 생성했다.
- README가 없는 기존 Node 앱에는 full 하네스가 비침투적으로 붙었다. 하네스 적용 커밋은 기존 앱 파일을 바꾸지 않았고, 이후 `build` 단계에서만 계획에 따른 앱 코드 변경이 발생했다.
- README가 있는 기존 프로젝트에서는 충돌이 정상적으로 드러났다. dry-run과 실제 apply 모두 같은 충돌을 보고했고, 충돌 시 부분 복사를 하지 않는 안전 동작이 확인됐다.
- 세 fixture 모두 root `SPEC.md`, `tasks/plan.md`, `tasks/todo.md`, `docs/references` 금지 경로를 만들지 않았다.
- `codex exec` 실행 중 `unknown feature key in config: rmcp_client`와 `localhost:8080/mcp` 연결 실패 경고가 관찰됐지만, 시나리오 A/B의 `spec -> plan -> build` 진행을 막지는 않았다.
- `codex exec --sandbox workspace-write` 내부에서는 localhost socket bind가 제한됐다. 시나리오 A는 fixture 직접 셸에서 `npm run serve` listen을 별도 확인했다.
- full 템플릿은 기존 프로젝트의 `README.md`, `AGENTS.md`, `docs/`와 충돌하기 쉬운 배포 모델이다. 이는 덮어쓰지 않는 안전성 측면에서는 장점이지만, 이미 문서 구조가 있는 프로젝트에는 수동 병합 절차가 필요하다.

## 결정 로그

- 2026-04-26: 사용자 요청에 따라 3개 이상의 서브에이전트를 호출해 fixture 검증을 병렬로 진행한다.
- 2026-04-26: 실사용 검증은 성공 사례뿐 아니라 기존 프로젝트 충돌 사례도 포함한다. 충돌 감지는 full 템플릿의 중요한 안전 동작이기 때문이다.
- 2026-04-26: 기존 프로젝트 fixture B는 `README.md`를 의도적으로 만들지 않아 full 템플릿이 기존 소스와 package/test 파일에 비침투적으로 붙는지 확인했다.
- 2026-04-26: 기존 프로젝트 fixture C는 `README.md`를 의도적으로 만들어 충돌 보고와 무부분복사 동작을 확인했다.

## fixture 결과 요약

| 시나리오 | fixture | 최종 상태 | 주요 커밋 |
| --- | --- | --- | --- |
| A | `/tmp/harness-real-use-a-empty-project` | clean | `38264c1` build scaffold, `ff9971c` ExecPlan, `78f5cf9` spec, `c2c0ff9` template apply |
| B | `/tmp/harness-real-use-b-node-app` | clean | `4a9cd7b` usage counter flow, `c95b496` template apply, `73a7661` initial Node fixture |
| C | `/tmp/harness-real-use-c-python-cli` | clean | `07ea65d` initial Python CLI fixture |

## 후속 판단

- full 템플릿은 새 프로젝트 또는 문서 골격이 아직 없는 기존 프로젝트에 우선 적용하는 것이 적합하다.
- 이미 `README.md`, `AGENTS.md`, `docs/`가 있는 프로젝트에는 현재 `apply-template.py`의 충돌 보고를 기준으로 사람이 병합하는 절차가 필요하다.
- 반복적으로 기존 프로젝트에 적용할 계획이라면 `README.md`와 `docs/`를 제외하거나 선택 적용할 수 있는 별도 모드가 필요할 수 있다. 다만 이번 작업에서는 minimal 배포 모델을 설계하지 않는다.
- localhost bind 제한은 템플릿 문제가 아니라 현재 `codex exec` sandbox 환경 제약으로 보인다. UI 프로젝트 검증은 sandbox 밖 브라우저 smoke 또는 별도 승인 실행을 전제로 기록해야 한다.

## 완료 조건

- [x] 3개 이상의 fixture 검증 결과가 문서화되어 있다.
- [x] 최소 1개 이상의 적용 성공 사례가 `spec -> plan -> build` 흐름까지 확인되어 있다.
- [x] 기존 프로젝트 충돌 또는 마찰이 관찰되면 구체적인 경로와 후속 판단이 기록되어 있다.
- [x] 원 저장소 정적 검증이 통과한다.
- [x] 결과 문서가 completed로 이동되고 커밋되어 있다.
