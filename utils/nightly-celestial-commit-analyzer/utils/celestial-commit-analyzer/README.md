# 🌌 Celestial Commit Analyzer 🌠

The `celestial-commit-analyzer` is a whimsical-yet-useful utility designed to bring cosmic clarity to your project's commit history. It scans Git commit messages, evaluates their adherence to Conventional Commits, and performs a simple sentiment analysis to provide a "Celestial Alignment Score" and insightful cosmic wisdom.

Ensure your commits are not just code changes, but stellar contributions aligned with the universe's best practices!

## ✨ Features

*   **Conventional Commit Validation**: Checks if commit messages follow the [Conventional Commits specification](https://www.conventionalcommits.org/en/v1.0.0/).
*   **Simple Sentiment Analysis**: Identifies positive or negative tones within commit messages using a lightweight internal lexicon.
*   **Celestial Alignment Score**: Assigns a score (0-100) indicating how well a commit aligns with best practices and positive cosmic energy.
*   **Cosmic Wisdom**: Provides whimsical insights and suggestions for improving commit hygiene.
*   **Markdown Report**: Generates a human-readable report summarizing the analysis.

## 🚀 Usage

The utility can process commit messages either from a specified file or directly from standard input.

### From a File

To analyze commit messages stored in a text file (one message per line):

```bash
python src/analyzer.py path/to/your/commits.txt
```

Example `commits.txt`:
```
feat(auth): add user login functionality
fix: resolve critical bug in payment processing
chore: update dependencies
WIP: working on something big
```

### From Standard Input

To analyze messages typed directly into the terminal or piped from another command:

```bash
python src/analyzer.py
```
Then, type your commit messages one by one, pressing `Enter` after each.
To finish input:
*   On Unix-like systems (Linux, macOS): Press `Ctrl+D`.
*   On Windows: Press `Ctrl+Z` then `Enter`.

You can also pipe output from `git log` (or similar) directly:

```bash
git log --oneline --pretty=format:"%s" | python src/analyzer.py
```

## 🛠️ Development

### Prerequisites

*   Python 3.11+

### Running Tests

To ensure the celestial mechanics are working perfectly, run the tests:

```bash
python -m unittest tests/test_analyzer.py
```

## 📜 License

This utility is released under the [MIT License](LICENSE).
