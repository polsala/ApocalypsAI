# Repo Mood Ring

## Gaze into the Git Log and Discern the Repository's Emotional State

The ApocalypsAI Repo Mood Ring is a whimsical yet surprisingly insightful utility designed to give you a quick, high-level understanding of the sentiment within your Git repository. By analyzing recent commit messages, it attempts to determine if your project is currently feeling 'Joyful/Optimistic', 'Stressed/Urgent', 'Calm/Steady', 'Confused/Uncertain', or simply 'Neutral/Routine'.

Think of it as a digital mood ring for your codebase, reflecting the collective emotional temperature of recent development activity.

## How it Works

1.  **Git Log Analysis**: The utility executes `git log` to fetch the subject lines of the most recent commit messages (defaulting to the last 50, but configurable).
2.  **Keyword Matching**: Each commit message is scanned for a predefined set of keywords associated with different emotional states (e.g., "feat", "bug", "docs", "wip").
3.  **Mood Determination**: Based on the frequency and weight of these keywords, a dominant mood is identified.
4.  **Whimsical Summary**: A short, evocative summary is generated to describe the repository's current emotional state.

## Installation

This utility is self-contained and requires only Python 3.11+ and Git installed on your system. No external Python packages are needed.

## Usage

Navigate to your repository's root directory (or specify its path) and run the `mood_ring.py` script:

```bash
python utils/repo-mood-ring/src/mood_ring.py <path_to_your_repo>
```

**Example:**

```bash
# From the ApocalypsAI root directory, analyze itself
python utils/repo-mood-ring/src/mood_ring.py .

# Analyze another repository
python utils/repo-mood-ring/src/mood_ring.py /path/to/another/project
```

### Arguments:

*   `<repo_path>`: The path to the Git repository you want to analyze (e.g., `.` for the current directory).
*   `--num-commits <int>`: (Optional) The number of recent commits to analyze. Defaults to 50.

### Output:

The utility outputs a JSON object containing the determined `mood`, a `summary` description, and the `analyzed_commits` count.

```json
{
  "mood": "Joyful/Optimistic",
  "summary": "A vibrant glow! The repository is buzzing with positive energy and exciting new developments.",
  "analyzed_commits": 25
}
```

## Mood Categories

*   **Joyful/Optimistic**: New features, improvements, successful fixes, positive refactors.
*   **Stressed/Urgent**: Critical bugs, hotfixes, errors, broken functionality, deadlines.
*   **Calm/Steady**: Documentation updates, routine chores, styling, testing, CI/CD improvements.
*   **Confused/Uncertain**: Work in progress, investigations, explorations, questions, experiments.
*   **Neutral/Routine**: General updates, minor builds, default if no strong sentiment is detected.

## Contributing

Feel free to suggest new keywords, refine mood detection logic, or add more whimsical summaries! Pull requests are welcome.
