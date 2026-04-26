# 성능 체크리스트

성능 최적화는 측정에서 시작합니다. 추측으로 수정하지 말고 지표를 정하고, 병목을 확인한 뒤, 가장 작은 변경으로 개선 여부를 다시 측정합니다.

## Core Web Vitals 목표

| 지표 | 좋은 기준 | 의미 |
| --- | --- | --- |
| LCP | 2.5초 이하 | 주요 콘텐츠가 보이는 시간 |
| INP | 200ms 이하 | 사용자 입력에 대한 반응성 |
| CLS | 0.1 이하 | 레이아웃 이동 안정성 |
| TTFB | 800ms 이하 | 서버 첫 응답 시간 |

## TTFB 진단

- CDN cache hit 여부를 확인합니다.
- 서버 cold start 또는 connection pool 부족을 확인합니다.
- DB query latency와 N+1 query를 확인합니다.
- upstream API 호출이 request path를 막고 있는지 확인합니다.
- 인증/인가 middleware가 과도한 I/O를 수행하지 않는지 확인합니다.

## 프론트엔드 체크리스트

### 이미지

- 실제 표시 크기에 맞는 image size를 제공합니다.
- hero 또는 LCP 이미지는 preload를 고려합니다.
- lazy loading은 fold 아래 이미지에만 적용합니다.
- WebP/AVIF 같은 최신 format을 사용합니다.
- width/height 또는 aspect-ratio를 지정해 layout shift를 막습니다.

### JavaScript

- route 단위 code splitting을 적용합니다.
- 사용하지 않는 dependency와 polyfill을 제거합니다.
- 큰 chart, editor, map 라이브러리는 lazy load합니다.
- render path에서 비싼 계산은 memoization하거나 worker로 이동합니다.
- event handler에서 sync 작업이 길어지지 않게 합니다.

### CSS

- critical CSS와 나머지 CSS를 구분합니다.
- 대규모 selector와 unused CSS를 줄입니다.
- animation은 transform/opacity 중심으로 구성합니다.
- layout을 강제로 재계산하는 패턴을 피합니다.

### 폰트

- 필요한 weight와 subset만 로드합니다.
- `font-display: swap` 또는 적절한 fallback 전략을 사용합니다.
- self-hosting과 CDN 중 실제 latency가 낮은 방식을 선택합니다.

### 네트워크

- 동일 데이터를 중복 fetch하지 않습니다.
- cache header와 revalidation 전략을 명확히 둡니다.
- API 응답 payload를 필요한 필드로 제한합니다.
- pagination 또는 cursor를 사용해 list endpoint를 제한합니다.

### 렌더링

- 입력 중 매번 전체 목록을 re-render하지 않습니다.
- virtualized list를 고려합니다.
- layout shift를 만드는 늦은 content 삽입을 피합니다.
- skeleton과 reserved space로 loading 상태를 안정화합니다.

## 백엔드 체크리스트

### 데이터베이스

- query plan을 확인합니다.
- where/order by에 맞는 index가 있는지 확인합니다.
- N+1 query를 batch 또는 join으로 줄입니다.
- list endpoint에는 limit과 pagination이 있어야 합니다.

### API

- 응답 schema에서 불필요한 필드를 제거합니다.
- 느린 외부 호출은 timeout, retry, circuit breaker를 둡니다.
- cache 가능한 응답은 cache key와 invalidation 규칙을 명확히 합니다.
- synchronous job은 queue/background worker로 분리합니다.

### 인프라

- CDN, compression, HTTP/2 또는 HTTP/3 사용 여부를 확인합니다.
- autoscaling 기준이 실제 병목과 맞는지 확인합니다.
- observability에 p95/p99 latency와 error rate를 포함합니다.

## 측정 명령

```bash
# Lighthouse
npx lighthouse http://localhost:3000 --view

# bundle 분석
npm run build -- --analyze

# Vite bundle 시각화 예시
npx vite-bundle-visualizer

# bundle 크기 확인
du -sh dist/*
```

Web Vitals instrumentation 예시:

```typescript
import { onCLS, onINP, onLCP, onTTFB } from 'web-vitals';

onCLS(console.log);
onINP(console.log);
onLCP(console.log);
onTTFB(console.log);
```

## 흔한 안티패턴

- 측정 없이 "아마 빠를 것"이라는 이유로 refactor하는 것
- 모든 페이지에서 무거운 dependency를 eager load하는 것
- API list를 pagination 없이 반환하는 것
- 이미지 크기를 CSS로만 줄이고 원본 대용량 파일을 내려보내는 것
- cache invalidation 계획 없이 cache를 추가하는 것
- p50만 보고 p95/p99 latency를 무시하는 것
