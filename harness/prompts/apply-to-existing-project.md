# 기존 프로젝트 적용 프롬프트

아래 프롬프트를 Codex, Antigravity, Claude Code 같은 LLM 코딩 에이전트에게 그대로 전달한다. 값을 미리 채울 필요는 없다. 에이전트가 현재 폴더를 기본 대상으로 제안하되, 적용 전에는 대상과 충돌 가능성을 한 번 확인한다.

```text
https://raw.githubusercontent.com/karais89/agent-skills-for-codex/main/harness/INSTALL.md 를 읽고 그대로 따라 해줘.

작업 유형: 기존 프로젝트에 하네스 적용

요구사항:
- 대상 경로를 따로 말하지 않았으면 현재 작업 디렉터리를 제안해.
- 프로젝트 이름을 따로 말하지 않았으면 기존 README 제목, package.json name, Git repo 이름, 디렉터리 이름 순서로 추론해.
- 프로젝트 목적을 따로 말하지 않았으면 기존 README와 코드 구조에서 추론해. 근거가 부족하면 "확인 필요"로 남겨.
- 실제 적용 전에 대상 경로, 추론한 프로젝트 이름과 목적, 충돌 가능성을 한 번 확인 질문으로 보여주고 내 답을 기다려.
- README.md, AGENTS.md, ARCHITECTURE.md, docs/ 충돌이 있으면 덮어쓰지 말고 중단해.
- 정말 필요한 경우에만 짧게 질문해. 질문은 한 번에 1-3개까지만 해.
- 필요한 경우 https://github.com/karais89/agent-skills-for-codex 저장소를 임시 위치에 클론해서 사용해.
- 먼저 대상 프로젝트의 Git 상태와 기존 README.md, AGENTS.md, ARCHITECTURE.md, docs/ 존재 여부를 확인해.
- harness/templates를 직접 수동 복사하지 말고, INSTALL.md에 적힌 apply-template.py dry-run을 먼저 실행해.
- 충돌이 있으면 실제 적용하지 말고 충돌 경로와 병합 제안을 보고해.
- 충돌이 없을 때만 실제 적용해.
- README.md, ARCHITECTURE.md, AGENTS.md, docs/validation.md를 기존 프로젝트 코드와 명령에 맞게 보강해.
- root SPEC.md, tasks/plan.md, tasks/todo.md, docs/references는 만들지 마.
- 기존 테스트가 있으면 실행하고, 하네스 설정과 alias routing도 검증해.
- 가능하면 변경 사항을 커밋해.
- 마지막에 실행한 명령, 검증 결과, 대상 경로, 커밋 hash 또는 충돌 사유를 요약해.
```

## 충돌이 예상되는 경우

기존 프로젝트에 `README.md`, `AGENTS.md`, `ARCHITECTURE.md`, `docs/`가 이미 있으면 충돌이 정상이다. 이때 에이전트는 파일을 덮어쓰지 말고, 어떤 내용을 수동 병합해야 하는지 보고해야 한다.
