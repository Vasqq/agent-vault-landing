# Flare one-to-one landing-page walkthrough script

## Purpose

Create a conversational two to three minute script for an informal one-to-one call with a Flare developer. The speaker will present AgentVault by scrolling through the existing landing page instead of using a slide deck.

## Scope

- Add one new walkthrough script under `docs/` in the landing-page repository.
- Do not modify the landing page, presentation source, styles, JavaScript, or existing copy.
- Use only claims and proof already supported by the landing page and AgentVault documentation.
- Keep the simulated TEE limitation explicit: the testnet settlement and policy path were demonstrated, but host confidentiality, key isolation, and hardware attestation were not.

## Walkthrough route

The script follows the page in its current scroll order:

1. Hero: introduce AgentVault as the spending-authority layer between an AI agent and the Owner's funds.
2. Problem: explain what x402 standardizes and the spending-authority question it leaves open.
3. Mechanism: follow the Owner, Agent, FCC machine, Vault, and standard x402 settlement path.
4. Rules: name the four controls and use the rolling-budget card to show the different Agent and Owner views.
5. Demo and proof: state the Coston2 result, then give the simulated TEE disclosure.
6. Self-host and build summary: establish that the project can be run today without narrating the detailed setup commands.
7. Roadmap and close: explain the hosted direction and ask the Flare developer for feedback.

## Format and pacing

- Target 300 to 360 spoken words, approximately two to three minutes.
- Put short interaction cues on their own lines, such as `[scroll to Problem]` and `[flip the Rolling budget window card to Owner view]`.
- Keep interaction cues outside the spoken word count.
- Use first-person, plain English, and a conversational technical tone.
- Avoid investor language, inflated claims, em dashes, and generic marketing copy.
- End with two concrete feedback questions rather than a fundraising ask.

## Output

Create `docs/FLARE_1ON1_LANDING_WALKTHROUGH.md` with:

- a one-line runtime target;
- a short pre-call setup note;
- the word-for-word script divided by landing-page section;
- explicit scroll and interaction cues;
- a final source note identifying the landing page and AgentVault North Star as the claim basis.

## Acceptance checks

- The spoken copy is between 300 and 360 words.
- The route follows the current landing-page section order.
- The script covers the four policy rules, Coston2 proof, Owner exit, and hosted roadmap.
- The simulated TEE disclosure states that host confidentiality and hardware attestation do not hold in the recorded run.
- The script contains no em or en dashes.
- No files outside the new design note and final walkthrough script are changed.
