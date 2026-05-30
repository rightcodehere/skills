---
name: rc-design
description: Produces structured brand and design-system guidance, including token architecture, typography scales, accessibility checks, and design brief scaffolding. Use when users ask for brand direction, design-system setup, creative direction, or production-ready design documentation.
---

# Design

Build consistent brand and system-level design decisions that can be executed by engineering.

## When to Use This Skill

Use this skill when the user asks to:

- Define a brand direction or style system
- Create tokenized color, typography, spacing, and motion primitives
- Draft a design brief or creative direction framework
- Audit consistency and accessibility in a design system

Do not use this skill for low-level component implementation details.

## Workflow

### Step 1: Gather constraints

- Audience and positioning
- Platform constraints
- Accessibility targets
- Delivery channels and timeline

### Step 2: Define brand strategy

- Positioning statement
- Voice and tone guardrails
- Visual principles (3 to 5)

### Step 3: Build token system

Include at minimum:

- color
- typography
- spacing
- radius
- elevation
- motion

### Step 4: Validate accessibility

- WCAG AA contrast thresholds
- Semantic color roles
- Typography legibility at body sizes

### Step 5: Prepare implementation handoff

- Token map for code
- Component usage guidance
- Anti-pattern list

## Token example

```json
{
  "color": {
    "primary": { "$value": "#1B365D", "$type": "color" },
    "accent": { "$value": "#F5BD47", "$type": "color" }
  },
  "spacing": {
    "sm": { "$value": "8px", "$type": "dimension" },
    "md": { "$value": "16px", "$type": "dimension" }
  }
}
```

## Anti-patterns

- Briefs without measurable success criteria
- Inconsistent tokens between design and code
- Color systems without semantic usage rules
- Design decisions not documented for handoff

## Production Checklist

- [ ] Brief includes problem, scope, constraints, and success metrics
- [ ] Tokens are documented and exportable
- [ ] Accessibility checks passed
- [ ] Handoff guidance maps design to code

## Sources

- Design system and brand governance best practices
- W3C design token format
- WCAG 2.2 accessibility guidance
