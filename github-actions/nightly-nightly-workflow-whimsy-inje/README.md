# Nightly Workflow Whimsy Injector

Injects a random, whimsical, and positive message into a GitHub Actions workflow run summary, promoting a lighter atmosphere and a moment of digital zen.

## ✨ What it Does

This GitHub Action adds a delightful, randomly selected message to your workflow's run summary. It's a small touch to brighten your day, remind you to take a break, or simply add a bit of unexpected joy to your CI/CD pipeline.

## 🚀 Usage

Add this action to any step in your workflow. The message will be appended to the `GITHUB_STEP_SUMMARY` file, which GitHub automatically renders as part of your workflow run's summary page.

```yaml
name: My Whimsical Workflow

on: [push, workflow_dispatch]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build Project
        run: echo "Building..."

      - name: Inject Whimsy
        uses: ./utils/nightly-workflow-whimsy-injector # Path to this action in your repo
        id: whimsy_injection

      - name: Report Whimsy (Optional)
        run: echo "Today's dose of whimsy: ${{ steps.whimsy_injection.outputs.whimsy-message }}"

      - name: Deploy Project
        run: echo "Deploying..."
```

### Custom Messages

You can provide your own list of whimsical messages by creating a text file (one message per line) and passing its path to the `message-file` input.

`my_whimsical_messages.txt`:
```
May your code be clean and your coffee strong!
Remember to stretch your fingers and your imagination.
A pixelated rainbow for your digital journey!
```

```yaml
      - name: Inject Custom Whimsy
        uses: ./utils/nightly-workflow-whimsy-injector
        with:
          message-file: ./my_whimsical_messages.txt
```

## ⚙️ Inputs

| Input Name         | Description                                                                                             | Required | Default        |
|--------------------|---------------------------------------------------------------------------------------------------------|----------|----------------|
| `message-file`     | Optional path to a file containing whimsical messages (one per line). If not provided, uses internal defaults. | `false`  | (Internal list) |
| `test-message-index` | **For testing purposes only:** Picks the message at this 0-indexed position from the list. Overrides random selection. | `false`  | (Random)       |

## 📤 Outputs

| Output Name      | Description                               |
|------------------|-------------------------------------------|
| `whimsy-message` | The whimsical message that was injected. |

## 🧪 Testing

The action includes a `tests/test.yml` workflow that demonstrates how to use the `test-message-index` input for deterministic testing of the action's output and summary injection. This allows for reliable verification without relying on random selection during tests.
