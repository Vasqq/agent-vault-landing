# ASCII renderer

Renders the four Roman objects used on the landing page and converts them into layered ASCII text. Dev-time only: the browser never runs any of this. It just displays the committed JSON in `assets/ascii/`.

| Asset | Scene | What it is |
|---|---|---|
| `temple-hero` | `scene_temple.py` | Temple of Saturn close up, low angle, with the real restoration inscription on the architrave. Far columns dissolve into hex. |
| `temple-wide` | `scene_temple_wide.py` | The whole temple reconstructed, seen wide from above, on hills made of digital glyphs. |
| `ring-key` | `scene_objects.py` | A Roman ring-key. The bit dissolves into hex. |
| `coin` | `scene_objects.py` | The AgentVault coin: keyhole relief, beaded rim, AGENTVAVLT legend. |

## Run

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r tools/ascii/requirements.txt
python3 tools/ascii/build.py              # all four, about a minute each
python3 tools/ascii/build.py coin         # just one
```

Output is deterministic (fixed seeds). Commit the regenerated JSON.

The inscription and coin legend are drawn with a system bold serif/sans (DejaVu on Linux, Georgia/Arial on macOS or Windows). A different system font can shift a few characters; that is expected.

## How it works

1. `raymarch.py` is a small vectorised signed-distance-field raymarcher (numpy): soft shadows, ambient occlusion, a camera whose pixel aspect matches a monospace cell (0.6 wide by 1 tall).
2. Each `scene_*.py` builds geometry out of SDF primitives and returns a luminance grid with one value per character cell (supersampled).
3. `convert.py` maps luminance to a sparse-to-dense character ramp and splits it into up to three layers that share one grid:
   - `hi`: bright surfaces, coloured `--av-bronze-hi`
   - `lo`: shadowed surfaces, coloured `--av-verdigris`
   - `dg`: digital glyphs (`0`, `1`, hex), coloured `--av-digital`. This is where stone dissolves into the new era, and the temple-wide ground.
4. `build.py` writes `assets/ascii/<name>.json`: `{ name, rows, cols, cell_aspect, recommended_font_size, layers: { hi, lo, dg } }`.

## Tuning knobs

- `build.py`: `split` (hi/lo threshold), `gamma` (higher means more negative space), `floor` (darkest value that still prints), and the `column_dissolve(cols, front, width, power)` arguments that control where and how fast stone turns into glyphs.
- Scene files: camera position and target, light direction, and material albedo. Keep the camera's pixel aspect at 0.6 or the art will stretch.
