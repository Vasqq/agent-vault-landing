#!/usr/bin/env bash
# Rebuild the subset web fonts in assets/fonts from the full source fonts.
# Needs fontTools and brotli: pip install fonttools brotli
# Run again if new copy uses characters outside the ranges below.
set -euo pipefail

cd "$(dirname "$0")/../../assets/fonts"

# Latin-1, common punctuation and quotes, arrows, minus, and the ◆ ● marks.
UNICODES="U+0020-007E,U+00A0-00FF,U+0131,U+0152-0153,U+02C6,U+02DA,U+02DC,U+2010-2027,U+2030,U+2039-203A,U+2190-2193,U+2212,U+25C6,U+25CF"
FEATURES="kern,liga,calt,ccmp,locl,mark,mkmk"

for face in space-grotesk-400 space-grotesk-600 ibm-plex-mono-400 ibm-plex-mono-500 ibm-plex-mono-600; do
  pyftsubset "$face.ttf" --unicodes="$UNICODES" --layout-features="$FEATURES" \
    --flavor=woff --output-file="$face.woff"
done

# Variable fonts keep their 300-700 weight axis.
for face in cormorant-garamond-variable cormorant-garamond-italic-variable; do
  pyftsubset "$face.woff2" --unicodes="$UNICODES" --layout-features="$FEATURES" \
    --flavor=woff2 --output-file="$face-subset.woff2"
done

echo "Subset fonts written to assets/fonts."
