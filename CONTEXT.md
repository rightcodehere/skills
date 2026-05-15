# RightSkills Skill Authoring

This context defines the language used to keep skill content high quality and consistent across the RightSkills package. It focuses on correctness of SKILL.md, references, scripts, and cross-skill consistency.

## Language

**Skill Authoring Quality**:
The degree to which a skill is structurally correct, clear, and consistent with repository conventions.
_Avoid_: quality check, polish, cleanup

**Skill Definition**:
The canonical instructional contract for a skill, centered on SKILL.md and its declared behavior.
_Avoid_: prompt file, instruction blob

**Reference Material**:
Supporting documentation linked from a skill that expands guidance without changing core behavior.
_Avoid_: extra notes, random docs

**Skill Script**:
A utility script packaged with a skill to support repeatable tasks related to that skill.
_Avoid_: helper shell, ad-hoc command

**Consistency Rule**:
A repository-level convention that all skills must follow.
_Avoid_: style preference, optional guideline

**Certification Unit**:
The scope at which quality is assessed and approved, with each skill as the primary unit.
_Avoid_: release gate, package-only check

**Quality Gate**:
An objective pass/fail check required for a skill to be considered certifiable.
_Avoid_: suggestion, best-effort check

**Validation Surface**:
The execution environment where quality gates are run, constrained here to local developer workflow.
_Avoid_: pipeline-only enforcement, remote gate

**Enforcement Mode**:
How local validation is applied, requiring both automatic pre-commit checks and explicit manual invocation.
_Avoid_: advisory-only mode, hidden checks

**Hook Mechanism**:
The repository-standard tool used to install and run commit hooks, set here to Husky.
_Avoid_: ad-hoc git hooks, machine-local hook scripts

**Validator Runtime**:
The implementation language used for quality-gate logic, set here to Python with npm and Husky as entrypoints.
_Avoid_: mixed runtime implementations, shell-only gate logic

**Validation Scope**:
The set of skills checked per run, constrained here to changed skills only.
_Avoid_: full-repo default, package-wide sweep

**Change Source**:
The git file set used to compute changed skills, defined as staged files only.
_Avoid_: working-tree diff, mixed staged and unstaged detection

**Zero-Scope Behavior**:
The hook outcome when no changed skills are detected, defined as pass with an explicit skip message.
_Avoid_: hard failure, silent exit

**Mutation Policy**:
Whether validation can edit files, defined here as report-only with no automatic file changes.
_Avoid_: auto-fix in hook, implicit rewrites

**Gate Severity**:
The blocking level of a validation finding, using hard fail for registration mismatches.
_Avoid_: informational-only critical checks, ambiguous severity

**Warning Policy**:
The treatment of warning-level findings, defined as visible but non-blocking in pre-commit flow.
_Avoid_: warning-as-error by default, hidden warnings

**Description Rule Class**:
The category of frontmatter description checks, split into objective hard-fail rules and stylistic warning rules.
_Avoid_: all-hard-fail prose checks, unclassified description policy

**Validator Location**:
The repository path for validation tooling, defined as a top-level script under scripts/.
_Avoid_: per-skill validator placement, hidden tooling paths

**Validation Command**:
The contributor-facing npm command interface for running skill quality checks.
_Avoid_: undocumented direct script invocation, inconsistent command names

**Validation Output**:
The result format produced by the validator, using console summary with optional JSON export.
_Avoid_: console-only lock-in, machine-only opaque output

**Context Repository**:
A dedicated repository named with a `-context` suffix that centralizes cross-repo context artifacts for onboarding and ongoing alignment.
_Avoid_: per-repo context-only storage, ad-hoc docs folder

**Context Namespace**:
The naming base used to suggest a context repository name from selected repositories, with user override.
_Avoid_: fixed repo naming, auto-name without confirmation

**Context Slice**:
A per-repository folder inside the Context Repository that is named after the source repository and contains generated artifacts.
_Avoid_: flat file dump, mixed-repo context files

**Architecture Brief**:
A per-repository ARCHITECTURE.md document describing purpose, stack, system role, entry points, and external dependencies.
_Avoid_: implementation-level deep dive, glossary replacement

**Standards Tier**:
The level where standards are defined: project-level (workspace-wide), repo-level (stack-specific), and instruction-level (agent behavior).
_Avoid_: single-layer standards model, implicit standards scope

**Workspace Instruction Source**:
The authoritative workspace-level copilot-instructions.md file stored in the Context Repository and synced outward.
_Avoid_: scattered instruction sources, bidirectional editing

**Instruction Sync Policy**:
The synchronization rule for workspace instructions, defined as one-way from Context Repository to workspace root using a manual script.
_Avoid_: hidden auto-sync, bidirectional merge-by-default

**Soft Enforcement**:
Default behavior that drives context upkeep via instructions and checklists without hard commit blocking.
_Avoid_: mandatory failing hooks by default, no update signal

**Hard Enforcement Option**:
An optional setup toggle that adds hooks or CI checks to enforce context updates when code changes.
_Avoid_: always-on strict blocking, unavailable strict mode

**Idempotent Regeneration**:
Re-run behavior that updates generated artifacts in place while preserving manual edits where possible.
_Avoid_: destructive full regenerate, prompt-per-file overwrite loops

## Relationships

- A **Skill Definition** is evaluated by **Skill Authoring Quality**
- A **Certification Unit** is one **Skill Definition** by default
- A **Skill Definition** passes certification only if all required **Quality Gate** checks pass
- **Quality Gate** checks run on the configured **Validation Surface**
- **Enforcement Mode** determines when **Quality Gate** checks block or allow changes
- **Hook Mechanism** implements automatic local enforcement for **Enforcement Mode**
- **Validator Runtime** implements the concrete checks executed by local commands and hooks
- **Validation Scope** selects which **Certification Unit** items are validated on each run
- **Change Source** determines how **Validation Scope** resolves changed skills
- **Zero-Scope Behavior** defines hook outcome when **Validation Scope** resolves to no skills
- **Mutation Policy** constrains validation to diagnostics without modifying repository files
- **Gate Severity** controls whether a failed check blocks commit in local enforcement
- **Warning Policy** defines whether warning findings can block local commits
- **Description Rule Class** maps frontmatter checks to objective or stylistic enforcement levels
- **Validator Location** determines ownership boundary for cross-skill quality tooling
- **Validation Command** invokes checks from manual workflows and hook workflows
- **Validation Output** defines how findings are communicated to people and tooling
- A **Skill Definition** may include **Reference Material**
- A **Skill Definition** may include one or more **Skill Script** items
- **Consistency Rule** constrains every **Skill Definition**
- A **Context Repository** contains one **Context Slice** per selected repository
- Each **Context Slice** contains both glossary context and one **Architecture Brief**
- **Standards Tier** separates project-wide rules from repo-specific stack rules and instruction behavior
- **Workspace Instruction Source** is propagated by **Instruction Sync Policy**
- **Soft Enforcement** is the default enforcement mode for context maintenance
- **Hard Enforcement Option** can be enabled without changing the default
- **Idempotent Regeneration** governs safe re-runs of context generation

## Example dialogue

> **Dev:** "Does this new skill meet **Skill Authoring Quality** if the instructions are good but naming differs from the repo convention?"
> **Domain expert:** "No. It fails because **Consistency Rule** violations lower **Skill Authoring Quality** even when content is useful."

## Flagged ambiguities

- "setup" was initially broad; resolved here as improving **Skill Authoring Quality** only, not release or publishing workflow.
- Quality scope resolved: **Certification Unit** is per skill first, then aggregated for package readiness.
- Required baseline **Quality Gate** checks resolved: structure, naming, reference integrity, and Python-only skill scripts.
- Execution mode resolved: **Validation Surface** is local only, not CI.
- Local workflow resolved: **Enforcement Mode** is pre-commit plus manual command.
- Pre-commit mechanism resolved: **Hook Mechanism** is Husky.
- Validator implementation resolved: **Validator Runtime** is Python, wrapped by npm scripts and Husky.
- Validation selection resolved: **Validation Scope** is changed skills only.
- Change detection resolved: **Change Source** is `git diff --cached` staged files only.
- Empty selection resolved: **Zero-Scope Behavior** is pass with a clear skip message.
- Fix strategy resolved: **Mutation Policy** is report-only.
- Naming registration resolved: missing entry in .claude-plugin/plugin.json is a hard-fail **Gate Severity**.
- New-skill edge case resolved: staged creation of a skill folder without matching plugin registration is also hard-fail.
- Description policy resolved: objective constraints (present, <=1024 chars) are hard-fail; stylistic constraints are warning-only.
- Enforcement semantics resolved: **Warning Policy** is non-blocking.
- Tool placement resolved: **Validator Location** is top-level at scripts/validate-skills.py.
- Command contract resolved: use both npm run skills:validate (all skills) and npm run skills:validate:staged (staged-changed skills).
- Output contract resolved: console summary is required, with optional JSON output flag.
- Context storage resolved: use a dedicated **Context Repository** instead of per-repo commits.
- Layout resolved: use nested per-repo **Context Slice** folders named after source repositories.
- Naming resolved: suggest `-context` using **Context Namespace** detection and allow user override.
- Documentation split resolved: glossary data stays in CONTEXT.md; structure and stack live in **Architecture Brief**.
- Standards model resolved: use three **Standards Tier** levels with optional generation toggles.
- Standards discovery resolved: broad pattern search is used before generating new standards.
- Tech detection resolved: infer from repo config files first; ask user when ambiguous.
- ADR baseline resolved: create ADR folder skeleton only, no automatic ADR generation.
- Instruction ownership resolved: **Workspace Instruction Source** stays in context repo with one-way **Instruction Sync Policy**.
- Enforcement resolved: default to **Soft Enforcement** with optional **Hard Enforcement Option**.
- Re-run behavior resolved: apply **Idempotent Regeneration** rather than destructive regeneration.
