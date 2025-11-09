# Branch Name Generator

A tiny utility that creates whimsical, git‑friendly branch names. It can be used when you need a quick, memorable name for a new feature branch without spending time brainstorming.

## Features
- Generates an `adjective-noun` pair (e.g., `sparkling-unicorn`).
- Supports custom word counts (e.g., `brave-tiger-mystic`).
- Guarantees the result fits within the typical 50‑character Git branch limit.
- Deterministic when the random seed is set, making testing easy.

## Installation
The utility is self‑contained and requires only the Python standard library.
```bash
# Clone the repository (or copy the folder) and navigate to the utility
cd utils/branch-name-generator
```

## Usage
### As a module
```python
from src.branch_name_generator import generate_branch_name

print(generate_branch_name())          # e.g., "whispering-nebula"
print(generate_branch_name(3))         # e.g., "whispering-nebula-fuzzy"
```

### As a CLI script
```bash
python -m src.branch_name_generator
# prints a generated branch name
```

## Testing
Run the bundled tests with:
```bash
python -m unittest discover -s tests
```
All tests are deterministic and run offline.

## License
MIT – see the root `LICENSE` file.
