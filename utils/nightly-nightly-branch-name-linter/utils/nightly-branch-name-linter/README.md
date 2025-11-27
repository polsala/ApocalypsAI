# Nightly Branch Name Linter

A whimsical yet practical utility that checks whether a given Git branch name follows the **kebab‑case** convention (`lowercase-words-separated-by-dashes`).

## Features

- **Validate** a branch name.
- **Suggest** a kebab‑case version when the name is invalid.
- Zero external dependencies – pure Python 3.11.
- Comes with deterministic offline tests.

## Usage

```bash
python -m branch_linter <branch-name>
```

The command prints `✅ Valid` if the name is already kebab‑case, otherwise it prints:

```
❌ Invalid – suggested: <corrected-name>
```

## Implementation Details

- The core logic lives in `src/branch_linter.py`.
- Tests are located in `tests/test_branch_linter.py` and use simple assertions; no network calls are required.
