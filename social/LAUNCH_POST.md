# AgentVault launch post drafts

Recommended: **POST 1 — Milestone — proof-first**

---

```
POST 1 — Milestone — proof-first

COPY:
AI agents can pay x402 APIs. The harder question is who holds the private key.

I built AgentVault for Flare Summer Signal: an Owner-controlled Vault plus an FCC policy check before each payment.

3 payments settled on Coston2. The 4th hit the 0.35 budget and stopped.

Landing page (localhost for now): open the repo and run python3 -m http.server 8080 in agent-vault-landing.

MEDIA:
Type: screenshot
Capture: Desktop browser at http://localhost:8080 showing the hero receipt with 3 settled rows and 1 declined row, plus the proof section visible after a short scroll. Crop to 16:9. Include the SIMULATED / mock USDT0 chips in frame.
Alt text: AgentVault landing page showing a Coston2 authorization receipt with three settled payments and one budget decline, plus proof stats for Flare Summer Signal.
Redaction: No .env contents, no private keys, no ngrok URLs, no terminal scrollback with secrets. Browser tab bar clean.

TIMING: Weekday, 9:00–11:30 ET
TAGS: @FlareNetworks
CLAIM CHECK:
- "x402 APIs" → North Star §10, X402_LIVE_DEMO.md HTTP-402 arc
- "private key" / no payment-signing key in agent → North Star §6, §14
- "Flare Summer Signal" / FCC policy check → HACKATHON.md, North Star §7–§8
- "3 payments settled" / "4th" / "0.35 budget" → X402_LIVE_DEMO.md epoch 4 table (0.10 × 3, decline at 0.40 > 0.35)
- "Coston2" → X402_LIVE_DEMO.md deployed addresses
RISK: Do not imply a public URL exists yet. Do not claim REAL Confidential Space confidentiality.
```

---

```
POST 2 — Mechanism explainer — authority model

COPY:
x402 tells an API how to request and settle a payment.

It does not decide where the agent's spending authority lives.

AgentVault puts funds in an Owner-controlled Vault, keeps the payment-signing key out of the agent runtime, and uses a registered Flare FCC machine to approve each request against a private four-rule policy.

Demo proof on Coston2: 3 settled, 4th blocked, Owner withdrew 0.70.

MEDIA:
Type: diagram
Capture: Export the mechanism flow from the landing page section (Owner → four rules → Agent request → FCC check → Vault verify → x402 settle) as a 16:9 PNG from localhost, or recreate as a simple three-column comparison: raw private key / human approval / AgentVault.
Alt text: Flow diagram showing AgentVault's Owner Vault, private FCC policy check, and standard x402 settlement path on Flare.
Redaction: No mocked dashboard UI. No invented tx hashes.

TIMING: Weekday, 10:00–13:00 ET
TAGS: none (save @FlareNetworks for milestone posts)
CLAIM CHECK:
- x402 scope framing → North Star §4 L1, §10
- payment-signing key away from agent → North Star §6
- four-rule private policy → North Star §6, REQUIREMENTS v4
- FCC registered machine → North Star §8, X402_LIVE_DEMO.md machine identity
- "3 settled, 4th blocked, 0.70 withdrawn" → X402_LIVE_DEMO.md branded HTTP arc
RISK: Avoid saying "Coinbase is custodial." Avoid "impossible to drain" or production-security claims.
```
