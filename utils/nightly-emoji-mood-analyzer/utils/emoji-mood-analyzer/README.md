# Emoji Mood Analyzer

**What it does**

`emoji-mood-analyzer` reads a line of text (or stdin) and prints a single emoji that best represents the overall mood of the message. It uses a lightweight keyword‑based heuristic, so it works completely offline and has zero runtime dependencies beyond the Python standard library.

**Why it’s useful**

- Quickly add emotional context to commit messages, logs, or chat bot replies.
- Fun way to visualize sentiment without heavy NLP models.
- Fully deterministic and testable.

**Installation**

```bash
# Clone the repository (or copy the folder) and run the script directly
python utils/emoji-mood-analyzer/src/analyzer.py "I love this new feature!"
```

**CLI usage**

```bash
# Pass a string as an argument
python utils/emoji-mood-analyzer/src/analyzer.py "I am frustrated with the bugs."
# Or pipe input
echo "Everything works perfectly" | python utils/emoji-mood-analyzer/src/analyzer.py
```

**Supported moods**

| Mood | Emoji |
|------|-------|
| Happy | 😄 |
| Sad | 😢 |
| Angry | 😠 |
| Surprised | 😲 |
| Neutral | 😐 |

**Implementation details**

The script scans the input for sets of keywords associated with each mood. The first matching mood wins; if none match, it falls back to the neutral emoji.

**Testing**

Run the bundled tests with:

```bash
python -m unittest discover -s utils/emoji-mood-analyzer/tests
```
