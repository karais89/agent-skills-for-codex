# 하네스 템플릿 빌더 실행 계획

## 목적

`harness/templates/`를 사람이 직접 관리하는 원본이 아니라 빌드 산출물로 전환한다. 이 저장소 안에 full 배포 모델의 원본 파일 묶음을 두고, repo-local 스킬과 검증 스크립트로 `harness/templates/`를 재생성하거나 현재 산출물과 정확히 비교할 수 있게 한다.

## 현재 상태

- `harness/templates/`에는 다른 프로젝트 루트에 복사할 하네스 템플릿이 있다.
- 템플릿에는 `.agents`, `.codex`, `AGENTS.md`, `ARCHITECTURE.md`, `docs/`가 포함된다.
- 배포 모델은 우선 full로 둔다.
- 아직 `harness/templates/`의 source-of-truth와 재생성 검증 절차가 분리되어 있지 않다.

## 범위

- `harness/source/full/root/`를 full 템플릿 원본으로 만든다.
- 현재 `harness/templates/` 내용을 제거하지 않고 `harness/source/full/root/`에 복제한다.
- `harness/source/full/manifest.toml`을 추가해 full source와 output 경로를 명시한다.
- `.agents/skills/harness-template-build/` 스킬을 추가한다.
- `.agents/skills/harness-template-validate/` 스킬을 추가한다.
- `harness/scripts/build-template.py`를 추가한다.
- `harness/scripts/validate-template.py`를 추가한다.
- build 스크립트가 source에서 임시 출력물을 만들고 현재 `harness/templates/`와 byte-level로 비교할 수 있게 한다.
- validate 스크립트가 설정 파싱, skill frontmatter, hook alias, forbidden 파일, source/templates drift를 확인하게 한다.

## 제외 항목

- 현재 `harness/templates/` 삭제 또는 재배치.
- 다른 프로젝트에 실제 적용하는 `$harness-apply` 스킬 작성.
- minimal 배포 모델 설계.
- 템플릿 내용 자체의 큰 재설계.
- 브라우저 기반 `codex exec build` smoke 재실행.

## 진행 체크리스트

- [x] 현재 `harness/templates/` 상태를 확인한다.
- [x] `harness/source/full/root/`에 현재 템플릿을 복제한다.
- [x] `harness/source/full/manifest.toml`을 작성한다.
- [x] `harness/scripts/build-template.py`를 작성한다.
- [x] `harness/scripts/validate-template.py`를 작성한다.
- [x] `.agents/skills/harness-template-build/SKILL.md`를 작성한다.
- [x] `.agents/skills/harness-template-build/agents/openai.yaml`을 작성한다.
- [x] `.agents/skills/harness-template-validate/SKILL.md`를 작성한다.
- [x] `.agents/skills/harness-template-validate/agents/openai.yaml`을 작성한다.
- [x] build 스크립트로 source에서 만든 임시 출력물이 현재 `harness/templates/`와 정확히 일치하는지 확인한다.
- [x] validate 스크립트가 통과하는지 확인한다.
- [x] 변경 사항을 커밋한다.

## 검증 계획

| 항목 | 명령 | 기대 결과 |
| --- | --- | --- |
| 공백 검사 | `git diff --check` | 통과 |
| build 비교 | `python3 harness/scripts/build-template.py --check` | source와 `harness/templates/`가 일치 |
| validate | `python3 harness/scripts/validate-template.py` | 전체 검증 통과 |
| 스킬 검증 | `quick_validate.py`로 신규 스킬 2개 확인 | 통과 |
| 상태 확인 | `git status --short` | 의도한 파일만 변경 |

## 완료 조건

- [x] `harness/source/full/root/`가 현재 `harness/templates/`와 같은 파일 묶음을 가진다.
- [x] build 스크립트가 템플릿 산출물을 재생성하고 비교할 수 있다.
- [x] validate 스크립트가 full 템플릿의 기본 품질 기준을 확인한다.
- [x] 신규 스킬 2개가 루트 `.agents/skills/` 아래에서 유효하다.
- [x] 검증 결과가 이 문서에 기록되어 있다.
- [x] 변경 사항이 커밋되어 있다.

## 검증 기록

| 날짜 | 항목 | 실행한 검증 | 결과 |
| --- | --- | --- | --- |
| 2026-04-26 | 작업 전 상태 | `git status --short` | clean |
| 2026-04-26 | source 복제 | `cp -R harness/templates/. harness/source/full/root/` | 현재 템플릿을 full source로 복제 |
| 2026-04-26 | build 비교 | `python3 harness/scripts/build-template.py --check` | 통과: `harness/source/full/root`와 `harness/templates` 일치 |
| 2026-04-26 | validate | `python3 harness/scripts/validate-template.py` | 통과: 설정 파싱, skill frontmatter, hook, forbidden path, drift 확인 |
| 2026-04-26 | 신규 스킬 검증 | `quick_validate.py .agents/skills/harness-template-build`, `quick_validate.py .agents/skills/harness-template-validate` | 둘 다 통과 |
| 2026-04-26 | 공백 검사 | `git diff --check` | 통과 |
