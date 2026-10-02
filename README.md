# AgentVault Landing

Static localhost landing page for AgentVault. Product claims are verified against the protocol repository at `../agent-vault`.

## Preview locally

```bash
cd /Users/liampereira/Documents/Code/agent-vault-landing
python3 -m http.server 8080
```

Open [http://localhost:8080](http://localhost:8080).

Live site: [https://vasqq.github.io/agent-vault-landing/](https://vasqq.github.io/agent-vault-landing/)

## Validate claims and assets

```bash
python3 tests/validate_site.py
```

## Visual system

The page uses the Aerarium design: the treasury of Rome, rendered as ASCII. The spec, reference screenshots and prototypes live in `docs/revamp/` (start with `docs/revamp/REVAMP_SPEC.md`).

The ASCII figures are pre-rendered by `tools/ascii/` into `assets/ascii/*.json`; the browser only displays text. Regenerate them only if a scene changes (see `tools/ascii/README.md`):

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r tools/ascii/requirements.txt
python3 tools/ascii/build.py
```

Fonts are self-hosted and subset to the characters the page uses. The full source fonts sit next to the subsets in `assets/fonts/`. If new copy adds characters outside Latin-1 and basic punctuation, widen the ranges in `tools/fonts/subset.sh` and run it (needs `pip install fonttools brotli`).

## Regenerate social card (og:image)

```bash
npm install --no-save playwright
npx playwright install chromium
node tests/render_social_card.js
```

## Source of truth

- `../agent-vault/AGENTVAULT_NORTH_STAR.md`
- `../agent-vault/docs/X402_LIVE_DEMO.md`
- `../agent-vault/docs/HACKATHON.md`

Pushes to `main` deploy automatically to GitHub Pages via `.github/workflows/pages.yml`.
