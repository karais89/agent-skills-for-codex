# 참고 저장소 목록

확인일: 2026-04-26

외부 참고 저장소는 `reference-repos/adopted/` 또는 `reference-repos/supporting/` 아래에 클론하며, `reference-repos/` 전체는 `.gitignore`에 포함되어 현재 프로젝트의 Git 이력에는 저장하지 않는다. 참고 저장소의 코드는 직접 복사하기보다 구조, 문서화 방식, 스킬 구성, 에이전트 지침을 파악하는 용도로 우선 사용한다.

## 저장소

| 분류 | 용도 | 원격 저장소 | 로컬 경로 | 클론 기준 커밋 |
| --- | --- | --- | --- | --- |
| 채택 | Karpathy 스킬 참고 | https://github.com/forrestchang/andrej-karpathy-skills | `reference-repos/adopted/andrej-karpathy-skills` | `2c60614 Sync Chinese README with English version (add Cursor section) (#95)` |
| 채택 | agent-skills 스킬 참고 | https://github.com/addyosmani/agent-skills | `reference-repos/adopted/agent-skills` | `44b9e37 Merge pull request #66 from datfinesoul/opencode-skills` |
| 보조 | Codex 참고 | https://github.com/openai/codex | `reference-repos/supporting/openai-codex` | `355c40a Support end_turn in response.completed (#19610)` |
| 보조 | Superpower 스킬 참고 | https://github.com/obra/superpowers | `reference-repos/supporting/superpowers` | `6efe32c Use committed Codex plugin files in sync script` |
| 보조 | gstack 스킬 참고 | https://github.com/garrytan/gstack | `reference-repos/supporting/gstack` | `23c4d7b v1.13.0.0 feat: add Claude outside-voice skill (#1212)` |
| 보조 | Harness framework 참고 | https://github.com/jha0313/harness_framework | `reference-repos/supporting/harness_framework` | `da676bc chore: add .gitignore for build artifacts` |

여기서 보조는 현재 하네스의 기본축은 아니지만, 특정 품질 기준이나 향후 확장 판단에 참고하는 자료라는 뜻이다. 부분 채택, 보류, 참고 전용 자료를 함께 포함한다.

## 운영 규칙

- 참고 저장소는 외부 자료이므로 프로젝트 변경 사항과 섞어 커밋하지 않는다.
- 참고 저장소를 갱신할 때는 각 저장소 내부에서 `git pull` 또는 재클론을 수행하고, 필요한 경우 이 문서의 기준 커밋과 분류를 함께 갱신한다.
- 프로젝트 구현에는 참고 저장소의 패턴을 그대로 적용하기보다 현재 프로젝트 목적과 지침에 맞게 축약해서 반영한다.
