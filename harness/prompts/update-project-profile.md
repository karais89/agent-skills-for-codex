# 프로젝트 프로필 갱신 프롬프트

새 프로젝트를 만들 때 이름이나 목적을 나중에 정했다면, 아래 프롬프트를 Codex, Antigravity, Claude Code 같은 LLM 코딩 에이전트에게 전달한다. 값을 아직 정하지 않았다면 에이전트가 한 번 질문하게 둔다.

```text
https://raw.githubusercontent.com/karais89/agent-skills-for-codex/refs/heads/main/harness/INSTALL.md 를 읽고 프로젝트 프로필 갱신 절차를 따라줘.

요구사항:
- 현재 작업 디렉터리를 대상 프로젝트로 봐.
- 프로젝트 이름이나 목적을 내가 아직 말하지 않았다면, 적용 전에 한 번만 질문해.
- 내가 이름이나 목적을 나중에 정하겠다고 하면 문서를 꾸며 쓰지 말고 "아직 정하지 않음"으로 유지해.
- README.md, ARCHITECTURE.md, AGENTS.md, docs/validation.md를 프로젝트 이름과 목적에 맞게 갱신해.
- 아직 구현되지 않은 앱 런타임, API, UI, 저장소는 "아직 없음" 또는 "아직 정하지 않음"으로 남겨.
- root SPEC.md, tasks/plan.md, tasks/todo.md, docs/references는 만들지 마.
- 하네스 설정과 alias routing을 검증해.
- 가능하면 Update project profile 커밋을 만들어.
- 마지막에 변경한 파일, 검증 결과, 커밋 hash를 요약해.
```

## 값을 함께 주는 예시

```text
https://raw.githubusercontent.com/karais89/agent-skills-for-codex/refs/heads/main/harness/INSTALL.md 를 읽고 프로젝트 프로필 갱신 절차를 따라줘.

요구사항:
- 현재 작업 디렉터리를 대상 프로젝트로 봐.
- 프로젝트 이름은 Note Lab 이야.
- 프로젝트 목적은 개인용 노트 작성과 완료 상태 관리를 실험하는 앱이야.
- README.md, ARCHITECTURE.md, AGENTS.md, docs/validation.md를 프로젝트 이름과 목적에 맞게 갱신해.
- 아직 구현되지 않은 앱 런타임, API, UI, 저장소는 "아직 없음" 또는 "아직 정하지 않음"으로 남겨.
- root SPEC.md, tasks/plan.md, tasks/todo.md, docs/references는 만들지 마.
- 하네스 설정과 alias routing을 검증해.
- 가능하면 Update project profile 커밋을 만들어.
- 마지막에 변경한 파일, 검증 결과, 커밋 hash를 요약해.
```
