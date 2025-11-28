# Nightly Emoji Status Broadcaster

## Overview

`emoji-status-broadcaster` converts plain‑text status strings (e.g. `success`, `failure`, `in_progress`) into their corresponding emoji representations.  It can be used as:

* **Library** – import the functions in your Python code.
* **CLI** – pipe status words directly from the shell.

The mapping is deterministic and completely offline, making it safe for CI environments.

## Installation

The utility is self‑contained; just copy the folder into your repository and run the script with Python 3.11+.

```bash
python -m utils.nightly-emoji-status-broadcaster.src.broadcaster success failure in_progress
```

## API

```python
from utils.nightly-emoji-status-broadcaster.src.broadcaster import status_to_emoji, summarize_statuses

emoji = status_to_emoji("success")          # "✅"
summary = summarize_statuses(["success", "failure", "in_progress"])
# "✅ Success, ❌ Failure, ⏳ In Progress"
```

## Testing

Run the bundled tests with:

```bash
python -m unittest discover utils/nightly-emoji-status-broadcaster/tests
```

---

*Whimsical note*: If your CI ever feels gloomy, just sprinkle a few emojis and watch the morale rise! 🎉
