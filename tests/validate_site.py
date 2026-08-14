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
    "learns only whether each payment succeeded",
    "failedRuleIds",
    "vendor-allowlist",
    "rate-limit",
    # Honest SIMULATED-mode disclosure (README "Why it matters")
    "SIMULATED",
    "can see secrets",
    "hardware attestation is not real",
    # Deployment facts
    "chain ID 114",
    "Mock USDT0",
    "0.35",
    # Positioning and CTAs
    "Private",
    "Verifiable",
    "Non-custodial",
    "prompt injection",
    "Watch the demo",
    "Run your own",
    "Flare Summer Signal",
    "Flare Confidential Compute Track",
    # README-aligned walkthrough framing
    "four blind-agent rule runs",
    "Codex or Claude",
    "This video follows the README walkthrough",
]

REQUIRED_SCRIPT_PHRASES = [
    "0x5000…0510 · PRODUCTION",
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
]

REQUIRED_FILES = [
    "index.html",
    "styles.css",
    "script.js",
    "assets/fonts/fonts.css",
    "assets/fonts/space-grotesk-400.ttf",
    "assets/fonts/ibm-plex-mono-400.ttf",
    "assets/images/agentvault-wordmark.png",
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
    "https://coston2-explorer.flare.network/address/0x5A2eb4224224aBfF6D47f4369801e6f5fb828c1C",
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

    if re.search(r"payment key", html, re.IGNORECASE) and "payment-signing" not in html:
        errors.append("hero should use private key language, not bare payment key")

    css = read(ROOT / "styles.css") if (ROOT / "styles.css").is_file() else ""
    if "prefers-reduced-motion" not in css:
        errors.append("styles.css must respect prefers-reduced-motion")

    if (ROOT / "script.js").is_file():
        js = read(ROOT / "script.js")
        if "prefers-reduced-motion" not in js:
            errors.append("script.js must respect prefers-reduced-motion")
        for phrase in REQUIRED_SCRIPT_PHRASES:
            if phrase not in js:
                errors.append(f"missing required script phrase: {phrase!r}")

    if errors:
        print("validate_site.py: FAIL")
        for err in errors:
            print(f"  - {err}")
        return 1

    print("validate_site.py: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
