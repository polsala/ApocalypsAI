# nightly-hex-color-namer

**What it does**

`nightly-hex-color-namer` translates a standard 6‑digit hexadecimal color code (e.g., `#ff4500`) into a short, apocalyptic‑themed name such as **"Molten Ember"** or **"Void Ash"**.  The mapping is deterministic and self‑contained – no external APIs are called.

**Why it’s useful**

* Add personality to logs, dashboards, or CLI output.
* Keep a consistent, human‑readable reference for colors without maintaining a large palette.
* Fun for developers who love a little drama in their tooling.

**Installation**

The utility is completely self‑contained.  Simply copy the `utils/nightly-hex-color-namer` folder into your project and run the script with Python 3.11+.

```bash
python -m utils.nightly-hex-color-namer.src.color_namer --color "#ff4500"
```

**CLI usage**

```text
usage: color_namer.py --color HEX

Options:
  -h, --help        show this help message and exit
  --color HEX       Hexadecimal color code (e.g., "#ff4500" or "ff4500")
```

**Python API**

```python
from utils.nightly-hex-color-namer.src.color_namer import name_color

print(name_color("#ff4500"))  # → "Molten Ember"
```

**Supported colors**

The utility ships with a curated list of ~20 colors.  If a color is not in the list, the fallback name **"Mysterious Void"** is returned.

**Testing**

Run the bundled tests with:

```bash
python -m pytest utils/nightly-hex-color-namer/tests
```

---

*Created by the ApocalypsAI Nightly Integrator.*
