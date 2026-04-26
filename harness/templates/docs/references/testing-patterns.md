# 테스트 패턴 참고서

`test-driven-development` 스킬과 함께 쓰는 테스트 작성 기준입니다. 테스트는 구현 세부사항보다 관찰 가능한 동작을 검증해야 합니다.

## 기본 구조: Arrange, Act, Assert

```typescript
it('creates a task with pending status', () => {
  // Arrange
  const input = { title: 'Test Task', priority: 'high' };

  // Act
  const result = createTask(input);

  // Assert
  expect(result.title).toBe('Test Task');
  expect(result.priority).toBe('high');
  expect(result.status).toBe('pending');
});
```

## 테스트 이름 규칙

테스트 이름은 specification처럼 읽혀야 합니다.

```typescript
describe('TaskService.createTask', () => {
  it('creates a task with default pending status', () => {});
  it('throws ValidationError when title is empty', () => {});
  it('trims whitespace from title', () => {});
  it('generates a unique ID for each task', () => {});
});
```

권장 패턴:

```text
[대상]은 [조건]에서 [기대 동작]을 한다
```

## 자주 쓰는 assertion

```typescript
// 동등성
expect(result).toBe(expected);
expect(result).toEqual(expected);
expect(result).toStrictEqual(expected);

// 존재 여부
expect(result).toBeTruthy();
expect(result).toBeFalsy();
expect(result).toBeNull();
expect(result).toBeDefined();
expect(result).toBeUndefined();

// 숫자
expect(result).toBeGreaterThan(5);
expect(result).toBeLessThanOrEqual(10);
expect(result).toBeCloseTo(0.3, 5);

// 문자열
expect(result).toMatch(/pattern/);
expect(result).toContain('substring');

// 배열과 객체
expect(array).toContain(item);
expect(array).toHaveLength(3);
expect(object).toHaveProperty('key', 'value');

// 오류
expect(() => fn()).toThrow();
expect(() => fn()).toThrow(ValidationError);
expect(() => fn()).toThrow('specific message');

// 비동기
await expect(asyncFn()).resolves.toBe(value);
await expect(asyncFn()).rejects.toThrow(Error);
```

## Mocking 기준

mock은 system boundary에서 사용합니다. 내부 business logic을 mock하면 실제 동작을 검증하지 못합니다.

| mock 권장 | mock 지양 |
| --- | --- |
| database 호출 | 내부 utility 함수 |
| HTTP 요청 | business logic |
| file system | validation 함수 |
| 외부 API | data transformation |
| 시간과 날짜 | 순수 함수 |

### 함수 mock

```typescript
const mockFn = jest.fn();
mockFn.mockReturnValue(42);
mockFn.mockResolvedValue({ data: 'test' });

expect(mockFn).toHaveBeenCalledWith('arg1', 'arg2');
expect(mockFn).toHaveBeenCalledTimes(3);
```

### module mock

```typescript
jest.mock('./database', () => ({
  query: jest.fn().mockResolvedValue([{ id: 1, title: 'Test' }]),
}));
```

## React 또는 컴포넌트 테스트

접근 가능한 role과 label로 요소를 찾습니다. `data-testid`는 마지막 수단입니다.

```tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';

describe('TaskForm', () => {
  it('submits the form with entered data', async () => {
    const onSubmit = jest.fn();
    render(<TaskForm onSubmit={onSubmit} />);

    fireEvent.change(screen.getByRole('textbox', { name: /title/i }), {
      target: { value: 'New Task' },
    });
    fireEvent.click(screen.getByRole('button', { name: /create/i }));

    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith({ title: 'New Task' });
    });
  });
});
```

## API 또는 통합 테스트

```typescript
import request from 'supertest';
import { app } from '../src/app';

describe('POST /api/tasks', () => {
  it('creates a task and returns 201', async () => {
    const response = await request(app)
      .post('/api/tasks')
      .send({ title: 'Test Task' })
      .set('Authorization', `Bearer ${testToken}`)
      .expect(201);

    expect(response.body).toMatchObject({
      id: expect.any(String),
      title: 'Test Task',
      status: 'pending',
    });
  });

  it('returns 422 for invalid input', async () => {
    await request(app)
      .post('/api/tasks')
      .send({ title: '' })
      .set('Authorization', `Bearer ${testToken}`)
      .expect(422);
  });
});
```

## E2E 테스트

E2E는 가장 비싼 테스트입니다. 핵심 사용자 흐름에만 사용하고, 가능한 검증은 unit/integration test로 내립니다.

```typescript
import { test, expect } from '@playwright/test';

test('user can create and complete a task', async ({ page }) => {
  await page.goto('/');
  await page.fill('[name="email"]', 'test@example.com');
  await page.fill('[name="password"]', 'testpass123');
  await page.click('button:has-text("Log in")');

  await page.click('button:has-text("New Task")');
  await page.fill('[name="title"]', 'Buy groceries');
  await page.click('button:has-text("Create")');

  await expect(page.locator('text=Buy groceries')).toBeVisible();
  await page.click('[aria-label="Complete Buy groceries"]');
});
```

## 버그 수정: Prove-It 패턴

1. 버그를 재현하는 테스트를 먼저 작성합니다.
2. 현재 코드에서 그 테스트가 실패하는지 확인합니다.
3. 최소 수정으로 테스트를 통과시킵니다.
4. 관련 regression test와 전체 테스트를 실행합니다.

## 테스트 안티패턴

- 구현 세부사항을 검증하는 테스트
- 한 테스트에서 여러 개념을 동시에 검증하는 테스트
- flaky timeout에 의존하는 테스트
- 의미 없는 snapshot test
- 항상 통과하거나 항상 실패하는 테스트
- 실제로 검증하지 않는 mock assertion
