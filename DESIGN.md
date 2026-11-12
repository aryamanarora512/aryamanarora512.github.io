# Design contract — Aryaman Arora portfolio

Source: github.com/funboy322/avoid-ai-design (catalog of "AI tells"), plus our own rules. Where they disagree, what Aryaman chose wins.

## Direction
Dark, quiet, editorial-simple. One structural idea: the page is the work. Name, two lines, links, then straight into the experience. The only decoration is the field of interest icons behind it.

## Color (60 / 30 / 10)
- Ground `#08090c` (60) · ink `#f3f5f8`, secondary `#b7bec9`, muted `#7c8490` (30). Every text color is ≥ 4.5:1 on the ground.
- One accent `#5b8def` (10), derived from Duke blue. It has a job: hover, focus, pressed state, and the icons the cursor lights up. Nothing else is colored.
- No gradients, no glows, no gradient text, no colored shadows.

## Type
- Apple system font (SF Pro / SF Mono) — Aryaman's explicit choice. The catalog flags system fonts as a default, so the type is made distinct by scale and weight, not by a face: name 600 weight, very tight tracking; everything else regular/medium.
- Headlines say something specific. No taglines, no slogans.
- All headlines `text-wrap: balance`; paragraphs `text-wrap: pretty`. No orphans, no widow words.
- Sentence case. No all-caps eyebrows, no mono labels for decoration, no `A · B · C` meta strings, no arrows on links.

## Shape
- Inner radius = outer radius − padding (floored at 0). Tokens: `--r-card: 8px`, `--pad-card`. Image sits flush in its card, so it takes the full 8px; anything padded inside a container uses `calc(var(--r-card) - var(--pad-card))`.
- One surface level only. No cards inside cards, no left/top accent stripes, no icon chips.

## Motion
- One staggered entrance on page load (header only), ease-out, no overshoot. No reveal-on-scroll.
- Hover/focus transitions 200 ms ease-out. `prefers-reduced-motion` turns the entrance off.

## States
Every interactive element has hover, `:focus-visible` (2px accent outline), `:active`.

## Don't
Pill badges, status dots that pulse, sparkle icons, fake stat strips, centered hero template, three identical icon cards, glassmorphism, placeholder avatars/stock faces.
