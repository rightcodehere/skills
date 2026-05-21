---
name: rc-performance-profiler
description: Profiles and optimizes web performance across frontend and backend, covering Core Web Vitals, bundle analysis, server profiling, and caching strategy. Use when users ask to diagnose slow pages, improve Lighthouse metrics, reduce bundle size, or address API latency under load.
---

# Performance Profiler

Find real bottlenecks and apply targeted fixes that move measured metrics.

## When to Use This Skill

Use this skill when the user asks to:

- Improve LCP, INP, CLS, or TBT
- Run Lighthouse and interpret results
- Reduce JS/CSS payload size
- Profile backend CPU, memory, or query latency
- Set and enforce performance budgets in CI

## Workflow

### Step 1: Measure first

- Run Lighthouse multiple times and use median results
- Cross-check with field telemetry when available

### Step 2: Address Core Web Vitals

- LCP: preload critical assets and reduce render blocking
- INP: split long tasks and optimize event handlers
- CLS: reserve layout space for media and dynamic UI

### Step 3: Backend profiling

- CPU profile, heap snapshots, and p95/p99 latency review
- Identify N+1 queries and lock contention

### Step 4: Bundle and asset optimization

- Analyze chunk sizes
- Lazy-load below-fold modules only
- Keep first-load budgets explicit

### Step 5: Cache strategy

- Static assets via CDN with versioned long TTL
- API caching with clear invalidation rules
- Avoid caching sensitive or user-unique auth data

## Suggested budgets

- LCP below 2.5s
- INP below 200ms
- CLS below 0.1
- Total JS payload below 300KB gzipped

## Anti-patterns

- Optimizing before measuring
- Treating desktop performance as representative
- Over-splitting bundles into too many micro-chunks
- Ignoring performance regressions in CI

## Production Checklist

- [ ] Baseline metrics captured
- [ ] Core Web Vitals fixes applied and re-measured
- [ ] Backend hotspots profiled and mitigated
- [ ] Bundle budgets documented and enforced
- [ ] CI budget gates active

## Sources

- Lighthouse and web-vitals guidance
- Browser profiling best practices
- Production performance engineering patterns
