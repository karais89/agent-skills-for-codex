# public URL 기반 하네스 setup 프롬프트 검증 기록

## 목적

하네스 저장소를 public GitHub repo로 push하고, public URL을 기반으로 LLM에게 전달할 setup 프롬프트와 설치 지침이 실제로 동작하는지 확인한다.

## public 저장소

- repository: `https://github.com/karais89/agent-skills-for-codex`
- raw install guide: `https://raw.githubusercontent.com/karais89/agent-skills-for-codex/refs/heads/main/harness/INSTALL.md`
- 새 프로젝트 프롬프트: `https://raw.githubusercontent.com/karais89/agent-skills-for-codex/refs/heads/main/harness/prompts/new-project.md`
- 기존 프로젝트 적용 프롬프트: `https://raw.githubusercontent.com/karais89/agent-skills-for-codex/refs/heads/main/harness/prompts/apply-to-existing-project.md`
- 프로젝트 프로필 갱신 프롬프트: `https://raw.githubusercontent.com/karais89/agent-skills-for-codex/refs/heads/main/harness/prompts/update-project-profile.md`

## 결정

- 설치형 CLI나 `setup.sh`를 사용자-facing 인터페이스로 만들지 않는다.
- 사용자는 LLM에게 public `harness/INSTALL.md`를 읽고 따르라고 요청한다.
- 자동 복사는 사람이 직접 `cp`하지 않고 `harness/scripts/apply-template.py`를 통해 수행한다.
- 새 프로젝트 생성 흐름을 우선 지원하고, 기존 프로젝트 적용은 충돌이 없을 때만 수행한다.

## 진행 기록

| 단계 | 실행 | 결과 |
| --- | --- | --- |
| 1 | `gh repo create agent-skills-for-codex --public --source=. --remote=origin --push` | public repo 생성 및 기존 `main` push 완료. |
| 2 | `gh repo view karais89/agent-skills-for-codex --json nameWithOwner,visibility,url` | `visibility: PUBLIC` 확인. |
| 3 | `harness/INSTALL.md`, `harness/prompts/new-project.md`, `harness/prompts/apply-to-existing-project.md` 추가 | 커밋 `7c0f7ed` 생성. |
| 4 | `git push` | 최초 1회 HTTPS credential 문제로 실패. `gh auth setup-git` 후 push 성공. |
| 5 | `curl -L -o /tmp/harness-install-public.md <raw INSTALL URL>` | public raw INSTALL 접근 성공. |
| 6 | `curl -L -o /tmp/harness-new-project-prompt-public.md <raw new-project prompt URL>` | public raw 새 프로젝트 프롬프트 접근 성공. |
| 7 | `curl -L -o /tmp/harness-existing-project-prompt-public.md <raw existing-project prompt URL>` | public raw 기존 프로젝트 프롬프트 접근 성공. |
| 8 | `git clone https://github.com/karais89/agent-skills-for-codex.git /tmp/harness-public-smoke.nDjPad/source` | public clone 성공. |
| 9 | public clone에서 `python3 harness/scripts/build-template.py --check`, `python3 harness/scripts/validate-template.py` | 통과. |
| 10 | public clone에서 `python3 harness/scripts/apply-template.py --target /tmp/harness-public-smoke.nDjPad/note-lab --dry-run` | 복사 예정 56개, 충돌 0건. |
| 11 | public clone에서 `python3 harness/scripts/apply-template.py --target /tmp/harness-public-smoke.nDjPad/note-lab` | 적용 성공. |
| 12 | target 문서 초기화 | `README.md`, `ARCHITECTURE.md`, `AGENTS.md`, `docs/validation.md`를 Note Lab 목적에 맞게 갱신. |
| 13 | target 하네스 검증 | config parsing, skill frontmatter, `spec`/`plan`/`build` alias routing 통과. |
| 14 | target forbidden path 확인 | root `SPEC.md`, `tasks/`, `docs/references` 미생성 확인. |
| 15 | target Git 초기화와 커밋 | `git init`, `git add .`, `git commit -m "Initial harness project setup"` 성공. target 커밋 `a0e16be`. |

## 확인한 내용

- public URL만으로 하네스 소스 저장소를 클론할 수 있다.
- LLM에게 전달할 raw INSTALL URL과 prompt raw URL이 접근 가능하다.
- 새 프로젝트 target에 full 하네스 템플릿이 충돌 없이 적용된다.
- 문서 초기화 단계를 수행하면 `README.md`와 `ARCHITECTURE.md`가 앱 코드 없는 새 프로젝트 상태를 정확히 설명한다.
- 하네스 설정과 alias routing은 public clone으로 만든 target에서도 정상 동작한다.
- legacy/reference 경로는 생성되지 않는다.

## UX 보완 기록

2026-04-27에 사용자-facing prompt에서 `<target-path>`, `<project-name>`, `<one-line-brief>` 같은 placeholder 입력 방식을 제거했다.

- 대상 경로 기본값은 현재 작업 디렉터리로 정했다.
- 프로젝트 이름 기본값은 대상 디렉터리 이름으로 정했다.
- 프로젝트 목적을 받지 못하면 꾸며 쓰지 않고 "아직 정하지 않음"으로 문서화하도록 했다.
- 현재 작업 디렉터리가 하네스 소스 저장소이거나 비어 있지 않아 위험한 경우에만 에이전트가 짧게 질문하도록 했다.
- `/tmp/harness-ux-smoke.rEM3xg`에서 값 없는 새 프로젝트 setup 흐름을 수동 smoke로 확인했다.

검증:

- `rg`로 prompt와 INSTALL의 사용자 입력 placeholder 제거 확인.
- `python3 harness/scripts/build-template.py --check` 통과.
- `python3 harness/scripts/validate-template.py` 통과.
- UX smoke target에서 config parsing 통과.
- UX smoke target에서 `spec`, `plan`, `build` alias routing 통과.
- UX smoke target에서 root `SPEC.md`, `tasks/`, `docs/references` 미생성 확인.

2026-04-27에 새 프로젝트 생성 전에는 기본값을 조용히 적용하지 않고, 대상 경로/프로젝트 이름/프로젝트 목적을 한 번 확인하도록 바꿨다.

- 대상 경로는 현재 작업 디렉터리를 "제안"하되 사용자 확인 전에는 파일을 적용하지 않는다.
- 프로젝트 이름은 대상 디렉터리 이름을 "제안"한다.
- 프로젝트 목적은 사용자가 정하지 않았으면 "아직 정하지 않음"을 제안한다.
- 사용자가 이름이나 목적을 나중에 정하는 경우를 위해 `harness/prompts/update-project-profile.md`를 추가했다.
- 프로젝트 프로필 갱신 절차는 `README.md`, `ARCHITECTURE.md`, `AGENTS.md`, `docs/validation.md`를 갱신하고 config parsing, alias routing, forbidden path 확인을 수행한다.

## 남은 한계

- 이번 검증은 사람이 INSTALL 절차를 따라 수행한 smoke다. 별도 `codex exec`가 public prompt를 읽고 끝까지 수행하는 end-to-end 자동 검증은 아직 아니다.
- 기존 프로젝트 충돌 병합은 이번 범위가 아니다. 기존 프로젝트는 dry-run 충돌 보고까지만 prompt에 명시했다.
- 문서 초기화는 아직 스크립트가 아니라 LLM 지침 기반이다. 이 선택은 초경량 하네스 목적에 맞추기 위한 것이다.

## 완료 조건

- [x] public GitHub repo가 생성되고 `main`이 push되었다.
- [x] public raw INSTALL URL이 접근 가능하다.
- [x] 새 프로젝트용/기존 프로젝트용 prompt 파일이 public raw URL로 접근 가능하다.
- [x] public clone 기반으로 템플릿 정적 검증이 통과했다.
- [x] public clone 기반으로 새 프로젝트 target에 템플릿 적용이 성공했다.
- [x] target 문서가 프로젝트 목적에 맞게 초기화되었다.
- [x] target 하네스 설정과 alias routing 검증이 통과했다.
- [x] 결과가 문서화되었다.
