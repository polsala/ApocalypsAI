# Nightly PR Title Emoji Adder

This utility prepends a meaningful emoji to a pull‑request title based on the conventional‑commit prefix. It’s a quick visual cue for reviewers and maintainers.

## Usage

```bash
# As a command‑line tool
python -m emoji_adder "feat: add new authentication flow"
# → 🚀 feat: add new authentication flow

# As a library
from emoji_adder import add_emoji
print(add_emoji("fix: correct typo"))  # 🐛 fix: correct typo
```

## Prefix → Emoji Mapping
| Prefix      | Emoji |
|-------------|-------|
| `feat:`     | 🚀    |
| `fix:`      | 🐛    |
| `docs:`     | 📚    |
| `style:`    | 🎨    |
| `refactor:` | 🔧    |
| `test:`     | 🧪    |
| *none*      | ❓    |

The mapping is case‑insensitive and ignores leading/trailing whitespace.

## Installation

No installation is required; the module is pure Python and has no external dependencies.

## Tests

Run `pytest` from the `tests/` directory to verify deterministic behaviour.
