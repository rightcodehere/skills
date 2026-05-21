---
name: rc-component-forge
description: Builds production-grade UI components for React, Vue, and Svelte with typed props, complete state handling, accessibility, and testability. Use when users ask to create or refactor reusable components, define component APIs, or harden UI behavior across loading, empty, error, and success states.
---

# Component Forge

Build reusable UI components that survive real product conditions.

## When to Use This Skill

Use this skill when the user asks to:

- Build a new reusable component
- Refactor an existing component API
- Add loading, empty, error, and success states
- Improve accessibility and keyboard support
- Add component tests or harden edge-case behavior

Do not use this skill for full page layout strategy or global app architecture.

## Workflow

### Step 1: Classify component type

| Type | Purpose | Example |
| --- | --- | --- |
| Presentational | Pure rendering from props | Button, Badge, Card |
| Composed | Wraps children with interaction | Modal, Tooltip, Tabs |
| Data-bound | Fetches/displays remote data | UserProfile, OrderList |
| Form | Input and validation behavior | LoginForm, SearchBox |

### Step 2: Define a stable component contract

- Use explicit typed props
- Prefer named exports
- Keep one component per file
- Keep side effects outside render path

### Step 3: Cover mandatory states

Every data-bound component should define and render:

- idle
- loading
- empty
- error
- success

### Step 4: Accessibility baseline

- Keyboard reachable interactive controls
- Role and aria labels for non-text controls
- Focus trapping for dialogs
- role="status" for loading and role="alert" for errors
- Touch targets at least 44x44

### Step 5: Edge-case hardening

- Long text and overflow behavior
- Retry and cancellation flows
- Race-safe re-fetch behavior
- Null, undefined, and empty collection handling

## Reference pattern

```tsx
type LoadState<T> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "empty" }
  | { status: "error"; error: Error }
  | { status: "success"; data: T };
```

## Anti-patterns

- Default exports for shared component libraries
- Components with hidden side effects
- Missing loading or error states
- Accessibility added only after feature completion
- Components that exceed a single, clear responsibility

## Production Checklist

- [ ] Typed props and stable API
- [ ] Required states implemented
- [ ] Accessibility checks complete
- [ ] Tests cover critical behavior
- [ ] Edge cases validated

## Sources

- Inclusive Components patterns
- React, Vue, and Svelte official guidance
- WCAG 2.2 accessibility guidance
