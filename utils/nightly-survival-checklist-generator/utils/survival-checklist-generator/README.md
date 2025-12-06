# Survival Checklist Generator

A tiny, self‑contained Python utility that returns a ready‑to‑use survival checklist for a specified post‑apocalyptic scenario (e.g., *zombie*, *nuclear*, *meteor*).  It is deliberately lightweight, has no external dependencies, and ships with deterministic offline tests.

## Features
- One‑function public API: `generate_checklist(scenario: str) -> List[str]`
- Built‑in mappings for common scenarios
- Falls back to a generic checklist for unknown inputs
- Easy to extend by monkey‑patching the internal mapping (useful for custom projects)

## Installation & Usage
```bash
# Clone the repository (or copy the folder) and run the tests
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt  # (no extra deps needed)
```
```python
from src.generator import generate_checklist

print(generate_checklist("zombie"))
```

## Running the Tests
```bash
python -m unittest discover -s utils/survival-checklist-generator/tests
```

## Design Rationale
The utility is deliberately simple so it can be used in scripts, notebooks, or as a teaching example for deterministic testing with mocks.
