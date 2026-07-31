#!/usr/bin/env python3
"""Validate AgentVault landing page claims, assets, and metadata."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PHRASES = [
    "Your AI agent gets a budget,",
    "not a private key.",
    "spending-authority layer for standard",
    "private key ever entering the agent runtime",
    "Private",
    "Verifiable",
    "Non-custodial",
    "No agent wallet custody",
    "Budget window",
    "Flare Confidential Compute Track",
    "mock USDT0",
    "0.35",
    "0.70",
    "Flare Confidential Compute",
    "EIP-1271",
    "EIP-3009",
    "prompt injection",
    "Watch the demo",
    "Flare Summer Signal",
]

FORBIDDEN_PHRASES = [
    "npm install @agentvault/sdk",
    "impossible to drain",
    "physically cannot spend",
    "production confidentiality",
    "connected LLM",
    "public hard limits",
    "daily cap",
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
    "skills/frontend-design/SKILL.md",
]

REQUIRED_LINKS = [
    "https://docs.x402.org/introduction",
    "https://dev.flare.network/fcc/overview",
    "https://eips.ethereum.org/EIPS/eip-1271",
    "https://eips.ethereum.org/EIPS/eip-3009",
    "https://coston2-explorer.flare.network/address/0x5A2eb4224224aBfF6D47f4369801e6f5fb828c1C",
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

    if "https://x.com/agentvault_flr/status/2083192963287372177" not in html:
        errors.append("demo CTA must link to the live X demo post")

    if re.search(r"payment key", html, re.IGNORECASE) and "payment-signing" not in html:
        errors.append("hero should use private key language, not bare payment key")

    css = read(ROOT / "styles.css") if (ROOT / "styles.css").is_file() else ""
    if "prefers-reduced-motion" not in css:
        errors.append("styles.css must respect prefers-reduced-motion")

    if (ROOT / "script.js").is_file():
        js = read(ROOT / "script.js")
        if "prefers-reduced-motion" not in js:
            errors.append("script.js must respect prefers-reduced-motion")

    if errors:
        print("validate_site.py: FAIL")
        for err in errors:
            print(f"  - {err}")
        return 1

    print("validate_site.py: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
