# Landing page redesign — review checklist (2026-08-11)

Pre-flight audit before deploy. All items checked against the implemented page.

## Content & claims

- [x] Every tx hash and prompt traces to `docs/EVIDENCE.md`
- [x] No forbidden phrases (`validate_site.py` FORBIDDEN_PHRASES)
- [x] SIMULATED/testnet labeled once in proof bar (not sticky banner)
- [x] Stale "Next: MCP integration" removed; MCP listed as shipped
- [x] GitHub + README quickstart links present in nav, get-started, footer

## Accessibility & motion

- [x] Skip link present
- [x] `prefers-reduced-motion` in CSS and JS — no cycling, no typing, static reveal
- [x] Hero dot buttons have `aria-label` and `aria-pressed`
- [x] Mobile pane tabs for agent/owner views under 900px
- [x] `<noscript>` static budget-window fallback in hero

## Performance & stack

- [x] No animation libraries — vanilla JS only
- [x] Self-hosted fonts unchanged
- [x] Single CSS + single JS file

## Validation

```bash
python3 tests/validate_site.py   # PASS
python3 -m http.server 8080    # preview at localhost:8080
```

## Liam checkpoint

Screenshot review recommended for: hero cycler at 1280px and 390px, proof bar link row wrap, get-started code blocks on mobile.
