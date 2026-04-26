# 하네스 템플릿 사용성 정리 실행 계획

## 목적

`harness/source/full/root/`의 사용자-facing 문서를 대상 프로젝트에 복제했을 때 바로 읽히는 시작 문서로 정리한다. 템플릿 저장소 운영자용 설명과 fixture 검증 절차는 대상 프로젝트 문서에서 제거하거나 내부 문서로 분리한다.

## 현재 상태

- full 템플릿 원본은 `harness/source/full/root/`이다.
- `harness/templates/`는 빌드 산출물이다.
- 실제 `codex exec spec -> plan -> build` 시뮬레이션은 통과했다.
- root `README.md`에는 대상 프로젝트 문서와 템플릿 배포자용 설명이 섞여 있다.

## 범위

- `harness/source/full/root/README.md`를 대상 프로젝트용 시작 문서로 수정한다.
- `AGENTS.md`, `ARCHITECTURE.md`, `docs/README.md`, `docs/validation.md` 문구를 대상 프로젝트 관점에서 점검하고 필요한 최소 수정만 한다.
- source 변경 후 `harness/templates/`를 재생성한다.
- 템플릿 drift와 validate를 확인한다.

## 제외 항목

- full 배포 모델 변경.
- `$harness-apply` 스킬 또는 적용 스크립트 작성.
- Git 기반 현실 시뮬레이션 재실행.
- v0.1 완료 기준 전체 문서화.

## 진행 체크리스트

- [x] 템플릿 원본 문서의 메타 설명과 대상 프로젝트용 설명을 구분한다.
- [x] 대상 프로젝트 루트 `README.md`를 자연스러운 시작 문서로 수정한다.
- [x] 나머지 기본 문서의 자리표시자와 운영 문구를 점검한다.
- [x] `harness/templates/`를 source에서 재생성한다.
- [x] 검증 명령을 실행하고 결과를 기록한다.
- [x] 변경 사항을 커밋한다.

## 검증 계획

| 항목 | 명령 | 기대 결과 |
| --- | --- | --- |
| source/output drift | `python3 harness/scripts/build-template.py --check` | source와 output 일치 |
| template regenerate | `python3 harness/scripts/build-template.py --write` | 의도한 문서 변경이 output에 반영 |
| template validation | `python3 harness/scripts/validate-template.py` | 전체 검증 통과 |
| 공백 검사 | `git diff --check` | 통과 |

## 검증 기록

| 날짜 | 항목 | 실행한 검증 | 결과 |
| --- | --- | --- | --- |
| 2026-04-26 | source/output drift 확인 | `python3 harness/scripts/build-template.py --check` | 의도한 README 변경 때문에 `README.md` drift 감지 |
| 2026-04-26 | output 재생성 | `python3 harness/scripts/build-template.py --write` | 통과: `harness/templates/` 재생성 |
| 2026-04-26 | source/output drift 재확인 | `python3 harness/scripts/build-template.py --check` | 통과: source와 output 일치 |
| 2026-04-26 | template validation | `python3 harness/scripts/validate-template.py` | 통과 |
| 2026-04-26 | 공백 검사 | `git diff --check` | 통과 |
| 2026-04-26 | fixture 문서 확인 | `python3 harness/scripts/build-template.py --generate /tmp/harness-template-usability.SvYP8I/project` 후 `README.md` 확인 | 통과: README가 대상 프로젝트 시작 문서로 생성되고 legacy/reference 경로 없음 |

## 완료 조건

- [x] 복제된 root `README.md`가 템플릿 저장소 설명이 아니라 대상 프로젝트 시작 문서로 읽힌다.
- [x] `docs/references`, root `SPEC.md`, `tasks/plan.md`, `tasks/todo.md`를 유도하는 문구가 없다.
- [x] source와 output이 일치한다.
- [x] template validation이 통과한다.
- [x] 변경 사항이 커밋되어 있다.
