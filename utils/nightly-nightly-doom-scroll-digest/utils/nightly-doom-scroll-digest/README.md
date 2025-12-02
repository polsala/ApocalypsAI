# Nightly Doom Scroll Digest

## The Scroll of Recent Portents

This utility, the 'Nightly Doom Scroll Digest', is designed to provide a concise, yet dramatically-toned summary of recent activity within a specified GitHub repository. It acts as your daily oracle, revealing the latest 'anomalies', 'convergences', and 'temporal fluxes' that have transpired, ensuring you are always aware of the unfolding narrative of your project.

### Features

*   **Configurable Repository**: Specify any public or private GitHub repository.
*   **Time Window**: Define how many days back to look for activity.
*   **Dramatic Summaries**: Presents new issues, pull requests, and commits with a thematic flair.
*   **Direct Links**: Provides direct URLs to all mentioned activities for quick inspection.

### Usage

To run the digest generator, execute the `digest_generator.py` script with the required arguments:

```bash
python src/digest_generator.py \
  --repo-owner <repository_owner> \
  --repo-name <repository_name> \
  --github-token <your_github_token> \
  --days-back <number_of_days>
```

**Example:**

```bash
python src/digest_generator.py \
  --repo-owner polsala \
  --repo-name ApocalypsAI \
  --github-token ghp_YOUR_TOKEN \
  --days-back 7
```

### Arguments

*   `--repo-owner` (required): The owner of the GitHub repository (e.g., `polsala`).
*   `--repo-name` (required): The name of the GitHub repository (e.g., `ApocalypsAI`).
*   `--github-token` (required): A GitHub Personal Access Token with `repo` scope for private repositories, or `public_repo` for public ones. This is crucial for accessing the GitHub API and avoiding rate limits. **It is highly recommended to pass this via an environment variable or secure secret management, not directly on the command line in production environments.**
*   `--days-back` (optional, default: 1): The number of days to look back for activity.

### Example Output

```

--- The Scroll of Recent Portents ---

Date: 2023-10-27
Repository: polsala/ApocalypsAI

--- New Anomalies Detected (Issues) ---

*   [#123] The UI is melting again! (open) - https://github.com/polsala/ApocalypsAI/issues/123
*   [#122] Feature Request: Add more lasers (closed) - https://github.com/polsala/ApocalypsAI/issues/122

--- Convergences Observed (Pull Requests) ---

*   [#45] feat: Implement self-destruct button (merged) - https://github.com/polsala/ApocalypsAI/pull/45
*   [#44] fix: Prevent accidental self-destruct (open) - https://github.com/polsala/ApocalypsAI/pull/44

--- Temporal Fluxes Recorded (Commits) ---

*   [a1b2c3d] feat: Add more lasers (John Doe) - https://github.com/polsala/ApocalypsAI/commit/a1b2c3d
*   [e4f5g6h] docs: Update apocalypse timeline (Jane Smith) - https://github.com/polsala/ApocalypsAI/commit/e4f5g6h

--- The Oracle has spoken. ---
```
