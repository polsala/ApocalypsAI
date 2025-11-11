# Emoji Commit Helper

**What it does**

`emoji-commit-helper` scans a Git commit message and returns a single emoji that best represents the change. It’s perfect for teams that love to sprinkle a little personality into their commit history while keeping things consistent.

**Features**

- Zero‑dependency, pure Python 3.11.
- Simple keyword‑based mapping (e.g., `fix` → 🐛, `add` → ✨).
- CLI entry point for quick local use.
- Fully tested with deterministic offline unit tests.

**Installation**

```bash
# Clone the repository (or copy the folder) and install the utility in a venv
python -m venv .venv
source .venv/bin/activate
pip install -e utils/emoji-commit-helper
```

**Usage**

```bash
# As a module
python -c "from emoji_commit_helper import get_emoji_for_message; print(get_emoji_for_message('Fix typo in README'))"
# → 🐛

# As a CLI tool
python -m emoji_commit_helper "Add new feature for user login"
# → ✨ Add new feature for user login
```

**How it works**

The helper maintains a small, deterministic mapping of keyword groups to emojis. The first matching group wins; if none match, a generic wrench `🔧` is returned.

**Running the tests**

```bash
pytest utils/emoji-commit-helper/tests
```

---

*Feel free to tweak the keyword lists to match your team’s conventions!*
