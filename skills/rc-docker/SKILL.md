---
name: rc-docker
description: Optimizes Docker images with multi-stage builds, distroless bases, BuildKit cache mounts, multi-architecture builds, Docker Compose local development, security hardening (non-root user, seccomp, capabilities drop), and CVE scanning via docker scout and trivy. Use when users ask to write a Dockerfile, optimize image size, set up docker-compose, debug containers, harden container security, or scan for vulnerabilities.
---

# Docker

Production-grade Docker images, multi-stage builds, BuildKit optimization, security hardening, and vulnerability scanning.

## Before You Containerize

Answer these questions first:

- Does the app need process isolation? → Docker
- Will it deploy to Kubernetes? → Docker + distroless + non-root
- Is it a monolith with simple deployment? → Docker Compose
- Is it a static site? → Consider nginx:alpine single-stage
- Is the app latency-sensitive (sub-millisecond)? → Container overhead matters at extreme scale; consider bare metal

## Quick Start: `docker init`

For new projects, run `docker init` in the project root. It auto-detects the language and generates a Dockerfile, `.dockerignore`, and `compose.yaml` with best-practice defaults. Always review and harden the output—the generated files are a starting point, not production-ready.

## Multi-Stage Build Structure

Use this exact structure:

1. **Stage 1 (deps)**: Copy lock files → install production dependencies
2. **Stage 2 (build)**: Copy source → compile
3. **Stage 3 (runtime)**: Minimal base → copy artifacts from stages 1-2 → run as non-root

For Go projects, skip Stage 1 (Go has no runtime dependencies).

## Base Images by Stack

| Stack | Build Stage | Runtime |
| --- | --- | --- |
| Node.js | `node:22-slim` | `gcr.io/distroless/nodejs22-debian12` |
| Go | `golang:1.24-alpine` | `gcr.io/distroless/static-debian12` or `scratch` |
| Python | `python:3.12-slim` | `python:3.12-slim` |
| Rust | `rust:1.85-slim` | `gcr.io/distroless/cc-debian12` or `scratch` |

## BuildKit Optimizations

Enable BuildKit for cached layer caching:

```dockerfile
# syntax=docker/dockerfile:1.4
RUN --mount=type=cache,target=/root/.npm npm ci --omit=dev
```

Benefits: cache persists across builds, dramatically reduces build time.

## Dockerfile Anti-Patterns

| Anti-Pattern | Fix | Why |
| --- | --- | --- |
| Single-stage build | Multi-stage with distroless runtime | Final image contains build tools (5x larger, more attack surface) |
| `COPY . .` before `npm install` | Copy package files first, then install, then copy source | Docker caches by layer; source changes should invalidate only the last COPY |
| `latest` tag | Pin full version (`22.14-slim`, not `22-slim`) | `latest` means "whatever was pushed last"; a patch update can break your app |
| Root user in container | `USER nonroot` with distroless | Container escape bugs exist; non-root limits damage to the container |
| Secrets in build args | `RUN --mount=type=secret` (BuildKit) | Build args are stored in image metadata; anyone with image access can extract them |
| No `.dockerignore` | Add with `node_modules/`, `.git/`, `*.log`, `Dockerfile*` | Reduces build context size by 60-90%; prevents secret leaks from local `.env` |
| No healthcheck | `HEALTHCHECK --interval=30s CMD curl -f http://localhost/health` | Without healthcheck, orchestrators only detect process crashes, not app hangs |
| `npm install` in production | `npm ci --omit=dev` or `--production` | Dev dependencies add 100-200MB and increase CVEs from unused packages |

## Docker Compose for Local Development

```yaml
services:
  app:
    build: .
    ports: ["3000:3000"]
    develop:
      watch:
        - action: sync+restart
          path: ./src
          target: /app/src
    depends_on: [db]
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
  db:
    image: postgres:16-alpine
    volumes: ["pgdata:/var/lib/postgresql/data"]
volumes:
  pgdata:
```

Run `docker compose watch` for hot-reload on file changes.

## Multi-Platform Builds

```bash
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --cache-from=type=gha \
  --cache-to=type=gha,mode=max \
  --tag registry/app:latest \
  --push .
```

## CVE Scanning

```bash
# Using docker scout
docker scout cves myapp:latest

# Or trivy
trivy image myapp:latest
```

If critical CVEs are found, switch base image to a newer distroless tag or add patched dependencies in the builder stage.

## Pre-Flight Checklist

Before deploying a Docker image:

- [ ] `.dockerignore` exists and excludes `node_modules/`, `.git/`, `*.log`, `Dockerfile*`
- [ ] Multi-stage build with separate build and runtime stages
- [ ] Runtime stage uses distroless or minimal base
- [ ] `USER nonroot` (or equivalent) — never runs as root
- [ ] `HEALTHCHECK` defined with appropriate interval
- [ ] Secrets use `--mount=type=secret`, never `ENV` or `ARG`
- [ ] `npm ci --omit=dev` for production dependencies
- [ ] `docker scout quickview` or `trivy image` passes with zero HIGH/CRITICAL CVEs
- [ ] Image size verified: `docker images --format "{{.Size}}"`—should be <200MB for most apps
- [ ] `docker compose watch` tested in development
- [ ] Container starts and passes healthcheck within 30 seconds
- [ ] Logs go to stdout/stderr (no log files inside container)

## Sources

- Dockerfile best practices (docs.docker.com)
- BuildKit documentation
- Google distroless images
- Trivy vulnerability scanner
- Docker Scout documentation
