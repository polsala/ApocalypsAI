# Apocalypse Morale Boost Action

This GitHub Action prints a random morale‑boosting message suitable for a post‑apocalypse setting. It can be used in any workflow to add a bit of whimsical encouragement.

## Usage

```yaml
jobs:
  morale:
    runs-on: ubuntu-latest
    steps:
      - uses: ./.github/actions/nightly-apocalypse-morale-boost
        id: boost
      - run: echo "Boost: ${{ steps.boost.outputs.message }}"
```

## Outputs

- `message`: The selected morale‑boosting message.

## Implementation

The action is a composite action that runs a small Bash script (`src/boost.sh`) which selects a random line from a predefined list.
