# 하네스 산출물 기준

`harness/`는 다른 프로젝트에 적용할 하네스 산출물과 템플릿을 보관하는 영역이다. 이 저장소를 운영하기 위한 내부 문서는 `docs/project/`에 두고, 외부 참고와 판단 근거는 `docs/references/`에 둔다.

## 역할

- 대상 프로젝트에 복사하거나 설치할 수 있는 문서, 템플릿, 스크립트, 스킬을 보관한다.
- 이 저장소의 내부 운영 규칙을 그대로 노출하지 않고, 대상 프로젝트 사용자가 바로 적용할 수 있는 형태로 재작성한다.
- 산출물마다 적용 대상, 입력 파일, 기대 결과, 검증 방법을 함께 둔다.

## 배포 모델

현재 지원하는 배포 모델은 `full` 하나다. `full` 모델은 대상 프로젝트 루트에 repo-local Codex 하네스 전체를 복제한다.

포함 범위:

- `.agents/skills/`: 대상 프로젝트가 사용할 로컬 스킬과 wrapper 스킬.
- `.codex/config.toml`, `.codex/hooks.json`, `.codex/hooks/*.py`: alias routing과 안전 hook.
- `.codex/agents/*.toml`: read-only 검토용 전문 에이전트 설정.
- `AGENTS.md`, `ARCHITECTURE.md`, `README.md`: 대상 프로젝트 시작 문서와 작업 지침.
- `docs/product-specs/`, `docs/exec-plans/`, `docs/validation.md`: product spec, ExecPlan, 검증 기준.

제외 범위:

- `docs/references/`: 이 저장소의 참고 자료는 대상 프로젝트에 번들하지 않는다.
- 루트 `SPEC.md`, `tasks/plan.md`, `tasks/todo.md`: legacy workflow 산출물은 만들지 않는다.
- minimal 배포 모델: 아직 설계하지 않는다.

## Source와 Output

- source-of-truth: `harness/source/full/root/`
- generated output: `harness/templates/`
- manifest: `harness/source/full/manifest.toml`
- build/check script: `harness/scripts/build-template.py`
- validation script: `harness/scripts/validate-template.py`

템플릿 내용을 바꿀 때는 `harness/source/full/root/`를 먼저 수정한다. `harness/templates/`는 빌드 산출물이므로 직접 편집하지 않는다. 의도한 source 변경을 output에 반영할 때는 다음 명령을 사용한다.

```bash
python3 harness/scripts/build-template.py --write
```

source와 output이 같은지 확인할 때는 다음 명령을 사용한다.

```bash
python3 harness/scripts/build-template.py --check
```

## 적용 방식

현재 적용 방식은 명령 기반 복제다. 새 대상 프로젝트에 full 템플릿을 만들 때는 비어 있거나 아직 존재하지 않는 대상 디렉터리에 source를 생성한다.

```bash
python3 harness/scripts/build-template.py --generate /path/to/target-project
```

이미 존재하는 프로젝트 루트에 적용해야 하는 경우에는 충돌 파일을 먼저 검토한 뒤 `harness/templates/.` 내용을 대상 루트에 복사한다.

```bash
cp -R harness/templates/. /path/to/existing-project/
```

이 직접 복사 방식은 현재 full 모델의 배포 형태로 허용한다. 다만 충돌 해결, 기존 파일 병합, 백업, dry-run은 아직 자동화하지 않는다. 그런 기능은 후속 `$harness-apply` 스킬이나 적용 스크립트의 범위로 남긴다.

## 관리 결정

- `harness/source/full/root/`와 `harness/templates/`는 byte-level로 일치해야 한다.
- `harness/templates/`는 커밋하지만 사람이 직접 관리하는 원본으로 취급하지 않는다.
- `$harness-apply` 스킬은 지금 만들지 않는다. 현재는 `build-template.py --generate`와 직접 복사 절차로 충분히 검증한다.
- `harness/templates/README.md`는 대상 프로젝트에 복제될 README이므로 템플릿 배포자용 절차를 담지 않는다. 배포자용 절차는 이 문서에 둔다.

## 검증

하네스 템플릿은 이 저장소 루트에서 직접 실행해 검증하지 않는다. 먼저 템플릿을 테스트 프로젝트나 fixture에 적용하고, 그 적용 결과를 대상으로 검증한다.

템플릿이 실제 코딩 에이전트 행동을 바꾸는지 확인해야 할 때는 적용된 테스트 대상에서 `codex exec` 기반 시뮬레이션을 고려한다. 기본 실행 형태는 다음과 같다.

```bash
codex exec --cd <템플릿이 적용된 테스트 프로젝트> --sandbox workspace-write "<검증 프롬프트>"
```

시뮬레이션을 사용할 때는 다음을 남긴다.

- 실행한 명령과 입력 프롬프트
- 적용한 템플릿과 대상 파일
- 기대한 행동 변화
- 실제 결과와 남은 간극

full 템플릿 자체의 정적 검증은 다음 명령을 기준으로 한다.

```bash
python3 harness/scripts/build-template.py --check
python3 harness/scripts/validate-template.py
```
