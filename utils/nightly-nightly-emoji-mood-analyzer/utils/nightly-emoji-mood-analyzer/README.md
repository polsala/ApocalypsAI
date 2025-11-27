# Nightly Emoji Mood Analyzer

**What it does**

`emoji-mood-analyzer` scans a string for known emojis and returns a JSON‑compatible dictionary mapping each detected mood to the number of times it appears. It’s perfect for:

- Summarising the emotional tone of a Slack/Discord message.
- Adding a playful sentiment badge to a commit message.
- Any situation where you have a handful of emojis and need a quick, deterministic mood breakdown.

**Supported emojis & moods**

| Emoji | Mood |
|-------|------|
| 😀, 😃 | happy |
| 😂 | joy |
| 😢, 😭 | sad |
| 😡 | angry |
| 🤔 | thinking |
| 👍 | approval |
| 👎 | disapproval |
| ❤️ | love |
| 💔 | heartbreak |
| 🤯 | mindblown |
| 🥳 | celebration |

**Installation**

The utility is self‑contained; just copy the `src/` folder into your project or run it directly:

```bash
python -m utils/nightly-emoji-mood-analyzer/src/analyzer "😀😂👍"
```

**CLI usage**

```bash
python -m utils/nightly-emoji-mood-analyzer/src/analyzer "Your emoji string here"
```

The script prints a pretty‑printed JSON object, e.g.:

```json
{
  "happy": 1,
  "joy": 1,
  "approval": 1
}
```

**Programmatic usage**

```python
from utils.nightly-emoji-mood-analyzer.src.analyzer import analyze_emojis
mood_counts = analyze_emojis("😀😂👍")
```

**Testing**

Run the bundled tests with:

```bash
python -m unittest discover utils/nightly-emoji-mood-analyzer/tests
```

---

*Created by the ApocalypsAI Nightly Integrator.*
