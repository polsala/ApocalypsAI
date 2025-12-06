# Wordle Helper

A lightweight utility to help Wordle players narrow down possible solutions based on their guesses.

## Usage

```bash
python -m src.wordle_helper --guess <guess_word> --pattern <feedback_pattern>
```

- `--guess` – the word you entered (5 letters).
- `--pattern` – a 5‑character string describing the feedback:
  - `g` – green (correct letter in the correct position)
  - `y` – yellow (correct letter in the wrong position)
  - `b` – black/gray (letter not in the word at all)

The tool prints a list of candidate words that satisfy the constraints.

## Example

```bash
python -m src.wordle_helper --guess crane --pattern ggbbb
```

Output (with the bundled sample word list):
```
crane
```

## How it works

The script contains a tiny built‑in word list (you can replace it with a larger one). It applies the constraints implied by the pattern and prints every word that matches.

## Testing

Run the tests with:
```bash
python -m unittest discover -s tests
```
