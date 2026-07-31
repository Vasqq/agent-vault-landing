# AgentVault Landing — Design Plan (frontend-design skill)

## Subject grounding
- **Subject:** AgentVault, a Flare FCC spending-authority layer for agentic x402 payments.
- **Audience:** Crypto-literate retail and developers (private keys, prompt injection, testnets).
- **Single job:** Explain what AgentVault is and prove the Coston2 demo in one viewport, then drive to "Watch the demo."

## Token system

| Token | Value | Role |
|-------|-------|------|
| `--bg` | `#111318` | Page ground |
| `--panel` | `#1a1c22` | Receipt card, sections |
| `--panel-2` | `#20232a` | Nested surfaces |
| `--teal` | `#9bb9bb` | Verified, links, primary accent |
| `--text` | `#dadee8` | Body |
| `--muted` | `#90939b` | Secondary copy |
| `--red` | `#b77a7a` | Declined row only |
| `--blue` | `#8aa0be` | External protocol links |
| `--line` | `rgba(155,185,187,.24)` | Hairline rules |

**Type:** Space Grotesk (display + body), IBM Plex Mono (receipt, labels, amounts, statuses).

**Layout:** Demo-first split hero. Left: thesis + CTA. Right: live authorization receipt (the proof artifact). Below: problem → mechanism flow → Coston2 proof ledger → trust boundary → hackathon built → close.

**Signature element:** The authorization receipt — four payment rows that resolve in sequence on load (settled / settled / settled / declined). This is AgentVault's world: policy checks rendered as terminal output, not marketing cards.

**Aesthetic risk (justified):** Dense monospace receipt as the hero visual instead of a screenshot or gradient stat block. Matches build-in-public, proof-first positioning.

## Self-critique vs brief
- Avoided: purple gradients, Inter/Roboto, generic "3 stats + gradient" hero, numbered 01/02/03 decoration.
- Kept quiet: nav, section headers, hackathon badge — receipt carries the memory.
- Motion: one orchestrated receipt reveal only; respects `prefers-reduced-motion`.
