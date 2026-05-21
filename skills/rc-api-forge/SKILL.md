---
name: rc-api-forge
description: Provides API design guidance for REST, GraphQL, and webhooks, including OpenAPI 3.1, pagination, rate limiting, idempotency, versioning, and consistent error contracts. Use when users ask to design an API, create endpoints, define REST or GraphQL schemas, generate OpenAPI specs, or review HTTP API behavior.
---

# API Forge

Design APIs that developers can implement, document, and operate reliably.

## When to Use This Skill

Use this skill when the user asks to:

- Design a REST API, GraphQL API, or webhook contract
- Define endpoints, resources, methods, status codes, or response envelopes
- Generate or review an OpenAPI 3.1 specification
- Add pagination, rate limiting, idempotency, versioning, or webhook delivery rules
- Audit an HTTP API for consistency, security, and production readiness

Do not use this skill for database schema design, frontend integration details, or non-HTTP protocols such as gRPC, WebSocket, or MQTT.

## Suggested Workflow

### Step 1: Determine the API style

Choose the interface before designing resources:

| Type | Best for | Output |
| --- | --- | --- |
| REST | CRUD and resource-oriented APIs | OpenAPI 3.1 |
| GraphQL | Flexible reads across multiple resources | SDL plus resolver rules |
| Webhook | Event-driven notifications | Delivery and signature contract |

### Step 2: Define resources and naming

- Use noun-based, plural resource names such as `/users` and `/orders`
- Keep nesting shallow; prefer at most two levels such as `/users/{id}/orders`
- Model actions as sub-resources only when CRUD does not fit, such as `/orders/{id}/cancel`
- Use query parameters for filtering and sorting, such as `/users?role=admin`
- Prefer kebab-case paths such as `/order-items`

### Step 3: Map HTTP methods correctly

| Method | Purpose | Idempotent | Safe |
| --- | --- | --- | --- |
| GET | Read a resource | Yes | Yes |
| POST | Create a resource | No | No |
| PUT | Replace a resource | Yes | No |
| PATCH | Partially update a resource | No | No |
| DELETE | Remove a resource | Yes | No |

Avoid using POST as a generic escape hatch when another method communicates intent more precisely.

### Step 4: Standardize the response contract

Use one response envelope across the API unless the protocol already defines one:

```json
{
  "data": {},
  "meta": {
    "page": 1,
    "per_page": 25,
    "total": 100
  },
  "error": null,
  "request_id": "req_abc123"
}
```

For GraphQL and JSON:API, keep their native envelopes and make the error contract equally consistent.

### Step 5: Design pagination up front

Prefer cursor-based pagination for public or high-volume endpoints:

```json
{
  "data": [],
  "meta": {
    "next_cursor": "def456",
    "has_more": true
  }
}
```

- Default page size: 25
- Maximum page size: 100
- Keep cursors opaque; do not expose raw internal identifiers

### Step 6: Define status codes explicitly

Use exact status codes instead of broad success and failure buckets:

| Code | When |
| --- | --- |
| 200 | Successful read or update |
| 201 | Resource created |
| 204 | Successful delete with no body |
| 400 | Malformed request |
| 401 | Missing or invalid authentication |
| 403 | Authenticated but not allowed |
| 404 | Resource not found |
| 409 | Conflict or duplicate |
| 422 | Validation failure |
| 429 | Rate limit exceeded |
| 500 | Internal error |
| 502 | Downstream dependency failure |
| 503 | Maintenance or overload |

### Step 7: Normalize error handling

Every error response should include a machine-readable code, a short human-readable message, and a correlation identifier:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Email is required",
    "details": [
      {
        "field": "email",
        "code": "required",
        "message": "Email is required"
      }
    ],
    "request_id": "req_a1b2c3d4e5f6",
    "docs_url": "https://docs.example.com/errors/validation"
  }
}
```

Never return stack traces, ORM errors, or internal service details to clients.

### Step 8: Add operational rules

#### Rate limiting

- Default algorithm: token bucket
- Send `X-RateLimit-Limit`, `X-RateLimit-Remaining`, and `X-RateLimit-Reset` headers
- Return `429` with `Retry-After` when the limit is exceeded
- Apply stricter limits to login, password reset, and MFA endpoints

#### Versioning

- Prefer URL-path versioning for public REST APIs, such as `/v1/users`
- Use deprecation and sunset headers before breaking changes
- Provide at least a six-month migration window for public consumers

#### Idempotency

- Support `Idempotency-Key` on create and other non-idempotent operations that may be retried
- Reuse the cached response for the same key and same request body within the TTL
- Return `409` if the same key is reused with a different request body

#### Webhooks

- Use an event envelope with stable event types and timestamps
- Retry with exponential backoff
- Expect a fast `200` acknowledgment from the consumer
- Verify signatures with HMAC-SHA256 and a timing-safe comparison

## OpenAPI 3.1 Expectations

When generating or reviewing OpenAPI, every endpoint should include:

- A concise summary
- Parameters with location, schema, examples, and descriptions
- All expected responses and status codes
- A request body for POST, PUT, and PATCH when applicable
- Authentication and rate-limit behavior where relevant

## GraphQL Expectations

- Use queries for reads, mutations for writes, and subscriptions only when real-time behavior is justified
- Limit query depth and complexity
- Use DataLoader or equivalent batching to avoid N+1 resolver behavior
- Return structured errors with machine-readable extension codes

## API Security Checklist

- Enforce HTTPS and modern TLS
- Validate inputs at the boundary
- Use parameterized queries only
- Keep secrets out of responses and logs
- Limit request size and parser depth
- Configure CORS per environment; never use `*` with credentials
- Set baseline security headers
- Rate-limit authentication and recovery endpoints

## Anti-Patterns

- Verb-heavy URLs such as `/getUsers`
- Deeply nested resources that expose internal coupling
- Page-based pagination for high-churn feeds
- Missing `X-RateLimit-*` headers
- Generic `500` responses with stack traces
- Breaking changes without versioning and sunset communication
- POST-only APIs that ignore HTTP method semantics
- Inconsistent error shapes across endpoints

## Production Checklist

- [ ] OpenAPI 3.1 covers every public endpoint
- [ ] Response envelopes are consistent
- [ ] Pagination strategy is defined
- [ ] Rate limiting is documented and enforced
- [ ] Idempotency is implemented where retries are expected
- [ ] Webhook verification is specified for every inbound event
- [ ] Versioning and deprecation policy are documented
- [ ] Error responses include `code` and `request_id`
- [ ] Security controls are defined at the boundary

## Sources

- Stripe API patterns for idempotency, pagination, and webhooks
- GitHub REST API patterns for resource naming and versioning
- Twilio webhook verification patterns
- OpenAPI 3.1 specification
- JSON:API specification
- GraphQL Relay connection guidance
- RFC 7231 and RFC 6585 for HTTP semantics and status codes