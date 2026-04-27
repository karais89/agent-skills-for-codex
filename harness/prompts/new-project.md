# 새 프로젝트 생성 프롬프트

아래 프롬프트를 Codex, Antigravity, Claude Code 같은 LLM 코딩 에이전트에게 그대로 전달한다. 값을 미리 채울 필요는 없다. 에이전트가 대상 경로, 프로젝트 이름, 프로젝트 목적의 기본값을 제안하고 적용 전에 한 번 확인한다.

```text
https://raw.githubusercontent.com/karais89/agent-skills-for-codex/refs/heads/main/harness/INSTALL.md 를 읽고 그대로 따라 해줘.

작업 유형: 새 프로젝트 생성

요구사항:
- 대상 경로를 따로 말하지 않았으면 현재 작업 디렉터리를 제안해.
- 프로젝트 이름을 따로 말하지 않았으면 대상 디렉터리 이름을 제안해.
- 프로젝트 목적을 따로 말하지 않았으면 "아직 정하지 않음"을 제안해.
- 파일을 적용하기 전에 대상 경로, 프로젝트 이름, 프로젝트 목적을 한 번 확인 질문으로 보여주고 내 답을 기다려.
- 내가 목적은 나중에 정한다고 하면 꾸며서 쓰지 말고 "아직 정하지 않음"으로 문서화해.
- setup 완료 후 이름이나 목적을 바꾸려면 harness/prompts/update-project-profile.md 프롬프트를 사용하면 된다고 알려줘.
- 필요한 경우 https://github.com/karais89/agent-skills-for-codex 저장소를 임시 위치에 클론해서 사용해.
- harness/templates를 직접 수동 복사하지 말고, INSTALL.md에 적힌 apply-template.py 절차를 사용해.
- 적용 전 dry-run을 실행하고 충돌이 있으면 중단해.
- README.md, ARCHITECTURE.md, AGENTS.md, docs/validation.md를 새 프로젝트 목적에 맞게 초기화해.
- root SPEC.md, tasks/plan.md, tasks/todo.md, docs/references는 만들지 마.
- 하네스 설정과 alias routing을 검증해.
- 가능하면 Git 저장소를 초기화하고 Initial harness project setup 커밋을 만들어.
- 마지막에 실행한 명령, 검증 결과, 대상 경로, 커밋 hash를 요약해.
```

## 값을 함께 주는 예시

```text
https://raw.githubusercontent.com/karais89/agent-skills-for-codex/refs/heads/main/harness/INSTALL.md 를 읽고 그대로 따라 해줘.

작업 유형: 새 프로젝트 생성

요구사항:
- 대상 경로는 ../note-lab 이야.
- 프로젝트 이름은 Note Lab 이야.
- 프로젝트 목적은 개인용 노트 작성과 완료 상태 관리를 실험하는 작은 앱이야.
- 그래도 파일을 적용하기 전에 이 값으로 진행할지 한 번 확인해.
- 필요한 경우 https://github.com/karais89/agent-skills-for-codex 저장소를 임시 위치에 클론해서 사용해.
- harness/templates를 직접 수동 복사하지 말고, INSTALL.md에 적힌 apply-template.py 절차를 사용해.
- 적용 전 dry-run을 실행하고 충돌이 있으면 중단해.
- README.md, ARCHITECTURE.md, AGENTS.md, docs/validation.md를 새 프로젝트 목적에 맞게 초기화해.
- root SPEC.md, tasks/plan.md, tasks/todo.md, docs/references는 만들지 마.
- 하네스 설정과 alias routing을 검증해.
- 가능하면 Git 저장소를 초기화하고 Initial harness project setup 커밋을 만들어.
- 마지막에 실행한 명령, 검증 결과, 대상 경로, 커밋 hash를 요약해.
```
