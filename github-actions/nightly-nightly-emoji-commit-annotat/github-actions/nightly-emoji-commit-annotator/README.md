# Nightly Emoji Commit Annotator

A whimsical GitHub Action that appends a random (or deterministic) emoji to a given message, perfect for brightening commit messages, PR titles, or any text in your CI pipelines.

## Usage

```yaml
uses: ./github-actions/nightly-emoji-commit-annotator
with:
  message: "Refactor authentication flow"
```

The action outputs `annotated_message` which will be the original message followed by an emoji.

## Inputs

- `message` (required): The text to annotate.

## Outputs

- `annotated_message`: The original message with an appended emoji.

## Example

```yaml
- name: Annotate commit message
  id: annotate
  uses: ./github-actions/nightly-emoji-commit-annotator
  with:
    message: ${{ github.event.head_commit.message }}

- name: Show result
  run: echo "Annotated: ${{ steps.annotate.outputs.annotated_message }}"
```

## Implementation Details

The action is a tiny Node.js script that selects an emoji from a built‑in list. If the environment variable `SEED` is set, the selection becomes deterministic (useful for testing).
