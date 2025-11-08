# Random ANSI Art Generator

Utility that creates random ANSI‑colored block art.

## Features
- Deterministic output when a seed is provided.
- Simple CLI for quick generation.
- Pure Python, no external dependencies.

## Installation
Copy the `src/` directory into your project or run the script directly.

## Usage
```bash
python -m src.main --width 10 --height 5 --seed 42
```

## API
```python
from src.main import generate_art

art = generate_art(width=8, height=4, seed=123)
print(art)
```
