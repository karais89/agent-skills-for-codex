# 실행 계획 기준

`docs/exec-plans/`는 장시간 작업, 큰 변경, 여러 단계가 필요한 구현의 계획과 진행 상태를 보관한다.

## 디렉터리

- `active/`: 현재 진행 중인 ExecPlan을 둔다.
- `completed/`: 완료된 ExecPlan을 둔다.
- `template.md`: 새 ExecPlan을 만들 때 복사할 구조다.

## Alias workflow

- `plan` 또는 `plan:`: `$harness-exec-plan`을 사용해 `active/<slug>.md`를 작성하거나 갱신한다.
- `build` 또는 `build:`: `$harness-exec-build`를 사용해 active ExecPlan의 첫 번째 미완료 체크박스를 구현하고 검증한다.

`build` 한 번은 하나의 체크박스를 완료할 수 있는 크기를 목표로 한다. 체크박스는 검증이 끝난 뒤에만 완료 처리한다.

## 작성 기준

- 관련 product spec이 있으면 반드시 링크한다.
- 현재 상태와 범위를 먼저 적고, 구현 순서는 그 다음에 적는다.
- 체크리스트는 thin vertical slice 기준으로 쪼갠다.
- 각 항목에는 수용 기준과 검증 방법이 있어야 한다.
- 구현 중 발견한 사실과 결정은 같은 ExecPlan에 기록한다.
- 모든 항목이 완료되면 완료 회고를 추가하고, 사용자 확인 후 `completed/`로 이동한다.

## Legacy 경로 금지

이 하네스는 `tasks/plan.md`와 `tasks/todo.md`를 사용하지 않는다. 실행 계획과 체크리스트는 active ExecPlan 안에 함께 둔다.
