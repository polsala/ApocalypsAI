# Nightly Emoji Mood Generator

A tiny utility that scans the most recent commit messages of a repository and produces a single emoji that reflects the overall "mood" of the project.

## How it works
1. The utility reads a list of commit messages (provided by the caller).
2. Each message is scored for positivity or negativity using a simple keyword‑based heuristic.
3. The aggregate score maps to one of several emojis:
   - 😄  (very positive)
   - 🙂  (positive)
   - 😐  (neutral)
   - 🙁  (negative)
   - 😞  (very negative)

## Usage
```bash
python -m nightly_emoji_mood_generator <path-to-commit-messages.txt>
```
The input file should contain one commit message per line.

## Running the tests
```bash
python -m unittest discover -s utils/nightly-emoji-mood-generator/tests
```
