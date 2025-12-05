# Nightly Apocalypse Codename Generator

A whimsical utility to generate unique, memorable, and suitably grim codenames for your projects, branches, or temporary releases. Embrace the chaos with names like `Rusty-Beacon`, `Feral-Vault`, or `Shadow-Drifter`!

## 🔮 Usage

To generate a codename, simply run the Python script:

```bash
python src/codename_generator.py
```

Example Output:
```
Generated Codename: Wasteland-Nomad
```

## ✨ Features

*   **Whimsical & Thematic:** Generates names inspired by post-apocalyptic landscapes and survival.
*   **Simple & Self-Contained:** A single Python script with no external dependencies.
*   **Deterministic Tests:** Includes tests that mock randomness for consistent verification.

## 🛠️ Development

### Running Tests

Ensure you are in the `utils/nightly-apocalypse-codename-generator/` directory and run:

```bash
python -m unittest discover tests
```

### Structure

```
.
├── README.md
├── src/
│   └── codename_generator.py
└── tests/
    └── test_codename_generator.py
```
