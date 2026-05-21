---
name: rc-test-commander
description: Designs practical test strategies centered on behavior coverage, with integration-first guidance, API mocking, E2E critical-path tests, and flaky-test remediation. Use when users ask to add tests, improve reliability, structure CI test pipelines, or reduce escaped defects.
---

# Test Commander

Build tests that catch real failures with sustainable maintenance cost.

## When to Use This Skill

Use this skill when the user asks to:

- Add missing tests for new or existing features
- Improve confidence in user flows
- Set up integration, E2E, or visual regression tests
- Reduce flaky tests and CI instability

## Strategy

Default to integration-heavy testing, then add unit and E2E where they add unique value.

- Unit: pure logic
- Integration: component + API + state interactions
- E2E: critical business flows only

## Workflow

### Step 1: Select the right level

Pick the smallest level that validates the behavior end-to-end for the risk.

### Step 2: Cover mandatory states for data UI

- loading
- empty
- error
- success
- retry/race behavior

### Step 3: Stabilize external boundaries

- Use deterministic API mocking
- Use factories for realistic data
- Reset test state between runs

### Step 4: Harden E2E scope

Keep E2E to core revenue/critical journeys.
Record traces/screenshots on failure.

### Step 5: Deflake immediately

One repeat flake should trigger immediate fix or explicit temporary skip.

## Anti-patterns

- Testing implementation details over user-visible behavior
- Huge snapshots that change constantly
- Over-mocking core business logic
- E2E suites used for all scenarios

## Production Checklist

- [ ] Integration tests cover behavior-critical states
- [ ] E2E tests cover only top critical flows
- [ ] Mocking is isolated to I/O boundaries
- [ ] CI captures traces/artifacts on failure
- [ ] Flake policy is enforced

## Sources

- Testing-library and Playwright guidance
- Practical test pyramid/trophy patterns
- CI test reliability practices
