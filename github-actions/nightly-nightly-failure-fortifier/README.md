# Nightly Failure Fortifier

A GitHub Action to inject a dose of whimsical, apocalypse-themed encouragement into your workflow summaries, specifically when a workflow fails. Because even in the darkest timelines, a little fortifying wisdom can help.

## 🚀 Usage

Add this action to your workflow, typically at the end, and configure it to run `if: failure()`.

```yaml
name: My CI Workflow

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Simulate a failing step
        run: exit 1 # This step will fail

      - name: Post Fortifying Message on Failure
        if: failure()
        uses: polsala/ApocalypsAI/nightly-failure-fortifier@main # Replace 'main' with your branch/tag
        with:
          messages: |
            "Even the strongest bunkers have a crack. Patch it up, survivor!"
            "The wasteland teaches resilience. This failure is just another lesson."
            "A broken circuit today means a stronger grid tomorrow. Keep building!"
            "Don't let the void consume your spirit. Debug, rebuild, overcome!"
            "The gears grind, but they never stop. Neither should you."
          fallback_message: "The void whispers, 'Try again, survivor.'"

      - name: Another step that runs after failure (e.g., cleanup)
        if: always()
        run: echo "Cleanup complete."
```

## ⚙️ Inputs

- `messages` (required):
  A multiline string of whimsical, apocalypse-themed messages or survival tips. The action will randomly select one from this list.
  Each message should be on a new line. You can optionally wrap them in quotes.

- `fallback_message` (optional, default: "The void whispers, 'Try again, survivor.'"):
  A single message to use if no `messages` are provided or if the provided `messages` list is empty after parsing.

## ✨ How it Works

When triggered (ideally `if: failure()`), the action selects a random message from the `messages` input. This message is then appended to the GitHub Actions workflow summary, providing a moment of reflection or dark humor amidst a failed build. If no messages are provided, it defaults to the `fallback_message`.
