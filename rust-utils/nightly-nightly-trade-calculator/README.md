# nightly-trade-calculator

A whimsical Rust CLI that evaluates the fairness of barter trades in a post‑apocalyptic world.

## Usage

```sh
cargo run -- give water=3 food=2 receive ammo=1 medicine=1
```

The tool will compute the total value of each side using a built‑in price list and report whether the trade is fair.

## Price List

- water: 2
- food: 3
- ammo: 5
- medicine: 8
- fuel: 4

## Output

- `Fair trade!`
- `Unfair trade: you lose X value.`
- `Unfair trade: you gain X value.`
