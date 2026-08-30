Nightly Commit Emoji Enhancer

Adds a random emoji to the most recent commit message. This reusable GitHub Actions workflow can be invoked from other workflows to automatically brighten commit history.

Usage:

In your workflow, call:

jobs:
  add-emoji:
    uses: ./github-actions/nightly-commit-emoji-enhancer/src/workflow.yml
    with:
      emoji_list: '🚀,✨,🔥'

The workflow will pick a random emoji from the list (or default list) and amend the last commit, then force‑push.

Note: Requires write permissions on the repository.
