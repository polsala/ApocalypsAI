Nightly PR Celebration Action

This GitHub Action posts a whimsical celebratory comment on a pull request when it is merged. It extracts the PR number and title from the webhook payload and uses the GITHUB_TOKEN to create a comment like:

🎉 Congratulations on merging PR #42: Fix time distortion! Keep the apocalypse at bay!

Usage:

Create a workflow that triggers on pull_request_target with types: [closed] and runs this action.

Add the action to your repo under .github/actions/nightly-pr-celebration-action.
