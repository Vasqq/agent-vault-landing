# Flare one-to-one landing-page walkthrough: AgentVault

*Target runtime: approximately two minutes 30 seconds*

## Before the call

[Open the landing page at the top. Let the hero animation settle before you begin.]

## Hero

[Keep the hero and Agent/Owner terminal visible.]

AgentVault started with a question: how can an AI agent pay for an API without putting a private key inside its runtime? It is a spending-authority layer for standard x402 on Flare. The Owner keeps funds in a Vault. The agent gets a revocable Credential and can request payments, but never signs or sends a transaction.

## Problem

[Scroll to "The layer x402 doesn't define."]

x402 standardizes how an API asks for payment and how that payment settles. It does not decide where the agent's spending authority lives or who enforces limits. If a private key sits inside an LLM-driven process, prompt injection, tool misuse, loops, and replay become financial risk.

## Mechanism

[Scroll to "How AgentVault works" and point across the diagram.]

The flow separates requesting a payment from the authority to sign it. The Owner deposits USDT0 and sets the policy. The agent sends an encrypted request with its Credential. A registered Flare Confidential Compute machine checks the policy and signs EIP-3009 only when a request passes. The Vault verifies the machine and payment terms through EIP-1271, then standard x402 settlement pays the Vendor.

## Rules

[Scroll to "The rules behind every payment."]

There are four controls: a Vendor allowlist, rolling budget, maximum payment, and rate limit. The visibility boundary matters. The agent sees only paid or declined, so it cannot inspect the rules and adapt around them. The Owner monitor sees the verified policy reason.

[Flip the "Rolling budget window" card to Owner view.]

## Demo and proof

[Point back to the rolling-budget result, then scroll through "Watch the demo."]

In the Coston2 run, three payments of 0.10 USDT0 settled. A fourth would have taken spending to 0.40, above the Owner's 0.35 rolling budget, so it was declined before settlement. The Owner then paused spending and withdrew the remaining 0.70. This run used simulated TEE mode. The settlement and policy path were verified, but host confidentiality, signing-key isolation, and hardware attestation did not hold. Those properties require REAL Confidential Space.

## Self-host and build summary

[Scroll past the detailed commands to "Built during Flare Summer Signal."]

AgentVault is self-hosted today. The page includes the setup and demo path, but the short version is that the Owner keeps the funds and the agent never receives the payment key.

## Roadmap and close

[Scroll to "What's next."]

The next product step is a hosted option, while keeping self-hosting available, followed by a small fee only on approved payments. I would value your take on two things: does this Owner and agent boundary feel right for Flare developers, and what would make a hosted version useful inside the ecosystem?

## Sources

- `index.html`
- `/Users/liampereira/Documents/Code/agent-vault/docs/AGENTVAULT_NORTH_STAR.md`
