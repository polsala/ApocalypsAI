# Nightly Repo Storyteller

## 📜 Once Upon a Commit...

This utility transforms the mundane `git log` into a captivating narrative, telling the story of your repository's journey. It identifies key milestones, celebrates prolific contributors, and paints a picture of your project's evolution, all with a touch of whimsy.

## ✨ Features

*   **Chronological Narrative**: Generates a story from the earliest commit to the latest.
*   **Contributor Spotlight**: Highlights the most active developers.
*   **Milestone Recognition**: Points out significant commits (e.g., initial setup, major features, bug fixes).
*   **Development Pace**: Gives a sense of how active the repository has been.

## 🚀 Usage

To run the storyteller from your repository's root directory (or any subdirectory within a Git repository):

```bash
python src/storyteller.py
```

The story will be printed to standard output.

## 🛠️ Development

### Requirements

*   Python 3.11+
*   `git` installed and accessible in your PATH.

### Running Tests

Navigate to the `utils/nightly-repo-storyteller` directory and run:

```bash
python -m unittest tests/test_storyteller.py
```

## 🧙 How it Works

The `storyteller.py` script uses Python's `subprocess` module to execute `git log` commands. It parses the output to extract commit details like author, date, and message. This data is then analyzed to identify patterns, calculate statistics, and finally, to generate a human-readable, whimsical story about the repository's life and the adventurers who shaped it.
