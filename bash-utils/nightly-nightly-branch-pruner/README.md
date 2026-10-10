# nightly-branch-pruner

Utility to list (and optionally delete) local git branches that have already been merged into a base branch (default `main`). Helps keep your repository tidy.

## Usage

```sh
./branch_pruner.sh [-b base_branch] [-d] [-r remote]
```

- `-b base_branch` : Base branch to compare against (default: `main`).
- `-d` : Delete the merged branches (dry‑run by default).
- `-r remote` : Remote name to delete remote branches as well (default: none).

The script prints the branches it would delete. With `-d` it actually deletes them locally and, if `-r` is provided, also on the remote.

## Example

```sh
# Dry‑run (default)
./branch_pruner.sh

# Delete merged branches locally
./branch_pruner.sh -d

# Delete merged branches locally and on origin
./branch_pruner.sh -d -r origin
```

## Safety

The script never deletes the base branch itself and skips `main`/`master`. Use `-d` only when you are sure.
