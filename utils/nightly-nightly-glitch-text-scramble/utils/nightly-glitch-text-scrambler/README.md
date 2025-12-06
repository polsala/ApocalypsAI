# Nightly Glitch-Text Scrambler

## Overview

The Nightly Glitch-Text Scrambler is a whimsical utility designed to introduce controlled "corruption" into text strings. Whether you're aiming for a post-apocalyptic aesthetic in your UI, generating unique placeholder data, or testing how your systems handle malformed input, this scrambler can inject a touch of digital decay. It applies various effects like character substitution, insertion, deletion, and case shifts, all configurable by an intensity level.

## Usage

The utility provides a `scramble_text` function that takes a string and an optional `intensity` parameter (0.0 to 1.0) to control the degree of glitching. A higher intensity means more pronounced corruption. For deterministic results, a `seed` can also be provided.

### Command Line (Example)

While primarily a library function, you can run the `scrambler.py` directly for a quick test:

```bash
python src/scrambler.py "Hello, ApocalypsAI community!" --intensity 0.3
```

### As a Library

```python
from src.scrambler import scramble_text

# Basic scrambling
original_text = "The quick brown fox jumps over the lazy dog."
glitched_text = scramble_text(original_text, intensity=0.2)
print(f"Original: {original_text}")
print(f"Glitched: {glitched_text}")

# More intense scrambling
more_glitched_text = scramble_text(original_text, intensity=0.7, seed=42)
print(f"More Glitched (seeded): {more_glitched_text}")

# Minimal scrambling
minimal_glitch = scramble_text("System online.", intensity=0.05)
print(f"Minimal Glitch: {minimal_glitch}")
```

## Features

*   **Configurable Intensity**: Control the level of corruption from subtle to severe.
*   **Deterministic Output**: Use a `seed` for reproducible glitch patterns.
*   **Multiple Glitch Types**: Includes character substitution, insertion, deletion, and case changes.
*   **Self-contained**: No external dependencies beyond Python's standard library.

## Installation

This utility is self-contained. Simply place the `nightly-glitch-text-scrambler` folder within your `utils/` directory.

## Development

To run tests:

```bash
python -m unittest tests/test_scrambler.py
```
