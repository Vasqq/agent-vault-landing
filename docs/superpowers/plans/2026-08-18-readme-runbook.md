# README Runbook Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the condensed Run guide with the full, readable README setup and demo walkthrough.

**Architecture:** `index.html` remains the single content source for the landing page. `styles.css` extends the existing Run-section patterns for subsection and walkthrough content. `tests/validate_site.py` guards against regression to condensed or incomplete instructions.

**Tech Stack:** Static HTML, CSS, Python validator.

## Global Constraints

- Use `../agent-vault/README.md` as the source of truth.
- Preserve README commands and agent prompts verbatim except required HTML escaping.
- Maintain the existing terminal-editorial design language and mobile responsiveness.
- Do not retain the condensed guide or claim that the page is condensed.

---

### Task 1: Add coverage for the full guide

**Files:**
- Modify: `tests/validate_site.py`

- [ ] Add required text checks for `Setup`, `Demo walkthrough`, the two-terminal instruction, `agentvault up --check --mcp-client codex`, `./scripts/agentvault-vendors.sh --wait-ready`, the Phase B policy label, and the four README rule identifiers.
- [ ] Add a forbidden-text check for `This is the condensed setup path.`
- [ ] Run `python3 tests/validate_site.py` and confirm it fails only because the full-guide content is absent.

### Task 2: Render the README setup sequence

**Files:**
- Modify: `index.html`

- [ ] Replace the existing condensed ordered list with a `Setup` subsection containing README steps 1–9 in order.
- [ ] Put each README step title above its copyable command block and place README-derived reason, safety, or wait-state content before the command it explains.
- [ ] Include separate commands for Codex and Claude in steps 3, 4, and 9.
- [ ] Retain the Credential and Policy digest distinction, second Vendor, Owner monitor, and two-terminal instructions.

### Task 3: Render the README demo walkthrough

**Files:**
- Modify: `index.html`

- [ ] Add a `Demo walkthrough` subsection after Setup.
- [ ] Include the Phase A policy, four exact agent prompts, their expected results, the Phase B policy update, and monitor restart in the original README order.
- [ ] Remove the old condensed-path note.

### Task 4: Style and verify the long-form guide

**Files:**
- Modify: `styles.css`
- Test: `tests/validate_site.py`

- [ ] Add only the layout rules necessary to distinguish the two subsections and long walkthrough prompts while preserving the current sharp, mono-oriented system.
- [ ] Add a mobile override for any new multi-column rules.
- [ ] Run `python3 tests/validate_site.py` and `git diff --check`; both must succeed.
