#!/usr/bin/env python3
"""Validate AgentVault landing page claims, assets, and metadata."""

from __future__ import annotations

import gzip
import hashlib
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COPY_BASELINE = ROOT / "tests" / "fixtures" / "copy-baseline.txt"
COMMANDS_BASELINE = ROOT / "tests" / "fixtures" / "commands-baseline.json"

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
    # Aerarium revamp
    "docs/revamp/REVAMP_SPEC.md",
    "assets/fonts/cormorant-garamond-variable.woff2",
    "assets/fonts/cormorant-garamond-italic-variable.woff2",
    "assets/fonts/OFL-cormorant-garamond.txt",
    "assets/ascii/temple-hero.json",
    "assets/ascii/ring-key.json",
    "assets/ascii/coin.json",
    "assets/ascii/temple-wide.json",
    "tools/ascii/README.md",
]

# Spec section 5: name -> (cols, rows)
ASCII_GRIDS = {
    "temple-hero": (220, 125),
    "ring-key": (130, 66),
    "coin": (120, 66),
    "temple-wide": (330, 104),
}

# Spec section 3
AV_TOKENS = {
    "--av-bg": "#16130F",
    "--av-panel": "#1F1A15",
    "--av-well": "#100D0A",
    "--av-bronze": "#B08D57",
    "--av-bronze-hi": "#D8B67E",
    "--av-verdigris": "#6E9A8C",
    "--av-digital": "#5E8A7C",
    "--av-ok": "#86B3A3",
    "--av-decline": "#CF6A52",
    "--av-text": "#E8DFCC",
    "--av-muted": "#A69A86",
    "--av-label": "#7D9A8F",
    "--av-link": "#9FC2B5",
    "--av-line": "rgba(176,141,87,0.26)",
}

# Old aesthetic: must not come back in any shipped source file.
FORBIDDEN_SOURCE_STRINGS = [
    "#9bb9bb",
    "#7a9294",
    "fonts.googleapis.com",
    "ascii-vault.txt",
    "void-scan",
    "ascii-field",
    "setVaultState",
]

# Spec section 7: outlined Roman numerals replace "01 / Problem" indexes.
SECTION_HEADINGS = [
    ("problem", "I", "Problem"),
    ("mechanism", "II", "Mechanism"),
    ("rules", "III", "Rules"),
    ("demo-video", "IV", "Record"),
    ("get-started", "V", "Run"),
    ("built", "VI", "Delta"),
    ("roadmap", "VII", "Roadmap"),
]

REQUIRED_CSS_HOOKS = [".plate", ".btn-primary", ".btn-secondary", ".section-numeral"]

# SHA-256 of the hero SCENARIOS array as it was on main before the revamp.
# The cycler is restyled, never re-scripted (spec section 2).
SCENARIOS_SHA256 = "0e2fc99e7100fbb05934f5ce84c49c92edce8c39f9e4b31f9e610a81be7a2cc6"

HERO_PLATE = [
    "AERARIUM",
    "Temple of Saturn, Forum Romanum",
    "The treasury of Rome sat inside this temple. Money left it only on authority.",
]

SEAL_PHRASES = ["SPECTAVIT", "FCC · 114"]

# Spec section 7: Agent and Owner stack on mobile instead of switching tabs.
FORBIDDEN_HERO_STRINGS = ["mobile-pane-tabs", "pane-tab", "show-owner"]

# Spec section 8 plates for sections I to IV: name, place, sentence.
PLATES_I_IV = [
    ("CLAVIS ANULARIS", "Roman ring-key, bronze",
     "Romans wore the key to a strongbox on a finger. Whoever held the ring could open the chest."),
    ("TESSERA NUMMVLARIA", "Inspector’s tag, bone",
     "Tied to a sealed bag of coin and marked SPECTAVIT: this has been examined."),
    ("TABVLAE CERATAE", "Wax-tablet diptych",
     "Romans kept receipts on hinged wax tablets. Two leaves, one record."),
    ("INSCRIPTIO", "The public record",
     "What settles is carved where anyone can read it. Why it was refused is not."),
]

COIN_LANE_PHRASES = [
    "A payment, in motion · Approved",
    "A payment, in motion · Declined",
    "→ PAID",
    "← DECLINED · the funds stay in the Vault",
    "FCC checkpoint",
    "FCC · VERIFIED",
    "reason stays private",
]

RULES_PHRASES = [
    "Choose a rule to see what the Agent was told and what the Owner reads.",
    "Agent view",
    "Owner view",
    "what the Agent is told",
    "what the Owner reads",
]

# The flip cards and their hover hint are replaced by tabs and a diptych.
FORBIDDEN_RULES_STRINGS = ["Hover or tap a card", "rule-card", "rule-turn"]

MECHANISM_ACTORS = ["Owner", "Owner", "Agent", "FCC machine", "Vault"]

FRIEZE_TOKENS = [
    "AGENT_PAYMENT_LOOP_START",
    "PROVING_RULES_IN_TEE_ENVIRONMENT",
    "VERIFIED_BY_FLARE_NETWORK",
    "COSTON2_SETTLE_X402",
]

# Spec section 8 plates for Run, Roadmap and Close.
PLATES_V_CLOSE = [
    ("GRADVS", "The podium steps", "Nine steps up to your own treasury."),
    ("MILIARIVM", "Roman milestone", "Stone markers counted the miles along every Roman road."),
    ("AERARIUM", "Temple of Saturn, reconstructed", "The whole treasury, standing on new ground."),
]

ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]

# Spec section 9: page weight under ~400KB gzipped, social card excluded.
PAGE_BUDGET_BYTES = 400 * 1024

# Animated classes that must rest under prefers-reduced-motion (spec section 6).
REDUCED_MOTION_CLASSES = [".floater", ".coin-mover", ".tessera--pass", ".tessera--fail",
                          ".coin-phase--a", ".coin-phase--b", ".frieze-track", ".monitor-decline-dot"]

# Baseline copy that spec section 8 removes on purpose. Everything else in
# tests/fixtures/copy-baseline.txt must stay on the page.
COPY_BASELINE_RETIRED = {
    "01 / Problem",
    "02 / Mechanism",
    "03 / Rules",
    "04 / Record",
    "05 / Run",
    "06 / Delta",
    "07 / Roadmap",
    "Hover or tap a card to switch from the Agent's view to the Owner's.",
    # Misspelled X handle, corrected by Liam on 2026-09-26 (see X_HANDLE).
    "@itzbankotez",
}

# Footer credit, spelling confirmed by Liam on 2026-09-26.
X_HANDLE = "@itzbanknotez"
X_HANDLE_URL = "https://x.com/itzbanknotez"

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


VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
    "source", "track", "wbr",
}
NON_CONTENT_TAGS = {"script", "style", "template"}


class Node:
    def __init__(self, tag: str, attrs: dict[str, str], parent: "Node | None"):
        self.tag = tag
        self.attrs = attrs
        self.parent = parent
        self.children: list["Node | str"] = []

    @property
    def classes(self) -> list[str]:
        return self.attrs.get("class", "").split()

    def iter(self):
        yield self
        for child in self.children:
            if isinstance(child, Node):
                yield from child.iter()

    def find_all(self, pred) -> list["Node"]:
        return [n for n in self.iter() if pred(n)]

    def text(self) -> str:
        parts: list[str] = []
        for child in self.children:
            if isinstance(child, Node):
                if child.tag not in NON_CONTENT_TAGS:
                    parts.append(child.text())
            else:
                parts.append(child)
        return normalize(" ".join(parts))


class TreeBuilder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#root", {}, None)
        self.cur = self.root

    def handle_starttag(self, tag, attrs):
        node = Node(tag, {k: (v or "") for k, v in attrs}, self.cur)
        self.cur.children.append(node)
        if tag not in VOID_TAGS:
            self.cur = node

    def handle_startendtag(self, tag, attrs):
        self.cur.children.append(Node(tag, {k: (v or "") for k, v in attrs}, self.cur))

    def handle_endtag(self, tag):
        # Pop to the matching open tag; ignore stray end tags.
        node = self.cur
        while node is not None and node.tag != tag:
            node = node.parent
        if node is not None and node.parent is not None:
            self.cur = node.parent

    def handle_data(self, data):
        self.cur.children.append(data)


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def parse_html(html: str) -> Node:
    builder = TreeBuilder()
    builder.feed(html)
    builder.close()
    return builder.root


def visible_text_nodes(html: str) -> list[str]:
    """Text nodes a reader can see. Skips scripts, styles and aria-hidden art."""
    out: list[str] = []

    def walk(node: Node) -> None:
        if node.tag in NON_CONTENT_TAGS or node.attrs.get("aria-hidden") == "true":
            return
        for child in node.children:
            if isinstance(child, Node):
                walk(child)
            else:
                text = normalize(child)
                if text:
                    out.append(text)

    walk(parse_html(html))
    return out


def check_copy_baseline(html: str, errors: list[str]) -> None:
    if not COPY_BASELINE.is_file():
        errors.append(f"missing copy baseline: {COPY_BASELINE.relative_to(ROOT)}")
        return
    page_text = " ".join(visible_text_nodes(html))
    for line in read(COPY_BASELINE).splitlines():
        if not line or line.startswith("#") or line in COPY_BASELINE_RETIRED:
            continue
        if line not in page_text:
            errors.append(f"locked copy missing or changed: {line!r}")


def check_ascii_assets(errors: list[str]) -> None:
    for name, (cols, rows) in ASCII_GRIDS.items():
        path = ROOT / "assets" / "ascii" / f"{name}.json"
        if not path.is_file():
            continue
        try:
            data = json.loads(read(path))
        except json.JSONDecodeError as exc:
            errors.append(f"{name}.json is not valid JSON: {exc}")
            continue
        if (data.get("cols"), data.get("rows")) != (cols, rows):
            errors.append(f"{name}.json must be {cols}x{rows}")
        layers = data.get("layers", {})
        for layer in ("hi", "lo", "dg"):
            if layer not in layers:
                errors.append(f"{name}.json is missing the {layer} layer")
                continue
            if not layers[layer]:
                continue  # coin has an empty dg layer
            lines = layers[layer].split("\n")
            if len(lines) != rows or any(len(line) > cols for line in lines):
                errors.append(f"{name}.json {layer} layer does not fit its {cols}x{rows} grid")


def check_tokens(css: str, errors: list[str]) -> None:
    root_blocks = " ".join(re.findall(r":root\s*\{([^}]*)\}", css))
    for token, value in AV_TOKENS.items():
        match = re.search(re.escape(token) + r"\s*:\s*([^;]+);", root_blocks)
        found = re.sub(r"\s+", "", match.group(1)).lower() if match else None
        if found != value.lower():
            errors.append(f":root must define {token}: {value}")


def check_section_headings(tree: Node, errors: list[str]) -> None:
    for section_id, numeral, label in SECTION_HEADINGS:
        found = tree.find_all(lambda n: n.attrs.get("id") == section_id)
        if not found:
            errors.append(f"missing section #{section_id}")
            continue
        section = found[0]
        numerals = section.find_all(lambda n: "section-numeral" in n.classes)
        labels = section.find_all(lambda n: "section-label" in n.classes)
        if not numerals or numerals[0].text() != numeral:
            errors.append(f"#{section_id} must open with the outlined numeral {numeral}")
        if not labels or not labels[0].text().startswith(label):
            errors.append(f"#{section_id} must carry the section label {label!r}")


def check_header(tree: Node, errors: list[str]) -> None:
    wordmarks = tree.find_all(lambda n: "wordmark" in n.classes)
    if not wordmarks:
        errors.append("header must have a wordmark")
    else:
        mark = wordmarks[0]
        if mark.text() != "AgentVault" or mark.find_all(lambda n: n.tag == "img"):
            errors.append("wordmark must be the text AgentVault, not an image")
    toggles = tree.find_all(lambda n: "menu-toggle" in n.classes)
    if not toggles:
        errors.append("header must have a mobile menu button")
    else:
        toggle = toggles[0]
        target = toggle.attrs.get("aria-controls", "")
        if toggle.tag != "button" or "aria-expanded" not in toggle.attrs:
            errors.append("menu toggle must be a button with aria-expanded")
        if not target or not tree.find_all(lambda n: n.attrs.get("id") == target):
            errors.append("menu toggle aria-controls must point at the nav")


def desktop_diagram(html: str) -> str:
    """Slice of index.html holding only the desktop mechanism <svg>."""
    idx = html.find('id="mechanism-diagram"')
    if idx < 0:
        return html
    start = html.rfind("<svg", 0, idx)
    end = html.find("</svg>", idx)
    if start < 0 or end < 0:
        return html
    return html[start:end + len("</svg>")]


def check_ascii_figure(tree: Node, name: str, errors: list[str]) -> None:
    """Spec section 5: reserved em box, aria-hidden, three stacked layers."""
    cols, rows = ASCII_GRIDS[name]
    boxes = tree.find_all(lambda n: n.attrs.get("data-ascii") == name)
    if len(boxes) != 1:
        errors.append(f"page must hold exactly one data-ascii={name!r} figure")
        return
    box = boxes[0]
    hidden = box
    while hidden is not None and hidden.attrs.get("aria-hidden") != "true":
        hidden = hidden.parent
    if hidden is None:
        errors.append(f"{name} art must be aria-hidden")
    style = re.sub(r"\s+", "", box.attrs.get("style", ""))
    if f"--cols:{cols}" not in style or f"--rows:{rows}" not in style:
        errors.append(f"{name} box must reserve --cols:{cols} and --rows:{rows} inline")
    layers = [c for c in box.children if isinstance(c, Node) and c.tag == "pre"]
    order = [next((k for k in ("dg", "lo", "hi") if f"ascii-layer--{k}" in p.classes), None) for p in layers]
    if order != ["dg", "lo", "hi"]:
        errors.append(f"{name} must stack three <pre> layers in order dg, lo, hi")


def check_hero(tree: Node, html: str, css: str, js: str, errors: list[str]) -> None:
    check_ascii_figure(tree, "temple-hero", errors)

    if "calc(var(--cols) * 0.6em)" not in css or "calc(var(--rows) * 1em)" not in css:
        errors.append("ASCII boxes must be sized in em from --cols/--rows (no layout shift)")
    if "assets/ascii/" not in js or "fetch(" not in js:
        errors.append("script.js must load ASCII art from assets/ascii/ with fetch")
    if "rootMargin" not in js:
        errors.append("below-the-fold ASCII art must load lazily via IntersectionObserver")

    for phrase in HERO_PLATE:
        if phrase not in html:
            errors.append(f"missing hero plate copy: {phrase!r}")

    for phrase in SEAL_PHRASES:
        if phrase not in js:
            errors.append(f"Owner monitor seal must render {phrase!r} from the script shell")
    noscripts = tree.find_all(lambda n: n.tag == "noscript")
    fallback = " ".join(n.text() for n in noscripts)
    if not all(p in fallback for p in SEAL_PHRASES):
        errors.append("noscript fallback must include the SPECTAVIT seal")
    seals = tree.find_all(lambda n: "monitor-seal" in n.classes)
    if not seals or any(s.attrs.get("aria-hidden") != "true" for s in seals):
        errors.append("the SPECTAVIT seal must be aria-hidden")

    match = re.search(r"var SCENARIOS = \[.*?\n  \];", js, re.S)
    if not match or hashlib.sha256(match.group(0).encode()).hexdigest() != SCENARIOS_SHA256:
        errors.append("hero SCENARIOS data changed; the cycler is restyle-only")

    stage = tree.find_all(lambda n: "hero-stage-wrap" in n.classes)
    node = stage[0] if stage else None
    while node is not None and "hero-copy" not in node.classes and "hero-grid" not in node.classes:
        node = node.parent
    if not stage or node is not None:
        errors.append("the proof stage must sit below the hero copy at full content width")

    if not re.search(r"@keyframes\s+av-float\b", css):
        errors.append("styles.css must define the av-float floating-glyph animation")
    if "data-floaters" not in js or tree.find_all(lambda n: "floater" in n.classes):
        errors.append("floating glyphs must be generated by script.js, not hard-coded")

    for needle in FORBIDDEN_HERO_STRINGS:
        for name, text in (("index.html", html), ("styles.css", css), ("script.js", js)):
            if needle in text:
                errors.append(f"{needle!r} in {name}: Agent and Owner panels stack on mobile")


def by_id(tree: Node, node_id: str) -> "Node | None":
    found = tree.find_all(lambda n: n.attrs.get("id") == node_id)
    return found[0] if found else None


def check_mechanism(tree: Node, html: str, css: str, errors: list[str]) -> None:
    section = by_id(tree, "mechanism")
    if section is None:
        return
    order = [html.find('<ol class="flow"'), html.find('id="mechanism-diagram"'), html.find('class="coin-lane"')]
    if -1 in order or order != sorted(order):
        errors.append("#mechanism must run step cards, then the diagram, then the coin lane")

    actors = [n.text() for n in section.find_all(lambda n: "flow-actor" in n.classes)]
    if actors != MECHANISM_ACTORS:
        errors.append(f"mechanism step cards must carry actor labels {MECHANISM_ACTORS}")

    vertical = by_id(tree, "mechanism-diagram-vertical")
    if vertical is None or vertical.tag != "svg":
        errors.append("mechanism needs a vertical mobile SVG with id mechanism-diagram-vertical")
    else:
        v_html = html[html.find('id="mechanism-diagram-vertical"'):]
        v_html = v_html[:v_html.find("</svg>")]
        if "diagram-node--" in v_html:
            errors.append("the mobile diagram must use its own diagram-v-* class names")
    wrappers = section.find_all(lambda n: n.attrs.get("role") == "img")
    labels = {w.attrs.get("aria-label") for w in wrappers}
    if len(wrappers) != 2 or len(labels) != 1:
        errors.append("both diagram wrappers must be role=img with the same description")
    if not re.search(r"\.flow-diagram--vertical\s*\{[^}]*display:\s*none", css):
        errors.append("the mobile diagram must be display:none outside the mobile breakpoint")

    check_ascii_figure(tree, "coin", errors)
    for phrase in COIN_LANE_PHRASES:
        if phrase not in html:
            errors.append(f"missing coin lane copy: {phrase!r}")
    for name in ("av-coin", "av-stamp-pass", "av-stamp-fail", "av-phase-a", "av-phase-b"):
        if not re.search(r"@keyframes\s+" + name + r"\b", css):
            errors.append(f"coin lane keyframes {name} missing")


def check_rules(tree: Node, html: str, css: str, js: str, errors: list[str]) -> None:
    for phrase in RULES_PHRASES:
        if phrase not in html:
            errors.append(f"missing rules copy: {phrase!r}")
    for needle in FORBIDDEN_RULES_STRINGS:
        for name, text in (("index.html", html), ("styles.css", css), ("script.js", js)):
            if needle in text:
                errors.append(f"old flip-card remnant {needle!r} in {name}")

    lists = tree.find_all(lambda n: n.attrs.get("role") == "tablist")
    tabs = tree.find_all(lambda n: n.attrs.get("role") == "tab")
    panels = tree.find_all(lambda n: n.attrs.get("role") == "tabpanel")
    if len(lists) != 1 or len(tabs) != 4 or len(panels) != 4:
        errors.append("rules need one tablist with four tabs and four tabpanels")
        return
    shown = [p for p in panels if "hidden" not in p.attrs]
    if len(shown) != 1:
        errors.append("exactly one rule panel must be visible (no hidden attribute)")
    selected = [t for t in tabs if t.attrs.get("aria-selected") == "true"]
    if len(selected) != 1 or "Rule 02" not in selected[0].text():
        errors.append("Rule 02 must be the one selected tab by default")
    if shown and selected and shown[0].attrs.get("id") != selected[0].attrs.get("aria-controls"):
        errors.append("the visible rule panel must belong to the selected tab")
    for tab in tabs:
        panel = by_id(tree, tab.attrs.get("aria-controls", ""))
        if panel is None or panel.attrs.get("aria-labelledby") != tab.attrs.get("id"):
            errors.append("each rule tab must control a panel labelled by that tab")
            break
    for key in ("ArrowLeft", "ArrowRight", "Home", "End"):
        if key not in js:
            errors.append(f"rule tabs must handle the {key} key")


def check_sections_i_iv(tree: Node, errors: list[str]) -> None:
    for name, place, sentence in PLATES_I_IV:
        plates = tree.find_all(lambda n: "plate" in n.classes and name in n.text())
        if not plates or place not in plates[0].text() or sentence not in plates[0].text():
            errors.append(f"missing plate {name} with its place and sentence")
    check_ascii_figure(tree, "ring-key", errors)

    friezes = tree.find_all(lambda n: "frieze" in n.classes)
    if not friezes or friezes[0].attrs.get("aria-hidden") != "true":
        errors.append("record needs an aria-hidden frieze band")
    else:
        text = friezes[0].text()
        if any(text.count(token) < 2 for token in FRIEZE_TOKENS):
            errors.append("frieze must repeat each token at least twice for a seamless loop")


def raw_text(node: Node) -> str:
    return "".join(raw_text(c) if isinstance(c, Node) else c for c in node.children)


def check_commands(tree: Node, css: str, errors: list[str]) -> None:
    """Every shell block must stay byte-identical so it copy-pastes cleanly."""
    codes = [
        raw_text(n) for n in tree.iter()
        if n.tag == "code" and n.parent is not None and n.parent.tag == "pre"
        and n.parent.parent is not None and "shell" in n.parent.parent.classes
    ]
    if not COMMANDS_BASELINE.is_file():
        errors.append(f"missing {COMMANDS_BASELINE.relative_to(ROOT)}")
    elif codes != json.loads(read(COMMANDS_BASELINE)):
        errors.append("shell blocks changed: commands must match tests/fixtures/commands-baseline.json")
    # Commands never wrap; only task prompts (their own class) may.
    for selectors, body in re.findall(r"([^{}]+)\{([^{}]*)\}", css):
        sel = [x.strip() for x in selectors.split(",")]
        if any(x in (".shell code", ".shell pre", ".shell pre code") for x in sel):
            if re.search(r"white-space:\s*(pre-wrap|break-spaces|normal)", body):
                errors.append(f"{selectors.strip()} must not wrap commands")


def check_run_to_close(tree: Node, errors: list[str]) -> None:
    for name, place, sentence in PLATES_V_CLOSE:
        plates = [
            n for n in tree.find_all(lambda n: "plate" in n.classes)
            if name in n.text() and place in n.text()
        ]
        if not plates or sentence not in plates[0].text():
            errors.append(f"missing plate {name} ({place}) with its sentence")

    steps = tree.find_all(lambda n: "run-steps" in n.classes and "demo-steps" not in n.classes)
    titles = []
    if steps:
        titles = [
            c.text() for li in steps[0].children if isinstance(li, Node) and li.tag == "li"
            for c in li.children if isinstance(c, Node) and c.tag == "h3"
        ]
    stairs = tree.find_all(lambda n: "stairs" in n.classes)
    if not stairs or stairs[0].attrs.get("aria-hidden") != "true":
        errors.append("run needs an aria-hidden .stairs figure")
    else:
        blocks = stairs[0].find_all(lambda n: "stair" in n.classes)
        got = [b.text() for b in blocks]
        want = [f"{r}. {t}" for r, t in zip(ROMAN, titles)]
        if len(blocks) != 9 or got != want:
            errors.append("stairs must be nine blocks, I to IX, titled like the nine setup steps")

    check_ascii_figure(tree, "temple-wide", errors)

    close = by_id(tree, "close-title")
    kicker = close.find_all(lambda n: n.tag == "em") if close else []
    if not kicker or kicker[0].text() != "Control for the Owner.":
        errors.append("close headline must set 'Control for the Owner.' as its italic second line")

    footers = tree.find_all(lambda n: n.tag == "footer" and "site-footer" in n.classes)
    footer_text = footers[0].text() if footers else ""
    if X_HANDLE not in footer_text or "AgentVault · Flare Confidential Compute Track" not in footer_text:
        errors.append("footer row must hold the credits and the track line")

    milestones = tree.find_all(lambda n: "roadmap-node" in n.classes)
    if len(milestones) != 2 or not tree.find_all(lambda n: "roadmap-base" in n.classes):
        errors.append("roadmap must draw two milestones on a shared base strip")


def gz_size(path: Path) -> int:
    data = path.read_bytes()
    return min(len(data), len(gzip.compress(data, 9)))


def check_budget(tree: Node, fonts_css: str, errors: list[str]) -> None:
    """Worst case: every font face fonts.css declares, every ASCII figure,
    every image and preload index.html references (og:image excluded)."""
    files = {"index.html", "styles.css", "script.js", "assets/fonts/fonts.css"}
    files |= {"assets/fonts/" + f.lstrip("./") for f in re.findall(r'url\("([^"]+)"\)', fonts_css)}
    files |= {str(p.relative_to(ROOT)) for p in (ROOT / "assets" / "ascii").glob("*.json")}
    for node in tree.iter():
        ref = node.attrs.get("src") if node.tag == "img" else None
        if node.tag == "link" and node.attrs.get("rel") in ("stylesheet", "preload"):
            ref = node.attrs.get("href")
        if ref and not re.match(r"^(https?:)?//", ref):
            files.add(ref.split("?")[0])
    missing = [f for f in files if not (ROOT / f).is_file()]
    if missing:
        errors.append(f"page references missing files: {missing}")
    total = sum(gz_size(ROOT / f) for f in files if (ROOT / f).is_file())
    if total > PAGE_BUDGET_BYTES:
        errors.append(f"page weight {total // 1024}KB gzipped exceeds the {PAGE_BUDGET_BYTES // 1024}KB budget")


def check_hardening(css: str, js: str, errors: list[str]) -> None:
    if not re.search(r"\.is-paused[^{]*\{[^}]*animation-play-state:\s*paused", css):
        errors.append("styles.css must pause animations under .is-paused")
    if "is-paused" not in js:
        errors.append("script.js must toggle is-paused for off-screen sections")

    reduced = " ".join(re.findall(r"@media \(prefers-reduced-motion: reduce\)\s*\{((?:[^{}]*\{[^{}]*\})*)", css))
    for cls in REDUCED_MOTION_CLASSES:
        if cls not in reduced:
            errors.append(f"reduced-motion styles must cover {cls}")

    menu = js[js.find("Header menu"):] if "Header menu" in js else ""
    if '"Tab"' not in menu or '"Escape"' not in menu:
        errors.append("the mobile menu must trap Tab focus and close on Escape")

    if not re.search(r'@font-face\s*\{[^}]*"Cormorant Fallback"[^}]*size-adjust', read(ROOT / "assets/fonts/fonts.css")):
        errors.append("fonts.css must define a metric-matched Cormorant Fallback (no swap shift)")


def check_social_and_docs(errors: list[str]) -> None:
    card = read(ROOT / "assets/images/social-card.html")
    if 'data-ascii="temple-hero"' not in card or "--av-bg" not in card:
        errors.append("social card must use the temple-hero art and Aerarium tokens")
    for needle in ("#9bb9bb", "#7a9294", "fonts.googleapis.com"):
        if needle in card.lower():
            errors.append(f"social card still uses {needle}")
    if "temple-hero.json" not in read(ROOT / "tests/render_social_card.js"):
        errors.append("render_social_card.js must fill the card's temple-hero art")
    aesthetic = read(ROOT / "docs/CLAUDE-INIT-AESTHETIC.md").lstrip()
    if not aesthetic.startswith(">") or "docs/revamp/REVAMP_SPEC.md" not in aesthetic[:600] or "uperseded" not in aesthetic[:600]:
        errors.append("docs/CLAUDE-INIT-AESTHETIC.md must open with a superseded notice pointing at the spec")
    design = read(ROOT / "docs/DESIGN_PLAN.md")
    if "docs/revamp/REVAMP_SPEC.md" not in design[:800]:
        errors.append("docs/DESIGN_PLAN.md must point its visual sections at the spec")
    readme = read(ROOT / "README.md")
    if "tools/ascii" not in readme or "docs/revamp/REVAMP_SPEC.md" not in readme:
        errors.append("README must mention the spec and the ASCII renderer")


def check_local_only(tree: Node, errors: list[str]) -> None:
    for node in tree.iter():
        ref = None
        if node.tag in ("script", "img", "source", "iframe"):
            ref = node.attrs.get("src")
        elif node.tag == "link":
            ref = node.attrs.get("href")
        if ref and re.match(r"^(https?:)?//", ref):
            errors.append(f"third-party request in page: <{node.tag}> {ref}")


def main() -> int:
    if len(sys.argv) == 3 and sys.argv[1] == "--write-copy-baseline":
        # One-off: freeze the visible copy of a given index.html.
        lines = dict.fromkeys(visible_text_nodes(read(Path(sys.argv[2]))))
        COPY_BASELINE.parent.mkdir(parents=True, exist_ok=True)
        COPY_BASELINE.write_text(
            "# Visible text of index.html before the Aerarium revamp. Do not edit.\n"
            + "\n".join(lines) + "\n",
            encoding="utf-8",
        )
        print(f"wrote {COPY_BASELINE.relative_to(ROOT)} ({len(lines)} lines)")
        return 0

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

    # Spec section 7: a vertical mobile SVG now shares the page, so the node
    # counts read only the desktop diagram. The conditions are unchanged.
    diagram_html = desktop_diagram(html)
    if diagram_html is html:
        errors.append('desktop mechanism SVG must carry id="mechanism-diagram"')

    if diagram_html.count(">Vault</text>") != 1:
        errors.append("mechanism diagram must contain exactly one Vault node")

    if html.count("<polyline") < 2:
        errors.append("mechanism diagram must use orthogonal routes for policy and signing")

    if 'points="400,116 625,116 625,65"' not in html:
        errors.append("mechanism diagram must route the signing line right, then up into the Vault")

    if 'x1="700" y1="36" x2="775" y2="36"' not in html:
        errors.append("mechanism diagram must settle directly from Vault to Vendor")

    if 'stroke-dasharray="5 4"' not in html or '>AgentVault</text>' not in html:
        errors.append("mechanism diagram must show a labeled dashed AgentVault system boundary")

    if 'stroke-dasharray="5 4"' not in diagram_html or '>AgentVault</text>' not in diagram_html:
        errors.append("desktop mechanism diagram must keep its labeled dashed AgentVault boundary")

    if diagram_html.count('class="diagram-node--external"') != 3:
        errors.append("mechanism diagram must style Owner, Agent, and Vendor as external actors")

    if diagram_html.count('class="diagram-node--internal"') != 2:
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

    # Aerarium foundations
    tree = parse_html(html)
    check_ascii_assets(errors)
    check_tokens(css, errors)
    check_section_headings(tree, errors)
    check_header(tree, errors)
    check_local_only(tree, errors)
    check_copy_baseline(html, errors)

    # Aerarium hero and proof
    js_text = read(ROOT / "script.js") if (ROOT / "script.js").is_file() else ""
    check_hero(tree, html, css, js_text, errors)

    # Aerarium sections I to IV
    check_mechanism(tree, html, css, errors)
    check_rules(tree, html, css, js_text, errors)
    check_sections_i_iv(tree, errors)

    # Aerarium run through close
    check_commands(tree, css, errors)
    check_run_to_close(tree, errors)

    # Aerarium hardening
    check_hardening(css, js_text, errors)
    check_social_and_docs(errors)

    credit = [a for a in tree.find_all(lambda n: n.tag == "a") if a.text() == X_HANDLE]
    if not credit or credit[0].attrs.get("href") != X_HANDLE_URL:
        errors.append(f"footer must credit {X_HANDLE} linking to {X_HANDLE_URL}")
    if "itzbankotez" in html:
        errors.append("misspelled X handle itzbankotez still in index.html")

    fonts_css = read(ROOT / "assets/fonts/fonts.css") if (ROOT / "assets/fonts/fonts.css").is_file() else ""
    for style in ("normal", "italic"):
        if not re.search(
            r'@font-face\s*\{[^}]*"Cormorant Garamond"[^}]*font-style:\s*' + style, fonts_css
        ):
            errors.append(f"fonts.css must self-host Cormorant Garamond ({style})")
    if '"Cormorant Garamond"' not in css:
        errors.append("styles.css must use Cormorant Garamond for display type")

    for hook in REQUIRED_CSS_HOOKS:
        if not re.search(re.escape(hook) + r"[\s,{:.]", css):
            errors.append(f"styles.css must define the {hook} component")

    sources = {"index.html": html, "styles.css": css, "assets/fonts/fonts.css": fonts_css}
    if (ROOT / "script.js").is_file():
        sources["script.js"] = read(ROOT / "script.js")
    for name, text in sources.items():
        for needle in FORBIDDEN_SOURCE_STRINGS:
            if needle.lower() in text.lower():
                errors.append(f"old aesthetic remnant {needle!r} in {name}")
    check_budget(tree, fonts_css, errors)

    if (ROOT / "assets/ascii-vault.txt").exists():
        errors.append("assets/ascii-vault.txt must be removed")

    if errors:
        print("validate_site.py: FAIL")
        for err in errors:
            print(f"  - {err}")
        return 1

    print("validate_site.py: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
