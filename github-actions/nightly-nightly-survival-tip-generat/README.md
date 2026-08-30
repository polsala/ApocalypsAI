# Survival Tip Generator Action

Generates a whimsical post‑apocalyptic survival tip based on a numeric seed. The tip is exposed as the `survival_tip` output for downstream steps.

## Inputs

- `seed` (required): Integer seed to select the tip.

## Outputs

- `survival_tip`: The generated survival tip.

## Example

```yaml
steps:
  - uses: ./nightly-survival-tip-generator
    with:
      seed: 42
  - run: echo "Tip: ${{ steps.nightly-survival-tip-generator.outputs.survival_tip }}"
```
