# 문서 색인

이 디렉터리는 프로젝트 요구사항, 실행 계획, 검증 기준을 보관한다.

## 제품 요구사항

- [제품 요구사항 색인](product-specs/index.md)
- [제품 요구사항 템플릿](product-specs/template.md)

`spec` 또는 `spec:` alias는 `$harness-product-spec`을 사용해 `docs/product-specs/<slug>.md`를 작성하거나 갱신한다.

## 실행 계획

- [실행 계획 기준](exec-plans/README.md)
- [실행 계획 템플릿](exec-plans/template.md)
- `exec-plans/active/`: 진행 중인 ExecPlan
- `exec-plans/completed/`: 완료된 ExecPlan

`plan` 또는 `plan:` alias는 `$harness-exec-plan`을 사용해 active ExecPlan을 만든다. `build` alias는 `$harness-exec-build`를 사용해 active ExecPlan의 다음 미완료 항목을 구현하고 검증 결과를 같은 문서에 남긴다.

## 검증

- [검증 기록과 기준](validation.md)

상세 테스트 패턴, 보안 체크리스트, 성능 체크리스트, 접근성 체크리스트는 프로젝트 필요에 따라 별도 문서로 추가한다.

## 금지된 legacy 산출물

이 하네스는 `spec`, `plan`, `build` workflow에서 루트 `SPEC.md`, `tasks/plan.md`, `tasks/todo.md`를 만들지 않는다.
