# README Content Alignment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the landing page an accurate, concise presentation of the README's connected four-policy Agent/Owner walkthrough.

**Architecture:** The README remains the factual source of truth. The landing page summarizes its proof and linked onboarding path; static HTML owns visible narrative and the animated hero owns only factual scenario data.

**Tech Stack:** Static HTML, CSS, vanilla JavaScript, Python assertion script.

## Global Constraints

- Preserve the current cyber-noir visual system and the final YouTube demo URL.
- Make no claim of real hardware confidentiality; retain the SIMULATED disclosure.
- Use the README's final Coston2 deployment identities and rule-lab terminology.
- The landing page must not suggest four separate agents or an executable quickstart that omits required README steps.

---

### Task 1: Lock README-aligned public claims in validation

**Files:**
- Modify: `tests/validate_site.py`

**Interfaces:**
- Consumes: `index.html` text and source URL literals.
- Produces: a non-zero exit when stale machine identity, standalone-demo framing, four-agent wording, or Claude-only quickstart copy returns.

- [x] **Step 1: Add failing assertions**

Require the final machine short hash `0x5000…0510`, the phrase `four blind-agent rule runs`, `Codex or Claude`, and the final-demo sentence beginning `This video follows the README walkthrough`. Reject `0xa417…3Be5` and `tripped by <strong>4 blind agents</strong>`.

- [x] **Step 2: Run the validator to verify it fails**

Run: `python3 tests/validate_site.py`

Expected: FAIL because the page still contains the stale hero identity and old proof framing.

- [x] **Step 3: Update validation only for README-backed claims**

Do not add copy requirements unrelated to the final README workflow.

- [x] **Step 4: Re-run the validator**

Run: `python3 tests/validate_site.py`

Expected: it still fails until Tasks 2 and 3 change the page.

### Task 2: Correct proof identity and represent the README architecture accurately

**Files:**
- Modify: `script.js`
- Modify: `index.html`

**Interfaces:**
- Consumes: README deployment identity `0x5000fbf0E824c19d3c99812007cDc5823dEB0510` and its four-rule model.
- Produces: a hero owner terminal that renders `0x5000…0510 · PRODUCTION`, and an accessible diagram that distinguishes funding from the Agent-request path.

- [x] **Step 1: Replace the stale dynamic machine identity**

In `renderScenarioShell`, replace `<dt>machine</dt><dd>0xa417…3Be5 · PRODUCTION</dd>` with `<dt>machine</dt><dd>0x5000…0510 · PRODUCTION</dd>`.

- [x] **Step 2: Revise the SVG connection topology**

Keep the existing nodes, but remove the implied `Vault → Agent` sequence. Show a separate Owner-to-Vault funding line, then a payment path `Agent → FCC machine → EIP-3009 → Vault → x402`; label the Agent node `Credential` and the FCC node `4 private rules`.

- [x] **Step 3: Preserve accessible narration**

Update the flow diagram's `aria-label` to describe the two lanes: Owner funds the Vault; the Agent requests with its Credential; FCC checks the private policy and signs; the Vault verifies and settles x402.

### Task 3: Reframe the demo and condensed onboarding around the README walkthrough

**Files:**
- Modify: `index.html`

**Interfaces:**
- Consumes: README steps 8–10 and the final YouTube link.
- Produces: a demo panel that says the video follows the README's connected two-terminal four-policy workflow, and onboarding that directs users to the README for either client and full rule lab.

- [x] **Step 1: Correct proof-bar wording**

Replace `tripped by 4 blind agents` with `four blind-agent rule runs`.

- [x] **Step 2: Replace standalone-demo wording**

Replace the current three-paid/fourth-budget-only paragraph with a concise statement that the video walks through README steps 8–10: Owner monitor and Agent terminal side by side; vendor allowlist, rolling budget window, maximum payment, and rate limit; Agent sees a flat result while the Owner sees the verified private cause. Retain the link to the YouTube walkthrough.

- [x] **Step 3: Clarify the setup is condensed**

State that the landing page commands are the setup path and that the README supplies the complete connected rule lab, including the second Vendor, ordered prompts, Phase B policy update, and Codex/Claude variants. Replace Claude-only commands with an explicit `<client>` placeholder and show `agentvault up --check --mcp-client <client>`, `agentvault up --mcp-client <client>`, and `agentvault agent start --client <client>`.

### Task 4: Verify source-level and visual-facing integrity

**Files:**
- Test: `tests/validate_site.py`

- [x] **Step 1: Run the landing-page validator**

Run: `python3 tests/validate_site.py`

Expected: `validate_site.py: PASS`.

- [x] **Step 2: Scan for stale evidence**

Run: `rg -n '0xa417…3Be5|tripped by <strong>4 blind agents</strong>|Watch the demo on X|agentvault_flr/status' index.html script.js tests/validate_site.py`

Expected: no matches.

- [x] **Step 3: Check patch whitespace and scope**

Run: `git diff --check && git diff -- index.html script.js tests/validate_site.py`

Expected: no whitespace errors; only the intended landing-page alignment changes plus this plan.
