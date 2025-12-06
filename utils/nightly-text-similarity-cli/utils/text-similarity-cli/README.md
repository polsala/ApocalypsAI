# Text Similarity CLI

A whimsical‑yet‑useful utility that calculates the **Jaccard similarity** between two strings.

## What it does
- Tokenises each input on whitespace, lower‑cases tokens, and treats the resulting sets as the basis for similarity.
- Returns a similarity score in the range `[0.0, 1.0]` where `1.0` means the texts are identical in terms of word set.

## Installation & Usage
```bash
# Clone the repository (if you haven't already)
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI

# Run the utility (Python 3.11 required)
python -m utils.text-similarity-cli.src.similarity "The quick brown fox" "the QUICK fox jumps"
```

The command prints a floating‑point similarity value, e.g. `0.5`.

## API
```python
from utils.text-similarity-cli.src.similarity import jaccard_similarity

score = jaccard_similarity("hello world", "world of code")
```

## Testing
```bash
pytest utils/text-similarity-cli/tests
```

All tests are deterministic and run offline.
