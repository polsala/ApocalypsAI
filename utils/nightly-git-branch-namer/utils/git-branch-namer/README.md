# Git Branch Namer

**Utility:** Generate a short, kebab‑case Git branch name from a commit message.

## Why?
Keeping branch names short and descriptive improves readability in pull‑request lists and CI pipelines. Manually crafting them can be tedious, especially when the commit message is long or contains punctuation.

## How it works
1. Normalises the commit message to lower‑case.
2. Removes non‑alphanumeric characters (except spaces).
3. Splits the message into words.
4. Takes the first *N* words (default 4) and joins them with hyphens.
5. Truncates the result to a maximum of 30 characters and ensures it starts with a letter.

## Installation
```bash
# From the repository root
cd utils/git-branch-namer
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # (empty for now)
```

## Usage
```bash
python -m src.branch_namer "Add support for user authentication"
# => add-support-for-user
```

You can also import the function in your own scripts:
```python
from src.branch_namer import suggest_branch_name

branch = suggest_branch_name("Fix bug in payment processing")
print(branch)  # => fix-bug-in-payment
```

## Testing
```bash
pytest -q
```

## License
MIT © ApocalypsAI
