# Nightly Quantum Quibble Quencher

A whimsical utility to help resolve minor disagreements or make trivial decisions by randomly selecting an option from a given list. Perfect for when the fate of the last can of beans, or the direction of your next scavenging run, hangs in the balance.

## 🌌 Purpose

In the chaotic post-apocalyptic world, even the smallest decisions can feel monumental. Should we fortify the east wall or the west? Who gets the last ration bar? The Quantum Quibble Quencher steps in to provide a definitive (and entirely random) answer, freeing up valuable cognitive resources for more pressing matters like avoiding irradiated squirrels.

## ✨ Features

*   **Random Selection**: Picks one option fairly from any list you provide.
*   **Simple CLI**: Easy to use from your terminal.
*   **Deterministic (for testing)**: Uses standard Python `random` module, but tests are mocked for reliability.

## 🚀 Usage

To quench a quibble, simply run the script with your options as arguments:

```bash
python src/quencher.py "Fortify East Wall" "Fortify West Wall" "Go Scavenging"
```

Example output:

```
The Quantum Quibble Quencher has spoken! The chosen path is: 'Fortify West Wall'
```

If you run without any options, `argparse` will show usage and exit:

```bash
python src/quencher.py
```

Output:

```
usage: quencher.py [-h] options [options ...]
Quantum Quibble Quencher: Resolve minor disagreements or make trivial decisions by randomly selecting an option.
quencher.py: error: the following arguments are required: options
```

## 🛠️ Development

### Running Tests

Navigate to the `utils/nightly-quantum-quibble-quencher` directory and run:

```bash
python -m unittest tests/test_quencher.py
```

### Dependencies

This utility uses only standard Python libraries. No external dependencies are required.

## 📜 License

This project is licensed under the MIT License - see the `LICENSE` file in the repository root for details.
