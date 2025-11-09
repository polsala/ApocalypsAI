# Emoji Mood Analyzer

A whimsical yet practical utility that reads a line of text and returns a single emoji representing the overall mood.

## Features
- **Library function** `analyze_mood(text: str) -> str` for programmatic use.
- **Command‑line interface** for quick ad‑hoc analysis.
- **Zero external dependencies** – pure Python 3.11 standard library.
- **Deterministic offline tests** using mocks.

## Installation
Simply copy the `utils/emoji-mood-analyzer/` folder into your project or install it as a submodule.

```bash
python -m utils.emoji-mood-analyzer.src.analyzer "I love sunny days!"
```

## Usage
### As a library
```python
from utils.emoji-mood-analyzer.src.analyzer import analyze_mood

emoji = analyze_mood("I am feeling great today!")
print(emoji)  # 😊
```

### As a CLI
```bash
python -m utils.emoji-mood-analyzer.src.analyzer "I am so angry about the traffic"
# Output: 😠
```

## Mood Mapping
| Mood | Keywords (case‑insensitive) | Emoji |
|------|----------------------------|-------|
| Happy | happy, joy, love, great, wonderful, fantastic | 😊 |
| Sad | sad, sorrow, upset, depressed, down | 😢 |
| Angry | angry, mad, furious, rage, upset | 😠 |
| Neutral/Other | *none of the above* | 🤔 |

## Testing
Run the test suite with:
```bash
python -m unittest discover -s utils/emoji-mood-analyzer/tests
```
All tests are deterministic and do not require network access.
