# AGENTS.md

## 프로젝트 지침

- 이 프로젝트는 Git으로 관리한다.
- 모든 문서는 한글로 작성한다.
- `AGENTS.md`는 프로젝트 지침의 짧은 진입점으로 유지하고, 세부 지식은 `docs/` 아래에 정리한다.
- `docs/project/`는 이 저장소를 개발하고 운영할 때 따르는 내부 문서로 사용한다.
- `harness/`는 다른 프로젝트에 적용할 하네스 산출물과 템플릿을 보관한다.
- 내부 운영 문서와 하네스 산출물을 섞지 않는다. 산출물로 승격할 내용은 `harness/`에 별도로 정리한다.
- 외부 참고 저장소는 `reference-repos/adopted/` 또는 `reference-repos/not-adopted/` 아래에 클론하며 Git 추적 대상에서 제외한다.
- 참고 저장소 목록과 사용 목적은 `docs/references/analyses/reference-repositories.md`에서 확인한다.
- OpenAI Harness Engineering과 Codex 실행 계획 문서는 `docs/references/adopted/` 아래의 한글 참고 문서를 우선 확인한다.
- 복잡한 기능 구현, 큰 리팩터링, 장시간 작업은 실행 계획을 먼저 작성하거나 갱신한 뒤 진행한다.
- 하네스 템플릿은 별도 테스트 대상에 적용한 뒤 검증한다. 필요한 경우 템플릿이 적용된 테스트 프로젝트에서 `codex exec` 기반 시뮬레이션을 실행하고 절차와 결과를 문서화한다.
- 의미 있는 작업 단위가 완료되면 별도 요청이 없어도 관련 변경 사항을 확인한 뒤 자동으로 커밋한다.
