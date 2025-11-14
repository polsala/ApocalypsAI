# Pre-Commit Pep Talk Generator

## Overview

Feeling a bit drained before that next commit? The `pre-commit-pep-talk` utility is here to inject a dose of whimsy and motivation into your development workflow! This simple Python script analyzes your staged Git changes and delivers a tailored, often humorous, pep talk right before you commit.

It's designed to be integrated as a `pre-commit` hook, adding a moment of reflection and a smile to your coding routine.

## Features

*   **Contextual Pep Talks**: Messages vary based on the size and scope of your staged changes (no changes, small, medium, large).
*   **Whimsical & Encouraging**: Lightens the mood during development.
*   **Self-Contained**: Pure Python, minimal dependencies.
*   **Easy Integration**: Designed for use with Git `pre-commit` hooks.

## Installation

1.  **Navigate to your repository's `.git/hooks` directory**:
    ```bash
    cd .git/hooks
    ```

2.  **Create a new file named `pre-commit` (or edit an existing one)**:
    ```bash
    touch pre-commit
    chmod +x pre-commit
    ```

3.  **Add the following lines to your `pre-commit` file**:
    ```bash
    #!/bin/sh
    # Run the ApocalypsAI Pre-Commit Pep Talk Generator
    python3 ../../utils/pre-commit-pep-talk/src/pep_talk.py

    # IMPORTANT: If you have other pre-commit checks, add them here.
    # If any pre-commit hook exits with a non-zero status, the commit will be aborted.
    # For this utility, we always exit 0 to not block commits.
    exit 0
    ```

    *Note: Adjust the `python3` path if necessary for your environment. The path `../../utils/pre-commit-pep-talk/src/pep_talk.py` assumes you are running from `.git/hooks` and the `utils` directory is at the repository root.*

## Usage

Once installed, simply stage your changes (`git add .`) and attempt to commit (`git commit -m "Your message"`). The pep talk will be printed to your console before the commit message editor appears (or before the commit is finalized if using `-m`).

```bash
# Stage some changes
git add .

# Commit and receive your pep talk!
git commit -m "feat: added cosmic alignment to commit messages"
```

## Example Output

```
✨ ApocalypsAI Pre-Commit Pep Talk ✨

You're weaving a tapestry of logic, one thoughtful change at a time. The digital loom hums with your progress. Keep up the excellent work!
```

## Development

To run the script manually for testing:

```bash
python3 utils/pre-commit-pep-talk/src/pep_talk.py
```
