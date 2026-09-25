# nightly-emoji-commit-annotator

A tiny GitHub Action that adds a random emoji in front of a commit message. Great for sprinkling a little personality into your commit history without any manual effort.

## Usage

Add this action as a step in any workflow where you have access to the commit message (e.g., after a `git commit` or in a PR workflow).

```yaml
steps:
  - name: Get last commit message
    id: get_msg
    run: |
      echo "msg=$(git log -1 --pretty=%B)" >> $GITHUB_OUTPUT

  - name: Annotate commit with emoji
    uses: ./
    with:
      commit_message: ${{ steps.get_msg.outputs.msg }}

  - name: Show annotated message
    run: |
      echo "Annotated: ${{ steps.annotate.outputs.annotated_message }}"
```

The action outputs `annotated_message` which you can use in subsequent steps (e.g., for tagging releases, posting to Slack, etc.).

## How it works

The action runs a small Bash script that:
1. Holds a static list of emojis.
2. Picks one based on a deterministic seed (the workflow run ID) or the current timestamp.
3. Prepends the chosen emoji to the provided commit message.
4. Emits the result via the standard GitHub Actions output mechanism.

## Testing

Run the provided test script locally:

```bash
chmod +x tests/test_annotate.sh
./tests/test_annotate.sh
```

The test forces a known seed to ensure the emoji selection is predictable.
