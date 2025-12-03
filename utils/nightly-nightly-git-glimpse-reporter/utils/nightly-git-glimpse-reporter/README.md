# Nightly Git Glimpse Reporter

## 🌌 The Great Git Glimpse: Your Repository's Pulse at a Glance 🌌

In the ever-shifting sands of the post-apocalyptic digital landscape, keeping track of your project's heartbeat is crucial. The **Nightly Git Glimpse Reporter** is a whimsical-yet-powerful utility designed to provide a concise, human-readable summary of recent Git activity within any given repository. No more sifting through endless `git log` outputs – get the vital signs of your codebase with a single command!

### ✨ What it Does

This utility scans a specified Git repository and reports on:
*   **Total Commits**: The overall commit count of the repository.
*   **Recent Commits**: A count and a snippet of the most recent commits within a configurable timeframe (default: last 7 days).
*   **Top Active Authors**: Identifies and lists the most prolific contributors in the recent period.
*   **Recently Active Branches**: Highlights branches that have seen recent activity, helping you spot ongoing work.

It's like a quick health check for your project, perfect for daily stand-ups, project overviews, or just satisfying your curiosity about who's been busy building the future (or dismantling the past).

### 🛠️ How to Use

1.  **Navigate to the utility's directory**:
    ```bash
    cd utils/nightly-git-glimpse-reporter
    ```
2.  **Run the `git_glimpse.py` script**:
    Provide the path to the Git repository you want to analyze.

    ```bash
    python src/git_glimpse.py /path/to/your/git/repo
    ```

    **Example**: If you want to analyze the parent `polsala/ApocalypsAI` repository:
    ```bash
    python src/git_glimpse.py ../../
    ```

3.  **Optional Arguments**:
    *   `--days <int>`: Specify the number of past days to consider for "recent" activity (default: `7`).
    *   `--top-authors <int>`: Specify how many top active authors to list (default: `3`).

    ```bash
    python src/git_glimpse.py /path/to/your/git/repo --days 30 --top-authors 5
    ```

### 🚀 Example Output

```
--- Git Glimpse Report for 'ApocalypsAI' ---
Total Commits: 1234
Recent Commits (last 7 days): 15
  - abcde1 Agent Alpha Implemented new feature X
  - fghij2 Agent Beta Fixed critical bug Y
  - klmno3 Agent Alpha Refactored module Z
  - pqrst4 Agent Gamma Updated documentation
  - uvwxy5 Agent Beta Added more tests for Y
  ... and 10 more.
Top Active Authors (last 7 days):
  - Agent Alpha (7 commits)
  - Agent Beta (5 commits)
  - Agent Gamma (3 commits)
Recently Active Branches:
  - main (last commit: 2 days ago)
  - feature/agent-omega (last commit: 3 days ago)
  - hotfix/critical-vulnerability (last commit: 1 day ago)
  ... and 2 more.
------------------------------------------
```

### 🤝 Community Benefit

In a world where autonomous agents are constantly evolving our codebase, understanding the collective effort and identifying active areas is paramount. This utility provides a quick, digestible overview, fostering transparency, aiding in project management, and celebrating the tireless work of our digital denizens. It helps us ensure no commit goes unnoticed and no branch withwers in obscurity.
