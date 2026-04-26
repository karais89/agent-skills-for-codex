# 접근성 체크리스트

UI를 만들거나 수정할 때 빠르게 확인하는 접근성 기준입니다. 자동 검사만으로는 충분하지 않으므로 키보드, 스크린 리더, 시각 대비, 폼 오류 처리를 함께 확인합니다.

## 필수 점검

### 키보드 내비게이션

- 모든 인터랙티브 요소는 `Tab`으로 접근 가능해야 합니다.
- 현재 focus 위치가 시각적으로 명확해야 합니다.
- 모달과 메뉴는 focus trap과 `Esc` 닫기를 지원해야 합니다.
- 버튼, 링크, 입력 필드는 키보드만으로 실행할 수 있어야 합니다.
- DOM 순서와 시각적 순서가 크게 어긋나지 않아야 합니다.

### 스크린 리더

- 페이지에는 의미 있는 heading 구조가 있어야 합니다.
- 이미지에는 목적에 맞는 `alt`가 있어야 합니다. 장식 이미지는 빈 `alt=""`를 사용합니다.
- 아이콘 버튼에는 `aria-label` 또는 보이는 텍스트가 있어야 합니다.
- 동적으로 바뀌는 상태는 필요한 경우 `aria-live`로 전달합니다.
- form control은 label과 연결되어야 합니다.

### 시각 표현

- 텍스트와 배경 대비는 일반 텍스트 기준 최소 4.5:1을 목표로 합니다.
- 색상만으로 상태를 전달하지 않습니다. 텍스트, 아이콘, 패턴을 함께 사용합니다.
- 작은 화면과 확대 배율에서도 텍스트가 겹치거나 잘리지 않아야 합니다.
- animation은 과하지 않아야 하며, 사용자 설정 `prefers-reduced-motion`을 고려합니다.

### 폼

- 모든 입력에는 명시적 label이 있어야 합니다.
- 오류 메시지는 필드와 가까이 표시하고, 스크린 리더가 읽을 수 있어야 합니다.
- 필수 입력은 시각 표시뿐 아니라 접근 가능한 설명도 제공해야 합니다.
- 제출 실패 후 focus가 적절한 오류 위치로 이동해야 합니다.

### 콘텐츠

- 링크 텍스트는 단독으로도 목적을 알 수 있어야 합니다.
- button은 동작, link는 이동에 사용합니다.
- heading level을 건너뛰지 않습니다.
- table은 데이터 표에만 사용하고, header cell을 명확히 지정합니다.

## HTML 패턴

### 버튼과 링크

```html
<!-- 동작: button -->
<button type="button" aria-label="삭제">
  <TrashIcon />
</button>

<!-- 이동: link -->
<a href="/settings">설정으로 이동</a>
```

### label 연결

```html
<label for="email">이메일</label>
<input id="email" name="email" type="email" autocomplete="email" />
```

### 오류 메시지

```html
<label for="title">제목</label>
<input
  id="title"
  name="title"
  aria-invalid="true"
  aria-describedby="title-error"
/>
<p id="title-error">제목을 입력하세요.</p>
```

### ARIA 사용 원칙

- 네이티브 HTML로 표현할 수 있으면 ARIA를 추가하지 않습니다.
- ARIA role을 추가했다면 필요한 keyboard interaction도 직접 구현해야 합니다.
- `aria-hidden="true"`는 스크린 리더에서 완전히 숨긴다는 뜻입니다. focus 가능한 요소에는 사용하지 않습니다.

## 테스트 도구

```bash
# 자동 접근성 검사
npx axe http://localhost:3000

# Lighthouse 접근성 점수 확인
npx lighthouse http://localhost:3000 --only-categories=accessibility
```

브라우저 수동 확인:

- Chrome DevTools -> Lighthouse -> Accessibility
- Chrome DevTools -> Elements -> Accessibility tree
- macOS VoiceOver: `Cmd + F5`
- Windows: NVDA 또는 JAWS
- Linux: Orca

## ARIA live region 빠른 기준

| 상황 | 권장 값 |
| --- | --- |
| 저장 완료, 필터 적용 같은 일반 상태 | `aria-live="polite"` |
| 오류, 세션 만료 같은 즉시 알려야 하는 상태 | `aria-live="assertive"` |
| 너무 자주 바뀌는 값 | live region 사용을 피하거나 debounce |

## 흔한 안티패턴

- `div`에 click handler만 붙이고 keyboard handler를 빼먹는 것
- input placeholder를 label 대신 쓰는 것
- focus outline을 제거하고 대체 표시를 제공하지 않는 것
- `aria-label="button"`처럼 역할만 반복하는 label
- 색상만으로 성공/실패를 표현하는 것
- modal 뒤의 페이지를 스크린 리더가 계속 읽을 수 있게 두는 것
