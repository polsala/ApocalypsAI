# Emoji Date Formatter

**Utility name:** `emoji-date-formatter`

## What it does

`emoji-date-formatter` takes an ISO‑formatted date string (`YYYY‑MM‑DD`) and returns a playful emoji version:

* Each digit (`0‑9`) is replaced by its corresponding *keycap* emoji (e.g., `1` → `1️⃣`).
* The month component is replaced by a seasonal plant emoji instead of the numeric month:
  * `01` → 🌸 (Cherry Blossom)
  * `02` → 🌼 (Blossom)
  * `03` → 🌻 (Sunflower)
  * `04` → 🌹 (Rose)
  * `05` → 🌷 (Tulip)
  * `06` → 🌺 (Hibiscus)
  * `07` → 🌱 (Seedling)
  * `08` → 🌲 (Evergreen Tree)
  * `09` → 🌳 (Deciduous Tree)
  * `10` → 🌴 (Palm Tree)
  * `11` → 🌵 (Cactus)
  * `12` → 🌾 (Sheaf of Rice)

The result is a string that can be used in chat, logs, or anywhere a bit of visual flair is welcome.

## Installation & Usage

The utility is self‑contained; just copy the `src/emoji_date.py` file into your project or run it directly from the repository.

```bash
python -m utils.emoji-date-formatter.src.emoji_date 2024-10-31
# Output: 2️⃣0️⃣2️⃣4🌴-3️⃣1️⃣
```

## API

```python
from utils.emoji-date-formatter.src.emoji_date import format_date

emoji_str = format_date("2024-10-31")
# "2️⃣0️⃣2️⃣4🌴-3️⃣1️⃣"
```

## Testing

Run the bundled tests with `pytest`:

```bash
cd utils/emoji-date-formatter
pytest -q
```

All tests are deterministic and offline.
