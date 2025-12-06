# nightly-commit-emoji

**What it does**

`nightly-commit-emoji` scans a Git commit message for a few well‑chosen keywords and returns a single emoji that best represents the change. It’s completely offline, has zero runtime dependencies beyond the Python standard library, and can be used in commit‑msg hooks, CI pipelines, or just for fun.

**Why it’s useful**

* Makes commit logs more expressive and searchable.
* Encourages developers to think about the nature of their change.
* No network calls – deterministic and safe for CI.

**Installation**

```bash
# Clone the repository (or copy the folder) and add it to your PATH
cd utils/nightly-commit-emoji
python -m pip install .   # optional, installs as a console script
```

Or simply run the module directly:

```bash
python -m src.commit_emoji "Add unit tests for user model"
```

**Usage**

```bash
# As a module
python -m src.commit_emoji "Fix bug in authentication flow"
# => 🐛

# As a script (if installed as a console entry point)
commit-emoji "Update documentation for API endpoints"
# => 📚
```

**Supported keywords & emojis**

| Keyword(s)               | Emoji |
|--------------------------|-------|
| `fix`, `bug`, `error`    | 🐛    |
| `add`, `create`, `new`   | ✨    |
| `remove`, `delete`, `rm` | 🗑️    |
| `refactor`, `clean`      | 🛠️    |
| `test`, `tests`          | ✅    |
| `doc`, `docs`, `readme`  | 📚    |
| `performance`, `speed`   | 🚀    |
| `merge`                  | 🔀    |
| `ci`, `cd`, `pipeline`   | 🤖    |
| `security`, `auth`       | 🔒    |

If no keyword matches, the utility falls back to the neutral emoji `🔧`.

**Running the test suite**

```bash
python -m unittest discover -s tests
```
