# Repo Mood Ring

## 🔮 What is the Repo Mood Ring?

The Repo Mood Ring is a whimsical-yet-insightful utility that scans your recent Git commit messages and attempts to gauge the overall "mood" of your repository. By analyzing keywords in commit messages, it provides a simple sentiment overview (Positive, Negative, or Neutral/Mixed), offering a quick pulse check on project health and team morale.

Think of it as a digital mood ring for your codebase!

## ✨ Features

*   **Sentiment Analysis**: Categorizes commit messages into Positive, Negative, or Neutral/Mixed sentiments based on a curated keyword list.
*   **Recent Activity Focus**: Analyzes a configurable number of recent commits.
*   **Simple & Self-Contained**: Written in Python, with no external dependencies beyond standard library.
*   **Whimsical Insights**: Provides a fun, high-level overview of development trends.

## 🚀 How to Use

1.  **Navigate to your Git repository**:
    ```bash
    cd /path/to/your/repo
    ```

2.  **Run the utility**:
    ```bash
    python3 utils/repo-mood-ring/src/mood_ring.py [NUMBER_OF_COMMITS]
    ```
    Replace `[NUMBER_OF_COMMITS]` with the desired number of recent commits to analyze (e.g., `50`). If omitted, it defaults to `20`.

### Example Output:

```
🔮 Repo Mood Ring Analysis 🔮
Total Commits Analyzed: 20
Positive Commits:      12 (60.0%)
Negative Commits:       3 (15.0%)
Neutral/Mixed Commits:  5 (25.0%)

Overall Repo Mood: ✨ Positive ✨

Recent Commit Moods:
- feat: Add new user authentication module (Positive)
- fix: Resolve critical database connection error (Neutral/Mixed)
- docs: Update README with new installation steps (Positive)
- bug: Fix typo in error message (Neutral/Mixed)
- chore: Update dependencies (Neutral/Mixed)
...
```

## 🛠️ Development & Testing

The utility is self-contained and uses Python's `subprocess` module to interact with Git. Tests are located in `tests/test_mood_ring.py` and use mocks to ensure determinism and offline execution.

To run tests:
```bash
python3 -m unittest utils/repo-mood-ring/tests/test_mood_ring.py
```
