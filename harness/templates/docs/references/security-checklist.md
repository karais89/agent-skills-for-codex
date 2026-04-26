# 보안 체크리스트

보안 검토는 이론적 위험보다 실제 악용 가능성과 영향도를 우선합니다. 사용자 입력, 인증/인가, 데이터 보호, dependency, 오류 노출을 기본 축으로 점검합니다.

## 커밋 전 빠른 확인

- secret, token, private key가 코드나 로그에 포함되지 않았는지 확인합니다.
- 새 입력 경로는 validation과 normalization을 거칩니다.
- 데이터 접근은 인증뿐 아니라 인가까지 확인합니다.
- dependency 변경이 있으면 취약점 audit을 실행합니다.
- 오류 응답이 stack trace나 내부 경로를 노출하지 않는지 확인합니다.

## 인증

- 비밀번호는 bcrypt, scrypt, argon2 같은 강한 알고리즘으로 hash합니다.
- session cookie에는 `HttpOnly`, `Secure`, `SameSite`를 적용합니다.
- password reset token은 만료 시간과 1회 사용 제한을 둡니다.
- 로그인, reset, OTP 검증 endpoint에는 rate limit을 둡니다.
- OAuth flow는 `state`와 PKCE를 사용합니다.

## 인가

- 보호된 endpoint마다 권한을 확인합니다.
- 사용자 소유 리소스 조회는 owner check를 포함합니다.
- admin 기능은 role 또는 permission 기반으로 분리합니다.
- IDOR 방지를 위해 URL path의 id를 그대로 신뢰하지 않습니다.

## 입력 검증

- boundary에서 schema validation을 수행합니다.
- SQL/NoSQL query는 parameterized API를 사용합니다.
- shell command에는 사용자 입력을 직접 연결하지 않습니다.
- redirect URL은 allowlist로 제한합니다.
- 파일 업로드는 확장자, MIME type, 크기, 실제 content를 함께 확인합니다.

## 보안 헤더

권장 기본값:

```http
Content-Security-Policy: default-src 'self'
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), microphone=(), camera=()
```

서비스 특성에 따라 CSP는 필요한 source만 좁게 추가합니다.

## CORS

안전한 기본 정책:

```typescript
app.use(cors({
  origin: ['https://app.example.com'],
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
}));
```

피해야 할 설정:

```typescript
app.use(cors({
  origin: '*',
  credentials: true,
}));
```

## 데이터 보호

- PII와 secret은 로그에 남기지 않습니다.
- 민감 필드는 API 응답에서 제외합니다.
- 전송 구간은 HTTPS를 사용합니다.
- 저장 데이터 암호화가 필요한 도메인인지 확인합니다.
- backup과 export 파일도 동일한 보호 수준을 적용합니다.

## Dependency 보안

```bash
# dependency audit
npm audit

# 가능한 자동 수정
npm audit fix

# Python
pip-audit

# Rust
cargo audit
```

Critical 또는 High 취약점은 release blocker로 취급합니다. 자동 수정이 breaking change를 만들 수 있으므로 lockfile diff와 테스트 결과를 함께 확인합니다.

## 오류 처리

사용자에게 보여줄 오류:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "입력값을 확인하세요."
  }
}
```

노출하면 안 되는 정보:

- stack trace
- SQL query
- 내부 파일 경로
- secret 또는 token 일부
- dependency 버전과 내부 service name

## OWASP Top 10 빠른 기준

| 항목 | 확인 질문 |
| --- | --- |
| Broken Access Control | 모든 리소스 접근에 인가 확인이 있는가? |
| Cryptographic Failures | 민감 데이터가 적절히 보호되는가? |
| Injection | query와 command가 parameterized API를 쓰는가? |
| Insecure Design | 위협 모델과 abuse case를 고려했는가? |
| Security Misconfiguration | 기본 설정, debug mode, CORS, header가 안전한가? |
| Vulnerable Components | 취약 dependency가 없는가? |
| Auth Failures | session, password, token 수명주기가 안전한가? |
| Data Integrity Failures | webhook, package, update의 무결성을 검증하는가? |
| Logging Failures | 보안 이벤트가 기록되고 alert 가능한가? |
| SSRF | 외부 URL fetch가 allowlist와 network 제한을 갖는가? |
