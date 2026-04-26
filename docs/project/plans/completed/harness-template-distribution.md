# 하네스 템플릿 배포 방식 확정 실행 계획

## 목적

full 하네스 템플릿의 원본, 산출물, 적용 방식을 문서로 명확히 한다. 다른 프로젝트에 복제해 쓰는 모델을 우선 고정하고, `$harness-apply` 스킬은 별도 후속 작업으로 남긴다.

## 현재 상태

- full source-of-truth는 `harness/source/full/root/`이다.
- generated output은 `harness/templates/`이다.
- `harness/scripts/build-template.py`는 `--check`, `--write`, `--generate <target>`을 제공한다.
- `harness/README.md`는 산출물 영역 원칙은 설명하지만 현재 full 배포 모델과 적용 계약을 충분히 명시하지 않는다.

## 범위

- `harness/README.md`에 full 배포 모델을 명시한다.
- source-of-truth와 generated output의 편집 규칙을 명시한다.
- 적용 방식은 우선 `build-template.py --generate <target>`와 `harness/templates/.` 직접 복사를 허용하는 모델로 정리한다.
- `$harness-apply` 스킬은 지금 만들지 않고 후속 작업으로 둔다.
- 내부 문서 색인이 새 계약과 모순되지 않게 조정한다.

## 제외 항목

- `$harness-apply` 스킬 작성.
- 적용 스크립트 추가.
- minimal 배포 모델 설계.
- Git 기반 현실 시뮬레이션 재실행.

## 진행 체크리스트

- [x] 배포 모델과 적용 계약을 `harness/README.md`에 정리한다.
- [x] 내부 문서 색인의 링크 설명을 현재 역할에 맞게 수정한다.
- [x] 검증 명령을 실행하고 결과를 기록한다.
- [x] 변경 사항을 커밋한다.

## 검증 계획

| 항목 | 명령 | 기대 결과 |
| --- | --- | --- |
| source/output drift | `python3 harness/scripts/build-template.py --check` | source와 output 일치 |
| template validation | `python3 harness/scripts/validate-template.py` | 전체 검증 통과 |
| builder tests | `python3 harness/scripts/test-template-builder.py` | 통과 |
| 공백 검사 | `git diff --check` | 통과 |

## 검증 기록

| 날짜 | 항목 | 실행한 검증 | 결과 |
| --- | --- | --- | --- |
| 2026-04-26 | 1번 결과 재검증 | `git status --short`, `python3 harness/scripts/build-template.py --check`, `python3 harness/scripts/validate-template.py`, `python3 harness/scripts/test-template-builder.py`, `git diff --check` | 통과: worktree clean, source/output 일치, template validation 통과, builder test 2개 통과 |
| 2026-04-26 | source/output drift | `python3 harness/scripts/build-template.py --check` | 통과: source와 output 일치 |
| 2026-04-26 | template validation | `python3 harness/scripts/validate-template.py` | 통과 |
| 2026-04-26 | builder tests | `python3 harness/scripts/test-template-builder.py` | 통과: 2 tests |
| 2026-04-26 | 공백 검사 | `git diff --check` | 통과 |
| 2026-04-26 | `--generate` 적용 방식 | `/tmp/harness-generate-contract.YXTp7W/project`에 `python3 harness/scripts/build-template.py --generate` 실행 후 핵심 파일과 forbidden path 확인 | 통과: `AGENTS.md`, `.codex/hooks.json`, `.agents/skills` 존재, legacy/reference 경로 없음 |
| 2026-04-26 | 직접 복사 적용 방식 | `/tmp/harness-copy-contract.*`에 `cp -R harness/templates/. <target>/` 실행 후 핵심 파일과 forbidden path 확인 | 통과: `README.md`, `.codex/config.toml`, `docs/exec-plans/active` 존재, legacy/reference 경로 없음 |

## 완료 조건

- [x] `harness/source/full/root/`가 source-of-truth임이 명확하다.
- [x] `harness/templates/`가 generated output임이 명확하다.
- [x] 현재 적용 방식과 후속 `$harness-apply` 범위가 분리되어 있다.
- [x] 검증이 통과했다.
- [x] 변경 사항이 커밋되어 있다.
