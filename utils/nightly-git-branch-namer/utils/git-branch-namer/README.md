# Git Branch Namer

**Utility name:** `git-branch-namer`

## What it does
`git-branch-namer` takes a human‑readable description (e.g. an issue title) and turns it into a tidy, kebab‑case Git branch name.  An optional prefix (like `feat`, `fix`, `chore`, …) can be added to keep your repository’s naming convention consistent.

## Why it’s useful
* No more manual fiddling with spaces, punctuation, or capital letters.
* Guarantees deterministic, repeatable branch names – great for automation scripts.
* Works offline, has no external dependencies, and ships with a full test suite.

## Installation & usage
```bash
# Clone the repository (or copy the folder into your own repo)
# Ensure you have Python 3.11+
cd utils/git-branch-namer
python -m src.branch_namer "Add user login feature" --prefix feat
# → feat/add-user-login-feature
```

### CLI arguments
| Argument | Description |
|----------|-------------|
| `title` (positional) | The raw description you want to convert. |
| `--prefix` | Optional prefix to prepend (e.g. `feat`, `fix`). |
| `--separator` | Separator character, default `-`. |

## Running the tests
```bash
cd utils/git-branch-namer
python -m unittest discover -s tests
```

## License
MIT – see the root `LICENSE` file.
