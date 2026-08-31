# Flare one-to-one landing-page walkthrough: AgentVault

*Target runtime: approximately two minutes 30 seconds*

## Before the call

[Open the landing page at the top. Let the hero animation settle before you begin.]

## Hero

[Keep the hero and Agent/Owner terminal visible.]

I built AgentVault around a question: how can an AI agent pay for an API without putting a private key in its runtime? It is a spending-authority layer for standard x402 on Flare. The Owner keeps funds in a Vault. The agent gets a revocable Credential, can request payments, but never signs or sends a transaction.

## Problem

[Scroll to "The layer x402 doesn't define."]

I start from x402's gap: it standardizes how an API asks for payment and how that payment settles, but does not decide where the agent's spending authority lives or who enforces limits. A private key in an LLM-driven process turns prompt injection, tool misuse, loops, and replay into financial risk.

## Mechanism

[Scroll to "How AgentVault works" and point across the diagram.]

The way I structured the flow separates payment requests from signing authority. The Owner deposits USDT0 and sets policy. The agent sends an encrypted request with its Credential. A registered Flare Confidential Compute machine checks policy and signs EIP-3009 only when it passes. The Vault verifies the machine and payment terms through EIP-1271, then standard x402 settlement pays the Vendor.

## Rules

[Scroll to "The rules behind every payment."]

I put four controls behind the boundary: a Vendor allowlist, rolling budget, maximum payment, and rate limit. I wanted the agent to see only paid or declined, so it cannot inspect rules and adapt around them. The Owner monitor sees the verified policy reason.

[Flip the "Rolling budget window" card to Owner view.]

## Demo and proof

[Point back to the rolling-budget result, then scroll through "Watch the demo."]

In my Coston2 run, three payments of 0.10 USDT0 settled. A fourth would have taken spending to 0.40, above the Owner's 0.35 rolling budget, so it was declined before settlement. The Owner then paused spending and withdrew the remaining 0.70. This was simulated TEE mode. The settlement and policy path were verified, but host confidentiality, signing-key isolation, and hardware attestation did not hold. Those properties require REAL Confidential Space.

## Self-host and build summary

[Scroll past the detailed commands to "Built during Flare Summer Signal."]

I keep AgentVault self-hosted today. The page includes setup and demo path; the short version is the Owner keeps funds and the agent never receives the payment key.

## Roadmap and close

[Scroll to "What's next."]

My next step is a hosted option that keeps self-hosting available, followed by a small fee only on approved payments. I would value your take: does this Owner and agent boundary feel right for Flare developers, and what would make a hosted version useful inside the ecosystem?

## Sources

- `index.html`
- `/Users/liampereira/Documents/Code/agent-vault/docs/AGENTVAULT_NORTH_STAR.md`
