# 하네스 3개 앱 E2E 및 개선 workflow 검증

## 목적

공개 하네스 설치 프롬프트를 사용해 빈 프로젝트 3개를 만들고, 각 프로젝트에서 `spec -> plan -> build` workflow가 실제 앱 생성과 후속 개선 적용까지 반복 가능한지 확인한다.

이번 검증은 하네스 템플릿 자체를 로컬에서 복사하는 것이 아니라, 공개 저장소의 설치 프롬프트를 기준으로 새 프로젝트를 부트스트랩하는 흐름을 대상으로 한다.

## 테스트 대상

| 프로젝트 | 경로 | 앱 목적 | 담당 |
| --- | --- | --- | --- |
| Focus Timer CLI | `/tmp/harness-app-e2e-timer` | 집중 세션 시작, 완료, 요약을 관리하는 Python CLI | 서브에이전트 A |
| Flashcards CLI | `/tmp/harness-app-e2e-flashcards` | JSON deck 기반 플래시카드 학습 Python CLI | 서브에이전트 B |
| Expense Splitter | `/tmp/harness-app-e2e-splitter` | 참여자별 지출을 균등 정산하는 Python CLI | 서브에이전트 C |

## 진행 체크리스트

- [x] 3개 빈 프로젝트를 서로 다른 `/tmp` 경로에 준비한다.
- [x] 각 프로젝트에서 공개 `harness/prompts/new-project.md` 설치 프롬프트를 사용한다.
- [x] 각 프로젝트에서 초기 앱 생성을 `spec -> plan -> build` 순서로 실행한다.
- [x] 초기 앱 테스트와 smoke 검증을 실행한다.
- [x] 각 앱에서 개선 후보를 선정한다.
- [x] 개선 후보 3개를 다시 `spec -> plan -> build` 순서로 적용한다.
- [x] 개선 후 테스트와 smoke 검증을 실행한다.
- [x] root `SPEC.md`, `tasks/plan.md`, `tasks/todo.md`, `docs/references`가 생성되지 않았는지 확인한다.
- [x] 원 저장소의 템플릿 검증을 다시 실행한다.
- [x] 결과와 발견 사항을 문서화한다.

## 실행한 공통 검증

원 저장소에서 먼저 템플릿 상태를 확인했다.

```bash
python3 harness/scripts/build-template.py --check
python3 harness/scripts/validate-template.py
```

결과:

- `harness/source/full/root`와 `harness/templates` drift 없음.
- full template validation 통과.

각 테스트 프로젝트에서는 다음 흐름을 공통으로 확인했다.

```bash
codex exec --skip-git-repo-check --cd <target> --sandbox danger-full-access "<public setup prompt + answers>"
codex exec --cd <target> --sandbox danger-full-access "spec: ..."
codex exec --cd <target> --sandbox danger-full-access "plan: ..."
codex exec --cd <target> --sandbox danger-full-access "build..."
python3 -m unittest discover -s tests
find . -path './.git' -prune -o \( -path './SPEC.md' -o -path './tasks/plan.md' -o -path './tasks/todo.md' -o -path './docs/references' \) -print
```

## 초기 앱 생성 결과

| 프로젝트 | 결과 | 테스트 | 최종 초기 커밋 |
| --- | --- | --- | --- |
| Focus Timer CLI | 하네스 적용 후 product spec, active ExecPlan, Python CLI 구현 완료 | `python3 -m unittest discover -s tests`: 9개 통과. start, complete, summary smoke 통과 | `936afcc` |
| Flashcards CLI | 하네스 적용 후 deck 저장, add/list/quiz CLI 구현 완료 | `python3 -m unittest discover -s tests`: 17개 통과. add/list/quiz smoke 통과 | `b87ee19893f2588296ec7083ac508baef3648d78` |
| Expense Splitter | 하네스 적용 후 지출 정산 CLI 구현 완료 | `python3 -m unittest`: 7개 통과. 정상 정산, 중복 참여자, 잘못된 금액 smoke 통과 | `77be81bf27d8f2e6ddc50af81af807ea8898d2f9` |

세 프로젝트 모두 공개 설치 프롬프트를 사용했고, 하네스 적용 후 root `SPEC.md`, `tasks/plan.md`, `tasks/todo.md`, `docs/references`는 생성되지 않았다.

## 개선 workflow 검증 결과

| 프로젝트 | 개선 내용 | workflow 결과 | 테스트 | 최종 개선 커밋 |
| --- | --- | --- | --- | --- |
| Focus Timer CLI | `summary --today`, `summary --since YYYY-MM-DD` 날짜 범위 요약 추가 | 개선 spec 생성, active ExecPlan 생성, 4회 build pass로 구현과 문서 갱신 완료 | 23개 unit test 통과. 전체 요약, 오늘 요약, 날짜 이후 요약, 미래 날짜 0건, 잘못된 날짜 exit 2 smoke 통과 | `77f3611` |
| Flashcards CLI | stable card ID 기반 `edit`, `delete` 명령 추가 | 개선 spec/plan 생성 후 5개 task를 build pass로 완료 | 40개 unit test 통과. edit ID 유지, delete 후 번호 재사용 금지, 잘못된 ID와 malformed deck 보호 smoke 통과 | `7b9f7fbe40068fe112c9df0bfd39d4085db0e4c7` |
| Expense Splitter | `--interactive` 대화형 입력 모드 추가 | 개선 spec/plan 생성 후 명시적 ExecPlan 대상 build로 완료 | 14개 unit test 통과. flag 기반 정산, piped stdin interactive 정산, 불완전 입력, quit smoke 통과 | `82a3a730d35223e27379ea21c6d2ede2f30af4e8` |

## 로컬 재검증 기록

검증 완료 후 원 작업 컨텍스트에서 세 프로젝트를 다시 확인했다.

| 프로젝트 | 재실행 명령 | 결과 |
| --- | --- | --- |
| Focus Timer CLI | `python3 -m unittest discover -s tests` | 23개 통과 |
| Flashcards CLI | `python3 -m unittest discover -s tests` | 40개 통과 |
| Expense Splitter | `python3 -m unittest discover -s tests` | 14개 통과 |

금지 경로 확인 결과:

- 세 프로젝트 모두 `SPEC.md`, `tasks/plan.md`, `tasks/todo.md`, `docs/references` 검색 결과 없음.
- Flashcards CLI와 Expense Splitter는 최종 `git status --short --branch`가 clean.
- Focus Timer CLI는 기능 검증 후 `focus_timer/__pycache__/`, `tests/__pycache__/`가 untracked로 남았다. 생성 앱에 `.gitignore`가 없어 생긴 앱 품질 이슈이며, 하네스 alias나 산출물 경로 계약 위반은 아니다.

## 발견 사항

- 공개 설치 프롬프트 기반 bootstrap은 3개 빈 프로젝트에서 모두 동작했다.
- `spec`, `plan`, `build` alias는 루트 `SPEC.md`와 `tasks/`를 만들지 않고 `docs/product-specs/`, `docs/exec-plans/active/`를 사용했다.
- 개선 workflow도 단발성이 아니라 반복 적용 가능했다. 세 프로젝트 모두 초기 앱 생성 뒤 별도 개선 spec과 ExecPlan을 만들고 구현까지 완료했다.
- active ExecPlan이 여러 개 남아 있는 Expense Splitter에서는 bare `build`가 선택을 요구했다. 명시적으로 개선 ExecPlan을 지정하면 정상 진행됐다. 이는 현재 `$harness-exec-build` 계약과 일치한다.
- Flashcards bootstrap 과정에서 첫 설치 시 confirmation 지점에서 멈춰, 확인 문구를 포함한 non-interactive prompt로 재실행했다. 공개 프롬프트를 LLM에게 줄 때는 적용 확인 답변까지 한 번에 포함하는 방식이 더 안정적이다.
- 일부 nested Codex 실행은 sandbox DNS, `/Users/kaya/.codex/sessions` 접근, non-TTY resume 같은 환경 제약을 만났다. 같은 작업을 `danger-full-access`와 명시적 확인 prompt로 재시도하면 완료됐다.
- 생성 앱 수준에서는 Python 프로젝트 공통 `.gitignore`가 빠질 수 있다. 하네스 템플릿 자체의 문제는 아니지만, 새 프로젝트 생성 UX를 엄격히 보려면 기본 profile 문서나 setup prompt에서 언어별 `.gitignore` 생성을 유도할지 검토할 수 있다.

## 판단

현재 하네스 템플릿은 초경량 하네스 엔지니어링 용도로 사용할 가치가 있다.

- 빈 프로젝트에 full 하네스를 적용하고 바로 앱을 만드는 경로가 재현됐다.
- 초기 구현 후 개선 사항을 다시 `spec -> plan -> build`로 넣는 반복성이 확인됐다.
- 하네스 산출물 경로가 기존 legacy 구조로 되돌아가지 않았다.
- 실패 지점은 템플릿 구조보다 nested Codex 실행 환경과 generated app hygiene 쪽에 가깝다.

다만 실제 배포 UX에서는 다음을 보강할 가치가 있다.

- 공개 설치 프롬프트에 confirmation 답변까지 포함한 non-interactive 예시를 더 명확히 둔다.
- 여러 active ExecPlan이 있을 때 `build: <plan path>`를 쓰는 예시를 README 또는 prompt에 추가한다.
- 새 앱 생성 후 언어별 `.gitignore`를 앱 구현 단계에서 만들도록 `build` 요청 예시나 검증 기준에 포함할지 검토한다.

## 완료 조건

- [x] 서브에이전트로 3개 프로젝트를 분리 검증했다.
- [x] 세 프로젝트 모두 공개 설치 프롬프트를 사용했다.
- [x] 세 프로젝트 모두 초기 앱 생성 workflow를 완료했다.
- [x] 세 프로젝트 모두 개선 workflow를 완료했다.
- [x] 개선 사항은 3개 적용했다.
- [x] 테스트와 smoke 검증 결과가 기록되어 있다.
- [x] 금지 경로 부재가 확인되어 있다.
- [x] 남은 마찰과 개선 후보가 기록되어 있다.
