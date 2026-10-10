# Commit Emoji Annotator Action

Adds a random, whimsical emoji prefix to a commit message (or any string) and returns it as an output.

## Usage
```yaml
name: Annotate Commit Message
on:
  workflow_dispatch:
    inputs:
      message:
        description: "The original commit message"
        required: true
jobs:
  annotate:
    runs-on: ubuntu-latest
    steps:
      - uses: ./
        with:
          message: "${{ github.event.head_commit.message }}"
      - name: Show annotated message
        run: echo "Annotated: ${{ steps.annotate.outputs.annotated_message }}"
```

## Inputs
| Name | Description | Required |
|------|-------------|----------|
| `message` | The original message to annotate. | Yes |

## Outputs
| Name | Description |
|------|-------------|
| `annotated_message` | The original message prefixed with a random emoji. |

## How it works
The action runs a small Bash script that selects a random emoji from a curated list and prepends it to the supplied message.

## License
MIT © ApocalypsAI
