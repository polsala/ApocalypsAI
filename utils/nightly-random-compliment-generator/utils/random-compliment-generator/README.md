# Random Compliment Generator

A tiny command‑line utility that prints a random morale‑boosting compliment. Perfect for team chats, bots, or a personal pick‑me‑up.

## Features

- Choose a category (`general`, `work`, `coding`) or let it pick from all.
- Zero external dependencies – pure Python 3.11.
- Installable as a module or run directly.

## Installation

```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI
python -m venv .venv
source .venv/bin/activate
pip install -e utils/random-compliment-generator
```

## Usage

```bash
python -m utils.random-compliment-generator.src.compliment          # any compliment
python -m utils.random-compliment-generator.src.compliment -c work # work‑related
```

## Testing

```bash
python -m unittest discover utils/random-compliment-generator/tests
```
