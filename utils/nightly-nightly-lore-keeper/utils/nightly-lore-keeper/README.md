# Nightly Lore Keeper

The Nightly Lore Keeper is a vigilant utility designed to safeguard the integrity of your project's historical chronicles – its Git commit messages. In the post-apocalyptic landscape of code, a clear and consistent commit history is paramount for understanding the evolution of your codebase and ensuring future maintainability.

This tool automatically scans recent commit messages against a set of configurable rules, helping to enforce conventions like subject line length, conventional commit prefixes, and the presence of descriptive bodies.

## Features

*   **Subject Line Length Check**: Ensures commit subject lines adhere to a maximum character limit (default: 72).
*   **Conventional Commit Enforcement**: Verifies that subject lines start with a recognized conventional commit type (e.g., `feat:`, `fix:`, `docs:`).
*   **Body Presence Check**: Can be configured to require a commit body, especially for shorter subject lines, promoting detailed explanations.
*   **Excludes Merge Commits**: Focuses only on authored commits, ignoring automatically generated merge messages.
*   **Configurable Rules**: Easily adjust rules to fit your team's specific "lore" standards.

## Usage

To run the Lore Keeper, navigate to the root of your Git repository and execute the `lore_keeper.py` script:

```bash
python src/lore_keeper.py
```

The script will check the last 10 non-merge commit messages by default and report any violations to standard output.

### Configuration

The rules are currently hardcoded within `src/lore_keeper.py` in the `main()` function's `config` dictionary. You can modify these values directly to customize the Lore Keeper's vigilance:

```python
# Default configuration in src/lore_keeper.py
config = {
    'num_commits_to_check': 10,             # Number of recent non-merge commits to check
    'max_subject_length': 72,               # Maximum allowed characters for the subject line
    'conventional_commit_prefixes': [       # List of required prefixes for conventional commits
        'feat:', 'fix:', 'docs:', 'chore:', 'refactor:', 'test:', 'build:', 'ci:', 'perf:', 'revert:'
    ],
    'min_body_length': 0,                   # Minimum required characters for the commit body (0 for no requirement)
    'require_body_for_short_subject': False # If True, requires a body if subject length < 20 chars
}
```

**Note**: Future versions might introduce external configuration files (e.g., `lore_keeper.json` or `pyproject.toml`) for easier customization without modifying the source code.

## Development

### Running Tests

To ensure the Lore Keeper is functioning correctly, run its self-contained tests:

```bash
python -m unittest tests/test_lore_keeper.py
```

The tests use `unittest.mock` to simulate Git command output, ensuring deterministic and offline execution.

## Exit Codes

*   `0`: All recent commit messages adhere to the configured lore.
*   `1`: One or more commit message violations were detected.
*   `2`: No commit messages found or unable to retrieve them (e.g., not in a Git repo, or no commits yet).
