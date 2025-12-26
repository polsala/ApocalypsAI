# Nightly Apocalypse Survival Tip

A tiny GitHub Action that selects a random post‑apocalyptic survival tip and exposes it via the `tip` output.

## Usage
```yaml
name: Survival Tip
on:
  workflow_dispatch:
jobs:
  tip:
    runs-on: ubuntu-latest
    steps:
      - uses: ./
        id: tip
      - run: echo "Survival tip: ${{ steps.tip.outputs.tip }}"
```

## How it works
The action runs a small Node.js script that picks a tip from an internal list. The selected tip is emitted using the standard `::set-output` command.

## Custom tip selection (testing)
Set the environment variable `FORCE_RANDOM` to a number between `0` and `1` to force a deterministic choice (useful for testing).

## License
MIT
