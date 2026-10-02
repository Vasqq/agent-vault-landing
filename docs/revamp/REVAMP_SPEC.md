# AgentVault landing · Aerarium revamp spec

Status: approved design, ready to implement. This document supersedes `docs/CLAUDE-INIT-AESTHETIC.md` and the visual sections of `docs/DESIGN_PLAN.md`. Where they disagree, this wins.

Visual targets live in `docs/revamp/reference/`:

- `desktop-*.png` and `mobile-*.png`: one screenshot per section, at 1440px and 390px (2x), reduced motion on. These are the pictures to match.
- `prototype-desktop.html` and `prototype-mobile.html`: the same designs as HTML. Open them over the local server (`http://localhost:8080/docs/revamp/reference/prototype-desktop.html`) to watch the motion and to read exact values. They are inline-styled mockups, not production code. Do not copy their structure; copy their values.

---

## 1. The idea

AgentVault is presented as the treasury of Rome, rendered by a machine.

The page is a walk: you arrive at the steps of the Temple of Saturn (the *aerarium*, Rome's treasury), move through it section by section, and at the end step back to see the whole building standing on ground made of digital glyphs. Ancient institution, new kind of customer.

Three rules keep it coherent. Every new element has to obey them.

1. **One rendering grammar.** Every image is a real Roman object, 3D-rendered, turned into ASCII with one character ramp: bronze highlights, verdigris shadows. No other illustration style, no icons-as-art, no photos.
2. **One meaning for the dissolve.** Stone breaking into `0`/`1`/hex glyphs means "the past becoming AgentVault's era". It is never decoration.
3. **Storytelling lives in the plates.** Small museum labels name each object. Product copy stays product copy.

The coin is the thread through the page: it carries the keyhole mark, travels Vault → FCC checkpoint → Vendor, and is either stamped SPECTAVIT and paid, or stamped DECLINED and returned.

---

## 2. Technical decisions

- **Stay static.** Plain HTML, CSS and vanilla JS. No framework, no bundler, no build step. GitHub Pages deploy stays exactly as it is (`.github/workflows/pages.yml`). React/wagmi are not needed: nothing on this page connects a wallet.
- **ASCII is pre-rendered.** `tools/ascii/` renders the scenes (numpy/scipy/Pillow) into `assets/ascii/*.json`. The JSON is committed. The browser only displays text.
- **No third-party requests.** Fonts are self-hosted (`assets/fonts/`). Do not add Google Fonts or CDN links.
- **Keep what works in `script.js`:** the hero scenario cycler (typing, rows, dots, pause on hover/focus, `#hero-stage-caption`), section reveal, and reduced-motion handling. Restyle it; do not rewrite its data or behaviour.
- **Remove:** the ASCII vault sphere and its state machine (`.ascii-field`, `setVaultState`, `assets/ascii-vault.txt`), the `.void-scan` overlay, the pixel wordmark in the header (keep the PNG file itself, `tests/validate_site.py` requires it), and all cyan tokens.

---

## 3. Design tokens

Put these on `:root` as custom properties. The prefix `--av-` matches `tools/ascii/convert.py`.

| Token | Value | Use |
|---|---|---|
| `--av-bg` | `#16130F` | Page ground (warm basalt) |
| `--av-panel` | `#1F1A15` | Raised stone panels, proof bar, cards |
| `--av-well` | `#100D0A` | Recessed surfaces: terminals, code, diagram well |
| `--av-bronze` | `#B08D57` | Rules, borders, primary button, numerals |
| `--av-bronze-hi` | `#D8B67E` | ASCII highlights, italic headline, emphasis |
| `--av-verdigris` | `#6E9A8C` | ASCII shadows (`lo` layer) |
| `--av-digital` | `#5E8A7C` | Digital glyph layer (`dg`), at 0.8 opacity |
| `--av-ok` | `#86B3A3` | PAID, approved states, floating glyphs |
| `--av-decline` | `#CF6A52` | DECLINED, rule fired, decline states |
| `--av-text` | `#E8DFCC` | Primary text (travertine) |
| `--av-muted` | `#A69A86` | Body copy |
| `--av-label` | `#7D9A8F` | Mono labels, metadata |
| `--av-link` | `#9FC2B5` | Inline links (underlined, offset 3px, underline at 40% alpha) |
| `--av-line` | `rgba(176,141,87,0.26)` | Hairlines and quiet borders |
| Flare red | `#E62058` | Only the "flare" logotype in the hero eyebrow |

All text colours pass WCAG AA on `--av-bg`. Never put body text on the ASCII art; overlays only happen over sparse areas.

### Type

| Role | Face | Desktop | Mobile |
|---|---|---|---|
| H1 | Cormorant Garamond 500, line-height 0.98, tracking -0.01em. Second clause *italic* in `--av-bronze-hi` | 78px | 46px |
| H2 | Cormorant Garamond 500, line-height 1 | 56px | 40px |
| H3 | Cormorant Garamond 600 | 21–36px | 22–28px |
| Section numeral | Cormorant 500, outlined: `color: transparent; -webkit-text-stroke: 1px var(--av-bronze)` | 120px | 56px |
| Body | Space Grotesk 400, line-height 1.62 | 17px | 16px |
| Label | IBM Plex Mono 11px, uppercase, tracking 0.22em, `--av-label` | 11px | 10–11px |
| Code, terminals | IBM Plex Mono | 13–13.5px | 12px |
| Inscriptional caps (pills, proof items, marquee, wordmark) | Cormorant 600, uppercase, tracking 0.16–0.3em, `--av-bronze-hi` | 15–24px | 13–19px |

Wordmark: text, not image. `AGENTVAULT`, Cormorant 600, 24px (19px mobile), tracking 0.3em, `--av-bronze-hi`.

Separator between inscriptional items: a small diamond `◆` in `--av-bronze` at 0.6em, raised 0.28em, 0.4em side margins.

### Layout

- Content width 1296px, 72px gutters at 1440. Mobile gutters 24px.
- Breakpoints: `≥1200` desktop as referenced; `768–1199` tablet (two-column blocks stack, mechanism step cards wrap 3+2, diagram keeps desktop geometry scaled); `<768` mobile as referenced.
- Section rhythm: 120px top padding desktop, ~72px mobile. Section heading = outlined numeral + label + H2 on one baseline (desktop), stacked on mobile.
- Corners are square everywhere except the roadmap milestones.

---

## 4. Components

**Plate** (museum label). A short bronze rule (18×1px), then three lines: name in Plex Mono 9px, 500, tracking 0.3em, `--av-bronze-hi`; place in Cormorant italic 14px, `--av-text`; one sentence in Space Grotesk 11.5px, `--av-muted`. Whole plate at opacity 0.78, max width ~300px. No background, no border. Plates must stay small and quiet: they support the product, they never compete with it.

**Buttons.** 54px tall, square. Primary: `--av-bronze` fill, `--av-bg` text. Secondary: 1px `--av-bronze` border, `--av-text`. Space Grotesk 13px, 600, uppercase, tracking 0.18em. Hover: opacity 0.82. Visible focus ring: 2px `--av-bronze-hi` outline, 3px offset.

**Stone frame** (terminals, diptych leaves). Outer 1px `--av-bronze` border with 8–12px padding, inner 1px `--av-line` border around a `--av-well` surface. Leaves add `box-shadow: inset 0 2px 18px rgba(0,0,0,.6)`.

**Code block.** `--av-well`, 1px `--av-line` border, 2px left border in `--av-verdigris`. Optional label row (Codex / Claude) in 10px bronze mono. `overflow-x: auto; white-space: pre`. Never wrap commands.

**Tessera** (inspection tag). A small ring (16px circle, 1px border) overlapping a bordered tag: word in Cormorant 700 15px tracking 0.16em, sub-label in 9px mono.

**Frieze band.** Full-bleed 70px (56px mobile) `--av-panel` strip with bronze top/bottom borders and an inner double hairline (inset box-shadows), content scrolling horizontally.

---

## 5. ASCII system

### Assets

| File | Grid | Where | Font size desktop / mobile |
|---|---|---|---|
| `assets/ascii/temple-hero.json` | 220×125 | Hero, right-anchored | 7px / 3px |
| `assets/ascii/ring-key.json` | 130×66 | Problem | 9px / 2.6px |
| `assets/ascii/coin.json` | 120×66 | Mechanism coin lane | 2.2px / 1.6px |
| `assets/ascii/temple-wide.json` | 330×104 | Close | 7px / 2.1px |

Each JSON has `rows`, `cols` and `layers: { hi, lo, dg }`. A layer is rows joined by `\n`; spaces are empty cells. `coin` has no `dg` layer.

### Rendering

- One container per figure, `aria-hidden="true"`, holding three stacked `<pre>` elements (`dg` bottom, then `lo`, then `hi`) at `position: absolute; inset: 0`.
- Layer colours: `dg` = `--av-digital` at opacity 0.8; `lo` = `--av-verdigris`; `hi` = `--av-bronze-hi`.
- `pre` style: IBM Plex Mono, `line-height: 1em` (equal to font size), `letter-spacing: 0`, `margin: 0`, `pointer-events: none`, `user-select: none`.
- Size the container in `em` so the figure scales with one font-size and never causes layout shift: `font-size: var(--ascii-size); width: calc(var(--cols) * 0.6em); height: calc(var(--rows) * 1em)`. Set `--cols`/`--rows` in the markup, so the box is reserved before the JSON loads.
- Scale between breakpoints with `clamp()`, e.g. hero `--ascii-size: clamp(3px, 0.486vw, 7px)`.
- Load with a small loader in `script.js`: `fetch('assets/ascii/<name>.json')` (relative URL, works under `/agent-vault-landing/` on Pages), fill each `pre` with `textContent`. Load the hero immediately; load the others with an IntersectionObserver (rootMargin ~600px). If a fetch fails, leave the empty box: the art is decorative.
- Placement: hero temple bleeds off the right edge and sits behind nothing important; the far columns dissolve toward the headline. The wide temple is centred with the close headline above it.

### Regenerating

`tools/ascii/README.md`. Deterministic seeds. Only regenerate if a scene changes; commit the JSON.

---

## 6. Motion

Every animation is CSS unless noted, pauses when its section is off-screen (IntersectionObserver toggles `.is-paused` → `animation-play-state: paused` on descendants), and has a reduced-motion state.

| Element | Behaviour | Timing | Reduced motion |
|---|---|---|---|
| Floating glyphs (hero, problem, close) | Single hex/0/1 characters rise and drift left (translate −36px, −140px) while fading in then out. Random position, size 7–10px (6–7px mobile), `--av-ok`. Generate the spans in JS: ~46 hero, ~18 problem, ~40 close; about a third of those on mobile. | 7–15s each, linear, infinite, random negative delays | Static at opacity 0.45 |
| Hero cycler | Keep the existing scenario engine. Restyle only: rows arrive one by one; the Owner monitor and the SPECTAVIT seal appear after the decline. | Existing timings | Existing behaviour |
| Mechanism coin | One coin, one lane, 16s loop. First half: coin travels to the FCC checkpoint, SPECTAVIT tessera stamps in (scale 1.35→1, −4deg), coin continues to Vendor, lane reads Approved and "→ PAID". Second half: coin reaches checkpoint, DECLINED tessera stamps in, coin returns to Vault, lane reads Declined and "← DECLINED · the funds stay in the Vault". Translate distances from layout: checkpoint at 52% of lane width. | 16s ease-in-out infinite. Keyframes in the prototype (`coin1`, `passOn`, `failOn`, `phaseA`, `phaseB`) | Approved state, static |
| Frieze marquee | Tokens scroll left, content duplicated for a seamless loop | 48s linear infinite | Static |
| Section reveal | Keep existing `data-reveal` behaviour | Existing | Existing |

No parallax, no scroll-jacking, no motion on text.

---

## 7. Page, section by section

Keep the existing section ids and nav anchors: `#mechanism`, `#rules`, `#demo-video`, `#get-started`, plus `#problem`, `#built`, `#roadmap`. Section indexes change from `01 / Problem` style to outlined Roman numerals: I Problem, II Mechanism, III Rules, IV Record, V Run, VI Delta, VII Roadmap.

**Header.** Text wordmark left, five nav links right (Space Grotesk 12px, uppercase, tracking 0.2em, `--av-muted`), bottom hairline. Mobile: wordmark + a 44px menu button that opens the same five links.

**Hero** (`desktop-01`, `mobile-01`). Left column, 600px wide, top-aligned about 60px below the header: eyebrow (40px bronze rule, "flare" logotype, "Summer Signal · Flare Confidential Compute Track" label), H1, lede, the two CTAs, the Private ◆ Verifiable ◆ Non-custodial line, then the AERARIUM plate. Right: `temple-hero`, right-anchored, 876px tall, with floating glyphs over the dissolving far columns. Mobile: the temple first (full width, right edge bleeding), then the text stack.

**Proof** (the existing `#hero-stage`). Below the hero, full content width: the two-terminal stone frame. Agent panel left, Owner monitor right (stacked on mobile), bronze divider. The SPECTAVIT seal (two concentric circles, rotated −14deg, "SPECTAVIT" over "FCC · 114") sits bottom-right of the Owner panel and appears with the decline. Dots and the dynamic caption stay; caption in Cormorant italic 23px, centred.

**Proof bar.** 96px `--av-panel` band with bronze borders and inner double hairline. Left: the existing sentence. Right: the four declines in inscriptional caps with ◆ separators, `white-space: nowrap` on each item (the reference shows them wrapping; they should not). Mobile: stacked list.

**I · Problem.** Four existing paragraphs in a 560px column (first paragraph in `--av-text`). Right: `ring-key`, its bit dissolving, floating glyphs, CLAVIS ANULARIS plate beneath.

**II · Mechanism.** In this order:
1. The five existing step cards in one row (stacked on mobile), each with Roman numeral, actor label, title, body. Card IV (FCC) has a bronze border; the rest `--av-line`.
2. The architecture diagram in a recessed `--av-well` panel. **Keep the existing SVG geometry exactly** (coordinates, `line`/`polyline` routes, `diagram-node--external` ×3 and `diagram-node--internal` ×2 classes, the `>AgentVault</text>` and single `>Vault</text>` labels, the `role="img"` label). `tests/validate_site.py` asserts on these. Restyle with CSS only: internal nodes `--av-panel` fill, bronze stroke, plus an inner inset rect (unclassed) for a double border; external nodes `--av-bg` fill, `--av-line` stroke; node names Cormorant 600, sub-labels and arrow labels Plex Mono in `--av-label`; arrows and markers `--av-bronze`; boundary dashed bronze at 55% opacity; the "AgentVault" boundary label rendered uppercase with letter-spacing via CSS (`text-transform` works on SVG text), background knockout rect in `--av-bg`. Add classes to `<text>` elements for styling if needed; do not change their content. On mobile, render a vertical variant (see `mobile-03-mechanism.png`) as a second SVG shown only below 768px, hidden from assistive tech whenever it is not displayed. The diagram tests count occurrences across the whole file (exactly one `>Vault</text>`, exactly three external and two internal node classes), so first scope those checks to the desktop SVG (give it an id and slice the HTML to that element in the test), and give the mobile SVG its own class names. Do not weaken the checks themselves.
3. The coin lane (section 6).
4. TESSERA NUMMULARIA plate, right-aligned.

**III · Rules.** Replaces the four flip cards with tabs plus a diptych.
- Four tab buttons in a row (2×2 on mobile): "Rule 0N" label + rule name. Active tab: bronze border, `--av-panel` fill, `--av-text` name. `role="tablist"`/`tab`/`tabpanel`, arrow-key navigation, `aria-selected`. Default: Rule 02.
- The diptych: two stone-framed leaves joined by a hinge (two small bronze rings). Left leaf "Agent view": the task in italic `--av-muted`, the Agent status in `--av-ok`. Right leaf "Owner view": the reason in `--av-text`, the Owner status in `--av-decline`. Small italic captions bottom-right: "what the Agent is told" / "what the Owner reads" (desktop only). Mobile stacks the leaves with a horizontal hinge.
- **All four rules' text must stay in the HTML** (tests require every phrase). Render four panels and toggle `hidden`; do not inject copy from JS.
- TABULAE CERATAE plate, right-aligned.

**IV · Record** (`#demo-video`). Frieze band marquee (existing tokens), then the video link frame (760×428 desktop, full-width 16:9 mobile) with a bronze-ringed play glyph, beside the existing paragraph and the INSCRIPTIO plate.

**V · Run** (`#get-started`). Intro paragraphs and Prerequisites side by side (chips for each tool). Then the stairs: nine stone blocks ascending left to right, each with its Roman numeral and step title (mobile: an indented staircase list), GRADUS plate top-left. Then Setup, then the nine steps as full entries: numeral, title, code blocks (Codex/Claude variants labelled), notes and lists. Keep the existing classes the tests check: `.run-steps > li`, `.run-steps .step-list li::before`, `.run-steps.demo-steps--phase-b`.

**Demo walkthrough.** Existing copy. Phase A / Phase B headers with policy chips; tasks as `--av-panel` cards in a 2-column grid (stacked mobile): numeral, slug in mono, prompt in a code-style box that wraps (`overflow-wrap: anywhere`), usage line, "Expected result:" in bronze. Policy update code block and the two outline buttons at the end.

**VI · Delta** (`#built`). The four existing items as an inscription list: Roman numeral + paragraph, hairline between items.

**VII · Roadmap.** Intro line as the heading sub. The two items drawn as Roman milestones: arched-top stone panels (top radius ~180px desktop, 110px mobile), bronze border, standing on a shared base strip. MILIARIUM plate.

**Close.** Centred H2 ("Autonomy for the agent." / italic bronze "Control for the Owner."), the two CTAs, then `temple-wide` centred with floating glyphs rising off the digital hills, the AERARIUM (reconstructed) plate top-left of the art. Footer below: hairline, credits left, track + GitHub right (stacked on mobile).

---

## 8. Copy changes

Everything not listed here stays exactly as it is in `index.html` today.

**New plates** (name / place / sentence):

| Section | Name | Place | Sentence |
|---|---|---|---|
| Hero | AERARIUM | Temple of Saturn, Forum Romanum | The treasury of Rome sat inside this temple. Money left it only on authority. |
| Problem | CLAVIS ANULARIS | Roman ring-key, bronze | Romans wore the key to a strongbox on a finger. Whoever held the ring could open the chest. |
| Mechanism | TESSERA NUMMVLARIA | Inspector's tag, bone | Tied to a sealed bag of coin and marked SPECTAVIT: this has been examined. |
| Rules | TABVLAE CERATAE | Wax-tablet diptych | Romans kept receipts on hinged wax tablets. Two leaves, one record. |
| Record | INSCRIPTIO | The public record | What settles is carved where anyone can read it. Why it was refused is not. |
| Run | GRADVS | The podium steps | Nine steps up to your own treasury. |
| Roadmap | MILIARIVM | Roman milestone | Stone markers counted the miles along every Roman road. |
| Close | AERARIUM | Temple of Saturn, reconstructed | The whole treasury, standing on new ground. |

**Changed or added lines:**

- Rules hint: replace "Hover or tap a card to switch from the Agent's view to the Owner's." with "Choose a rule to see what the Agent was told and what the Owner reads." (One string for both layouts; the mockups used a left/right and a top/bottom variant, this replaces both.)
- Coin lane: "A payment, in motion · Approved" / "A payment, in motion · Declined"; "→ PAID"; "← DECLINED · the funds stay in the Vault"; stop labels "Vault", "FCC checkpoint", "Vendor"; tesserae "SPECTAVIT" / "FCC · VERIFIED" and "DECLINED" / "reason stays private".
- Rule leaves: "Agent view", "Owner view", "what the Agent is told", "what the Owner reads".
- Owner monitor seal: "SPECTAVIT", "FCC · 114".
- Section indexes: Roman numerals as listed in section 7.

Voice rules for any further copy: no em dashes, no hype, short sentences, no corporate "we".

---

## 9. Accessibility and performance

- All ASCII, floaters, seal and tesserae are `aria-hidden="true"`. The diagram keeps its `role="img"` description.
- Keyboard: tabs, menu button, cycler dots and all links reachable with visible focus. Mobile menu traps focus while open and closes on Escape.
- `prefers-reduced-motion` handled in both `styles.css` and `script.js` (tests require both).
- No horizontal page scroll at 390px. Only code blocks scroll sideways.
- Budget: page weight under ~400KB gzipped excluding the social card; no layout shift from ASCII loading (boxes reserved in CSS); Lighthouse performance and accessibility ≥ 90 on desktop and mobile.
- Update `og:image`: regenerate `assets/images/social-card.png` in the new style via `assets/images/social-card.html` and `tests/render_social_card.js` (temple-hero ASCII, H1, wordmark).

---

## 10. Tests

Test first. Before building each phase, extend `tests/validate_site.py` so it fails, then make it pass. Keep every existing check (content phrases, diagram geometry, links, meta, CSS/JS guardrails). Add at least:

- Required files: `assets/ascii/temple-hero.json`, `ring-key.json`, `coin.json`, `temple-wide.json`, `assets/fonts/cormorant-garamond-variable.woff2`.
- Required phrases: each plate name and sentence; the new rules hint; the coin lane strings.
- Forbidden phrases: "Hover or tap a card"; the old cyan hex values `#9bb9bb` and `#7a9294` anywhere in `styles.css`/`index.html`; `ascii-vault.txt`; `fonts.googleapis.com`.
- CSS must define every `--av-` token in section 3.
- Four rule panels present in HTML, exactly one without `hidden`.

---

## 11. Phases and acceptance

Work on a branch. Stop after each phase, report what changed, and wait for Liam to review on `python3 -m http.server 8080` before continuing.

1. **Foundations.** Tokens, fonts, base type, header, section heading component, plate, buttons, old aesthetic removed, test scaffolding. Accept: page renders in the new palette end to end even before the art lands; tests pass.
2. **Hero and proof.** ASCII loader and hero temple, floaters, restyled cycler with seal, proof bar. Accept: matches `desktop-01` / `mobile-01`; no layout shift; cycler behaviour unchanged.
3. **Sections I–IV.** Problem, mechanism (cards, restyled diagram with mobile variant, coin lane), rules tabs and diptych, record. Accept: matches `02`–`05`; diagram tests pass unchanged; tabs keyboard-accessible.
4. **Run through close.** Self-host, walkthrough, delta, roadmap, close with wide temple, footer. Accept: matches `06`–`10`; every command copy-pastes cleanly.
5. **Hardening.** Tablet breakpoint, reduced motion, off-screen pausing, mobile menu, Lighthouse, social card, README/doc updates (point `docs/CLAUDE-INIT-AESTHETIC.md` at this spec as superseded). Accept: section 9 budgets met.

Self-check before each report: Playwright screenshots at 1440 and 390, with reduced motion on and off, compared side by side against the reference PNGs.

Commits: one per phase at most, imperative subject lines without prefixes, e.g. "Add Aerarium tokens and typography", "Add hero temple and ASCII loader". Never push; Liam pushes.
