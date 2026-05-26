# RightSkills

> 46 battle-tested agent skills for real engineering teams.

Works with any agent that supports the [open skills ecosystem](https://skills.sh/): Claude Code, GitHub Copilot, Cursor, Codex, Windsurf, Cline, IBM Bob, and 50+ more.

## Quickstart

```bash
npx skills add rightcodehere/skills
```

Pick the skills you want, select which agents to install them on. Done.

## Local Skill Validation

This repo includes local quality gates for skill authoring consistency.

```bash
# validate all skills
npm run skills:validate

# validate only staged changed skills
npm run skills:validate:staged
```

Pre-commit uses Husky and runs `npm run skills:validate:staged`.
Warnings are non-blocking; errors block commit.

---

## Skill Reference

All skills are prefixed with `rc-` to avoid conflicts with other skill packages.

### Code Review & Audit (CodeProbe)

| Skill | Description |
|-------|-------------|
| `/rc-codeprobe` | Full orchestrator — run `/rc-codeprobe audit <path>` for a complete audit across all 9 domains |
| `/rc-codeprobe-solid` | SOLID principles violations — SRP, OCP, LSP, ISP, DIP |
| `/rc-codeprobe-security` | Security vulnerabilities — injection, XSS, CSRF, hardcoded secrets, broken auth |
| `/rc-codeprobe-architecture` | Architecture issues — god objects, circular deps, layer violations, missing boundaries |
| `/rc-codeprobe-code-smells` | Code smells — long methods, feature envy, dead code, magic numbers, deep nesting |
| `/rc-codeprobe-patterns` | Design patterns — recommends patterns where useful, flags misapplied patterns |
| `/rc-codeprobe-performance` | Performance — N+1 queries, O(n²) algorithms, race conditions, memory leaks |
| `/rc-codeprobe-error-handling` | Error handling — swallowed exceptions, missing retry/timeout, validation gaps |
| `/rc-codeprobe-testing` | Test quality — missing tests, mock abuse, brittle test data, coverage gaps |
| `/rc-codeprobe-framework` | Framework idioms — Laravel, React/Next.js, Python/Django best practices |
| `/rc-code-review` | Comprehensive PR review with 4-phase process, severity labels, 17+ language guides |

### Engineering Workflow

| Skill | Description |
|-------|-------------|
| `/rc-tdd` | TDD with red-green-refactor loop — builds features one vertical slice at a time |
| `/rc-diagnose` | Disciplined debugging — reproduce → minimise → hypothesise → instrument → fix → regression-test |
| `/rc-grill-with-docs` | Grill session that challenges your plan against CONTEXT.md and ADRs, updates docs inline |
| `/rc-improve-codebase-architecture` | Find deepening opportunities informed by domain language and architectural decisions |
| `/rc-triage` | Triage issues through a state machine of triage roles |
| `/rc-to-issues` | Break a plan/spec/PRD into independently-grabbable issue tracker tickets |
| `/rc-to-prd` | Turn current conversation context into a PRD and publish to the issue tracker |
| `/rc-zoom-out` | Get a higher-level map of relevant modules and callers in unfamiliar code |
| `/rc-prototype` | Build a throwaway prototype — terminal app for logic, or UI variations for design |
| `/rc-setup-skills` | Scaffold per-repo config (issue tracker, triage labels, domain docs) once per repo |
| `/rc-setup-context-repo` | Create and maintain a dedicated multi-repo context repository with CONTEXT/ARCHITECTURE docs, standards, and Copilot instruction sync |

### Productivity

| Skill | Description |
|-------|-------------|
| `/rc-grill-me` | Relentless interview about a plan until every decision branch is resolved |
| `/rc-caveman` | Ultra-compressed ~75% token reduction mode — drops filler, keeps technical accuracy |
| `/rc-handoff` | Compact conversation into a handoff document for another agent to pick up |
| `/rc-write-a-skill` | Create new skills with proper structure, progressive disclosure, and bundled resources |
| `/rc-find-skills` | Discover and install skills from the open skills ecosystem |
| `/rc-session-summary-prompt` | Generate a ready-to-paste handoff prompt to continue work in a new clean session |

### Infrastructure & DevOps

| Skill | Description |
|-------|-------------|
| `/rc-docker` | Optimize Docker images with multi-stage builds, distroless bases, BuildKit, multi-arch builds, and security hardening |
| `/rc-kubernetes` | Deploy and manage Kubernetes — Deployments, Services, Gateway API, service mesh, networking, autoscaling, security |
| `/rc-terraform` | Infrastructure as code with Terraform — modules, remote state, Stacks, test framework, preconditions/postconditions |
| `/rc-neon-postgres` | Set up and manage Neon PostgreSQL for serverless Postgres workloads |

### Frontend & Component Development

| Skill | Description |
|-------|-------------|
| `/rc-component-forge` | Design and build reusable UI components with accessibility and performance |
| `/rc-design` | Design system guidance and implementation for consistent UX/UI |
| `/rc-responsive-engine` | Build responsive, mobile-first layouts with modern CSS techniques |

### Testing & Performance

| Skill | Description |
|-------|-------------|
| `/rc-test-commander` | Manage and execute complex test suites with reporting and analysis |
| `/rc-performance-profiler` | Profile and optimize application performance — CPU, memory, network, rendering |

### Git & Workflow Utilities

| Skill | Description |
|-------|-------------|
| `/rc-git-commit-push` | Streamlined commit and push workflow with safety checks and conventional commits |
| `/rc-git-workflow` | Full git workflow management — branches, rebasing, conflict resolution, history cleanup |
| `/rc-git-guardrails` | Set up Claude Code hooks to block dangerous git commands before they execute |
| `/rc-skill-updater` | Keep installed skills up-to-date with automatic version checking and updates |

### Setup & Initialization

| Skill | Description |
|-------|-------------|
| `/rc-setup-pre-commit` | Set up Husky pre-commit hooks with lint-staged, Prettier, typecheck, and tests |
| `/rc-scaffold-exercises` | Create exercise directory structures with sections, problems, solutions, explainers |
| `/rc-migrate-to-shoehorn` | Migrate test `as` type assertions to `@total-typescript/shoehorn` |

---

## CodeProbe Commands

Once `/rc-codeprobe` is installed:

```bash
/rc-codeprobe audit src/         # Full audit — all 9 sub-skills in parallel
/rc-codeprobe quick src/         # Top 5 issues only
/rc-codeprobe security src/      # Security scan only
/rc-codeprobe solid src/         # SOLID check only
/rc-codeprobe architecture src/  # Architecture review only
/rc-codeprobe performance src/   # Performance audit only
/rc-codeprobe health             # Bird's-eye health dashboard
```

Reports save to `./codeprobe-reports/<timestamp>.md`. Read-only — never modifies your code.

---

## What Is This?

The open skills ecosystem is generating incredible work across the community. Rather than reinvent the wheel, RightCode Skills serves as a **curated umbrella** — bringing together the best skills from talented builders, adapting them to a consistent workflow, and filling gaps with original work where nothing good exists yet.

Every skill here has been reviewed, tested against real engineering workflows, and in many cases extended or restructured. The `rc-` prefix keeps the collection self-contained so it plays nicely alongside other skill packages without name collisions.

---

## Credits & Attribution

This collection stands on the shoulders of great work by:

### [Matt Pocock](https://github.com/mattpocock) — [mattpocock/skills](https://github.com/mattpocock/skills)

Matt built the engineering workflow backbone that most of this collection is built on. The following skills originate from his repo:

`diagnose` · `tdd` · `grill-me` · `grill-with-docs` · `triage` · `to-issues` · `to-prd` · `zoom-out` · `prototype` · `caveman` · `handoff` · `write-a-skill` · `git-guardrails` · `setup-pre-commit` · `scaffold-exercises` · `migrate-to-shoehorn` · `setup-skills`

### [Nishil Bhave](https://dev.to/nishilbhave) — [I built a multi-agent code review skill](https://dev.to/nishilbhave/i-built-a-multi-agent-code-review-skill-for-claude-code-heres-how-it-works-366i)

Nishil's article and architecture inspired the entire `codeprobe` system — the idea of routing a code audit to specialist sub-skills in parallel, scoring findings by severity, and generating copy-pasteable fix prompts. The implementation here extends that foundation significantly.

### [awesome-skills](https://github.com/awesome-skills) — [code-review-skill](https://github.com/awesome-skills/code-review-skill)

A community-maintained single-skill repo with an outstanding collection of language and framework-specific review guides (17+ languages). Powers `rc-code-review`.

---

If you're building skills and want your work included here, open an issue or PR.

---

## Installing Specific Skills

```bash
# Install just the code review tools
npx skills add @rightcode/skills --skill rc-codeprobe --skill rc-code-review

# Install all skills to all agents non-interactively
npx skills add @rightcode/skills --all

# Install globally (available in every project)
npx skills add @rightcode/skills -g
```

## License

MIT
