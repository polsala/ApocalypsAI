# Git Gremlin Groomer

## 🧹 Tame Your Local Git Branches!

The Git Gremlin Groomer is a whimsical yet highly practical utility designed to help you keep your local Git repository pristine. It identifies and suggests the removal of stale local branches – those that have been merged into your current `HEAD` or whose remote tracking branch has vanished into the cosmic void.

No more digital dust bunnies cluttering your `git branch` output! This tool helps you maintain a lean, mean, development machine.

## ✨ Features

*   **Identify Merged Branches**: Finds local branches that have already been merged into your current branch.
*   **Identify Gone Remote Branches**: Detects local branches whose corresponding remote branch no longer exists (marked as `[origin/branch: gone]`).
*   **Dry Run Mode**: Safely preview which branches would be deleted without making any changes.
*   **Interactive Deletion**: Optionally delete selected stale branches.

## 🚀 Usage

1.  **Navigate to your Git repository** in your terminal.
2.  **Run the groomer**: `python3 path/to/gremlin_groomer.py [options]`

### Options:

*   `--list` or `-l`: List all identified stale branches (default behavior if no other action is specified).
*   `--delete` or `-d`: Prompt to delete identified stale branches.
*   `--dry-run` or `-n`: Show what *would* be deleted without actually deleting anything. Can be combined with `--delete`.
*   `--current-branch <branch_name>`: Specify the branch to compare against for 'merged' status (defaults to current HEAD).

### Examples:

*   **Just list stale branches:**
    ```bash
    python3 utils/git-gremlin-groomer/src/gremlin_groomer.py --list
    ```

*   **Preview deletion of stale branches:**
    ```bash
    python3 utils/git-gremlin-groomer/src/gremlin_groomer.py --delete --dry-run
    ```

*   **Interactively delete stale branches:**
    ```bash
    python3 utils/git-gremlin-groomer/src/gremlin_groomer.py --delete
    ```

## 🛠️ Requirements

*   Python 3.6+
*   Git installed and accessible in your PATH

## 📦 Installation

Simply place the `gremlin_groomer.py` file in your desired location. It's self-contained!

```bash
mkdir -p utils/git-gremlin-groomer/src
mkdir -p utils/git-gremlin-groomer/tests
# Copy gremlin_groomer.py into src/ and test_gremlin_groomer.py into tests/
```
