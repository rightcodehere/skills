# RightSkills

> 31 battle-tested agent skills for real engineering teams.

Works with any agent that supports the [open skills ecosystem](https://skills.sh/): Claude Code, GitHub Copilot, Cursor, Codex, Windsurf, Cline, and 50+ more.

## Quickstart

```bash
npx skills add @rightcode/skills
```

Pick the skills you want, select which agents to install them on. Done.

---

## Skill Reference

All skills are prefixed with `rightcode-` to avoid conflicts with other skill packages.

### Code Review & Audit (CodeProbe)

| Skill | Description |
|-------|-------------|
| `/rightcode-codeprobe` | Full orchestrator — run `/rightcode-codeprobe audit <path>` for a complete audit across all 9 domains |
| `/rightcode-codeprobe-solid` | SOLID principles violations — SRP, OCP, LSP, ISP, DIP |
| `/rightcode-codeprobe-security` | Security vulnerabilities — injection, XSS, CSRF, hardcoded secrets, broken auth |
| `/rightcode-codeprobe-architecture` | Architecture issues — god objects, circular deps, layer violations, missing boundaries |
| `/rightcode-codeprobe-code-smells` | Code smells — long methods, feature envy, dead code, magic numbers, deep nesting |
| `/rightcode-codeprobe-patterns` | Design patterns — recommends patterns where useful, flags misapplied patterns |
| `/rightcode-codeprobe-performance` | Performance — N+1 queries, O(n²) algorithms, race conditions, memory leaks |
| `/rightcode-codeprobe-error-handling` | Error handling — swallowed exceptions, missing retry/timeout, validation gaps |
| `/rightcode-codeprobe-testing` | Test quality — missing tests, mock abuse, brittle test data, coverage gaps |
| `/rightcode-codeprobe-framework` | Framework idioms — Laravel, React/Next.js, Python/Django best practices |
| `/rightcode-code-review` | Comprehensive PR review with 4-phase process, severity labels, 17+ language guides |

### Engineering Workflow

| Skill | Description |
|-------|-------------|
| `/rightcode-tdd` | TDD with red-green-refactor loop — builds features one vertical slice at a time |
| `/rightcode-diagnose` | Disciplined debugging — reproduce → minimise → hypothesise → instrument → fix → regression-test |
| `/rightcode-grill-with-docs` | Grill session that challenges your plan against CONTEXT.md and ADRs, updates docs inline |
| `/rightcode-improve-codebase-architecture` | Find deepening opportunities informed by domain language and architectural decisions |
| `/rightcode-triage` | Triage issues through a state machine of triage roles |
| `/rightcode-to-issues` | Break a plan/spec/PRD into independently-grabbable issue tracker tickets |
| `/rightcode-to-prd` | Turn current conversation context into a PRD and publish to the issue tracker |
| `/rightcode-zoom-out` | Get a higher-level map of relevant modules and callers in unfamiliar code |
| `/rightcode-prototype` | Build a throwaway prototype — terminal app for logic, or UI variations for design |
| `/rightcode-setup-skills` | Scaffold per-repo config (issue tracker, triage labels, domain docs) once per repo |

### Productivity

| Skill | Description |
|-------|-------------|
| `/rightcode-grill-me` | Relentless interview about a plan until every decision branch is resolved |
| `/rightcode-caveman` | Ultra-compressed ~75% token reduction mode — drops filler, keeps technical accuracy |
| `/rightcode-handoff` | Compact conversation into a handoff document for another agent to pick up |
| `/rightcode-write-a-skill` | Create new skills with proper structure, progressive disclosure, and bundled resources |
| `/rightcode-find-skills` | Discover and install skills from the open skills ecosystem |
| `/rightcode-session-summary-prompt` | Generate a ready-to-paste handoff prompt to continue work in a new clean session |

### Utilities & Setup

| Skill | Description |
|-------|-------------|
| `/rightcode-git-guardrails` | Set up Claude Code hooks to block dangerous git commands before they execute |
| `/rightcode-setup-pre-commit` | Set up Husky pre-commit hooks with lint-staged, Prettier, typecheck, and tests |
| `/rightcode-scaffold-exercises` | Create exercise directory structures with sections, problems, solutions, explainers |
| `/rightcode-migrate-to-shoehorn` | Migrate test `as` type assertions to `@total-typescript/shoehorn` |

---

## CodeProbe Commands

Once `/rightcode-codeprobe` is installed:

```bash
/rightcode-codeprobe audit src/         # Full audit — all 9 sub-skills in parallel
/rightcode-codeprobe quick src/         # Top 5 issues only
/rightcode-codeprobe security src/      # Security scan only
/rightcode-codeprobe solid src/         # SOLID check only
/rightcode-codeprobe architecture src/  # Architecture review only
/rightcode-codeprobe performance src/   # Performance audit only
/rightcode-codeprobe health             # Bird's-eye health dashboard
```

Reports save to `./codeprobe-reports/<timestamp>.md`. Read-only — never modifies your code.

---

## Sources

Skills in this collection are drawn from:

- **Custom RightCode skills** — `codeprobe` multi-agent review system and supporting workflow skills
- **[mattpocock/skills](https://github.com/mattpocock/skills)** — `diagnose`, `tdd`, `grill-me`, `grill-with-docs`, `triage`, `to-issues`, `to-prd`, `zoom-out`, `prototype`, `caveman`, `handoff`, `write-a-skill`, `git-guardrails`, `setup-pre-commit`, `scaffold-exercises`, `migrate-to-shoehorn`
- **[awesome-skills/code-review-skill](https://github.com/awesome-skills/code-review-skill)** — `code-review` (17+ language guides, 4-phase process)

All skills are prefixed `rightcode-` to prevent naming conflicts when combined with other skill packages.

---

## Installing Specific Skills

```bash
# Install just the code review tools
npx skills add @rightcode/skills --skill rightcode-codeprobe --skill rightcode-code-review

# Install all skills to all agents non-interactively
npx skills add @rightcode/skills --all

# Install globally (available in every project)
npx skills add @rightcode/skills -g
```

## License

MIT
