# Aerarium Revamp Implementation Plan

> **For agentic workers:** Work one phase at a time. Stop after each phase and wait for Liam's review on `python3 -m http.server 8080`. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reskin the AgentVault landing page into the approved Aerarium visual system (`docs/revamp/REVAMP_SPEC.md`) without changing verified copy, beyond the section 8 copy changes.

**Architecture:** Same static page: `index.html`, `styles.css`, `script.js`, self-hosted fonts, no build step. New: pre-rendered ASCII JSON in `assets/ascii/` loaded by a small loader in `script.js`; all colour and type flow from `--av-*` custom properties on `:root`. The existing section ids, the hero scenario engine, section reveal and the diagram SVG geometry stay.

**Tech stack:** HTML, CSS, vanilla JS. Python standard library for `tests/validate_site.py`. Playwright (already in `node_modules`) for screenshots only, from a scratch script that is not committed.

**Branch:** `aerarium-revamp`. Plain imperative commit subjects. Never push.

**Update 2026-09-25:** Liam asked for no commits until all phases are done. The per-phase commit lines below are the intended subjects, held until then.

---

## Global constraints

- **Copy is locked.** Only the section 8 changes. Anything else that seems to need new words goes to Liam first (see Open questions).
- **Tests first.** Each phase starts by extending `tests/validate_site.py` so it fails, then builds until it passes. No existing check is deleted or loosened. The one spec-authorised change to existing checks (scoping the diagram counts to the desktop SVG, Phase 3) keeps each check's condition identical and only narrows the string it reads.
- **Diagram geometry is frozen.** No change to any coordinate, `points`, `x1/y1/x2/y2`, `width/height`, `stroke-dasharray`, node class or text content. Colour and font presentation attributes move to CSS (needed for the cyan-hex ban); classes may be added to `<text>`.
- **Script data is frozen.** The `SCENARIOS` array and cycler timings in `script.js` are not edited. Phase 2 adds a hash guard for this.
- **No third-party requests.** No CDN, no Google Fonts.
- **Reference defects are not copied.** The reference PNGs contain three layout bugs that contradict the spec. I will match the spec, not the bug:
  1. `mobile-01`: the Owner monitor overflows into the caption and proof bar.
  2. `mobile-10`: the AERARIUM plate sits on top of the ASCII temple (spec: never put text on the art).
  3. `desktop-01`: proof-bar items wrap (spec: `white-space: nowrap`).

## Self-check before every report

A scratch Playwright script (kept in the session scratchpad, not committed) captures:

- 1440px and 390px (2x), full page and per section, `reducedMotion: 'reduce'` and `'no-preference'`.
- Side-by-side composites against the matching `docs/revamp/reference/*.png`.
- `document.documentElement.scrollWidth <= innerWidth` at 390px (no horizontal scroll).
- Console errors and failed requests (must be none, and no non-localhost requests).

Plus `python3 tests/validate_site.py`, `node --check script.js`, `git diff --check`.

---

## Phase 1: Foundations

Tokens, fonts, base type, header, section heading component, plate, buttons, old aesthetic removed, test scaffolding. The page renders in the new palette end to end; hero art and section layouts land in later phases.

**Files:**
- Add (from `aerarium-revamp-package/`, copied as-is): `docs/revamp/**`, `assets/ascii/*.json`, `assets/fonts/cormorant-garamond-*.woff2`, `assets/fonts/OFL-cormorant-garamond.txt`, `tools/ascii/**`
- Modify: `assets/fonts/fonts.css` (append the two Cormorant `@font-face` blocks from the package)
- Add: `tests/fixtures/copy-baseline.txt`
- Modify: `tests/validate_site.py`, `index.html`, `styles.css`, `script.js`
- Delete: `assets/ascii-vault.txt`

### Tests (write first, confirm FAIL)

- [x] **Required files:** `assets/fonts/cormorant-garamond-variable.woff2`, `assets/fonts/cormorant-garamond-italic-variable.woff2`, `assets/fonts/OFL-cormorant-garamond.txt`, `assets/ascii/temple-hero.json`, `ring-key.json`, `coin.json`, `temple-wide.json`, `docs/revamp/REVAMP_SPEC.md`, `tools/ascii/README.md`.
- [x] **ASCII JSON shape:** each file parses, has `rows`, `cols`, `layers.hi`, `layers.lo`, `layers.dg`, and each layer has exactly `rows` lines of at most `cols` characters. Grids match spec section 5 (220×125, 130×66, 120×66, 330×104).
- [x] **Tokens:** `styles.css` defines all fourteen `--av-*` tokens from spec section 3 with their exact values (case-insensitive hex match; `--av-line` as `rgba(176,141,87,0.26)` with optional spaces).
- [x] **Fonts:** `fonts.css` declares `"Cormorant Garamond"` normal and italic; `styles.css` uses it.
- [x] **Forbidden, anywhere in `index.html` / `styles.css` / `script.js` / `fonts.css`:** `#9bb9bb`, `#7a9294` (case-insensitive), `fonts.googleapis.com`, `ascii-vault.txt`, `void-scan`, `ascii-field`, `setVaultState`. File `assets/ascii-vault.txt` must not exist.
- [x] **Text wordmark:** the `.wordmark` element contains the text `AgentVault` (uppercased in CSS) and no `<img`. `assets/images/agentvault-wordmark.png` stays in `REQUIRED_FILES`.
- [x] **Section numerals:** `#problem` … `#roadmap` each carry an outlined numeral element with I, II, III, IV, V, VI, VII in order, plus labels Problem, Mechanism, Rules, Record, Run, Delta, Roadmap. Old indexes `01 / Problem` … `07 / Roadmap` forbidden (the roadmap's own `01 / Hosting`, `02 / Pricing` are untouched).
- [x] **Component hooks exist in CSS:** `.plate`, `.btn-primary`, `.btn-secondary`, `.section-numeral`.
- [x] **Content-lock guard (new):** `tests/fixtures/copy-baseline.txt` holds every visible text node of today's `index.html` (captured once, before any edit, whitespace-normalised). The test asserts each baseline line still appears in the new page's normalised visible text. An explicit, commented allowlist covers only the section 8 removals (old section indexes; the old rules hint, added in Phase 3). This makes "content is locked" machine-checked for every later phase.

### Build

- [x] Copy package files into place; append Cormorant `@font-face` to `fonts.css`.
- [x] `:root` tokens; replace every old colour in `styles.css` with `--av-*`; delete old tokens (`--teal`, `--teal-muted`, `--blue`, etc.).
- [x] Base type: body Space Grotesk 17/1.62 (16 mobile) in `--av-muted`; H1/H2/H3 Cormorant per the type table; label and inscriptional-caps utility classes; `◆` separator utility.
- [x] Layout: 1296px content width, 72px gutters (24px mobile); section padding 120px / ~72px; square corners.
- [x] Header: text wordmark (Cormorant 600, 24px/19px, tracking 0.3em), five nav links (12px, uppercase, 0.2em), bottom hairline. Mobile: 44px menu button that toggles the same links (`aria-expanded`, `aria-controls`). Focus trap and Escape handling are finished in Phase 5.
- [x] Section heading component: outlined numeral (`-webkit-text-stroke: 1px var(--av-bronze)`, 120px / 56px) + label + H2, one baseline on desktop, stacked on mobile. Applied to all seven sections.
- [x] Plate component (CSS only; content arrives with each section's phase).
- [x] Buttons: 54px, square, primary bronze fill, secondary bronze border, 13px 600 uppercase 0.18em, hover opacity 0.82, 2px `--av-bronze-hi` focus ring at 3px offset. Global `:focus-visible` to match.
- [x] Remove: `.void-scan` element and CSS; ASCII vault `<pre>`, `.ascii-field` CSS, `setVaultState` and its calls; pixel wordmark `<img>`; `assets/ascii-vault.txt`; `crt-bloom` and other old-aesthetic keyframes.
- [x] Diagram SVG: remove only colour and `font-family` presentation attributes; add classes to `<text>` (`diagram-label`, `diagram-sub`, `diagram-edge-label`, `diagram-boundary-label`) and colour through CSS. Geometry untouched.
- [x] Bump the `styles.css?v=` cache-buster.

**Accept:** page renders in the Aerarium palette top to bottom at 1440 and 390; no cyan anywhere; tests pass.
**Commit:** `Add Aerarium tokens, typography and section headings`

---

## Phase 2: Hero and proof

ASCII loader and hero temple, floaters, restyled cycler with seal, proof bar.

### Tests (write first, confirm FAIL)

- [x] **Hero art container:** an element with `data-ascii="temple-hero"`, `aria-hidden="true"`, inline `--cols:220` and `--rows:125`, holding three `<pre>` layers in order `dg`, `lo`, `hi`.
- [x] **Loader:** `script.js` contains the relative `assets/ascii/` fetch path and an `IntersectionObserver`; CSS sizes `[data-ascii]` in `em` from `--cols`/`--rows` (checked by the presence of `calc(var(--cols) * 0.6em)`).
- [x] **Hero plate copy:** `AERARIUM`, `Temple of Saturn, Forum Romanum`, `The treasury of Rome sat inside this temple. Money left it only on authority.`
- [x] **Seal:** `SPECTAVIT` and `FCC · 114` in the `script.js` shell template and in the `<noscript>` fallback; the seal is `aria-hidden="true"`.
- [x] **Cycler data frozen:** SHA-256 of the `SCENARIOS` array literal in `script.js` equals the value captured from `main` before the revamp.
- [x] **Floaters:** CSS defines the floater keyframes and a reduced-motion rule for them; `script.js` generates them (no floater spans hard-coded in HTML).
- [x] **Mobile pane tabs removed** (spec: stack Agent and Owner on mobile): `mobile-pane-tabs` and `pane-tab` absent from HTML/CSS/JS.

### Build

- [x] ASCII loader in `script.js`: hero loads immediately; others lazily (rootMargin 600px); fills each `pre` via `textContent`; failures leave the reserved box.
- [x] Hero layout: 600px left column ~60px below header (eyebrow with 40px bronze rule, Flare logotype, label; H1 with italic bronze-hi second clause; lede; CTAs; ◆ line; plate). `temple-hero` right-anchored, 876px tall, `--ascii-size: clamp(3px, 0.486vw, 7px)`. Mobile: temple first, full width, bleeding right.
- [x] Floating glyphs: JS generates ~46 hero spans (about a third on mobile), random position, size, duration 7–15s, negative delays; static at 0.45 opacity under reduced motion.
- [x] Proof stage: stone frame, Agent left and Owner right with bronze divider (stacked on mobile, no overflow), rows arrive one by one (existing engine), Owner monitor and SPECTAVIT seal after the decline, caption Cormorant italic 23px centred, dots restyled. Shell template markup changes only; labels built from separate spans so the forbidden `agent · task` / `owner · monitor` strings never appear.
- [x] Proof bar: 96px `--av-panel` band, bronze borders, inner double hairline; lead sentence left; four declines in inscriptional caps with ◆ separators, `nowrap` per item; stacked list on mobile.

**Accept:** matches `desktop-01` / `mobile-01` (minus the overflow defect); no layout shift when the JSON lands (checked by measuring hero height before and after load); cycler behaviour unchanged.
**Commit:** `Add hero temple, ASCII loader and proof stage`

---

## Phase 3: Sections I to IV

Problem, mechanism (cards, restyled diagram with mobile variant, coin lane), rules tabs and diptych, record.

### Tests (write first, confirm FAIL)

- [x] **Diagram scoping (spec-directed):** give the desktop SVG `id="mechanism-diagram"`. The `>Vault</text>` count, `diagram-node--external` ×3 and `diagram-node--internal` ×2 checks read the slice of HTML for that element instead of the whole file. Conditions unchanged. Geometry string checks stay on the whole file.
- [x] **Mobile diagram:** a second SVG exists, uses only `diagram-v-*` class names (no `diagram-node--`), and its wrapper is hidden above 767px by CSS (`display: none`, which also removes it from the accessibility tree). Each wrapper carries `role="img"` and the existing label.
- [x] **Order:** in `#mechanism`, the step cards come before the diagram, the diagram before the coin lane.
- [x] **Coin lane strings:** `A payment, in motion · Approved`, `A payment, in motion · Declined`, `→ PAID`, `← DECLINED · the funds stay in the Vault`, `Vault`, `FCC checkpoint`, `Vendor`, `SPECTAVIT`, `FCC · VERIFIED`, `DECLINED`, `reason stays private`. Coin container `data-ascii="coin"`, `aria-hidden="true"`.
- [x] **Rules:** `role="tablist"` with exactly four `role="tab"` and four `role="tabpanel"`; exactly one panel without `hidden` and it is Rule 02; exactly one `aria-selected="true"`. `script.js` handles `ArrowLeft`, `ArrowRight`, `Home`, `End`. All existing rule phrases still required (unchanged). New: `Choose a rule to see what the Agent was told and what the Owner reads.`, `Agent view`, `Owner view`, `what the Agent is told`, `what the Owner reads`. Forbidden: `Hover or tap a card`, `rule-card`, `rule-turn`.
- [x] **Plates:** CLAVIS ANULARIS, TESSERA NUMMVLARIA, TABVLAE CERATAE, INSCRIPTIO, each with its place and sentence from section 8.
- [x] **Art containers:** `data-ascii="ring-key"` (130×66).
- [x] **Frieze:** marquee band is `aria-hidden="true"` and contains the four existing tokens twice (seamless loop).
- [x] **Content-lock allowlist** gains the old rules hint.

### Build

- [x] Problem: 560px copy column, first paragraph in `--av-text`; ring-key right (9px / 2.6px), floaters (~18), plate beneath.
- [x] Mechanism cards: five in a row, numeral + actor label + title + body; card IV bronze border; stacked on mobile.
- [x] Diagram: recessed `--av-well` panel; CSS restyle per spec (internal nodes panel fill + bronze stroke + unclassed inner inset rect; external nodes bg fill + line stroke; Cormorant node names; Plex labels; bronze arrows and markers; boundary dashed bronze 55%; boundary label uppercase with letter-spacing and `--av-bg` knockout). Mobile vertical SVG per `mobile-03`.
- [x] Coin lane: 16s loop from the prototype keyframes (`coin1`, `passOn`, `failOn`, `phaseA`, `phaseB`), checkpoint at 52% of lane width with translate distances derived from the layout (CSS custom properties set from lane width, no hard-coded 594/1134px); reduced motion shows the Approved state.
- [x] Rules: tabs (2×2 on mobile), diptych with hinge rings, four panels toggled with `hidden`, no copy injected from JS. The old flip-card decrypt script is removed (see Open question 6).
- [x] Record: frieze band (48s marquee), 760×428 video link frame with bronze-ringed play glyph beside the existing paragraph and INSCRIPTIO plate.

**Accept:** matches `02` to `05`; diagram tests pass with conditions unchanged; tabs work by keyboard.
**Commit:** `Restyle problem, mechanism, rules and record sections`

---

## Phase 4: Run through close

Self-host, walkthrough, delta, roadmap, close with wide temple, footer.

### Tests (write first, confirm FAIL)

- [x] **Commands frozen:** the text of every `.shell pre code` block equals the list captured from `main` (stored in `tests/fixtures/commands-baseline.txt`). CSS never sets `.shell code` to wrap (`pre-wrap` / `break-spaces` forbidden on `.shell code`; task prompts use their own class).
- [x] **Stairs:** nine stair blocks, numerals I to IX, titles matching the nine `.run-steps > li > h3` titles; stairs container `aria-hidden="true"` (the real steps follow directly).
- [x] **Plates:** GRADVS, MILIARIVM, and the close AERARIUM (`Temple of Saturn, reconstructed`, `The whole treasury, standing on new ground.`).
- [x] **Close art:** `data-ascii="temple-wide"` (330×104), `aria-hidden="true"`.
- [x] **Footer credit:** the confirmed X handle and its link (pending Open question 1).
- [x] Existing `.run-steps > li`, `.run-steps .step-list li::before`, `.run-steps.demo-steps--phase-b` checks unchanged.

### Build

- [x] Run: intro + Prerequisites side by side with chips; stairs (indented staircase list on mobile); Setup; nine full entries with Roman numerals, code blocks (2px verdigris left border, label row), notes and ◆ lists.
- [x] Walkthrough: Phase A / B headers with policy chips; task cards in a 2-column grid, prompts wrap (`overflow-wrap: anywhere`), "Expected result:" in bronze; policy update block and the two outline buttons.
- [x] Delta: inscription list, Roman numeral + paragraph, hairlines.
- [x] Roadmap: arched milestones (radius ~180px / 110px) on a shared base strip; intro as heading sub; plate.
- [x] Close: centred two-line H2 (second line italic bronze-hi, same words), CTAs, `temple-wide` centred with ~40 floaters, plate top-left of the art and never over it on mobile.
- [x] Footer: hairline, credits left, track + GitHub right, stacked on mobile. The existing `close-meta` and `site-footer` content merge into this row without wording changes.

**Accept:** matches `06` to `10`; every command copy-pastes cleanly (manual paste test of all shell blocks plus the frozen-commands check).
**Commit:** `Restyle self-host, walkthrough, roadmap and close`

---

## Phase 5: Hardening

Tablet breakpoint, reduced motion, off-screen pausing, mobile menu, Lighthouse, social card, docs.

### Tests (write first, confirm FAIL)

- [x] **Pausing:** CSS contains `.is-paused` with `animation-play-state: paused`; `script.js` toggles `is-paused` from an `IntersectionObserver`.
- [x] **Reduced motion:** a `prefers-reduced-motion` block covers the floater, coin, stamp, phase and frieze animations (checked by class names inside the media block).
- [x] **Mobile menu:** button has `aria-expanded` and `aria-controls`; `script.js` handles `Escape` and traps focus while open.
- [x] **Page weight:** gzipped sum of `index.html`, `styles.css`, `script.js`, `fonts.css`, every font file `fonts.css` declares that the page uses, every `assets/ascii/*.json`, and every image `index.html` references (excluding the social card) is under 400KB. This will fail today (see Open question 7).
- [x] **Social card:** `assets/images/social-card.html` uses `temple-hero` and the Aerarium tokens; no cyan.
- [x] **Docs:** `docs/CLAUDE-INIT-AESTHETIC.md` starts with a superseded notice pointing at `docs/revamp/REVAMP_SPEC.md`; README mentions `tools/ascii/`.

### Build

- [x] Tablet 768–1199: two-column blocks stack, mechanism cards wrap 3+2, diagram keeps desktop geometry scaled.
- [x] Off-screen pausing for every animated section.
- [x] Mobile menu focus trap and Escape.
- [x] Page-weight fixes (per Open question 7).
- [x] Lighthouse desktop and mobile, performance and accessibility ≥ 90.
- [x] Regenerate `social-card.png` via `node tests/render_social_card.js`.
- [x] README and doc updates.

**Accept:** section 9 budgets met.
**Commit:** `Harden Aerarium for tablet, motion and performance`

---

## Open questions

Resolution (2026-09-26): 1 answered by Liam (handle corrected). 2 to 6 and 8 went with the stated defaults after Liam's go-aheads. 7 and 9 approved: `brotli` installed for subsetting (fonts now 227KB worst-case total page), Lighthouse run (desktop 100/100/100/100, mobile 94/100/96/100; the mobile best-practices point is the 2 to 3px ASCII art).

1. **X handle (needed before Phase 4).** ~~The footer credits `@itzbankotez`.~~ **Answered 2026-09-26:** the handle and link are `@itzbanknotez` / `https://x.com/itzbanknotez`. Fixed in `index.html`, guarded by a test.
2. **Mechanism card actor labels (before Phase 3).** Spec section 7 asks for an actor label on each card (the prototype uses Owner, Owner, Agent, FCC machine, Vault), but section 8 does not list them as copy changes. My default: add them, since they reuse existing names. Confirm.
3. **Labels the mockups drop (before Phase 2).** The page shows `terminal 1 · owner` / `terminal 2 · agent` on code blocks and `request_payment` above the Agent rows. The prototypes show only Codex / Claude labels and no `request_payment`. My default: keep them, because copy is locked. Say if they should go.
4. **Flare mark (before Phase 2).** The prototype sets "flare" as text in Flare red; the page uses the official Flare logo PNG, which is already that red. My default: keep the official logo image.
5. **Plate spellings (before Phase 3).** Section 7 writes TESSERA NUMMULARIA / TABULAE CERATAE; section 8 and the prototypes write TESSERA NUMMVLARIA / TABVLAE CERATAE / GRADVS / MILIARIVM, and CLAVIS ANULARIS with a U. My default: section 8 exactly.
6. **Rules decrypt effect (Phase 3).** The current Owner-view "decrypt" scramble is motion on text, which spec section 6 rules out. My default: remove it with the flip cards.
7. **Page weight (Phase 5).** Fonts the page will load (Cormorant ~345KB, Space Grotesk and Plex TTFs ~35–55KB each) plus the 5000px-wide Flare PNG (~103KB) come to about 650KB gzipped, over the ~400KB target. Fix: subset fonts to Latin and convert TTFs to WOFF2 with `fonttools` (a dev-time `pip install`, nothing shipped), and resize the Flare PNG. Needs your OK to install `fonttools` then.
8. **Reference folder in the repo (Phase 1).** `docs/revamp/reference/` is ~10MB of PNGs plus the prototypes. Committing it also publishes it on GitHub Pages. My default: commit it, as the package README intends.
9. **Lighthouse (Phase 5).** Running it needs `npx lighthouse` (a package download). I'll ask before installing.
