# Accurate Mechanism Diagram Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Correct the mechanism SVG so private policy goes to FCC, one Vault verifies and pays, and Vendor is the payee.

**Architecture:** The SVG remains an inline, two-row diagram in `index.html`. The existing Python content validator gains positive and negative topology assertions so the diagram cannot regress to policy-in-Vault, two-Vault, or standalone-EIP-3009 representations.

**Tech Stack:** Static HTML/SVG, CSS (unchanged), Python standard-library validator, Node syntax checker.

## Global Constraints

- Do not change the existing diagram design, colors, fonts, box style, or layout language.
- Do not alter any landing-page section outside the mechanism SVG and its accessible label.
- Use one Vault box; show Owner funding Vault and setting private policy on FCC.
- Fold EIP-3009 into the FCC-to-Vault arrow and name the Vendor payee.

---

### Task 1: Add an accuracy regression guard

**Files:**
- Modify: `tests/validate_site.py`

**Interfaces:**
- Consumes: the complete `index.html` string already read by `validate_site.py`.
- Produces: a failed validator run if the corrected topology labels are absent or obsolete diagram labels return.

- [x] **Step 1: Write the failing test**

Add these required diagram phrases and forbidden obsolete phrases to the validator:

```python
REQUIRED_PHRASES += [
    "set private policy",
    "EIP-1271 verify + pay",
    "signs x402 (EIP-3009)",
    "Vendor",
    "x402 settle",
]

FORBIDDEN_DIAGRAM_PHRASES = [
    "fund · policy",
    '<text x="440" y="113" fill="#e8eaee" font-family="IBM Plex Mono, monospace" font-size="11" text-anchor="middle">EIP-3009</text>',
]
```

- [x] **Step 2: Run test to verify it fails**

Run: `python3 tests/validate_site.py`

Expected: FAIL because the existing SVG has no `set private policy`, `EIP-1271 verify + pay`, or `signs x402 (EIP-3009)` labels.

- [x] **Step 3: Write minimal implementation**

Replace only the SVG node and arrow text in `index.html` with the approved five-node topology, and update the SVG container `aria-label` to describe the same flow.

- [x] **Step 4: Run test to verify it passes**

Run: `python3 tests/validate_site.py && node --check script.js && git diff --check`

Expected: `validate_site.py: PASS` with no JavaScript syntax or whitespace errors.

- [x] **Step 5: Commit**

Do not commit unless the user explicitly asks. The working tree contains unrelated in-progress changes.
