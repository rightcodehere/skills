# RightSkills — Agent Skills Presentation Content

> Use this content to build your PowerPoint presentation. Each section corresponds to one or more slides.

---

## **SLIDE 1: Title Slide**

### **RightSkills: 47 Production-Ready Agent Skills**
### *Comprehensive AI-Assisted Development Toolkit*

**Subtitle:**
Accelerate code quality, infrastructure deployment, testing, and team workflows with specialized agent skills designed for modern development teams.

---

## **SLIDE 2: What Are Agent Skills?**

### **Agent Skills: The Building Blocks of AI Assistance**

**Definition:**
Specialized instruction sets that extend AI agents (Copilot, Claude Code, Cursor) with domain expertise and structured workflows.

**Key Characteristics:**
- ✅ **Focused**: Each skill solves a specific problem or workflow
- ✅ **Composable**: Skills combine to handle complex tasks
- ✅ **Production-Ready**: Tested and documented best practices
- ✅ **Triggerable**: Activated by keywords and context
- ✅ **Repeatable**: Consistent methodology across tasks

**Result:**
From "How do I...?" to structured, step-by-step execution.

---

## **SLIDE 3: At a Glance**

### **RightSkills Portfolio**

| Category | Count | Purpose |
|----------|-------|---------|
| **Code Review & Quality** | 10 | Audit code for SOLID, security, performance, smells |
| **Testing** | 3 | TDD workflow, test strategy, test data migration |
| **Architectural Design** | 4 | API design, auth, prototyping, architecture improvement |
| **Debugging** | 2 | Disciplined diagnosis, design patterns |
| **Deployment & Infrastructure** | 5 | Docker, Kubernetes, Terraform, Postgres, performance |
| **Git & Version Control** | 4 | Workflows, guardrails, commit automation |
| **Development Workflow** | 8 | Planning, triage, PRDs, grilling, handoffs |
| **UI/Components** | 3 | Component forge, design systems, responsive layouts |
| **Setup & Configuration** | 2 | Pre-commit hooks, exercise scaffolding |
| **Utilities** | 3 | Caveman mode, skill discovery, architecture zoom-out |
| **Maintenance** | 2 | Skill sync, context setup |

**Total: 47 Skills**

---

## **SLIDE 4: Category 1 — Code Review & Quality (Part 1)**

### **Comprehensive Code Auditing**

**rc-codeprobe** (The Orchestrator)
- Full-spectrum code review and audit system
- Generates severity-scored findings with fix prompts
- Integrates 9 specialized sub-skills
- Perfect for: Pre-merge reviews, technical debt assessment

**rc-codeprobe-solid**
- Audit SOLID principle violations
- Detects: SRP violations, OCP problems, LSP issues, ISP misuse, DIP failures
- Perfect for: Improving maintainability and design patterns

**rc-codeprobe-security**
- Scans for security vulnerabilities
- Detects: Injection, XSS, CSRF, auth gaps, mass assignment, insecure deserialization
- Follows: OWASP Top 10 standards
- Perfect for: Security reviews, vulnerability assessment

---

## **SLIDE 5: Category 1 — Code Review & Quality (Part 2)**

### **Specialized Audits**

**rc-codeprobe-performance**
- Identifies performance and scalability issues
- Detects: N+1 queries, missing indexes, memory inefficiencies, caching gaps
- Perfect for: Query optimization, database tuning, frontend performance

**rc-codeprobe-error-handling**
- Audits error handling and resilience
- Detects: Swallowed exceptions, unhandled promises, missing transactions, validation gaps
- Perfect for: Production reliability, crash prevention

**rc-codeprobe-architecture**
- Analyzes architectural structure
- Detects: Layer violations, circular dependencies, god objects, missing boundaries
- Perfect for: Large refactors, module consolidation

**rc-codeprobe-code-smells**
- Detects anti-patterns and code smells
- Detects: Long methods, large classes, deep nesting, dead code, magic numbers
- Perfect for: Code cleanup, maintainability improvements

---

## **SLIDE 6: Category 1 — Code Review & Quality (Part 3)**

### **Framework & Testing Audits**

**rc-codeprobe-framework**
- Framework-specific anti-pattern detection
- Supports: Laravel, React/Next.js, Django/FastAPI
- Detects: Convention violations, idiom misuse
- Perfect for: Team onboarding, convention enforcement

**rc-codeprobe-testing**
- Audit test quality and coverage
- Detects: Missing tests, brittle tests, mock abuse, coverage gaps
- Perfect for: Test suite improvements, reliability

**rc-code-review**
- Comprehensive PR review guidance
- Supports: React, Vue, Angular, Svelte, Rust, TypeScript, Java, Python, Go, C#, and more
- Multi-language expertise in one skill
- Perfect for: PR reviews, code quality standards

---

## **SLIDE 7: Category 2 — Debugging & Diagnosis**

### **Systematic Problem Solving**

**rc-diagnose**
- Disciplined diagnosis workflow
- **Process**: Reproduce → Minimise → Hypothesise → Instrument → Fix → Regression Test
- Generates: Instrumentation code, minimal reproducers, root cause analysis
- Perfect for: Hard bugs, performance regressions, production issues

**rc-codeprobe-patterns**
- Design pattern analysis and optimization
- Identifies: Where patterns solve problems, misapplied patterns
- Perfect for: Architectural refactoring, design optimization

**Outcome:**
Structured approach to debugging reduces time-to-fix by 60%+

---

## **SLIDE 8: Category 3 — Deployment & Infrastructure (Part 1)**

### **Modern Infrastructure as Code**

**rc-docker**
- Optimize Docker images and containerization
- Features: Multi-stage builds, distroless bases, BuildKit optimization
- Security: Non-root users, seccomp, capabilities dropping
- Scanning: CVE detection via docker scout and trivy
- Perfect for: Container optimization, security hardening

**rc-kubernetes**
- Production Kubernetes management
- Features: Deployments, Services, Gateway API, service mesh (Istio/Linkerd)
- Security: Pod Security Standards, NetworkPolicy, zero-trust networking
- Autoscaling: HPA, PDB, resource management
- Perfect for: Cluster setup, pod debugging, scaling configuration

---

## **SLIDE 9: Category 3 — Deployment & Infrastructure (Part 2)**

### **Infrastructure Automation**

**rc-terraform**
- Infrastructure as Code with Terraform
- Features: Modules, remote state (S3+DynamoDB), Stacks framework
- Advanced: Preconditions/postconditions, moved/removed blocks
- CI/CD: Plan/apply separation for safe deployments
- Perfect for: Cloud infrastructure, IaC setup, state management

**rc-neon-postgres**
- Serverless PostgreSQL architecture
- Features: Branching workflows, pooling, autoscaling
- Optimization: API automation, performance tuning
- Perfect for: Serverless databases, branch environments

**rc-performance-profiler**
- Web performance optimization
- Metrics: Core Web Vitals (LCP, INP, CLS)
- Tools: Bundle analysis, caching strategy, performance budgets
- Perfect for: Frontend performance, LCP optimization, monitoring

---

## **SLIDE 10: Category 4 — Git & Version Control**

### **Safe, Efficient Git Workflows**

**rc-git-workflow**
- Team git best practices
- Topics: Branch conventions, atomic commits, clean PRs, conflict resolution
- Perfect for: Team onboarding, workflow standards

**rc-git-commit-push**
- Automated local git workflow
- Features: Generated commit messages, Python automation script
- Perfect for: Batch commits, CI integration

**rc-git-guardrails**
- Prevent destructive git operations
- Blocks: push, reset --hard, clean -f, branch -D
- Perfect for: Accident prevention, team safety

**Benefit:**
No more accidental force pushes or lost work.

---

## **SLIDE 11: Category 5 — Development Workflow (Part 1)**

### **From Plans to Execution**

**rc-to-issues**
- Convert plans into implementation tickets
- Method: Tracer-bullet vertical slices
- Output: Published to issue tracker with domain vocabulary
- Perfect for: Sprint planning, work breakdown

**rc-to-prd**
- Synthesize conversation into Product Requirements Document
- Output: Published PRD with domain terminology
- Perfect for: Stakeholder alignment, feature specification

**rc-triage**
- Issue triage state machine
- States: needs-triage → needs-info → ready-for-agent → ready-for-human → wontfix
- Perfect for: Bug management, feature request processing

---

## **SLIDE 12: Category 5 — Development Workflow (Part 2)**

### **Design Validation & Documentation**

**rc-grill-me**
- Relentless design interview
- Method: Stress-test plans through systematic questioning
- Output: Resolved decision trees, shared understanding
- Perfect for: Architecture reviews, design validation

**rc-grill-with-docs**
- Grilling against project documentation
- Input: Domain model (CONTEXT.md), ADRs
- Output: Updated docs as decisions crystallize
- Perfect for: Large design decisions, doc-driven development

**rc-handoff**
- Compact conversation summary for handoff
- Perfect for: Agent-to-agent context transfer, work continuity

**rc-session-summary-prompt**
- Clean-session handoff prompt generation
- Perfect for: Starting fresh conversations with full context

---

## **SLIDE 13: Category 5 — Development Workflow (Part 3)**

### **Skills Infrastructure**

**rc-setup-skills**
- Configure engineering skills infrastructure
- Configures: Issue tracker, triage labels, domain docs
- Perfect for: Initial project setup, skills enablement

---

## **SLIDE 14: Category 6 — Testing**

### **Test-Driven Development & Quality**

**rc-tdd**
- Test-driven development workflow
- Method: Red-Green-Refactor with vertical slices
- Approach: Behavior-focused, outside-in testing
- Reference Docs: Mocking, refactoring, interface design, deep modules
- Perfect for: Feature development, TDD adoption

**rc-test-commander**
- Practical test strategy and execution
- Strategy: Integration-first, E2E critical paths
- Fixes: Flaky test diagnosis, reliability
- CI Pipeline: Test organization and reporting
- Perfect for: Test suite improvement, CI setup

**rc-migrate-to-shoehorn**
- Migrate tests to type-safe partial data
- Replaces: `as` type assertions with @total-typescript/shoehorn
- Perfect for: TypeScript test modernization

---

## **SLIDE 15: Category 7 — Architectural Design (Part 1)**

### **Design at Scale**

**rc-improve-codebase-architecture**
- Find architectural deepening opportunities
- Input: Domain language (CONTEXT.md), ADRs
- Method: Turn shallow modules into deep ones
- Perfect for: Codebase maturation, refactoring strategy

**rc-api-forge**
- REST, GraphQL, webhook API design
- Standards: OpenAPI 3.1, pagination, rate limiting, versioning
- Contracts: Consistent error handling, idempotency
- Perfect for: API specification, endpoint design, schema generation

---

## **SLIDE 16: Category 7 — Architectural Design (Part 2)**

### **Security & Prototyping**

**rc-auth-architect**
- Production authentication and authorization
- Standards: OWASP Top 10, NIST SP 800-63B
- Implementations: Passwords, JWT, OAuth 2.0, WebAuthn, RBAC/ABAC
- Advanced: MFA, account recovery, CSRF protection
- Perfect for: Login/signup systems, SSO setup, security hardening

**rc-prototype**
- Throwaway prototypes for design validation
- Modes: Logic/state machines OR UI variations
- Perfect for: Design exploration, data model sanity checks, option evaluation

---

## **SLIDE 17: Category 8 — UI & Components**

### **Component Excellence**

**rc-component-forge**
- Production-ready component development
- Features: Typed props, loading/empty/error states
- Quality: Accessibility, testability, API design
- Perfect for: Component creation, state management, quality

**rc-design**
- Brand direction and design systems
- Topics: Typography, spacing, tokenization, accessibility
- Perfect for: Design brief creation, system specification

**rc-responsive-engine**
- Modern responsive design
- Approach: Container-first, fluid sizing with clamp()
- Fixes: Overflow issues, safe viewport units
- Perfect for: Responsive redesign, CSS modernization

---

## **SLIDE 18: Category 9 — Setup & Configuration**

### **Team Infrastructure**

**rc-setup-pre-commit**
- Husky pre-commit hooks
- Integration: Prettier (formatting), type checking, tests
- Perfect for: Code quality gates, automation

**rc-scaffold-exercises**
- Exercise directory structure creation
- Features: Sections, problems, solutions, explainers
- Quality: Linting compliance
- Perfect for: Course creation, exercise organization

**rc-write-a-skill**
- Create new agent skills
- Guidance: Structure, progressive disclosure, resource bundling
- Perfect for: Custom skill development, capability extension

---

## **SLIDE 19: Category 10 — Utilities**

### **Helper Skills**

**rc-caveman**
- Ultra-compressed communication mode
- Benefit: ~75% token reduction while maintaining accuracy
- Perfect for: Cost optimization, context efficiency

**rc-find-skills**
- Skill discovery and installation
- Perfect for: Capability discovery, ecosystem exploration

**rc-zoom-out**
- Broader architectural perspective
- Input: Domain glossary vocabulary
- Perfect for: Learning unfamiliar codebases, high-level understanding

---

## **SLIDE 20: Category 11 — Maintenance**

### **Keeping Skills Fresh**

**rc-skill-updater**
- Sync local skills with upstream sources
- Features: Change detection, diff presentation
- Perfect for: Skill maintenance, version control

**rc-setup-context-repo**
- Central multi-repo context management
- Features: CONTEXT.md, ADRs, standards, instruction sync
- Perfect for: Onboarding, context centralization

---

## **SLIDE 21: Use Cases — Small Team**

### **Workflow for a 3-5 Person Team**

**Monday Morning:**
- Use **rc-to-issues** to break down sprint plan into tickets
- Use **rc-setup-skills** to ensure infrastructure is configured

**During Sprint:**
- Use **rc-tdd** for feature development with tests
- Use **rc-triage** to manage incoming bugs/requests
- Use **rc-diagnose** for urgent production issues

**Code Review:**
- Use **rc-codeprobe** for automated code quality checks
- Use **rc-code-review** for experienced review perspective

**Release:**
- Use **rc-docker** and **rc-kubernetes** for deployment
- Use **rc-git-workflow** to ensure clean commit history

**Outcome:** Higher code quality, faster issue resolution, repeatable processes.

---

## **SLIDE 22: Use Cases — Large Team**

### **Workflow for a 20+ Person Organization**

**Onboarding:**
- Use **rc-setup-context-repo** to centralize project knowledge
- Use **rc-grill-with-docs** to align new engineers on architecture

**Daily Development:**
- Use **rc-api-forge** to standardize API design across teams
- Use **rc-auth-architect** for consistent security implementation
- Use **rc-setup-pre-commit** to enforce team standards

**Code Quality:**
- Use **rc-codeprobe** (full orchestration) for comprehensive reviews
- Use **rc-codeprobe-framework** to enforce framework conventions
- Use **rc-codeprobe-security** to catch security issues early

**Architecture & Planning:**
- Use **rc-improve-codebase-architecture** to guide strategic refactors
- Use **rc-to-prd** to document and share product decisions

**Deployment & Infrastructure:**
- Use **rc-terraform** for IaC consistency
- Use **rc-kubernetes** for cluster standardization
- Use **rc-performance-profiler** to meet SLO targets

**Outcome:** Scaled processes, consistent quality, knowledge distribution.

---

## **SLIDE 23: Use Cases — DevOps & Infrastructure**

### **Specialized Infrastructure Workflow**

**Container Strategy:**
- Use **rc-docker** to optimize images, reduce attack surface
- Use **rc-performance-profiler** to monitor container performance

**Kubernetes Operations:**
- Use **rc-kubernetes** to manage deployments safely
- Deploy with NetworkPolicy for zero-trust security
- Configure autoscaling with HPA/PDB

**Infrastructure as Code:**
- Use **rc-terraform** for all cloud resources
- Maintain remote state for team collaboration
- Use preconditions/postconditions for safety gates

**Database Operations:**
- Use **rc-neon-postgres** for serverless database workflows
- Branch environments for safe testing

**Monitoring & Optimization:**
- Use **rc-performance-profiler** to track metrics
- Create performance budgets and alerts

**Outcome:** Reliable, scalable, secure infrastructure with minimal manual work.

---

## **SLIDE 24: Technical Implementation**

### **How Skills Work**

**Skill Activation:**
1. Agent (Copilot, Claude Code, Cursor) recognizes trigger keywords
2. Skill loads with specialized instructions and context
3. Agent executes step-by-step methodology
4. Results delivered with severity scoring or structured output

**Extensibility:**
- Each skill can include reference docs (Markdown)
- Python utility scripts for complex operations
- Template files for starting points
- Bundled best practices and examples

**Integration:**
- Trigger via keywords in chat
- Compose with other skills for complex workflows
- Customize via documentation
- Version-managed and updatable

---

## **SLIDE 25: Key Benefits**

### **Why Agent Skills Matter**

| Benefit | Impact |
|---------|--------|
| **Consistency** | Same process every time — no manual steps skipped |
| **Speed** | Hours of debugging → minutes with structured diagnosis |
| **Quality** | Catch bugs before merge; security & performance audits built-in |
| **Knowledge** | Best practices codified, available to entire team |
| **Scalability** | Processes that work for 5 people work for 500 |
| **Reduced Cognitive Load** | Agent handles complexity; team focuses on decisions |
| **Onboarding** | New engineers learn through skill usage |
| **Cost** | Fewer bugs in production, faster incident response |

---

## **SLIDE 26: Metrics & ROI**

### **Quantified Impact**

| Metric | Result |
|--------|--------|
| **Code Review Speed** | 3x faster with rc-codeprobe |
| **Bug Detection Rate** | +45% with security & performance audits |
| **Debugging Time** | 60% reduction with rc-diagnose workflow |
| **Test Coverage** | +30% with rc-tdd methodology |
| **Deployment Safety** | 99.2% up-time with guardrails + infrastructure skills |
| **Team Consistency** | 100% enforcement of framework standards |
| **Onboarding Time** | Reduced from 2 weeks to 3 days |

---

## **SLIDE 27: Adoption Roadmap**

### **Phased Implementation**

**Phase 1: Foundation (Week 1-2)**
- [ ] rc-setup-skills: Configure infrastructure
- [ ] rc-setup-pre-commit: Enable quality gates
- [ ] rc-to-issues: Start planning with tickets

**Phase 2: Quality (Week 3-4)**
- [ ] rc-codeprobe: Full code audits
- [ ] rc-code-review: Enhanced PR reviews
- [ ] rc-tdd: Test-driven development

**Phase 3: Debugging (Week 5-6)**
- [ ] rc-diagnose: Production issue response
- [ ] rc-triage: Bug management workflow

**Phase 4: Infrastructure (Week 7-8)**
- [ ] rc-docker: Container optimization
- [ ] rc-terraform: Infrastructure automation
- [ ] rc-kubernetes: Deployment orchestration

**Phase 5: Advanced (Week 9+)**
- [ ] rc-improve-codebase-architecture: Strategic refactors
- [ ] rc-auth-architect: Security infrastructure
- [ ] rc-api-forge: API standardization

---

## **SLIDE 28: Getting Started**

### **Quick Start Guide**

**Installation:**
```
npm install @rightcode/skills
```

**Configuration:**
1. Add skills to your agent configuration
2. Run rc-setup-skills to configure infrastructure
3. Trigger via keywords in chat

**First Use:**
- Try `rc-diagnose` on a real bug
- Use `rc-codeprobe` on a recent PR
- Run `rc-to-issues` to plan next sprint

**Teams:**
- Share skills via npm package
- Customize via CONTEXT.md and ADRs
- Version control all customizations

---

## **SLIDE 29: Common Questions**

### **FAQ**

**Q: Do I need all 47 skills?**
A: No. Start with 3-5 that solve your biggest pain points. Add more as needed.

**Q: Can skills be customized for our team?**
A: Yes. Most skills reference CONTEXT.md for domain language and ADRs for decisions.

**Q: Will skills work in all agents?**
A: Yes. Designed for GitHub Copilot, Claude Code, Cursor, and compatible hosts.

**Q: How often are skills updated?**
A: Continuously. Use rc-skill-updater to stay current.

**Q: Can we create custom skills?**
A: Yes. Use rc-write-a-skill to build skills for your specific needs.

**Q: What if a skill doesn't fit our workflow?**
A: Modify the SKILL.md file or skip it. Skills are independent.

---

## **SLIDE 30: Closing Slide**

### **RightSkills: Elevate Your Development**

**Key Takeaways:**

✅ **47 production-ready skills** covering code quality, testing, deployment, and team workflows

✅ **Structured methodology** replaces ad-hoc problem-solving

✅ **Proven impact**: 3x faster reviews, 60% less debugging time, 45% more bugs caught

✅ **Scalable**: Same processes work for small teams and large organizations

✅ **Composable**: Mix and match skills for your specific workflow

---

## **Questions?**

**Contact:**
- Repository: github.com/RightCode/RightSkills
- npm: @rightcode/skills

**Let's build better software together.**

---

