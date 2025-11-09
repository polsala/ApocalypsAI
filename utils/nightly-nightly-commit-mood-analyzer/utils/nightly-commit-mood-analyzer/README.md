# Nightly Commit Mood Analyzer

## 🌌 Repo Emotional Forecast

The `nightly-commit-mood-analyzer` is a whimsical utility designed to give you a quick pulse check on your repository's recent activity. It scans the latest Git commit messages and categorizes them into various 'moods', providing a fun and insightful 'Repo Emotional Forecast' for your project.

Ever wondered if your team is having a 'Joyful Jolt' or battling the 'Buggy Blues'? This tool will tell you!

## ✨ How It Works

1.  **Fetches Recent Commits**: It uses `git log` to retrieve commit messages from the last 24 hours (or a configurable number of commits).
2.  **Analyzes Sentiment**: Each commit message is scanned for keywords associated with predefined 'moods'.
3.  **Generates Report**: A Markdown report is created, summarizing the distribution of moods and highlighting the predominant emotional tone of the repository's recent development.

## 🚀 Usage

To run the mood analyzer, navigate to your repository's root directory and execute the script:

```bash
python utils/nightly-commit-mood-analyzer/src/mood_analyzer.py
```

### Configuration

By default, it analyzes commits from the last 24 hours. You can modify the `time_period` parameter when initializing `MoodAnalyzer` in `src/mood_analyzer.py` (e.g., `'--since="1 week ago"'`) or specify a number of commits (e.g., `'-n 50'`).

## 📊 Example Output

```markdown
# 🌌 Repo Emotional Forecast (Last 24 Hours)

## Current Mood: Refactor Rhapsody! 🎶

### Mood Breakdown:

*   **Refactor Rhapsody** (Refactoring, Cleaning, Optimizing): 5 commits (41.67%)
*   **Joyful Jolt** (New Features, Additions): 3 commits (25.00%)
*   **Buggy Blues** (Bug Fixes, Error Handling): 2 commits (16.67%)
*   **Documentation Delight** (Docs, Comments, READMEs): 1 commit (8.33%)
*   **Maintenance Mumble** (Chores, CI, Builds): 1 commit (8.33%)
*   **Neutral Nudge** (General, Uncategorized): 0 commits (0.00%)

---

*Total commits analyzed: 12*

*This forecast is based on the sentiment detected in commit messages. May your code be ever joyful!*
```
