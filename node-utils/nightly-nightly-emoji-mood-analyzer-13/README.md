Nightly Emoji Mood Analyzer
A whimsical command-line utility that reads a text file and outputs an emoji representing the overall mood of the text. Uses a tiny built‑in sentiment word list, works offline, and requires only Node.js.

Usage:
  node src/index.js <path-to-text-file>

The utility prints one of:
  😊  (positive / happy)
  😐  (neutral)
  😞  (negative / sad)

Implementation details:
- Simple word list based scoring.
- No external dependencies.
