# Flare one-to-one landing-page walkthrough cue sheet

## Purpose

Create a glanceable speaking aid from the existing landing-page walkthrough. It should help the presenter recover the point of each section, then speak naturally instead of reading complete sentences.

## Scope

- Add one cue sheet under `docs/` in the landing-page repository.
- Keep the full walkthrough script unchanged.
- Do not modify the landing page or presentation source.
- Use only facts, terminology, figures, and limitations already present in the full walkthrough.

## Structure

Follow the same seven-section route as the full walkthrough:

1. Hero
2. Problem
3. Mechanism
4. Rules
5. Demo and proof
6. Self-host and build summary
7. Roadmap and close

Each section contains:

- one page-action cue in square brackets;
- one short master cue that names the section's main talking point;
- nested factual prompts that give the presenter enough substance to elaborate accurately.

## Cue style

- Use fragments, labels, and short clauses rather than complete spoken sentences.
- Keep master cues easy to find while glancing at the document.
- Include enough detail to support natural improvisation without recreating the full script.
- Preserve exact technical terms where they matter, including x402, EIP-3009, EIP-1271, FCC, Credential, Vault, and REAL Confidential Space.
- Preserve the exact demo figures: three payments of 0.10 USDT0, a 0.35 rolling budget, a declined fourth payment at 0.40, and a remaining 0.70 withdrawal.
- Keep the simulated TEE disclosure explicit and impossible to overlook.
- Avoid polished marketing language, filler, em dashes, and en dashes.

## Output

Create `docs/FLARE_1ON1_LANDING_WALKTHROUGH_CUES.md` as a separate companion to `docs/FLARE_1ON1_LANDING_WALKTHROUGH.md`.

Target approximately 150 to 200 cue words, excluding headings and page-action cues.

## Acceptance checks

- The cue sheet follows the landing page in the same order as the full script.
- Every section has one master cue and supporting prompts.
- Prompts are not full script sentences.
- All claims can be traced to the existing walkthrough.
- The policy rules, proof figures, Owner exit, simulated TEE limits, roadmap, and feedback question remain available at a glance.
- The full script, landing page, and presentation remain unchanged.
