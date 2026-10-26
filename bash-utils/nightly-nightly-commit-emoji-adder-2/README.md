# nightly-commit-emoji-adder

Adds a context‑aware emoji to the most recent Git commit message.

## How it works

The script examines the latest commit (or a given commit hash) and looks for
keywords to decide which emoji best represents the change:

- `fix`, `bug`, `patch` → 🔧
- `add`, `feature`, `implement` → ✨
- `remove`, `delete`, `drop` → ❌
- `docs`, `readme` → 📚
- otherwise → 🛠️

If the commit message already starts with an emoji, the script leaves it
unchanged.

## Usage

```bash
# In a Git repository
./src/commit-emoji.sh          # annotate HEAD
./src/commit-emoji.sh <hash>   # annotate a specific commit
```

The script amends the commit, preserving the author and date.

## Requirements

- Bash 4+
- Git in `$PATH`

## License

MIT
