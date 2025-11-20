# Nightly Git Graveyard Gardener

## 🌿 Overview

Are your local Git repositories starting to resemble a digital graveyard, cluttered with forgotten branches and ghostly remnants of past merges? Fear not, for the **Nightly Git Graveyard Gardener** is here to bring order to the chaos!

This whimsical utility helps you prune stale local branches, identify and remove branches already merged into your main development line, and even clean up remote-tracking branches that no longer exist on the remote. Keep your local workspace tidy, efficient, and free from the specter of forgotten code.

## ✨ Features

*   **Automatic Pruning**: Identifies and suggests deletion of local branches that have been merged into your current branch (e.g., `main` or `master`).
*   **Remote Sync**: Detects local branches that no longer have a corresponding remote branch, indicating they've been deleted upstream.
*   **Remote-Tracking Cleanup**: Offers to prune remote-tracking branches (`origin/feature-x`) that no longer exist on the remote.
*   **Interactive Mode**: Prompts for confirmation before deleting branches (default behavior).
*   **Dry Run**: See what would be deleted without making any changes.

## 🚀 Usage

Navigate to the root of your Git repository and run the `gardener.py` script:

```bash
python src/gardener.py
```

### Options:

*   `--dry-run`: Show what would be deleted without performing any actions.
*   `--force`: Delete branches without asking for confirmation.
*   `--no-prune-remote`: Skip pruning remote-tracking branches.

Example:

```bash
python src/gardener.py --dry-run
python src/gardener.py --force
```

## 🛠️ Development

This utility is written in Python 3.11 and uses standard library modules. 

### Running Tests

```bash
python -m unittest tests/test_gardener.py
```

## 📜 License

This project is licensed under the MIT License - see the `LICENSE` file for details.
