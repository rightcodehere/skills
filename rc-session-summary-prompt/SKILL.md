---
name: rc-session-summary-prompt
description: 'Generate a clean-session handoff prompt from the current conversation. Use for summarize session, handoff prompt, continue in new chat, restart clean session, compact context, or carry work to a fresh conversation.'
argument-hint: 'Optional focus, such as backend, frontend, deployment, or debugging'
user-invocable: true
disable-model-invocation: false
---

# Session Summary Prompt

Use this skill when the user wants a ready-to-paste prompt that can start a new clean conversation without losing important working context.

## Goal
Produce a compact but complete handoff prompt based only on the current conversation and any directly relevant workspace facts already established.

## Output Rules
- Output a single ready-to-paste prompt.
- Prefer plain text or short markdown.
- Keep it concise but preserve actionable context.
- Do not include internal chain-of-thought.
- Do not include tool call transcripts unless the user explicitly asks for them.
- Include only facts that are established in the current session.
- If something is uncertain, label it as unverified.

## Required Sections
1. Objective
2. What was completed
3. Current verified state
4. Files or components touched
5. Outstanding issue or next task
6. Constraints, assumptions, or environment details
7. Immediate next step for the new session

## Procedure
1. Identify the current user goal and the most recent active problem.
2. Summarize concrete fixes, deployments, validations, and decisions already made.
3. List the exact files, services, or subsystems that matter for continuation.
4. Capture verified runtime facts, especially endpoints, deployment state, and test results.
5. End with a direct instruction the next session can act on immediately.

## Output Template
Use this structure:

```text
Continue from this session.

Objective:
[brief goal]

Completed:
- [completed item]
- [completed item]

Current verified state:
- [verified fact]
- [verified fact]

Relevant files and components:
- [file or service]: [why it matters]
- [file or service]: [why it matters]

Outstanding issue:
- [current blocker or remaining work]

Constraints and environment:
- [constraint]
- [environment detail]

Immediate next step:
[the first concrete thing to do in the new session]
```

## Optional Focus
If the user provides a focus area, bias the summary toward that area while still preserving any critical cross-cutting context.
