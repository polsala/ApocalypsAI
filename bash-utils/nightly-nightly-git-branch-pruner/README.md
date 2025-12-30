# nightly-git-branch-pruner

**Utility:** List (and optionally delete) local Git branches that have already been merged into the current branch **and** are older than a configurable number of days.

## Why?
In a busy repository, stale merged branches linger on developers' machines, cluttering `git branch` output and wasting disk space. This script helps you keep your local repo tidy without risking unmerged work.

## Installation
```bash
# Clone the utility into your preferred utilities directory
mkdir -p ~/apocalypsai-utils && cd ~/apocalypsai-utils
git clone https://github.com/your-org/ApocalypsAI.git  # (or just copy the folder)
chmod +x utils/bash-utils/nightly-git-branch-pruner/src/branch_pruner.sh
```
Add the script to your `$PATH` or invoke it directly:
```bash
./utils/bash-utils/nightly-git-branch-pruner/src/branch_pruner.sh [options]
```

## Usage
```bash
branch_pruner.sh [--days N] [-d]
```
- `--days N` – Only consider branches whose *last commit* is **older** than `N` days. Default is `30`.
- `-d` – Delete the branches that meet the criteria after listing them. **Use with care!**

### Examples
```bash
# Show branches older than 60 days that are already merged
branch_pruner.sh --days 60

# Show and delete those branches
branch_pruner.sh --days 60 -d
```

## How it works
1. Detect the current branch (`git rev-parse --abbrev-ref HEAD`).
2. Find all local branches merged into the current branch (`git branch --merged`).
3. For each merged branch, retrieve the timestamp of its most recent commit.
4. Compare that timestamp against the cutoff (`now - days*86400`).
5. Print matching branches; optionally delete them with `git branch -d`.

## Testing
Run the bundled test suite to verify functionality:
```bash
cd utils/bash-utils/nightly-git-branch-pruner/tests
bash test_branch_pruner.sh
```
The tests create a temporary Git repository, fabricate old and recent branches, and assert that the script correctly identifies (and optionally deletes) the stale merged branch.

## License
MIT – see the root `LICENSE` file.
