# Accurate Mechanism Diagram Design

## Goal

Correct the "How AgentVault works" SVG topology without changing its visual design or any other landing-page section.

## Approved diagram content

The existing two-row monochrome SVG keeps its box, line, arrow, typography, and layout language. It has five nodes: Owner, a single Vault, Agent, FCC machine, and Vendor.

- Owner to Vault is labeled `fund`; the Vault subtext includes `EIP-1271 verify + pay`.
- Owner to FCC machine is labeled `set private policy`.
- Agent to FCC machine is labeled `encrypted request`; Agent retains `Credential` subtext.
- FCC machine retains `4 private rules` and sends `signs x402 (EIP-3009)` to the Vault.
- Vault settles to Vendor, whose subtext is `x402 settle`.
- There is no standalone EIP-3009 node, no second Vault node, and no caption below the diagram.

## Constraints

- Modify only the mechanism SVG, its accessible description, and its focused landing-copy validation.
- Do not change CSS, colors, fonts, box style, layout language, or any other section.
- Preserve the current simple two-row composition.

## Verification

The landing validator must require the corrected labels and reject the obsolete standalone EIP-3009 node and Vault policy label. The site validator, JavaScript syntax check, and whitespace diff check must pass.
