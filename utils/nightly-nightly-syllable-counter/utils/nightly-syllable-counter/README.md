# Nightly Syllable Counter

## Overview

`nightly-syllable-counter` provides a **single function** `count_syllables(word: str) -> int` that returns an estimated syllable count for an English word. The implementation uses a lightweight heuristic (vowel‑group counting with a few common adjustments) and has **no external dependencies**.

## Why?

- Quickly gauge readability scores (e.g., Flesch‑Kincaid).
- Assist poets or lyricists in matching meter.
- Completely offline and deterministic – perfect for CI pipelines.

## Usage

```python
from src.syllable_counter import count_syllables

print(count_syllables("beautiful"))  # → 3
```

## Running the Tests

```bash
python -m unittest discover -s utils/nightly-syllable-counter/tests
```

## Implementation Details

The heuristic:
1. Convert the word to lowercase.
2. Count contiguous groups of vowels (`a e i o u y`).
3. Subtract one if the word ends with a silent "e" **and** the count is > 1.
4. Ensure a minimum of 1 syllable.

This is **not** a perfect linguistic model but works well for the majority of everyday words.
