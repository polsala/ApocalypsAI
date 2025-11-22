# nightly-emoji-mood-tracker

**Purpose**: Turn a simple text‑based mood log into a colorful emoji summary.

## How it works

1. Provide a log file where each line follows the format:
   ```
   YYYY-MM-DD <mood>
   ```
   *`<mood>`* can be one of `happy`, `sad`, `angry`, `neutral`.
2. The utility maps each mood to an emoji:
   - `happy` → 😄
   - `sad`   → 😢
   - `angry` → 😠
   - `neutral` → 😐
3. It then prints a concise summary:
   - Total entries
   - Count per mood
   - The most frequent mood (as an emoji)

## Installation & Usage

```bash
# Clone the repository (if you haven't already)
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI

# Navigate to the utility
cd utils/nightly-emoji-mood-tracker

# Run the tool (Python 3.11 required)
python -m src.mood_tracker --file path/to/mood.log
```

## Example

Given a `mood.log`:
```
2025-11-20 happy
2025-11-21 sad
2025-11-22 happy
2025-11-23 neutral
```
Running the tool yields:
```
Total entries: 4
happy   😄 : 2
sad     😢 : 1
neutral 😐 : 1
Most common mood: 😄 (happy)
```

## Testing

```bash
python -m unittest discover -s tests
```

All tests run offline and use mocks to simulate file I/O.
