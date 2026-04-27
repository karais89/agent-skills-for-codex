# 하네스 템플릿 릴리즈 체크리스트

## 목적

이 문서는 이 저장소에서 full 하네스 템플릿을 릴리즈 가능한 상태로 판단할 때 사용하는 내부 체크리스트다. 대상 프로젝트에 복제되는 사용자용 안내는 `harness/source/full/root/`에서 관리하고 `harness/templates/`로 생성하며, 이 문서는 저장소 운영자가 릴리즈 직전에 확인할 항목을 관리한다.

## 논리 검증

현재 릴리즈 모델은 다음 이유로 일관된다.

- source-of-truth는 `harness/source/full/root/`이고, `harness/templates/`는 생성 산출물이다.
- 적용 도구는 기본적으로 `harness/templates/`만 대상 프로젝트에 복사한다.
- `apply-template.py`는 충돌을 먼저 계산하고, 충돌이 있으면 아무 파일도 복사하지 않는다.
- full 모델은 새 프로젝트나 문서 골격이 없는 기존 프로젝트에 적합하다.
- 이미 `README.md`, `AGENTS.md`, `docs/`가 있는 기존 프로젝트에서는 충돌이 정상적인 안전 동작이다.
- `spec`, `plan`, `build` workflow는 `docs/product-specs/`와 `docs/exec-plans/`를 사용하며, root `SPEC.md`와 `tasks/` legacy 산출물을 만들지 않는다.
- `docs/references`는 이 저장소 내부 참고 자료이며 full 템플릿에는 포함하지 않는다.

따라서 릴리즈 기준은 새 배포 모델을 추가하는 문제가 아니라, 현재 full 모델이 적용 가능한 상태인지 판정하는 절차로 둔다.

## 릴리즈 후보 조건

- [ ] 변경이 `harness/source/full/root/` 원본에 먼저 반영되어 있다.
- [ ] `harness/templates/`는 원본에서 재생성되었고 source와 byte-level로 일치한다.
- [ ] `harness/source/full/manifest.toml`의 배포 모델이 `full`이다.
- [ ] 대상 프로젝트에 복제될 문서가 내부 운영 문서와 섞이지 않는다.
- [ ] root `SPEC.md`, `tasks/plan.md`, `tasks/todo.md`, `docs/references`가 템플릿에 없다.
- [ ] `spec`, `plan`, `build` alias가 각각 `$harness-product-spec`, `$harness-exec-plan`, `$harness-exec-build`로 안내된다.
- [ ] 충돌이 있는 기존 프로젝트에 적용할 때 부분 복사가 발생하지 않는다.
- [ ] 변경 유형에 맞는 fixture smoke가 문서화되어 있다.

## 필수 검증

릴리즈 후보는 최소한 다음 명령을 통과해야 한다.

```bash
python3 harness/scripts/build-template.py --check
python3 harness/scripts/validate-template.py
python3 harness/scripts/test-validate-template.py
python3 harness/scripts/test-template-builder.py
python3 harness/scripts/test-apply-template.py
git diff --check
```

## 변경 유형별 추가 검증

| 변경 유형 | 추가 검증 |
| --- | --- |
| 템플릿 문서 변경 | 임시 fixture에 적용한 뒤 `README.md`, `ARCHITECTURE.md`, `docs/*`가 `harness/templates/`와 일치하는지 확인한다. |
| 스킬 변경 | 모든 `.agents/skills/*/SKILL.md` frontmatter를 검증하고 관련 alias 또는 workflow smoke를 실행한다. |
| hook 또는 config 변경 | `.codex/hooks.json`, `.codex/config.toml`, `.codex/agents/*.toml` 파싱과 hook routing smoke를 실행한다. |
| 적용 도구 변경 | `test-apply-template.py`를 실행하고 새 대상, 기존 Git 대상, 충돌 대상 fixture를 확인한다. |
| `spec`, `plan`, `build` 계약 변경 | clean Git fixture에서 `codex exec "spec: ..."`, `codex exec "plan: ..."`, `codex exec "build"`를 실행한다. |
| UI 또는 브라우저 검증 기준 변경 | sandbox 밖 로컬 서버와 Playwright CLI 또는 동등한 브라우저 smoke 결과를 기록한다. |

## fixture 기준

릴리즈 전 fixture 검증은 목적에 따라 선택한다.

- 새 빈 프로젝트: full 템플릿이 초기 골격으로 바로 적용되는지 확인한다.
- 기존 앱 프로젝트: 기존 소스와 테스트를 바꾸지 않고 하네스가 붙는지 확인한다.
- 기존 문서 보유 프로젝트: `README.md` 같은 충돌이 명확히 보고되고 부분 복사가 발생하지 않는지 확인한다.
- UI 프로젝트: 실제 로컬 브라우저에서 초기 화면, 주요 상호작용, 콘솔 오류를 확인한다.

fixture 결과에는 다음을 남긴다.

- fixture 경로
- 적용 명령과 결과
- `spec -> plan -> build` 실행 여부
- 프로젝트별 테스트 또는 smoke 결과
- forbidden path 검색 결과
- 최종 Git 상태와 주요 fixture 커밋

## 릴리즈 노트 기준

릴리즈 또는 완료 문서에는 다음을 구분해서 적는다.

- 템플릿 문서 변경
- 스킬 변경
- hook 또는 config 변경
- 적용 스크립트 변경
- 검증 정책 변경
- 기존 프로젝트 적용 시 충돌 또는 수동 병합 필요성
- 남은 환경 제약

## 태그 기준

하네스 템플릿 릴리즈 태그는 저장소 전체 버전이 아니라 템플릿 산출물 버전을 가리킨다. 기본 태그명은 `harness-template-v<major>.<minor>` 형식으로 둔다.

- 첫 릴리즈 후보 태그명은 `harness-template-v0.1`이다.
- 태그는 릴리즈 노트와 필수 검증 기록이 커밋된 뒤 생성한다.
- 태그 대상 커밋은 `harness/source/full/root/`, `harness/templates/`, 검증 스크립트, 릴리즈 노트가 서로 일치하는 커밋이어야 한다.
- 태그 메시지에는 배포 모델, 핵심 변경, 검증 명령 결과를 요약한다.
- 릴리즈 후보를 검증만 하고 아직 고정하지 않을 때는 태그를 만들지 않고 릴리즈 노트의 상태를 `릴리즈 후보`로 둔다.

## 중단 기준

다음 중 하나라도 발생하면 릴리즈 후보로 보지 않는다.

- source와 output drift가 있다.
- template validation이 실패한다.
- forbidden legacy/reference 경로가 생성된다.
- 충돌 있는 대상에 부분 복사가 발생한다.
- `spec`, `plan`, `build` alias가 새 계약과 다르게 동작한다.
- 필수 검증을 실행하지 못했는데 이유와 남은 위험이 문서화되어 있지 않다.

## 완료 기준

- [ ] 필수 검증이 통과했다.
- [ ] 변경 유형에 맞는 추가 검증이 통과했거나, 실행하지 못한 이유가 기록되어 있다.
- [ ] 적용 대상과 제외 대상이 명확하다.
- [ ] 릴리즈 노트 또는 완료 문서가 남아 있다.
- [ ] 변경 사항이 커밋되어 있다.
