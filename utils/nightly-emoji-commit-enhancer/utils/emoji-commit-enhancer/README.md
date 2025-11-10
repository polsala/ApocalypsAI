# Emoji Commit Enhancer

Add a whimsical yet useful emoji prefix to your Git commit messages. The utility scans the message for common keywords (e.g., *fix*, *add*, *docs*) and prepends an appropriate emoji. If no keyword matches, a random default emoji is chosen.

## Installation

The utility is self‑contained – just copy the folder into your repository and run it with Python 3.11.

```bash
# From the repository root
python -m utils.emoji-commit-enhancer.src.enhance "Fix typo in README"
```

## Usage

```bash
python -m utils.emoji-commit-enhancer.src.enhance "Your commit message here"
```

### Example

```bash
$ python -m utils.emoji-commit-enhancer.src.enhance "Add new authentication endpoint"
➕ Add new authentication endpoint
```

## API

```python
from utils.emoji-commit-enhancer.src.enhance import enhance_message

new_msg = enhance_message("Refactor user model")
# new_msg == "♻️ Refactor user model"
```

## Testing

Run the bundled tests with:

```bash
python -m unittest discover utils/emoji-commit-enhancer/tests
```
