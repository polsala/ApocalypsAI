# Apocalypse Supply Calculator

A tiny, self‑contained utility that tells you how much water and food you need to survive a post‑apocalyptic scenario.

## Features
- Pure Python 3.11, no external dependencies.
- Deterministic calculations based on simple per‑person daily needs.
- CLI that prints a JSON object, perfect for piping into scripts.

## Assumptions
- **Water**: 3 liters per person per day.
- **Food**: 2000 kcal per person per day.

## Installation
Just copy the `utils/apocalypse-supply-calculator/` folder into your project or run it directly with Python:
```bash
python -m utils.apocalypse-supply-calculator.src.calculator <survivors> <days>
```

## Example
```bash
$ python -m utils.apocalypse-supply-calculator.src.calculator 5 3
{"water_liters": 45, "food_kcal": 30000}
```

## Testing
Run the bundled tests with:
```bash
python -m unittest discover -s utils/apocalypse-supply-calculator/tests
```
