# agent-skills-for-codex

`agent-skills-for-codex`는 새 프로젝트나 기존 프로젝트에 repo-local Codex 하네스를 적용하기 위한 초경량 템플릿 저장소다.

이 저장소는 앱을 생성하지 않는다. 대신 대상 프로젝트 안에 `.agents/`, `.codex/`, `AGENTS.md`, `README.md`, `ARCHITECTURE.md`, `docs/product-specs/`, `docs/exec-plans/`를 준비해 `spec -> plan -> build` 흐름으로 작업할 수 있게 만든다.

## 제공하는 것

| 영역 | 내용 |
| --- | --- |
| 로컬 스킬 | `spec`, `plan`, `build`, `test`, `review` 등 Codex 작업 흐름 |
| 로컬 hook | alias routing, 안전 정책, 검증 누락 방지 |
| 프로젝트 문서 | README, 아키텍처, product spec, ExecPlan, 검증 기준 |
| 적용 도구 | dry-run과 충돌 검사를 포함한 템플릿 적용 스크립트 |

## 빠른 시작

Codex, Antigravity, Claude Code 같은 LLM 코딩 에이전트에게 아래 프롬프트를 전달한다.

```text
https://raw.githubusercontent.com/karais89/agent-skills-for-codex/refs/heads/main/harness/INSTALL.md 를 읽고 그대로 따라 해줘.

작업 유형: 새 프로젝트 생성
```

에이전트는 파일을 적용하기 전에 대상 경로, 프로젝트 이름, 프로젝트 목적을 한 번 확인해야 한다. 이름이나 목적을 아직 정하지 않았다면 나중에 갱신할 수 있다.

자세한 절차는 [설치와 적용 방법](docs/installation.md)을 본다.

## 기본 workflow

하네스가 적용된 프로젝트에서는 다음 흐름을 사용한다.

| 입력 | 역할 | 산출물 |
| --- | --- | --- |
| `spec:` | 제품 요구사항과 수용 기준 작성 | `docs/product-specs/<slug>.md` |
| `plan:` | 구현 순서와 검증 계획 작성 | `docs/exec-plans/active/<slug>.md` |
| `build` | active ExecPlan의 다음 미완료 항목 구현 | 코드 변경과 ExecPlan 검증 기록 |

`spec`, `plan`, `build`는 root `SPEC.md`, `tasks/plan.md`, `tasks/todo.md`를 만들지 않는다.

## 설치 방식

권장 방식은 LLM에게 public `harness/INSTALL.md`를 읽고 수행하게 하는 것이다. 사용자는 복잡한 복사 명령을 직접 실행하지 않는다.

직접 실행이 필요하면 다음 방식도 가능하다.

```bash
git clone https://github.com/karais89/agent-skills-for-codex.git
cd agent-skills-for-codex
python3 harness/scripts/apply-template.py --target /path/to/project --dry-run
python3 harness/scripts/apply-template.py --target /path/to/project
```

수동 적용 전후 검증과 기존 프로젝트 충돌 처리 기준은 [설치와 적용 방법](docs/installation.md)에 정리되어 있다.

## 주요 문서

- [설치와 적용 방법](docs/installation.md)
- [하네스 설치 지침](harness/INSTALL.md)
- [새 프로젝트 생성 프롬프트](harness/prompts/new-project.md)
- [기존 프로젝트 적용 프롬프트](harness/prompts/apply-to-existing-project.md)
- [프로젝트 프로필 갱신 프롬프트](harness/prompts/update-project-profile.md)
- [하네스 산출물 기준](harness/README.md)
- [내부 문서 색인](docs/README.md)

## 검증

이 저장소에서 하네스 템플릿을 변경했다면 최소한 다음 명령을 실행한다.

```bash
python3 harness/scripts/build-template.py --check
python3 harness/scripts/validate-template.py
python3 harness/scripts/test-template-builder.py
python3 harness/scripts/test-apply-template.py
git diff --check
```

실제 사용 흐름을 바꾸는 변경은 `/tmp` fixture나 별도 테스트 프로젝트에 적용한 뒤 `spec -> plan -> build` smoke 결과를 문서화한다.
