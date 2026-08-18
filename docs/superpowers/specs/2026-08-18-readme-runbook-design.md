# README Runbook Design

## Goal

Make the landing page's Run section a faithful, usable presentation of the root `agent-vault/README.md` Quickstart instead of a condensed alternative.

## Structure

Keep the existing prerequisites block, then split the guide into two labeled subsections:

- **Setup:** README Quickstart steps 1–9. Use the page's numbered step pattern, one title per README step, a short README-derived instruction or reason before each command, separate Codex and Claude commands, and the README's safety and wait-state notes.
- **Demo walkthrough:** README Quickstart step 10. Preserve the Phase A and Phase B policy boundaries, every copyable agent task, expected outcome, the policy update, and the Owner-monitor restart.

## Copy rules

- `../agent-vault/README.md` is the source of truth.
- Preserve commands and agent prompts verbatim, except for HTML escaping.
- Keep labels and connective prose plain; do not add marketing language.
- Remove the current condensed five-step guide and its statement that it is condensed.

## Presentation

Continue the existing terminal-editorial system: sharp dividers, numbered setup steps, mono command blocks, and responsive single-column behavior. Add no new card language or decorative visual system.

## Verification

- Update the validator to require the two subheadings and representative README-only commands/prompts.
- Verify the old condensed wording is gone.
- Run `python3 tests/validate_site.py` and `git diff --check`.
