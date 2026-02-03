# nightly-git-gremlin-tracker

Detects unusual commit activity patterns in Git repositories.

## Usage

```bash
./src/git_gremlin_tracker.sh <repo-path> [threshold]
```

- `repo-path`: Path to the Git repository.
- `threshold`: (Optional) Number of commits to consider "unusual" (default: 10).

## Example

```bash
./src/git_gremlin_tracker.sh /path/to/repo 5
```

## Output

Prints a list of authors with unusual commit activity and their commit counts.
