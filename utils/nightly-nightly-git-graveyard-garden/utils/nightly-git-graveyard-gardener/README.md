# Nightly Git Graveyard Gardener

## 🌿 Overview

The Nightly Git Graveyard Gardener is a whimsical-yet-useful utility designed to help you prune the overgrown thickets of your local Git repository. Over time, local branches accumulate – merged, abandoned, or simply forgotten. This tool helps you identify and optionally delete these stale branches, keeping your local workspace tidy and your `git branch` output a joy to behold.

## ✨ Features

*   **Identify Merged Branches**: Finds local branches that have already been merged into your current `HEAD` (e.g., `main` or `develop`).
*   **Identify Stale Branches**: Detects branches that haven't seen activity in a configurable number of days.
*   **Interactive Deletion**: Prompts you before deleting any branches, giving you full control.
*   **Dry Run Mode**: See what would be deleted without actually performing any actions.

## 🚀 Usage

Navigate to your Git repository and run the `gardener.py` script.

```bash
python src/gardener.py --help
```

### Examples:

1.  **List all deletable branches (dry run):**
    ```bash
    python src/gardener.py --dry-run
    ```

2.  **List branches merged into `main` and older than 30 days, then interactively delete:**
    ```bash
    python src/gardener.py --merged --days 30
    ```

3.  **Delete all branches merged into `main` without confirmation (use with caution!):**
    ```bash
    python src/gardener.py --merged --force
    ```

## ⚙️ Arguments

*   `--merged`: Include branches that are already merged into the current HEAD.
*   `--days <N>`: Include branches whose last commit is older than `N` days.
*   `--dry-run`: Show what would be deleted without actually deleting anything.
*   `--force`: Delete branches without asking for confirmation. Use with extreme caution!
*   `--current-branch <name>`: Specify the current branch to compare against (defaults to `HEAD`). Useful for testing or specific scenarios.

## 🛠️ Development

The gardener uses standard Python and relies on `subprocess` to interact with Git.

### Running Tests

```bash
python -m unittest tests/test_gardener.py
```
