# 하네스 템플릿 기준

`harness/templates/`는 다른 프로젝트에 적용할 수 있는 문서 템플릿을 보관한다. 이 저장소 내부 운영 문서를 그대로 복사하지 않고, 대상 프로젝트 사용자가 바로 채울 수 있는 형태로 작성한다.

## 예정 템플릿

`harness/templates/`의 하위 구조는 대상 프로젝트 루트 기준 경로를 그대로 미러링한다.

```text
harness/templates/
  AGENTS.md
  ARCHITECTURE.md
  docs/
    README.md
    exec-plans/
      README.md
      active/
      completed/
      template.md
    validation.md
```

빈 디렉터리는 구현 시 자리표시자나 안내 파일로 Git에 보존한다.

템플릿을 추가할 때는 적용 대상, 필수 입력, 기대 결과, 검증 방법을 함께 설명한다.
