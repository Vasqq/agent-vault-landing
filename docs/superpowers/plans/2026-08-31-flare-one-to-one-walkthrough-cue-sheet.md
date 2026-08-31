# Flare one-to-one landing-page walkthrough cue sheet implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a glanceable cue-sheet companion to the existing AgentVault landing-page walkthrough.

**Architecture:** Add one standalone Markdown document that mirrors the full walkthrough's seven-section order. Each section uses a page-action cue, one master cue, and nested factual prompts drawn only from the approved full script.

**Tech Stack:** Markdown, shell verification commands, Git

## Global constraints

- Create only `docs/FLARE_1ON1_LANDING_WALKTHROUGH_CUES.md` during implementation.
- Keep `docs/FLARE_1ON1_LANDING_WALKTHROUGH.md`, the landing page, and presentation source unchanged.
- Target approximately 150 to 200 cue words, excluding headings and page-action cues.
- Use fragments, labels, and short clauses rather than a word-for-word script.
- Preserve x402, EIP-3009, EIP-1271, FCC, Credential, Vault, and REAL Confidential Space.
- Preserve the exact demo figures and simulated TEE limitations.
- Do not use em dashes or en dashes.

---

### Task 1: Create and verify the walkthrough cue sheet

**Files:**
- Create: `docs/FLARE_1ON1_LANDING_WALKTHROUGH_CUES.md`
- Reference without modifying: `docs/FLARE_1ON1_LANDING_WALKTHROUGH.md`

**Interfaces:**
- Consumes: the approved full walkthrough and cue-sheet design specification
- Produces: a standalone Markdown speaking aid for the landing-page walkthrough

- [ ] **Step 1: Record the clean baseline**

Run:

```bash
git status --short
git diff -- docs/FLARE_1ON1_LANDING_WALKTHROUGH.md
```

Expected: `.claude/` may remain untracked; the full walkthrough has no diff.

- [ ] **Step 2: Create the cue sheet**

Create `docs/FLARE_1ON1_LANDING_WALKTHROUGH_CUES.md` with exactly this content:

```markdown
# Flare one-to-one landing-page walkthrough cues

*Target runtime: approximately two minutes 30 seconds*

## Before the call

[Open at the hero. Let the animation settle.]

## Hero

[Keep the hero and Agent/Owner terminal visible.]

- **Master cue: Standard x402 authority, no agent key**
  - Owner funds Vault; revocable Credential
  - Requests only; never signs or sends

## Problem

[Scroll to "The layer x402 doesn't define."]

- **Master cue: x402 gap is spending authority**
  - Defines payment request plus settlement
  - Authority location and limit enforcement left open
  - Runtime key risks: prompt injection, tool misuse, loops, replay

## Mechanism

[Scroll to "How AgentVault works." Point across the diagram.]

- **Master cue: Requesting separate from signing**
  - Owner: deposit USDT0; set policy
  - Agent: encrypted request plus Credential
  - FCC: policy check; EIP-3009 signature on approval
  - Vault: verify machine plus terms via EIP-1271
  - x402 settlement pays Vendor

## Rules

[Scroll to "The rules behind every payment."]

- **Master cue: Owner controls the boundary**
  - Four controls: allowlist, rolling budget, maximum payment, rate limit
  - Agent: paid/declined; Owner: verified reason

## Demo and proof

[Point to the rolling-budget result, then scroll through "Watch the demo."]

- **Master cue: Three paid, fourth blocked**
  - Coston2: 3 x 0.10 USDT0 settled
  - Fourth: 0.40 vs 0.35 rolling budget; declined before settlement
  - Owner pause plus remaining 0.70 withdrawal
- **Must say: Simulated TEE limitations**
  - Verified: settlement path and policy checks
  - Did not hold: host confidentiality, signing-key isolation, hardware attestation
  - Those properties need REAL Confidential Space

## Self-host and build summary

[Scroll past the commands to "Built during Flare Summer Signal."]

- **Master cue: Usable today, self-hosted**
  - Setup plus demo path on page
  - Owner keeps funds; agent never gets payment key

## Roadmap and close

[Scroll to "What's next."]

- **Master cue: Hosted next, self-host remains**
  - Hosted option; small fee only on approved payments
  - Ask: boundary right for Flare developers?
  - Ask: what makes a hosted version useful?

## Source

- `docs/FLARE_1ON1_LANDING_WALKTHROUGH.md`
```

- [ ] **Step 3: Verify structure and required facts**

Run:

```bash
test "$(rg -c '^## (Hero|Problem|Mechanism|Rules|Demo and proof|Self-host and build summary|Roadmap and close)$' docs/FLARE_1ON1_LANDING_WALKTHROUGH_CUES.md)" -eq 7
test "$(rg -c 'Master cue:' docs/FLARE_1ON1_LANDING_WALKTHROUGH_CUES.md)" -eq 7
rg -n 'x402|EIP-3009|EIP-1271|FCC|Credential|Vault|REAL Confidential Space' docs/FLARE_1ON1_LANDING_WALKTHROUGH_CUES.md
rg -n '3 x 0\.10|0\.40 vs 0\.35 rolling budget|remaining 0\.70' docs/FLARE_1ON1_LANDING_WALKTHROUGH_CUES.md
rg -n 'host confidentiality, signing-key isolation, hardware attestation' docs/FLARE_1ON1_LANDING_WALKTHROUGH_CUES.md
```

Expected: both count checks pass; every required technical term, proof figure, and limitation appears.

- [ ] **Step 4: Verify copy and scope**

Run:

```bash
LC_ALL=C perl -CSDA -ne 'exit 1 if /\x{2013}|\x{2014}/' docs/FLARE_1ON1_LANDING_WALKTHROUGH_CUES.md
awk '!/^#/ && !/^\[/ && !/^\*/ && !/^- `docs\// {gsub(/[-*]/, ""); count += NF} END {print count; exit !(count >= 150 && count <= 200)}' docs/FLARE_1ON1_LANDING_WALKTHROUGH_CUES.md
git diff --check
git diff --exit-code -- docs/FLARE_1ON1_LANDING_WALKTHROUGH.md
git status --short
```

Expected: 150 to 200 cue words; no em or en dashes; no whitespace errors; the full walkthrough remains unchanged; only the new cue sheet and pre-existing `.claude/` entry appear outside committed planning files.

- [ ] **Step 5: Review the cue sheet as a speaking aid**

Read it top to bottom and confirm:

- each master cue can be located in one glance;
- every nested prompt supplies a concrete fact or speaking direction;
- the prompts support improvisation instead of reading like a second script;
- the simulated TEE disclosure is visually prominent and technically intact.

Expected: all four checks pass without adding unsupported claims.

- [ ] **Step 6: Commit the cue sheet**

```bash
git add docs/FLARE_1ON1_LANDING_WALKTHROUGH_CUES.md
git commit -m "docs: add landing walkthrough cue sheet"
```

Expected: one commit containing only the new cue sheet.
