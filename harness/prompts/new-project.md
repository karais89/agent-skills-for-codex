# 새 프로젝트 생성 프롬프트

아래 프롬프트를 Codex, Antigravity, Claude Code 같은 LLM 코딩 에이전트에게 그대로 전달한다. 값을 미리 채울 필요는 없다. 에이전트가 현재 폴더를 기본 대상으로 삼고, 필요한 경우에만 질문한다.

```text
https://raw.githubusercontent.com/karais89/agent-skills-for-codex/main/harness/INSTALL.md 를 읽고 그대로 따라 해줘.

작업 유형: 새 프로젝트 생성

요구사항:
- 대상 경로를 따로 말하지 않았으면 현재 작업 디렉터리를 기본값으로 사용해.
- 현재 작업 디렉터리가 비어 있지 않거나 하네스 소스 저장소처럼 보이면 적용 전에 나에게 확인해.
- 프로젝트 이름을 따로 말하지 않았으면 대상 디렉터리 이름을 사용해.
- 프로젝트 목적을 따로 말하지 않았으면 꾸며서 쓰지 말고 "아직 정하지 않음"으로 문서화해. 나중에 바꿀 수 있게 남겨둬.
- 정말 필요한 경우에만 짧게 질문해. 질문은 한 번에 1-3개까지만 해.
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
https://raw.githubusercontent.com/karais89/agent-skills-for-codex/main/harness/INSTALL.md 를 읽고 그대로 따라 해줘.

작업 유형: 새 프로젝트 생성

요구사항:
- 대상 경로는 ../note-lab 이야.
- 프로젝트 이름은 Note Lab 이야.
- 프로젝트 목적은 개인용 노트 작성과 완료 상태 관리를 실험하는 작은 앱이야.
- 필요한 경우 https://github.com/karais89/agent-skills-for-codex 저장소를 임시 위치에 클론해서 사용해.
- harness/templates를 직접 수동 복사하지 말고, INSTALL.md에 적힌 apply-template.py 절차를 사용해.
- 적용 전 dry-run을 실행하고 충돌이 있으면 중단해.
- README.md, ARCHITECTURE.md, AGENTS.md, docs/validation.md를 새 프로젝트 목적에 맞게 초기화해.
- root SPEC.md, tasks/plan.md, tasks/todo.md, docs/references는 만들지 마.
- 하네스 설정과 alias routing을 검증해.
- 가능하면 Git 저장소를 초기화하고 Initial harness project setup 커밋을 만들어.
- 마지막에 실행한 명령, 검증 결과, 대상 경로, 커밋 hash를 요약해.
```
