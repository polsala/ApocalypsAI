# Nightly Emoji Mood Analyzer

Utility that analyzes a short piece of text and returns an emoji representing the overall mood. Uses a lightweight keyword‑based approach, no external APIs. Handy for sprinkling emotional flair into commit messages, PR comments, chat bots, or any place you want a quick mood hint.

## Usage

```bash
python -m utils.nightly-emoji-mood-analyzer.src.mood_analyzer "I love this new feature!"
# Output: 😄
```

## How it works

The analyzer contains a hard‑coded mapping of **keywords** to **emoji** categories:

| Category | Keywords (case‑insensitive) | Emoji |
|----------|-----------------------------|-------|
| happy    | happy, love, great, awesome, fantastic, wonderful | 😄 |
| sad      | sad, disappointed, bad, terrible, upset | 😢 |
| angry    | angry, furious, hate, mad, outraged | 😠 |
| surprised| surprised, wow, amazing, unbelievable, shocking | 😲 |
| neutral  | *(fallback)* | 😐 |

The text is tokenised on whitespace, each token is compared against the keyword lists, and the category with the highest hit count wins. Ties are resolved by the order shown above (happy → sad → angry → surprised → neutral).

## Testing

Run the test suite with:

```bash
pytest utils/nightly-emoji-mood-analyzer/tests
```

All tests are deterministic and run offline.
