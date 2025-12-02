# The Great Git Gremlin - Stale Branch Purger

## Overview

The `nightly-git-gremlin-branch-purger` is a mischievous yet helpful utility designed to combat the digital dust bunnies of your local Git repository: stale branches. It scans your local branches, identifies those that haven't seen activity in a while (defaulting to 30 days), and gives you the option to list them or even purge them.

Keep your workspace clean and your `git branch` output manageable!

## Usage

This utility requires `git` to be installed and accessible in your system's PATH.

```bash
# Navigate to your Git repository
cd /path/to/your/repo

# To list stale branches (default threshold: 30 days)
python3 src/gremlin.py

# To list stale branches with a custom threshold (e.g., 60 days)
python3 src/gremlin.py --days 60

# To list and suggest deletion commands for stale branches
python3 src/gremlin.py --suggest-delete

# To actually delete stale branches (USE WITH CAUTION!)
# This will attempt to delete branches that are merged into the current HEAD.
# For unmerged branches, it will fail unless you use -D (force delete), which this script does NOT do.
python3 src/gremlin.py --delete

# Combine options, e.g., suggest deletion for branches older than 90 days
python3 src/gremlin.py --days 90 --suggest-delete
```

## How it Works

1.  It uses `git branch --format="%(refname:short)"` to list all local branches.
2.  For each branch, it fetches the last commit date using `git log -1 --format="%cd" --date=iso-strict <branch_name>`.
3.  It compares this date with the current date, considering a branch stale if it's older than the specified number of days.
4.  Based on the command-line arguments, it either prints the stale branches, suggests `git branch -d` commands, or attempts to execute them.

## Requirements

*   Python 3.6+
*   Git installed and configured
