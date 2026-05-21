---
name: rc-responsive-engine
description: Designs responsive interfaces using container-first layouts, fluid sizing with clamp, and safe mobile viewport units. Use when users ask to make UIs responsive across mobile, tablet, and desktop, remove overflow bugs, or modernize breakpoint-heavy CSS.
---

# Responsive Engine

Create responsive layouts that adapt cleanly across device sizes and input modes.

## When to Use This Skill

Use this skill when the user asks to:

- Make a page or component responsive
- Remove horizontal overflow on mobile
- Replace brittle breakpoint stacks
- Use container queries and fluid sizing
- Fix viewport-height behavior on mobile browsers

Do not use this skill for detailed visual brand direction.

## Core Principle

Prefer container-driven responsiveness for components.
Use media queries for global layout shifts and form-factor behavior.

## Workflow

### Step 1: Audit current behavior

Test at 320, 375, 768, 1024, and 1440 widths.
Log overflow, tiny touch targets, and unreadable typography.

### Step 2: Convert components to container queries

```css
.card-list {
  container-type: inline-size;
}

@container (min-width: 640px) {
  .card {
    grid-template-columns: 180px 1fr;
  }
}
```

### Step 3: Replace fixed units with fluid tokens

- Use clamp for text and spacing
- Prefer percentages and logical units
- Avoid px-only responsive math

### Step 4: Use safe viewport units

- Prefer min-height: 100dvh over 100vh for full-screen sections
- Keep svh/lvh fallbacks where needed

### Step 5: Add input-mode guards

- Gate hover interactions with @media (hover: hover)
- Expand touch targets for coarse pointers

## Anti-patterns

- Using media queries for every component variant
- Keeping h-screen or 100vh in mobile-critical views
- Hover-only behavior on touch devices
- Hardcoded pixel widths that force overflow

## Production Checklist

- [ ] No horizontal overflow at 320px
- [ ] Body text stays readable
- [ ] Touch targets are at least 44x44
- [ ] Component responsiveness uses container queries
- [ ] Full-height views use 100dvh-safe patterns

## Sources

- MDN docs on container queries and viewport units
- Responsive design best practices from web platform docs
