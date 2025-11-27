# Nightly Emoji Status Broadcaster

A tiny, self‑contained Python utility that turns human‑readable status strings into expressive emojis and can generate a one‑line summary for a list of statuses.

## Features

- `status_to_emoji(status: str) -> str` – maps common status keywords to emojis.
- `summarize_statuses(statuses: List[str]) -> str` – produces a compact, emoji‑rich summary line.
- Zero external dependencies; works with the standard library only.
- Fully unit‑tested and ready to be used in CI scripts, markdown reports, or terminal dashboards.

## Installation

Copy the `src/` folder into your project or add this utility as a submodule. No installation step required.

## Usage Example

```python
from src.broadcaster import status_to_emoji, summarize_statuses

print(status_to_emoji("success"))          # ✅
print(status_to_emoji("failure"))          # ❌
print(status_to_emoji("in-progress"))      # ⏳

statuses = ["success", "failure", "in-progress", "unknown"]
print(summarize_statuses(statuses))
# Output: ✅ ❌ ⏳ ❓ (4)
```

## Development & Testing

Run the tests with:

```bash
python -m unittest discover -s tests
```

All tests are deterministic and offline.
