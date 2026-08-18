#!/usr/bin/env python3
"""Validate AgentVault landing page claims, assets, and metadata."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PHRASES = [
    # Headline framing (README H1)
    "The authority layer between",
    "AI agents and your money.",
    "spending-authority layer for standard x402 on Flare",
    "private key ever entering the agent runtime",
    # Mechanism (README "When the Agent needs to pay ...")
    "revocable Credential instead of a private key",
    "Owner-run Gateway",
    "EIP-1271 contract signer",
    "Flare Confidential Compute",
    "EIP-1271",
    "EIP-3009",
    # The four private policy rules, exact README names
    "vendor allowlist",
    "maximum payment",
    "rolling budget window",
    "rate limit",
    # Agent-blind property and refusal asymmetry
    "blind to policy details",
    "The agent knows only whether each payment succeeded",
    "Pay a data provider that isn't on the Owner's approved list.",
    "3× PAID, then DECLINED",
    "Buy a report priced at $0.50.",
    "4× PAID, then DECLINED",
    "3× AUTHORIZED, then DECLINED",
    "4× AUTHORIZED, then DECLINED",
    "not on the Owner's approved vendor allowlist.",
    "above the $0.35 rolling budget.",
    "exceeds the $0.15 limit for any single payment.",
    "policy allows only four payments per hour.",
    "0.35",
    # Positioning and CTAs
    "Private",
    "Verifiable",
    "Non-custodial",
    "prompt injection",
    "Watch the demo",
    "Self-host AgentVault",
    "Flare Summer Signal",
    "Flare Confidential Compute Track",
    # README-aligned walkthrough framing
    "Four private policies. Four distinct declines.",
    "Codex or Claude",
    "Follow the README from setup to proof.",
    # Self-hosting hierarchy
    "Prerequisites",
    "Install these before cloning AgentVault.",
    "Setup",
    "Demo walkthrough",
    "Use two terminal windows:",
    "agentvault up --check --mcp-client codex",
    "./scripts/agentvault-vendors.sh --wait-ready",
    "Phase B policy",
    "vendor-allowlist",
    "budget-window",
    "max-per-payment",
    "rate-limit",
]

REQUIRED_SCRIPT_PHRASES = [
    "caption:",
    "private budget",
    "not approved",
    "request limit",
    "attempt_id:",
    "instruction_id:",
    "envelope:",
    "VERIFIED",
    "rule fired:",
]

REQUIRED_DIAGRAM_PHRASES = [
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

FORBIDDEN_SCRIPT_PHRASES = [
    "agent · task",
    "owner · monitor",
    "Agent sees no rule name, budget, or counter.",
    "ActionResult · verified",
    "owner-monitor decrypt",
    "failedRuleIds=",
]

FORBIDDEN_PHRASES = [
    "npm install @agentvault/sdk",
    "impossible to drain",
    "physically cannot spend",
    "production confidentiality",
    "connected LLM",
    "public hard limits",
    "daily cap",
    "Next: MCP integration",
    "tripped by <strong>4 blind agents</strong>",
    "0xa417…3Be5",
    "Demo environment: Coston2 (chain ID 114) with Mock USDT0",
    "View AgentVault on the Coston2 Explorer",
    "This is the condensed setup path.",
]

REQUIRED_FILES = [
    "index.html",
    "styles.css",
    "script.js",
    "assets/fonts/fonts.css",
    "assets/fonts/space-grotesk-400.ttf",
    "assets/fonts/ibm-plex-mono-400.ttf",
    "assets/images/agentvault-wordmark.png",
    "assets/images/Flare_FLR_Logo_full.png",
    "assets/images/social-card.png",
    "social/LAUNCH_POST.md",
    "docs/DESIGN_PLAN.md",
    "docs/EVIDENCE.md",
    "skills/frontend-design/SKILL.md",
]

REQUIRED_LINKS = [
    "https://docs.x402.org/introduction",
    "https://dev.flare.network/fcc/overview",
    "https://eips.ethereum.org/EIPS/eip-1271",
    "https://eips.ethereum.org/EIPS/eip-3009",
    "https://faucet.flare.network/coston2",
    "https://github.com/vasqq/agent-vault",
    "https://github.com/vasqq/agent-vault#quickstart",
    "https://youtu.be/BUQQIvgCKFQ",
]

REQUIRED_META = [
    'property="og:title"',
    'property="og:description"',
    'name="twitter:card"',
    'content="summary_large_image"',
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> int:
    errors: list[str] = []

    for rel in REQUIRED_FILES:
        if not (ROOT / rel).is_file():
            errors.append(f"missing required file: {rel}")

    if not (ROOT / "index.html").is_file():
        print("FAIL: index.html not found")
        return 1

    html = read(ROOT / "index.html")

    for phrase in REQUIRED_PHRASES:
        if phrase not in html:
            errors.append(f"missing required phrase: {phrase!r}")

    for phrase in REQUIRED_DIAGRAM_PHRASES:
        if phrase not in html:
            errors.append(f"missing required diagram phrase: {phrase!r}")

    for phrase in FORBIDDEN_DIAGRAM_PHRASES:
        if phrase in html:
            errors.append(f"obsolete diagram content present: {phrase!r}")

    if html.count(">Vault</text>") != 1:
        errors.append("mechanism diagram must contain exactly one Vault node")

    if html.count("<polyline") < 2:
        errors.append("mechanism diagram must use orthogonal routes for policy and signing")

    if 'points="400,116 625,116 625,65"' not in html:
        errors.append("mechanism diagram must route the signing line right, then up into the Vault")

    if 'x1="700" y1="36" x2="775" y2="36"' not in html:
        errors.append("mechanism diagram must settle directly from Vault to Vendor")

    if 'stroke-dasharray="5 4"' not in html or '>AgentVault</text>' not in html:
        errors.append("mechanism diagram must show a labeled dashed AgentVault system boundary")

    if html.count('class="diagram-node--external"') != 3:
        errors.append("mechanism diagram must style Owner, Agent, and Vendor as external actors")

    if html.count('class="diagram-node--internal"') != 2:
        errors.append("mechanism diagram must style FCC machine and Vault as internal components")

    for phrase in FORBIDDEN_PHRASES:
        if phrase.lower() in html.lower():
            errors.append(f"forbidden stale claim present: {phrase!r}")

    for link in REQUIRED_LINKS:
        if link not in html:
            errors.append(f"missing required link: {link}")

    for meta in REQUIRED_META:
        if meta not in html:
            errors.append(f"missing required meta tag fragment: {meta}")

    if "https://youtu.be/BUQQIvgCKFQ" not in html:
        errors.append("demo CTAs must link to the final YouTube demo")

    if "https://x.com/agentvault_flr/status/2083192963287372177" in html:
        errors.append("stale X demo link remains")

    if 'id="hero-stage-caption"' not in html:
        errors.append("hero scenario caption must have a dynamic target")

    if re.search(r"payment key", html, re.IGNORECASE) and "payment-signing" not in html:
        errors.append("hero should use private key language, not bare payment key")

    css = read(ROOT / "styles.css") if (ROOT / "styles.css").is_file() else ""
    if "prefers-reduced-motion" not in css:
        errors.append("styles.css must respect prefers-reduced-motion")
    if ".run-steps > li" not in css:
        errors.append("nested setup instructions must not inherit the main step counter layout")
    if ".run-steps .step-list li::before" not in css:
        errors.append("nested setup instructions must suppress inherited zero-padded counters")
    if ".run-steps.demo-steps--phase-b" not in css:
        errors.append("Phase B demo tasks must continue the walkthrough counter")
    if ".monitor-decline-dot" not in css:
        errors.append("Owner monitor decline indicator must have a dedicated animated state")

    if (ROOT / "script.js").is_file():
        js = read(ROOT / "script.js")
        if "prefers-reduced-motion" not in js:
            errors.append("script.js must respect prefers-reduced-motion")
        for phrase in REQUIRED_SCRIPT_PHRASES:
            if phrase not in js:
                errors.append(f"missing required script phrase: {phrase!r}")
        for phrase in FORBIDDEN_SCRIPT_PHRASES:
            if phrase in js:
                errors.append(f"forbidden stale script phrase present: {phrase!r}")

    if errors:
        print("validate_site.py: FAIL")
        for err in errors:
            print(f"  - {err}")
        return 1

    print("validate_site.py: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
