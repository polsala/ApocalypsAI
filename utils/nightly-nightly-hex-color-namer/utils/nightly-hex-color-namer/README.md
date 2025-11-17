# nightly‑hex‑color‑namer

**Purpose**: Convert an arbitrary hex colour (e.g., `#ff4500`) into the nearest human‑readable colour name from a curated list of common colours.

## Features
- Pure‑Python, no external dependencies.
- Works offline – the colour palette is baked into the source.
- Provides a tiny CLI (`python -m namer <hex>`) for quick terminal use.
- Deterministic unit tests.

## Usage
```bash
# As a module
python -c "from src.namer import name_color; print(name_color('#ff4500'))"
# → orange

# As a script
python -m src.namer '#00ff7f'
# → springgreen
```

## How it works
1. The utility ships a dictionary of ~140 CSS colour names and their hex values.
2. The input hex string is parsed to an RGB tuple.
3. Euclidean distance in RGB space is computed against every palette entry.
4. The name with the smallest distance is returned.

## License
MIT – see the repository root for details.
