# Agent runtime brief — dltx-corporate-template

This file is for the agent only. The user never sees it. Read it before authoring any slide for this skill.

## Core principle

The visual identity lives in `dltx-template.slides/assets/chrome.css` and in the three persistent chrome elements (top-right logo, 2px cobalt rule under the chapter title, bottom-right page number). On every new slide you author, link `chrome.css` and reproduce those chrome elements with the exact geometry recorded in the bundled templates — that consistency is what makes the deck feel branded. Do not redesign the chrome per slide.

## Context the agent must establish before generating

> Before producing the deck, the agent must know each item below.
> - If the user's prior messages already supply an item, use it; do NOT re-ask.
> - If an item can be reasonably inferred from the user's stated topic, infer it and state the assumption inline on slide 2.
> - Ask only what is missing AND cannot be inferred — one targeted question at a time, not a script.

1. **Deck topic and outline** — drives slide selection from the layout library; without a topic, the agent cannot decide which content layouts (numbered agenda vs. flow vs. comparison vs. gantt) to use.
2. **Brand to apply** — default is DLTX (logo at `assets/logo.png`). If the user names another company, ask whether they will supply a replacement logo PNG; if not, render the wordmark as text in the top-right corner using the same `181 × 69 px` slot.
3. **Language of the slide copy** — English / Japanese / mixed. The Arial-stack font stack in `chrome.css` already includes `Hiragino Sans, Yu Gothic, Meiryo` for CJK fallback, but the agent should still pick one primary language for headings to keep the type rhythm uniform.
4. **Cover variant preference** — light (internal / status) or blue (external / launch). Default: light.

## Mandatory checks (during generation)

- Every content slide (chapter-shell, agenda, flow, three-column, icon cards, case study, comparison, gantt) MUST include all three chrome elements with the exact source geometry: logo at `left:1063px; top:25px; width:181px; height:69px`, horizontal cobalt rule at `left:35px; top:107px; width:1209px; height:2px`, page number bottom-right at `left:1205px; top:673px` (or `top:625px` when the bottom band is present, or `top:697px` on the comparison table whose grid extends lower).
- Chapter title text colour is BLACK (`var(--color-ink)`), 28pt bold, NOT cobalt — the rule below it carries the brand. Cobalt titles are reserved for the cover slide.
- Section dividers carry NO chrome (no logo, no rule, no page number) — they are full-bleed colour fields with one centred-left "Section Title" string.
- Cover slides carry the logo (top-right on light, top-left on blue) but no rule and no page number — that's the source convention.
- For new content slides, copy the closest bundled layout (e.g. `05-agenda-numbered.html` for a 3-7-row agenda) and replace the text — do NOT author the chrome from scratch.
- Polarity rule: on white / sky / light backgrounds, text is `var(--color-ink)` black. On cobalt / blue / navy section dividers, text is `#FFFFFF` white. Never invisible-on-bg.
- Never alter `chrome.css` palette values when authoring a new content slide — if the user needs a custom brand colour, override the four cobalt/blue/sky/navy CSS variables ONCE in a new `:root` override at the top of `chrome.css`, do not hard-code hex colours inside individual slides.

## Template selection

Default deck shape when the user gives only a topic + slide count:

| Slide count requested | Default playlist |
|-----------------------|------------------|
| 3-5 (short)           | `01-cover-light` → 1× content (closest match) → `09-case-study` or `10-comparison-table` → `15-divider-navy` (closing) |
| 6-9 (standard)        | `01-cover-light` → `05-agenda-numbered` → `12-divider-cobalt` → 3× content → `15-divider-navy` |
| 10-15 (full)          | the full bundled playlist as-is, with content layouts reshuffled to the user's outline |

If the user specifies "client-facing / launch / external", swap `01-cover-light` for `02-cover-blue`.

## Use the bundled deck as a starting point

The skill ships a complete 15-slide reference deck at `dltx-template.slides/`. Treat it as the canonical implementation. For every new deck:

1. Copy `dltx-template.slides/` to `<user-deck-name>.slides/`.
2. Edit `manifest.json` — set the new title, prune the playlist down to what the user actually needs.
3. Delete unused slide HTML files from `slides/`.
4. Edit the remaining slides in place — replace placeholder copy ("Presentation Title", "Chapter Title", "Text goes here.", "Title", "Design Format", "Comparison Criteria 1", etc.) with the user's content. Keep ALL chrome elements and ALL geometry untouched.
5. If the brand is NOT DLTX, replace `assets/logo.png` with the user-supplied PNG (any width up to 360 px, height up to 140 px — the `<img>` tags use `object-fit: contain`).

## Recommended 15-slide structure

| # | Page | Purpose |
|---|------|---------|
| 1  | `01-cover-light.html`         | Internal/status cover — title in cobalt on white with a thin geometric blue band at the bottom. |
| 2  | `02-cover-blue.html`          | External/launch cover — title in white on a cobalt + sky shape composition. |
| 3  | `03-chapter-blank.html`       | Empty chapter shell — black title, cobalt rule. Use as the base layout for any content slide not covered by 5-11. |
| 4  | `04-chapter-accent.html`      | Same as 3, plus a thin decorative blue band at the bottom. Use for the first slide of a major section. |
| 5  | `05-agenda-numbered.html`     | 5-row numbered list (01-05) with title + sub-label + duration. Use for the agenda / table of contents. |
| 6  | `06-agenda-flow.html`         | Vertical "Past → Future" flow: 3 stacked tiles (sky → blue → cobalt) connected by downward arrows. |
| 7  | `07-three-column.html`        | Horizontal "Problem → Solution" flow: 3 cards connected by right-pointing arrows. Use for cause-effect, before/after-with-middle, or step-by-step transformations. |
| 8  | `08-icon-cards.html`          | 3 image/icon cards with cobalt title bar. Use for case-study summaries or product lineup. |
| 9  | `09-case-study.html`          | 3 stacked grey rows, each labelled "Case Study 1/2/3" in cobalt. Use for narrative case studies that need 2-3 lines of body each. |
| 10 | `10-comparison-table.html`    | A/B comparison table with 3 criteria rows. Symbols (○ △ ✕) signal verdict per row. |
| 11 | `11-schedule-gantt.html`      | 12-month gantt with 6 task rows. Use for project plans. |
| 12 | `12-divider-cobalt.html`      | Section divider — primary cobalt (use for the most important chapter). |
| 13 | `13-divider-sky.html`         | Section divider — light sky (use for supporting / context chapters). |
| 14 | `14-divider-blue.html`        | Section divider — mid blue (use for middle chapters). |
| 15 | `15-divider-navy.html`        | Section divider — dark navy (use for closing / appendix / Q&A). |
