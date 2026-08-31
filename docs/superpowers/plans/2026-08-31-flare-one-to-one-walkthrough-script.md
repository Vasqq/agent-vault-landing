# Flare one-to-one landing walkthrough implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a two to three minute word-for-word script for presenting AgentVault by scrolling through the existing landing page.

**Architecture:** Add one standalone Markdown document under `docs/`. The document follows the landing page's current section order, separates spoken copy from interaction cues, and bases every technical claim on the landing page and AgentVault North Star.

**Tech Stack:** Markdown, Node.js command-line validation, existing HTML and Markdown sources.

## Global Constraints

- Do not modify the landing page, presentation source, styles, JavaScript, or existing copy.
- The spoken script must contain 300 to 360 words and take approximately two to three minutes.
- Keep interaction cues outside the spoken word count.
- State that the recorded run used simulated TEE mode, so host confidentiality, key isolation, and hardware attestation did not hold.
- Use plain, first-person English with no investor language, em dashes, or en dashes.
- Follow this order: Hero, Problem, Mechanism, Rules, Demo and proof, Self-host and build summary, Roadmap and close.

---

### Task 1: Landing-page walkthrough script

**Files:**
- Create: `docs/FLARE_1ON1_LANDING_WALKTHROUGH.md`
- Reference: `index.html`
- Reference: `/Users/liampereira/Documents/Code/agent-vault/docs/AGENTVAULT_NORTH_STAR.md`
- Reference: `/Users/liampereira/Documents/Code/agent-vault/presentation/agentvault-flare-1on1/SCRIPT.md`

**Interfaces:**
- Consumes: current landing-page section order and existing AgentVault claim language.
- Produces: one copy-ready walkthrough with spoken paragraphs and bracketed page-action cues.

- [ ] **Step 1: Verify the output does not already exist**

Run:

```bash
test ! -e docs/FLARE_1ON1_LANDING_WALKTHROUGH.md
```

Expected: exit status 0.

- [ ] **Step 2: Draft the complete walkthrough**

Create `docs/FLARE_1ON1_LANDING_WALKTHROUGH.md` with this structure:

```markdown
# Flare one-to-one landing-page walkthrough: AgentVault

*Target runtime: approximately two minutes 30 seconds*

## Before the call

[Open the landing page at the top. Let the hero animation settle before you begin.]

## Hero

[Keep the hero and Agent/Owner terminal visible.]

AgentVault started with one question: how can an AI agent pay for an API without putting a private key inside its runtime? It is a spending-authority layer for standard x402 on Flare. The Owner keeps the funds in a Vault. The agent gets a revocable Credential and can request payments, but it never signs or sends a transaction.

## Problem

[Scroll to "The layer x402 doesn't define."]

x402 standardizes how an API asks for payment and how that payment settles. It does not decide where the agent's spending authority lives or who enforces its limits. If a private key sits inside an LLM-driven process, prompt injection, tool misuse, loops, and replay become financial risk.

## Mechanism

[Scroll to "How AgentVault works" and point across the diagram.]

The flow separates requesting a payment from the authority to sign it. The Owner deposits USDT0 and sets the policy. The agent sends an encrypted request with its Credential. A registered Flare Confidential Compute machine checks the policy and signs EIP-3009 only when the request passes. The Vault verifies the machine and payment terms through EIP-1271, then standard x402 settlement pays the Vendor.

## Rules

[Scroll to "The rules behind every payment."]

There are four controls: a Vendor allowlist, rolling budget, maximum payment, and rate limit. The useful part is the visibility boundary. The agent sees only paid or declined, so it cannot inspect the rules and adapt around them. The Owner monitor sees the verified policy reason.

[Flip the "Rolling budget window" card to Owner view.]

## Demo and proof

[Point back to the rolling-budget result, then scroll through "Watch the demo."]

In the Coston2 run, three payments of 0.10 USDT0 settled. A fourth would have taken spending to 0.40, above the Owner's 0.35 rolling budget, so it was declined before settlement. The Owner then paused spending and withdrew the remaining 0.70. This run used simulated TEE mode. The settlement and policy path were verified, but host confidentiality, signing-key isolation, and hardware attestation did not hold. Those properties require REAL Confidential Space.

## Self-host and build summary

[Scroll past the detailed commands to "Built during Flare Summer Signal."]

AgentVault is self-hosted today. The page includes the complete setup and demo path, but the short version is that the Owner keeps the funds and the agent never receives the payment key.

## Roadmap and close

[Scroll to "What's next."]

The next product step is a hosted option, while keeping self-hosting available, followed by a small fee only on approved payments. I would value your take on two things: does this Owner and agent boundary feel right for Flare developers, and what would make a hosted version useful inside the ecosystem?

## Sources

- `index.html`
- `/Users/liampereira/Documents/Code/agent-vault/docs/AGENTVAULT_NORTH_STAR.md`
```

- [ ] **Step 3: Validate structure, length, punctuation, and required claims**

Run:

```bash
node - <<'NODE'
const fs = require('fs');
const text = fs.readFileSync('docs/FLARE_1ON1_LANDING_WALKTHROUGH.md', 'utf8');
const spoken = text
  .split('\n')
  .filter((line) => !line.startsWith('#') && !line.startsWith('*') && !line.startsWith('[') && !line.startsWith('- `'))
  .join(' ');
const words = spoken.match(/[A-Za-z0-9][A-Za-z0-9'.-]*/g) || [];
const required = [
  '## Hero',
  '## Problem',
  '## Mechanism',
  '## Rules',
  '## Demo and proof',
  '## Self-host and build summary',
  '## Roadmap and close',
  'simulated TEE mode',
  'host confidentiality',
  'hardware attestation',
];
if (words.length < 300 || words.length > 360) throw new Error(`spoken word count: ${words.length}`);
for (const phrase of required) if (!text.includes(phrase)) throw new Error(`missing: ${phrase}`);
if (/[—–]/.test(text)) throw new Error('dash character found');
console.log(`PASS: ${words.length} spoken words`);
NODE
```

Expected: `PASS: <number> spoken words`, where the number is between 300 and 360.

- [ ] **Step 4: Audit the script against its sources and humanize it**

Read the script aloud and compare every technical claim and number with `index.html` and `AGENTVAULT_NORTH_STAR.md`. Remove promotional filler, forced transitions, repetitive sentence shapes, and any claim not present in those sources. Confirm that the interaction cues match real page headings and controls.

- [ ] **Step 5: Re-run validation and inspect the repository scope**

Run:

```bash
git diff --check
git status --short
```

Expected: no whitespace errors; only `docs/FLARE_1ON1_LANDING_WALKTHROUGH.md` is newly changed beyond the already committed design and plan documents and any pre-existing user files.

- [ ] **Step 6: Commit the walkthrough**

```bash
git add docs/FLARE_1ON1_LANDING_WALKTHROUGH.md
git commit -m "docs: add Flare landing walkthrough script"
```
