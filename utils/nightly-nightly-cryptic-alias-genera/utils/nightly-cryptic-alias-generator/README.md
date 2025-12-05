# Nightly Cryptic Alias Generator

## Purpose
The Nightly Cryptic Alias Generator is a whimsical yet practical utility designed to distill complex or lengthy identifiers (like file paths, branch names, or utility names) into short, memorable, and evocative aliases. In the sprawling post-apocalyptic landscape of ApocalypsAI, where long technical names can be cumbersome, this tool provides a quick, deterministic way to refer to entities with a touch of mystery and charm.

## How it Works
Given any input string, the generator uses a cryptographic hash to deterministically select an adjective and a noun from a predefined lexicon of "apocalyptic" and "whimsical" terms. The result is a unique, two-word alias that remains consistent for the same input, making it ideal for quick references, internal documentation, or even as a fun way to name new components.

## Usage

```bash
python src/alias_generator.py "path/to/your/complex/file_name.py"
# Example Output: "Temporal Shard"

python src/alias_generator.py "nightly-nightly-config-schema-valida"
# Example Output: "Runic Oracle"

python src/alias_generator.py "main-branch-refactor-feature-x-bugfix"
# Example Output: "Shadow Beacon"
```

### As a Library
You can also import and use the `generate_alias` function in your Python projects:

```python
from utils.nightly-cryptic-alias-generator.src.alias_generator import generate_alias

alias = generate_alias("my/important/data/archive.zip")
print(f"The alias for your archive is: {alias}")
```

## Development
The utility is written in Python 3.11 and has no external dependencies beyond the standard library.

### Running Tests
To ensure the generator is functioning correctly and deterministically:

```bash
python -m unittest utils/nightly-cryptic-alias-generator/tests/test_alias_generator.py
```
