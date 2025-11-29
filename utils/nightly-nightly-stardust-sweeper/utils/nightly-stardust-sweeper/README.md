# Nightly Stardust Sweeper

## 🌌 Sweeping Away the Digital Stardust 🌌

The Nightly Stardust Sweeper is a whimsical yet practical utility designed to help keep your Git repositories sparkling clean. Over time, development branches can accumulate like cosmic dust, cluttering your repository and making navigation difficult. This tool identifies and lists "stale" branches – those that haven't seen activity in a configurable number of days – allowing you to easily identify candidates for cleanup.

Think of it as your personal digital garden gnome, pruning the overgrown branches of your codebase!

## ✨ Features

*   **Stale Branch Detection**: Identifies branches based on their last commit date.
*   **Configurable Threshold**: Set how many days of inactivity define a "stale" branch.
*   **Repository Agnostic**: Works with any local Git repository.
*   **Safe**: Only *lists* stale branches; it never deletes them. You decide what to prune!

## 🚀 Usage

1.  **Navigate to your repository**:
    ```bash
    cd /path/to/your/git/repo
    ```

2.  **Run the sweeper**:
    ```bash
    python3 src/stardust_sweeper.py --days 90
    ```
    This will list all branches that have not had a commit in the last 90 days.

    You can also specify a different repository path:
    ```bash
    python3 src/stardust_sweeper.py --repo /another/path/to/repo --days 180
    ```

## 🛠️ Development

The `stardust_sweeper.py` script uses standard `git` commands via `subprocess`. It's designed to be lightweight and self-contained.

## 🧪 Testing

To run the tests, navigate to the `nightly-stardust-sweeper` directory and execute:

```bash
python3 -m unittest tests/test_stardust_sweeper.py
```

Tests are fully mocked and do not require an actual Git repository or network access.
