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
