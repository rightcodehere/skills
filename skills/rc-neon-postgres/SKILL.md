---
name: rc-neon-postgres
description: Guides Neon serverless Postgres architecture and operations, including connection patterns, branching workflows, pooling, autoscaling behavior, and API/CLI automation. Use when users ask for Neon-specific implementation advice, serverless Postgres tuning, or branch-based environment workflows.
---

# Neon Postgres

Implement Neon-specific Postgres patterns for serverless and modern cloud workloads.

## When to Use This Skill

Use this skill when the user asks to:

- Set up or optimize Neon Postgres
- Choose connection methods for serverless vs long-running services
- Implement Neon branching for previews and isolated testing
- Configure pooling, autoscaling, and scale-to-zero tradeoffs
- Automate operations with Neon CLI or API

Do not use this skill for generic Postgres tuning unrelated to Neon.

## Workflow

### Step 1: Determine runtime model

- Serverless/edge workloads
- Long-running backend services
- CI preview environment automation

### Step 2: Choose connection strategy

- Use Neon serverless driver for serverless runtimes
- Use pooled connections for bursty concurrency
- Keep TLS and environment-secret handling explicit

### Step 3: Adopt branch-based environments

- Branch per feature/preview when appropriate
- Keep production branch stable
- Merge and clean branch lifecycle intentionally

### Step 4: Plan for scale-to-zero behavior

- Document cold-start implications
- Use warmup patterns for latency-sensitive endpoints

### Step 5: Operational safeguards

- IP/network restrictions where required
- Restore and recovery procedures
- Cost and quota monitoring

## Error handling focus

- Connection exhaustion: verify pooling mode
- Branch quota errors: review plan limits and cleanup
- Latency spikes after idle: account for resume behavior

## Anti-patterns

- Reusing one branch for all environments
- Ignoring pooled connections in serverless traffic
- Hardcoding secrets in source
- Treating Neon-specific behavior as generic Postgres defaults

## Production Checklist

- [ ] Connection method selected per runtime
- [ ] Pooling strategy configured where needed
- [ ] Branch lifecycle documented
- [ ] Restore/recovery path tested
- [ ] Access restrictions and secrets handling verified

## Sources

- Neon official documentation and operational guidance
- Postgres connection and pooling practices
