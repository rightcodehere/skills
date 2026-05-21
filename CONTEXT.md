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

**Orchestrator Agent**:
A distributable agent role that coordinates workflow by invoking multiple specialized skills or agents.
_Avoid_: master prompt, generic assistant

**Specialist Agent**:
A distributable agent role scoped to one domain capability and invoked directly or via an Orchestrator Agent.
_Avoid_: random helper, one-off bot

**Agent Distribution Unit**:
The packaged set of agent definitions shipped to a team for installation and consistent use.
_Avoid_: local prompt folder, personal setup

**Skill Dependency**:
An explicit reliance by an agent on one or more installed skills for core behavior.
_Avoid_: optional tip, incidental reference

**Artifact Separation Policy**:
The rule that agent packages and skill packages are versioned and released independently even when agents depend on skills.
_Avoid_: lockstep release, single-bundle-only policy

**Repository Topology Policy**:
The rule that agent distribution is isolated in a dedicated repository separate from existing skills and legacy agent repos.
_Avoid_: dual active sources, same-repo coupling with legacy artifacts

**Installation Surface Policy**:
The rule that skills and agents are installed through separate explicit commands.
_Avoid_: implicit auto-install chaining, hidden combined installer

**Dependency Enforcement Policy**:
The rule that agent installation blocks when required skills are missing or below declared minimum versions.
_Avoid_: silent downgrade, warning-only compatibility checks

**Compatibility Ownership Policy**:
The rule that the agent package is the source of truth for required minimum skill versions.
_Avoid_: split ownership, skills-side compatibility matrix ownership

**Breaking Change Gate Policy**:
The rule that new major versions of required skills are treated as incompatible until the agent package explicitly declares support.
_Avoid_: optimistic major upgrades, runtime-only validation

**Distribution Audience Policy**:
The rule that the agent package is published publicly from initial release rather than kept internal-first.
_Avoid_: private-only launch, delayed public availability by default

**Package Identity Policy**:
The rule that the agents artifact uses a distinct public package identity from the skills artifact.
_Avoid_: shared package identity, ambiguous install target

**Agent Package Identity**:
The selected public identity for the agents artifact, currently expressed as rightcodehere/agents.
_Avoid_: skills package name reuse, unnamed placeholder

**Identifier Split Policy**:
The rule that public npm package identity and source repository path are distinct canonical identifiers.
_Avoid_: single overloaded identifier string, install-path ambiguity

**Agent NPM Identity**:
The canonical npm package name for agents, set to @rightcode/agents.
_Avoid_: rightcodehere/agents as npm name, inferred unscoped name

**Agent Repository Path**:
The canonical source repository path for agents, set to RightCodeAI.
_Avoid_: superseded repository slugs, mixed identifier usage

**Auto-Install Policy**:
The rule that agent installation never auto-installs missing skills and instead returns explicit remediation steps.
_Avoid_: implicit dependency installation, side-effectful installer behavior

**Agent Workspace Layout Policy**:
The rule that agent artifacts live in a top-level agents/ package with workflow assets maintained alongside as first-class distribution content.
_Avoid_: nesting agents under skills/, hidden workflow asset locations

**Workflow Artifact Boundary Policy**:
The rule that distributable workflow templates live under agents/workflows while .github/workflows remains reserved for CI automation.
_Avoid_: mixing distributable templates into CI workflow folders, split ownership of templates

**Source of Truth Policy**:
The rule that RightCodeAI is the only active source for agent and workflow distribution changes.
_Avoid_: mirrored editing across repos, ambiguous ownership

**Legacy Freeze Policy**:
The rule that RightSkills and ramukaka remain unchanged for ongoing agent/workflow evolution except optional pointer documentation.
_Avoid_: continued feature edits in legacy repos, parallel release streams

**Baseline Migration Policy**:
The rule that existing ramukaka agent, workflow template, and governance artifacts are copied into RightCodeAI as the initial starting point.
_Avoid_: blank-slate rewrite without carry-over, governance-doc omission, unmanaged cherry-pick migration

**Cutover Sync Policy**:
The rule that migration uses a one-time snapshot with no temporary bidirectional or rolling sync.
_Avoid_: transitional mirroring, delayed ownership transfer

**Release Ownership Policy**:
The rule that publish authority for the agents package is restricted to a small designated maintainer group.
_Avoid_: open publish access, ad-hoc release permissions

**Release Channel Policy**:
The rule that the agents package is published directly to the latest channel at launch instead of staged prerelease tags.
_Avoid_: mandatory beta-first channeling, implicit prerelease gating

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
- An **Orchestrator Agent** coordinates one or more **Specialist Agent** items
- A **Specialist Agent** can declare one or more **Skill Dependency** items
- An **Agent Distribution Unit** can include both **Orchestrator Agent** and **Specialist Agent** items
- **Artifact Separation Policy** governs how an **Agent Distribution Unit** versions against its **Skill Dependency** set
- **Repository Topology Policy** constrains where independently versioned artifacts are maintained
- **Installation Surface Policy** governs operator-facing install commands for skills versus agents
- **Dependency Enforcement Policy** validates **Skill Dependency** requirements at agent install time
- **Compatibility Ownership Policy** assigns manifest ownership for **Skill Dependency** version requirements
- **Breaking Change Gate Policy** constrains major-version upgrade behavior under **Dependency Enforcement Policy**
- **Distribution Audience Policy** constrains release visibility and onboarding requirements for agent artifacts
- **Package Identity Policy** governs external naming clarity between skills and agents artifacts
- **Agent Package Identity** implements **Package Identity Policy** for the agents artifact
- **Identifier Split Policy** governs canonical mapping between package registry identity and source repository path
- **Agent NPM Identity** and **Agent Repository Path** implement **Identifier Split Policy**
- **Auto-Install Policy** constrains dependency remediation behavior under **Dependency Enforcement Policy**
- **Agent Workspace Layout Policy** implements **Repository Topology Policy** at directory-structure level
- **Workflow Artifact Boundary Policy** refines **Agent Workspace Layout Policy** for template placement
- **Source of Truth Policy** defines canonical edit and release ownership
- **Legacy Freeze Policy** constrains post-cutover changes in prior repositories
- **Baseline Migration Policy** defines initial content population strategy for the new source repository
- **Cutover Sync Policy** defines transition mechanics from baseline migration to steady-state ownership
- **Release Ownership Policy** governs who can publish the agents package
- **Release Channel Policy** governs which distribution channel receives initial public releases

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
- Language resolved: "agents" in this discussion means distributable team agents, split into **Orchestrator Agent** and **Specialist Agent** roles with explicit **Skill Dependency**.
- Packaging resolved: adopt **Artifact Separation Policy** so agent distribution versions independently from skill packages.
- Topology superseded: same-repo distribution was replaced by isolation in a dedicated repository under **Repository Topology Policy**.
- Installation resolved: apply **Installation Surface Policy** with separate install commands for skills and agents.
- Compatibility resolved: enforce **Dependency Enforcement Policy** with hard-fail behavior for missing or incompatible skills.
- Ownership resolved: apply **Compatibility Ownership Policy** with agent package as compatibility source of truth.
- Upgrade safety resolved: apply **Breaking Change Gate Policy** by blocking new skill majors until explicit agent compatibility release.
- Audience resolved: adopt **Distribution Audience Policy** with public distribution from day one.
- Naming resolved: adopt **Package Identity Policy** with agent identity set to **Agent Package Identity** = rightcodehere/agents.
- Identifier resolved: apply **Identifier Split Policy** with **Agent NPM Identity** = @rightcode/agents and **Agent Repository Path** = rightcodehere/agents.
- Repository identity superseded: **Agent Repository Path** now resolves to RightCodeAI as canonical source-of-truth repo.
- Naming continuity resolved: retain **Agent NPM Identity** = @rightcode/agents while repository metadata points to RightCodeAI.
- Remediation resolved: enforce **Auto-Install Policy** with fail-only behavior and explicit install instructions.
- Layout resolved: apply **Agent Workspace Layout Policy** with a top-level agents/ package and explicit workflow assets.
- Reference pattern confirmed: existing ramukaka layout uses .github/agents plus .github/workflows-templates as the source model.
- Workflow placement resolved: apply **Workflow Artifact Boundary Policy** with distributable templates in agents/workflows.
- Cutover resolved: apply **Source of Truth Policy** with RightCodeAI as canonical repository for agent/workflow evolution.
- Legacy handling resolved: apply **Legacy Freeze Policy** to keep RightSkills and ramukaka unchanged except optional migration pointers.
- Migration resolved: apply **Baseline Migration Policy** by importing ramukaka agent/workflow assets as the starting baseline.
- Migration scope resolved: include governance assets (policy, capability matrix, registry) in the **Baseline Migration Policy** copy set.
- Transition resolved: apply **Cutover Sync Policy** with one-time copy and immediate no-sync steady state.
- Release control resolved: apply **Release Ownership Policy** with limited publish authority.
- Channel resolved: apply **Release Channel Policy** with direct publish to latest.
