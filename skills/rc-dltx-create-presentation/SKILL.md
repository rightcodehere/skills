---
name: rc-dltx-create-presentation
display_name: Build a DLTX Corporate Deck like an In-House Brand Designer
description: "Build a corporate deck the way an in-house brand designer actually builds one — cobalt-blue typographic system, two cover variants, four section dividers, and a full set of content layouts (numbered agenda, vertical flow, three-column problem-to-solution, icon cards, case study, comparison table, gantt schedule). Bilingual EN/JP. Logo and wordmark are swappable so the same skeleton can carry another corporate brand."
metadata:
  short-description: One cobalt-blue typographic skeleton — swap the logo, keep the rhythm.
lang: en-US
category: enterprise-strategy
previews:
  - previews/01-cover-light.png
  - previews/02-cover-blue.png
  - previews/05-agenda-numbered.png
  - previews/07-three-column.png
  - previews/08-icon-cards.png
  - previews/10-comparison-table.png
  - previews/11-schedule-gantt.png
  - previews/12-divider-cobalt.png
thumbnails:
  - thumbnails/01-cover-light.png
  - thumbnails/02-cover-blue.png
  - thumbnails/05-agenda-numbered.png
  - thumbnails/07-three-column.png
  - thumbnails/08-icon-cards.png
  - thumbnails/10-comparison-table.png
  - thumbnails/11-schedule-gantt.png
  - thumbnails/12-divider-cobalt.png
tags:
  - template
  - corporate
  - bilingual
canvas:
  width: 1280
  height: 720
---

# Build a DLTX Corporate Deck like an In-House Brand Designer

> One cobalt-blue typographic skeleton — swap the logo, keep the rhythm.

## Why this skill works

- **The chrome is the brand.** A 2px cobalt rule under the chapter title, a logo glyph at top-right, and a quiet bottom-right page number repeat on every slide — the audience reads "this is one document" before they read a single word.
- **A reader scanning the deck in 30 seconds can tell where each section starts** — full-bleed cobalt / sky / blue / navy dividers reset the eye between chapters, and color depth signals chapter weight without a TOC.
- **You bring an outline and a wordmark; the skill brings the type scale, palette, and 11 production-ready content layouts** — no Figma trip, no "I'll fix the spacing in v2."

## Methodology cheat-sheet

**Chrome-as-Brand** — every slide carries the same three chrome elements (top-right logo, cobalt rule under the title, bottom-right page number) so the typographic system, not a logo decal, is what makes the deck feel branded.[^1]

The skill bundles the full visual system extracted from the source DLTX PowerPoint template — palette, type scale, chrome geometry — into a single `chrome.css` linked from every slide. To rebrand for another company, the user replaces only `assets/logo.png` and adjusts the four CSS variables `--color-cobalt / --color-blue / --color-sky / --color-navy`; the 15 layouts inherit the change automatically.[^2]

Layouts cluster into three families, each with a fixed visual rhythm:

1. **Covers (×2)** — light cover for internal / status decks, blue cover for client-facing / launch decks.
2. **Section dividers (×4)** — cobalt / sky / blue / navy. Use depth to signal chapter weight (cobalt = primary, navy = closing, sky = supporting).
3. **Content layouts (×9)** — chapter shells (blank, accent), numbered agenda, vertical flow with arrows, three-column problem-to-solution, three-image cards, case-study stacked rows, A/B comparison table, gantt schedule.

## Before / After

### Cover slide

> **Typical PPT template**
> ![Generic title slide]
> "Presentation Title"
> "by Author Name | Date"
> Centered, navy serif on grey gradient.

> **This skill's rewrite**
> Title-locked at left, 46pt Arial Bold in cobalt `#1746FF`, set against a white page with a thin geometric blue band at the bottom edge and the DLTX glyph parked top-right. Date and company line are 18pt black, left-aligned beneath the title — the same column the next 14 slides will continue.

### Section divider

> **Typical PPT template**
> Full-bleed photograph + centered white "Section 02 — Implementation" serif title with a thin underline rule.

> **This skill's rewrite**
> Full-bleed brand cobalt (no photo). "Section Title" set 64pt Arial Bold white, anchored bottom-left. Three other divider variants (sky, blue, navy) signal chapter weight by color depth — same geometry, four moods.

## What this skill produces

- 15 HTML slides on a **1280 × 720** canvas (16:9).
- Two cover variants, four section dividers, nine content layouts.
- Shared design system in `assets/chrome.css` (cobalt-blue palette, Arial-stack type scale, fixed geometry).
- Swappable `assets/logo.png` — replace the file (any width, ≤ 360 × 140 px) to rebrand the entire deck.
- Bilingual-ready: copy is in English by default; Japanese text renders correctly thanks to the Hiragino Sans / Yu Gothic / Meiryo font fallback stack in `chrome.css`.

## Sources

[^1]: Daiichi Life Techno Cross PowerPoint template (`DLTX_PPT_Format_EN.potx`) — official internal corporate template, 15 slides, 1280×720, 2025 edition. Source of all geometry, palette, and chrome conventions captured by this skill.
[^2]: `chrome.css` in the bundled `dltx-template.slides/assets/` directory — single source of truth for palette (`--color-cobalt #1746FF`, `--color-sky #3FC3F5`, `--color-blue #0099FF`, `--color-navy #000080`) and type scale (cover 46pt, chapter 28pt, section 48pt, body 16pt).
