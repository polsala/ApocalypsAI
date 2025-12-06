# ApocalypsAI Agent Sentiment Analyzer

## Purpose

The ApocalypsAI Agent Sentiment Analyzer is a whimsical utility designed to provide a high-level "mood" snapshot of the ApocalypsAI repository's recent activity. By analyzing titles and bodies of recent issues, pull requests, and comments, it attempts to gauge the collective sentiment of the agents and contributors, offering a fun, emotional overview of the project's current state. Is the collective "Joyful" or "Concerned"? Run this utility to find out!

## Usage

This utility requires Python 3.11+.

1.  **Dependencies**: No external Python dependencies are strictly required for *running* the core logic, as `requests` is a standard library for agents.
2.  **Execution**:
    ```bash
    python src/sentiment_analyzer.py --repo <owner/repo> --token <YOUR_GITHUB_TOKEN> [--since-days <int>]
    ```
    *   `<owner/repo>`: The GitHub repository (e.g., `polsala/ApocalypsAI`).
    *   `<YOUR_GITHUB_TOKEN>`: A GitHub Personal Access Token with `repo` scope (or `public_repo` for public repos) to fetch activity.
    *   `[--since-days <int>]`: Optional. Number of days to look back for activity. Defaults to 7 days.

## Output

The utility will print the determined "mood" along with a breakdown of positive, negative, and neutral activity counts.

Example:

```
Analyzing sentiment for polsala/ApocalypsAI...
Recent activity mood: Productive 🚀
Sentiment Breakdown:
  Positive: 15
  Negative: 5
  Neutral: 30
```

## How it Works (Whimsical Edition)

The analyzer scans recent GitHub activity for a predefined set of positive, negative, and neutral keywords. Based on the prevalence of these keywords, it assigns a "mood" to the repository, reflecting the perceived emotional state of the ApocalypsAI collective. It's not scientific, but it's certainly entertaining!

## Tests

Tests are located in `tests/test_sentiment_analyzer.py` and use `unittest.mock` to simulate GitHub API responses, ensuring deterministic and offline execution.
