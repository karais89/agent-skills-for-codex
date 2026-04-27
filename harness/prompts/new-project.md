# 새 프로젝트 생성 프롬프트

아래 프롬프트를 Codex, Antigravity, Claude Code 같은 LLM 코딩 에이전트에게 그대로 전달한다. `<...>` 값만 실제 값으로 바꾼다.

```text
https://raw.githubusercontent.com/karais89/agent-skills-for-codex/main/harness/INSTALL.md 를 읽고 그대로 따라 해줘.

작업 유형: 새 프로젝트 생성
대상 경로: <target-path>
프로젝트 이름: <project-name>
프로젝트 목적: <one-line-brief>

요구사항:
- 필요한 경우 https://github.com/karais89/agent-skills-for-codex 저장소를 임시 위치에 클론해서 사용해.
- harness/templates를 직접 수동 복사하지 말고, INSTALL.md에 적힌 apply-template.py 절차를 사용해.
- 적용 전 dry-run을 실행하고 충돌이 있으면 중단해.
- README.md, ARCHITECTURE.md, AGENTS.md, docs/validation.md를 새 프로젝트 목적에 맞게 초기화해.
- root SPEC.md, tasks/plan.md, tasks/todo.md, docs/references는 만들지 마.
- 하네스 설정과 alias routing을 검증해.
- 가능하면 Git 저장소를 초기화하고 Initial harness project setup 커밋을 만들어.
- 마지막에 실행한 명령, 검증 결과, 대상 경로, 커밋 hash를 요약해.
```

## 예시

```text
https://raw.githubusercontent.com/karais89/agent-skills-for-codex/main/harness/INSTALL.md 를 읽고 그대로 따라 해줘.

작업 유형: 새 프로젝트 생성
대상 경로: ../note-lab
프로젝트 이름: Note Lab
프로젝트 목적: 개인용 노트 작성과 완료 상태 관리를 실험하는 작은 앱

요구사항:
- 필요한 경우 https://github.com/karais89/agent-skills-for-codex 저장소를 임시 위치에 클론해서 사용해.
- harness/templates를 직접 수동 복사하지 말고, INSTALL.md에 적힌 apply-template.py 절차를 사용해.
- 적용 전 dry-run을 실행하고 충돌이 있으면 중단해.
- README.md, ARCHITECTURE.md, AGENTS.md, docs/validation.md를 새 프로젝트 목적에 맞게 초기화해.
- root SPEC.md, tasks/plan.md, tasks/todo.md, docs/references는 만들지 마.
- 하네스 설정과 alias routing을 검증해.
- 가능하면 Git 저장소를 초기화하고 Initial harness project setup 커밋을 만들어.
- 마지막에 실행한 명령, 검증 결과, 대상 경로, 커밋 hash를 요약해.
```
