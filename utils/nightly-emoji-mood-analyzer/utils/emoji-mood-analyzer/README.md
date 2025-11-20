# Emoji Mood Analyzer

Utility that takes a piece of text and returns an emoji representing its overall sentiment (positive 😊, neutral 😐, negative 😞). Simple keyword‑based approach, no external dependencies.

## Usage

```bash
python -m src.analyzer "I love this wonderful day!"
# 😊
```

## How it works

- **Positive words** list: `love`, `wonderful`, `great`, `fantastic`, `happy`, `excellent`, `good`, `awesome`, `joy`, `delight`, `pleased`, `amazing`
- **Negative words** list: `hate`, `terrible`, `bad`, `awful`, `sad`, `horrible`, `worst`, `angry`, `disappointed`, `pain`, `depressed`, `unhappy`
- If more positive than negative words → 😊
- If more negative than positive words → 😞
- Otherwise → 😐

## Testing

Run `pytest` in the utility folder:

```bash
cd utils/emoji-mood-analyzer
pytest
```
