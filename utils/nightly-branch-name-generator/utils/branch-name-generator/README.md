# Branch Name Generator

A whimsical yet practical utility that turns any piece of text—like an issue title—into a clean, kebab‑case Git branch name.

## Features

- Normalises case and whitespace.
- Strips disallowed characters, keeping only alphanumerics and hyphens.
- Collapses consecutive hyphens and trims leading/trailing hyphens.
- Truncates to a sensible length (50 characters).
- Detects naming collisions against a supplied list of existing branches and appends a numeric suffix (`-1`, `-2`, …) to guarantee uniqueness.

## Usage

```bash
python -m branch_name_generator "Add support for user avatars" --existing "feature/login,bugfix/avatar"
```

Will output:
```
add-support-for-user-avatars
```

If `add-support-for-user-avatars` already exists, the utility will emit `add-support-for-user-avatars-1` (or `-2`, etc.).

## Running the Tests

```bash
cd utils/branch-name-generator
python -m unittest discover -s tests
```

All tests are deterministic and run offline.
