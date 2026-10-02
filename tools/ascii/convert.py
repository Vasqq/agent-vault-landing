"""Luminance grid -> layered ASCII.

Every asset is split into up to three text layers that share one character grid,
so they can be stacked as absolutely positioned <pre> elements (or drawn to canvas)
and coloured independently:

  hi  bright surfaces           -> --av-bronze-hi
  lo  shadowed surfaces         -> --av-verdigris
  dg  "digital" glyphs (0/1/hex) -> --av-digital   (the new era breaking through)

A layer string is rows joined by "\n", each row right-stripped. Spaces are empty cells.
"""
import numpy as np

RAMP = " .`:;-=+ixXYUCLQ0O#%@"      # sparse -> dense; tuned so mid-tones stay airy
HEX = "0123456789abcdef"
BAYER4 = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16.0


def ascii_layers(g, hit, *, split, gamma, floor, dissolve=None, digital_mask=None, seed=11):
    """Stone glyphs split into hi/lo by brightness; cells where `dissolve(r, c)` is high
    turn into digital glyphs, with a little hex dust drifting in the empty space nearby."""
    rng = np.random.default_rng(seed)
    rows, cols = g.shape
    hi, lo, dg = [], [], []
    for r in range(rows):
        H, L, D = [], [], []
        for c in range(cols):
            v = g[r, c] ** gamma
            f = dissolve(r, c) if dissolve else 0.0
            dm = digital_mask[r, c] if digital_mask is not None else False
            if v < floor or hit[r, c] < 0.2:
                dust = f > 0.05 and rng.random() < 0.012 * f * (1 - f) * 4
                H.append(' '); L.append(' '); D.append(rng.choice(list(HEX)) if dust else ' ')
                continue
            if dm or rng.random() < f:
                H.append(' '); L.append(' ')
                D.append(rng.choice(list("01" if v > 0.35 else HEX)) if rng.random() > f * 0.55 else ' ')
                continue
            ch = RAMP[min(len(RAMP) - 1, int(v * (len(RAMP) - 1) + 0.5))]
            D.append(' ')
            if ch == ' ':
                H.append(' '); L.append(' ')
            elif v >= split:
                H.append(ch); L.append(' ')
            else:
                L.append(ch); H.append(' ')
        hi.append(''.join(H).rstrip()); lo.append(''.join(L).rstrip()); dg.append(''.join(D).rstrip())
    return '\n'.join(hi), '\n'.join(lo), '\n'.join(dg)


def landscape_layers(g, hit, ground, seed=5):
    """Wide temple: stone glyphs for the building, ordered-dithered digital glyphs for the ground
    (so the ploughed furrows survive as lines of 0/1/hex)."""
    rng = np.random.default_rng(seed)
    rows, cols = g.shape
    gg = g[ground]
    lo_, hi_ = np.percentile(gg, 20), np.percentile(gg, 97)
    hi, lo, dg = [], [], []
    for r in range(rows):
        H, L, D = [], [], []
        for c in range(cols):
            v = g[r, c]
            if hit[r, c] < 0.3:
                H.append(' '); L.append(' '); D.append(' '); continue
            if ground[r, c]:
                H.append(' '); L.append(' ')
                q = np.clip((v - lo_) / (hi_ - lo_), 0, 1) ** 1.3
                on = q > BAYER4[r % 4, c % 4] * 0.9 + 0.08
                D.append((rng.choice(list('01')) if q > 0.55 else rng.choice(list(HEX))) if on else ' ')
                continue
            v = v ** 1.2
            if v < 0.06:
                H.append(' '); L.append(' '); D.append(' '); continue
            ch = RAMP[min(len(RAMP) - 1, int(v * (len(RAMP) - 1) + 0.5))]
            D.append(' ')
            if v >= 0.45:
                H.append(ch); L.append(' ')
            else:
                L.append(ch); H.append(' ')
        hi.append(''.join(H).rstrip()); lo.append(''.join(L).rstrip()); dg.append(''.join(D).rstrip())
    return '\n'.join(hi), '\n'.join(lo), '\n'.join(dg)


def column_dissolve(cols, front, width, power):
    """Dissolve strength rising toward the left edge: 0 right of `front`, 1 at `front - width`."""
    return lambda r, c: float(np.clip((cols * front - c) / (cols * width), 0, 1)) ** power
