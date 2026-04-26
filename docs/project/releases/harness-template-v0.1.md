# 하네스 템플릿 v0.1 릴리즈 후보

## 판정

- 상태: 릴리즈 후보
- 판정일: 2026-04-26
- 배포 모델: `full`
- 태그 후보: `harness-template-v0.1`
- 태그 생성 여부: 미생성

현재 full 하네스 템플릿은 새 프로젝트나 하네스 문서 골격이 없는 기존 프로젝트에 적용 가능한 릴리즈 후보로 판단한다. 이미 `README.md`, `AGENTS.md`, `ARCHITECTURE.md`, `docs/` 문서 체계를 가진 프로젝트에서는 충돌이 정상적인 안전 동작이며, 자동 병합 대상이 아니다.

## 포함 범위

- repo-local `.agents/skills/`
- repo-local `.codex/config.toml`, `.codex/hooks.json`, `.codex/hooks/*.py`
- `.codex/agents/*.toml`
- 대상 프로젝트용 `AGENTS.md`, `README.md`, `ARCHITECTURE.md`
- `docs/product-specs/`
- `docs/exec-plans/`
- `docs/validation.md`

## 제외 범위

- `docs/references`
- 루트 `SPEC.md`
- `tasks/plan.md`
- `tasks/todo.md`
- minimal 배포 모델
- 기존 프로젝트 문서 자동 병합

## 주요 계약

- source-of-truth는 `harness/source/full/root/`이다.
- generated output은 `harness/templates/`이다.
- `harness/templates/`는 직접 편집하지 않는다.
- `spec` alias는 `$harness-product-spec`로 연결된다.
- `plan` alias는 `$harness-exec-plan`으로 연결된다.
- `build` alias는 `$harness-exec-build`로 연결된다.
- `$harness-apply`는 이 저장소의 적용 도구이며 대상 프로젝트 템플릿에 번들하지 않는다.

## 변경 요약

- full 템플릿의 source/output 구조를 고정했다.
- 대상 프로젝트에 복제할 starter `README.md`와 `ARCHITECTURE.md`를 프로젝트별로 수정 가능한 템플릿 형식으로 다듬었다.
- `docs/references`를 템플릿 번들에서 제외하는 정책을 검증 스크립트에 반영했다.
- `apply-template.py`로 dry-run, 충돌 감지, 부분 복사 방지를 제공했다.
- 릴리즈 가능 기준과 내부 릴리즈 체크리스트를 문서화했다.

## 검증 기록

| 날짜 | 검증 | 결과 |
| --- | --- | --- |
| 2026-04-26 | `python3 harness/scripts/build-template.py --check` | 통과: source와 output 일치 |
| 2026-04-26 | `python3 harness/scripts/validate-template.py` | 통과: manifest, config, skill frontmatter, alias routing, forbidden path 검증 |
| 2026-04-26 | `python3 harness/scripts/test-template-builder.py` | 통과: 2 tests |
| 2026-04-26 | `python3 harness/scripts/test-apply-template.py` | 통과: 5 tests |
| 2026-04-26 | `git diff --check` | 통과 |
| 2026-04-26 | `/tmp/harness-release-v0.1.QojJkK/project` fixture 적용 | 통과: 56개 파일 복사, 충돌 0 |
| 2026-04-26 | fixture `README.md`, `ARCHITECTURE.md` 비교 | 통과: `harness/templates/`와 byte-level 일치 |
| 2026-04-26 | fixture forbidden path 검색 | 통과: `SPEC.md`, `tasks`, `docs/references` 없음 |

## 기존 smoke 근거

- `docs/project/plans/completed/harness-real-use-validation.md`: 새 빈 프로젝트, README 없는 기존 Node 앱, README 충돌 기존 Python CLI 프로젝트에 대한 실제 적용 검증을 기록했다.
- `docs/project/plans/completed/harness-local-browser-smoke.md`: `spec -> plan -> build` 이후 생성된 UI를 로컬 브라우저와 Playwright CLI로 확인한 기록을 남겼다.

위 smoke 이후 starter `README.md`와 `ARCHITECTURE.md` 문구가 다듬어졌지만, alias routing과 build workflow 계약은 바뀌지 않았다. 최신 문서 변경은 별도 fixture 적용과 byte-level 비교로 보강했다.

## 알려진 제약

- 기존 프로젝트의 충돌 파일은 자동 병합하지 않는다.
- 대상 프로젝트에 이미 다른 문서 체계가 있으면 수동 비교와 선택 반영이 필요하다.
- `codex exec` smoke는 실행 환경의 Codex 설정, sandbox, 네트워크 상태에 영향을 받을 수 있다.
- 실제 릴리즈 태그는 이 릴리즈 후보 문서와 검증 결과가 커밋된 뒤 별도로 생성한다.

## 릴리즈 조건

- [x] source와 output이 일치한다.
- [x] full manifest 정책이 유지된다.
- [x] forbidden legacy/reference 경로가 없다.
- [x] 적용 스크립트가 충돌 시 부분 복사를 하지 않는다.
- [x] starter 문서가 템플릿에서 대상 프로젝트용 형태로 제공된다.
- [x] 릴리즈 후보 문서가 남아 있다.
- [ ] 릴리즈 태그가 생성되어 있다.
