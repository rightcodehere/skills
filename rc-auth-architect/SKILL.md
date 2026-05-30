---
name: rc-auth-architect
description: Implements production authentication following OWASP Top 10 and NIST SP 800-63B standards, covering password hashing, session management, JWT, OAuth 2.0, WebAuthn/Passkeys, RBAC/ABAC authorization, CSRF protection, MFA, and account recovery. Use when users ask to build login/signup systems, implement authentication, set up authorization, enable SSO, add passkeys, or audit auth security.
---

# Auth Architect

Production authentication and authorization following OWASP Top 10, NIST SP 800-63B, and OAuth 2.0 standards.

## When to Use This Skill

Use this skill when the user asks to:

- Implement authentication (login, signup, sessions)
- Design authorization (RBAC, ABAC, permissions)
- Add multi-factor authentication (TOTP, WebAuthn, passkeys)
- Implement OAuth 2.0 or OIDC for SSO
- Audit existing authentication against security standards
- Design password reset and account recovery flows
- Implement CSRF protection and session management

Do not use this skill for API key management, encryption at rest, or network-level security.

## Authentication Methods

| Method | Use Case | Security | Complexity |
| --- | --- | --- | --- |
| Session-based (httpOnly cookies) | Server-rendered web apps | High | Low |
| JWT + refresh tokens | SPAs, mobile, APIs | High | Medium |
| OAuth 2.0 + OIDC | Third-party login, SSO | High | High |
| WebAuthn/Passkeys | Passwordless, high-security | Very High | Medium |
| Magic links/OTP | Low-friction, email-based | Medium | Low |

## Password Security (NIST SP 800-63B)

- Minimum 12 characters (no maximum below 64)
- No composition rules (uppercase/number/symbol required weakens security)
- Check against HaveIBeenPwned API (k-anonymity)
- Hash with Argon2id (memory=19456, iterations=2) or BCrypt (cost=12 minimum)
- Rate limit login attempts (5 per 15 minutes per IP+username)

## Session Management

- Session ID: `crypto.randomUUID()` (never sequential)
- Storage: Redis or database with TTL
- Idle timeout: 30 minutes (sensitive), 2 hours (standard)
- Absolute timeout: 24 hours
- Rotate on login, privilege change, password change
- Use httpOnly, Secure, SameSite=Strict cookies

## JWT Implementation

- Access token: 15-minute expiry, RS256 (asymmetric) or HS256 (symmetric)
- Refresh token: 7-day expiry, rotated on every use
- Include reuse detection: if a used refresh token is presented, revoke all user tokens
- Never store in localStorage or sessionStorage

## OAuth 2.0 + PKCE

- Authorization Code flow with PKCE (RFC 7636) for public clients
- Code verifier: `crypto.randomBytes(32).toString('base64url')`
- Code challenge: `SHA256(code_verifier).toString('base64url')`
- Code lifetime: 5 minutes, single use
- Scopes: apply principle of least privilege

## WebAuthn/Passkeys (FIDO2)

- Registration ceremony: generate challenge, verify attestation, store credential ID
- Authentication ceremony: generate challenge, verify signature against stored public key
- No passwords needed; biometric or PIN verification instead
- Highest security level; resistant to phishing

## Authorization

### RBAC (Role-Based Access Control)

```
User → Role(s) → Permission(s)
admin: ["users:*", "orders:*", "settings:*"]
manager: ["orders:read", "orders:write", "users:read"]
user: ["orders:read", "profile:write:own"]
```

Format: `resource:action[:scope]`

### ABAC (Attribute-Based Access Control)

```
Allow if:
  user.department === resource.department
  AND user.clearance >= resource.classification
  AND resource.country IN user.authorizedCountries
```

## CSRF Protection

- Cookie-level: `SameSite=Strict` on session cookie
- Token-level: CSRF token in forms (hidden input + cookie, compare server-side)
- Header-level: Custom header (`X-Requested-By: XMLHttpRequest`) for API calls

## MFA Implementation

| Factor | Security | Complexity |
| --- | --- | --- |
| TOTP (Authenticator app) | High | Low |
| Hardware key (FIDO2/WebAuthn) | Very High | Medium |
| SMS OTP | Medium (SIM swap risk) | Low |
| Backup codes (10 single-use) | High (as backup) | Low |

## Error Handling Best Practices

- Return generic messages on auth failure (never reveal which part failed)
- Always log the specific reason internally
- Return 401 for both "email not found" and "wrong password"
- Rate limit login and password-reset endpoints
- Lock account after 5 failed attempts (30-minute lockout)
- Notify users on new device login, password change, MFA change

## Production Checklist

- [ ] Password hashing with Argon2id or BCrypt
- [ ] Password breach check (HaveIBeenPwned API)
- [ ] Rate limiting on login, password reset, MFA
- [ ] Refresh token rotation with reuse detection
- [ ] Session cookies with httpOnly, Secure, SameSite=Strict
- [ ] MFA available for all users
- [ ] Account lockout after N failures
- [ ] Audit logging of all auth events
- [ ] OAuth PKCE for public clients
- [ ] WebAuthn attestation verified server-side
- [ ] Password reset: time-limited token (15 min), single use, sent to verified email
- [ ] Session absolute timeout: 24 hours

## Anti-Patterns to Avoid

- JWT in localStorage (XSS reads it)
- Refresh token without rotation
- Password composition rules (weakens security)
- No rate limiting on login
- MFA optional or unprompted
- Hardcoded JWT secrets
- Sequential or predictable user IDs
- Missing audit logging

## Sources

- OWASP Top 10 (2025)
- NIST SP 800-63B (Digital Identity Guidelines)
- RFC 7519 (JWT), RFC 6749 (OAuth 2.0), RFC 7636 (PKCE)
- WebAuthn Level 2 (W3C Recommendation)
- Auth0 and AWS Cognito architecture patterns
