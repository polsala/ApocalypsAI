# Mood Emoji Generator

Utility that converts a short piece of text into a mood emoji using simple keyword heuristics. It can be used in scripts, commit hooks, or any place you want a quick visual sentiment indicator.

## Usage
```bash
python -m mood_emoji "I am happy and excited!"
# => 😄
```

Or import the function in your own Python code:
```python
from mood_emoji import get_mood_emoji
emoji = get_mood_emoji("Feeling sad today.")
print(emoji)  # 😞
```

## How it works
The tool tokenises the input text, counts occurrences of a small curated list of positive and negative words, and returns:
- 😄 for overall positive sentiment
- 😞 for overall negative sentiment
- 😐 when sentiment is neutral or unknown

The implementation is deliberately lightweight and has **no external dependencies**, making it safe to run in any CI environment.
