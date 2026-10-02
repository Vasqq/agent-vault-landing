# Kickoff prompt for Claude Code

Paste everything below the line into a fresh Claude Code session started in the `agent-vault-landing` repository root.

---

We're revamping this landing page into a new visual system called Aerarium. The design is finished and approved. Your job is to implement it faithfully, in phases, with me reviewing each phase on my local server before you continue.

Read these first, in this order, before you touch any code:

1. `docs/revamp/REVAMP_SPEC.md`: the source of truth. It supersedes `docs/CLAUDE-INIT-AESTHETIC.md` and the visual parts of `docs/DESIGN_PLAN.md`.
2. The reference screenshots in `docs/revamp/reference/` (`desktop-*.png`, `mobile-*.png`). These are what the page must look like.
3. `docs/revamp/reference/prototype-desktop.html` and `prototype-mobile.html`. Serve the repo with `python3 -m http.server 8080` and open them to see the motion and read exact values. They are mockups: take values from them, not structure.
4. The current `index.html`, `styles.css`, `script.js` and `tests/validate_site.py`, so you know what exists and what the tests protect.
5. `skills/frontend-design/SKILL.md`.
6. `tools/ascii/README.md` and the JSON in `assets/ascii/`.

Ground rules:

- Content is locked. The copy on the page is verified against the protocol repo. Only make the copy changes listed in section 8 of the spec. If something else seems to need a wording change, ask me.
- Stay static: HTML, CSS, vanilla JS, no framework, no build step, no third-party requests.
- Test first. For each phase, extend `tests/validate_site.py` so it fails for the thing you're about to build, then build it. Never weaken or delete an existing check to make it pass. If an existing check blocks the design, stop and tell me.
- Keep the diagram's SVG geometry and the test-anchored classes exactly as they are; restyle with CSS.
- Before each report, check your own work: Playwright screenshots at 1440px and 390px, reduced motion on and off, compared against the matching reference PNGs. Fix what doesn't match before showing me.
- Work on a branch called `aerarium-revamp`. At most one commit per phase, with plain imperative subject lines and no prefixes, for example "Add Aerarium tokens and typography". Do not push.

Process:

1. Write an implementation plan to `docs/superpowers/plans/2026-09-25-aerarium-revamp.md`, following the five phases in section 11 of the spec. Include the test changes per phase. Show me the plan and wait for my go-ahead.
2. Then do Phase 1 only. Stop, summarize what changed, list anything you were unsure about, and tell me what to look at on `http://localhost:8080`.
3. Continue phase by phase, only after I say go.

One question to raise with me in your plan rather than decide yourself: the footer credits the X handle `@itzbankotez`. Confirm that spelling with me before Phase 4.

Start by reading, then write the plan.
