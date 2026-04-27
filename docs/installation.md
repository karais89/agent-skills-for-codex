# 설치와 적용 방법

이 문서는 `agent-skills-for-codex` 하네스를 실제 프로젝트에 적용하는 방법을 설명한다. 여기서 "설치"는 패키지를 전역 설치한다는 뜻이 아니라, 대상 프로젝트 루트에 repo-local Codex 하네스 파일을 적용한다는 뜻이다.

## 권장 방식

권장 방식은 LLM 코딩 에이전트에게 public 설치 지침을 읽고 수행하게 하는 것이다. 사용자가 `harness/templates`를 직접 복사하지 않는다.

새 프로젝트를 만들 때는 에이전트에게 아래 프롬프트를 전달한다.

```text
https://raw.githubusercontent.com/karais89/agent-skills-for-codex/refs/heads/main/harness/INSTALL.md 를 읽고 그대로 따라 해줘.

작업 유형: 새 프로젝트 생성
```

에이전트는 적용 전에 다음 값을 한 번 확인해야 한다.

- 대상 경로
- 프로젝트 이름
- 프로젝트 목적

이름이나 목적을 아직 정하지 않았다면 그대로 진행할 수 있다. 이 경우 문서에는 "아직 정하지 않음"으로 남기고, 나중에 프로젝트 프로필 갱신 프롬프트로 바꾼다.

## 새 프로젝트 생성

새 프로젝트 생성 프롬프트:

```text
https://raw.githubusercontent.com/karais89/agent-skills-for-codex/refs/heads/main/harness/prompts/new-project.md 를 읽고 따라 해줘.
```

프롬프트에 값을 함께 주고 싶다면 이렇게 쓴다.

```text
https://raw.githubusercontent.com/karais89/agent-skills-for-codex/refs/heads/main/harness/INSTALL.md 를 읽고 그대로 따라 해줘.

작업 유형: 새 프로젝트 생성

요구사항:
- 대상 경로는 ../note-lab 이야.
- 프로젝트 이름은 Note Lab 이야.
- 프로젝트 목적은 개인용 노트 작성과 완료 상태 관리를 실험하는 앱이야.
```

값을 줘도 에이전트는 파일 적용 전에 한 번 확인해야 한다.

## 기존 프로젝트에 적용

기존 프로젝트에 적용할 때는 충돌이 정상적으로 발생할 수 있다. 특히 `README.md`, `AGENTS.md`, `ARCHITECTURE.md`, `docs/`가 이미 있으면 자동 덮어쓰기를 하지 않는다.

기존 프로젝트 적용 프롬프트:

```text
https://raw.githubusercontent.com/karais89/agent-skills-for-codex/refs/heads/main/harness/prompts/apply-to-existing-project.md 를 읽고 따라 해줘.
```

에이전트는 다음 순서로 진행해야 한다.

1. 대상 프로젝트의 Git 상태와 기존 문서 구조를 확인한다.
2. 하네스 저장소를 임시 위치에 클론하거나 기존 로컬 clone을 사용한다.
3. `apply-template.py --dry-run`으로 충돌을 확인한다.
4. 충돌이 있으면 실제 적용하지 않고 충돌 경로를 보고한다.
5. 충돌이 없을 때만 실제 적용한다.
6. README, ARCHITECTURE, AGENTS, `docs/validation.md`를 기존 프로젝트 기준으로 보강한다.
7. 하네스 설정과 기존 테스트를 검증한다.

## 이름과 목적을 나중에 정하기

새 프로젝트 생성 시 이름이나 목적을 나중에 정했다면, 대상 프로젝트에서 아래 프롬프트를 사용한다.

```text
https://raw.githubusercontent.com/karais89/agent-skills-for-codex/refs/heads/main/harness/prompts/update-project-profile.md 를 읽고 따라 해줘.

요구사항:
- 프로젝트 이름은 Note Lab 이야.
- 프로젝트 목적은 개인용 노트 작성과 완료 상태 관리를 실험하는 앱이야.
```

이 절차는 다음 파일을 갱신한다.

- `README.md`
- `ARCHITECTURE.md`
- `AGENTS.md`
- `docs/validation.md`

구현되지 않은 런타임, API, UI, 저장소는 추측해서 쓰지 않고 "아직 없음" 또는 "아직 정하지 않음"으로 남긴다.

## 직접 적용

LLM 에이전트 없이 직접 적용해야 한다면 다음 명령을 사용한다.

```bash
git clone https://github.com/karais89/agent-skills-for-codex.git
cd agent-skills-for-codex

python3 harness/scripts/build-template.py --check
python3 harness/scripts/validate-template.py

python3 harness/scripts/apply-template.py --target /path/to/project --dry-run
python3 harness/scripts/apply-template.py --target /path/to/project
```

직접 적용한 경우에도 대상 프로젝트의 README, ARCHITECTURE, AGENTS, `docs/validation.md`는 프로젝트에 맞게 갱신해야 한다.

## 적용되는 파일

full 하네스는 대상 프로젝트 루트에 다음 구조를 만든다.

| 경로 | 역할 |
| --- | --- |
| `.agents/skills/` | repo-local Codex 스킬 |
| `.codex/config.toml` | Codex 로컬 설정 |
| `.codex/hooks.json` | hook 등록 |
| `.codex/hooks/*.py` | alias routing과 안전 hook |
| `.codex/agents/*.toml` | 검토용 로컬 에이전트 설정 |
| `AGENTS.md` | Codex 작업 지침 |
| `README.md` | 프로젝트 시작 문서 |
| `ARCHITECTURE.md` | 장기 구조와 설계 결정 |
| `docs/product-specs/` | product spec |
| `docs/exec-plans/` | active/completed ExecPlan |
| `docs/validation.md` | 검증 명령과 기준 |

다음 경로는 만들지 않는다.

- root `SPEC.md`
- `tasks/plan.md`
- `tasks/todo.md`
- `docs/references`

## 적용 후 검증

대상 프로젝트에서 최소한 다음을 확인한다.

```bash
python3 - <<'PY'
import json
import tomllib
from pathlib import Path

root = Path.cwd()
json.loads((root / ".codex/hooks.json").read_text())
tomllib.loads((root / ".codex/config.toml").read_text())
for path in sorted((root / ".codex/agents").glob("*.toml")):
    tomllib.loads(path.read_text())
print("config ok")
PY
```

alias routing도 확인한다.

```bash
python3 .codex/hooks/user_prompt_submit.py <<'JSON'
{"hook_event_name":"UserPromptSubmit","prompt":"spec 새 기능 요구사항을 정리해줘"}
JSON
```

출력에 `$harness-product-spec`와 `docs/product-specs/` 안내가 포함되어야 한다.

금지 경로가 생기지 않았는지도 확인한다.

```bash
find . \( -path ./.git \) -prune -o \( -path ./SPEC.md -o -path ./tasks -o -path ./docs/references \) -print
```

정상이라면 출력이 없어야 한다.

## 문제 해결

`README.md`나 `docs/` 충돌이 발생하면 자동 적용을 중단한다. 기존 프로젝트 문서와 하네스 템플릿 문서를 비교해 필요한 항목만 수동으로 병합한다.

raw GitHub URL을 읽을 때 이전 내용이 보이면 `refs/heads/main` 형태의 URL을 사용한다.

```text
https://raw.githubusercontent.com/karais89/agent-skills-for-codex/refs/heads/main/harness/INSTALL.md
```

하네스가 적용된 뒤에는 대상 프로젝트에서 `spec:`, `plan:`, `build` 순서로 작업을 시작한다.
