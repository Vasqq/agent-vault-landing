#!/usr/bin/env python3
"""Render every AgentVault ASCII asset into assets/ascii/*.json.

    pip install -r tools/ascii/requirements.txt
    python3 tools/ascii/build.py              # all assets
    python3 tools/ascii/build.py temple-hero  # just one

Output is deterministic (fixed seeds). Commit the JSON; the browser never runs this.
"""
import json, sys, time
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
OUT = HERE.parents[1] / "assets" / "ascii"

import convert  # noqa: E402


def temple_hero():
    import scene_temple
    g, hit = scene_temple.render_close()
    cols = g.shape[1]
    hi, lo, dg = convert.ascii_layers(g, hit, split=0.42, gamma=1.3, floor=0.07,
                                      dissolve=convert.column_dissolve(cols, 0.36, 0.30, 1.2), seed=11)
    return dict(hi=hi, lo=lo, dg=dg), dict(grid=g.shape, desktop_px=7, mobile_px=3,
        note="Hero. Anchor to the right edge; the far (left) columns dissolve into hex toward the headline.")


def temple_wide():
    import scene_temple_wide
    g, hit, ground = scene_temple_wide.render_wide()
    hi, lo, dg = convert.landscape_layers(g, hit, ground, seed=5)
    return dict(hi=hi, lo=lo, dg=dg), dict(grid=g.shape, desktop_px=7, mobile_px=2.1,
        note="Close. Centre horizontally; the ground is entirely digital glyphs in furrows.")


def ring_key():
    import scene_objects
    g, hit = scene_objects.render_key()
    cols = g.shape[1]
    hi, lo, dg = convert.ascii_layers(g, hit, split=0.45, gamma=1.1, floor=0.06,
                                      dissolve=convert.column_dissolve(cols, 0.42, 0.25, 1.1), seed=11)
    return dict(hi=hi, lo=lo, dg=dg), dict(grid=g.shape, desktop_px=9, mobile_px=2.6,
        note="Problem section. The bit (upper left) dissolves: the key is what the Agent must never hold.")


def coin():
    import scene_objects
    g, hit = scene_objects.render_coin()
    g = np.clip((g - 0.25) / 0.6, 0, 1)   # stretch so the keyhole relief and rim read
    hi, lo, _ = convert.ascii_layers(g, hit, split=0.5, gamma=1.25, floor=0.04, seed=11)
    return dict(hi=hi, lo=lo, dg=""), dict(grid=g.shape, desktop_px=2.2, mobile_px=1.6,
        note="Mechanism section. Travels Vault -> FCC checkpoint -> Vendor (or back). No digital layer.")


ASSETS = {"temple-hero": temple_hero, "temple-wide": temple_wide, "ring-key": ring_key, "coin": coin}


def main(names):
    OUT.mkdir(parents=True, exist_ok=True)
    for name in names or ASSETS:
        t0 = time.time()
        layers, meta = ASSETS[name]()
        rows, cols = (int(x) for x in meta.pop("grid"))
        doc = dict(name=name, rows=rows, cols=cols, cell_aspect=0.6,
                   font="IBM Plex Mono, line-height equal to font-size, letter-spacing 0",
                   recommended_font_size=meta, layers=layers)
        (OUT / f"{name}.json").write_text(json.dumps(doc, ensure_ascii=False))
        print(f"{name}: {cols}x{rows} in {time.time() - t0:.1f}s -> {OUT / (name + '.json')}")


if __name__ == "__main__":
    main(sys.argv[1:])
