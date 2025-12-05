# Nightly Quantum Quibble Quencher

## Overview

In the chaotic aftermath, even the smallest decisions can feel monumental. The "Nightly Quantum Quibble Quencher" is your go-to utility for resolving minor disagreements, making quick choices, or simply adding a touch of fate to your daily routine. Whether it's deciding who gets the last can of irradiated beans or which direction to scavenge, let the Quantum Quibble Quencher make the call!

## Features

*   **Coin Flip**: Get a definitive "Heads" or "Tails".
*   **Dice Roll**: Roll a standard 6-sided die, or specify any number of sides for more complex fate-weaving.
*   **Option Chooser**: Provide a list of options, and the Quencher will pick one for you.

## Installation

This utility is self-contained and requires Python 3.11+. No external dependencies are needed.

```bash
cd utils/nightly-quantum-quibble-quencher
# No installation steps needed, just run directly.
```

## Usage

Run the `quencher.py` script from its directory.

### Coin Flip

```bash
python src/quencher.py coin
# Output: Heads
```

### Dice Roll

Roll a standard 6-sided die:
```bash
python src/quencher.py dice
# Output: 4
```

Roll a custom-sided die (e.g., 20-sided):
```bash
python src/quencher.py dice 20
# Output: 17
```

### Choose an Option

Provide a space-separated list of options:
```bash
python src/quencher.py choose "Scavenge East" "Fortify West" "Nap Indefinitely"
# Output: Nap Indefinitely
```

## Development & Testing

To run the tests:

```bash
cd utils/nightly-quantum-quibble-quencher
python -m unittest tests/test_quencher.py
```
