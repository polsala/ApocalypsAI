# Nightly Survival Packer

Generates a random survival kit list that fits within a user‑specified weight limit using a greedy knapsack algorithm. Perfect for post‑apocalyptic role‑play or real‑world emergency prep.

## Installation

```sh
npm install -g ts-node typescript
```

## Usage

```sh
npx ts-node src/index.ts --max-weight 12
```

Outputs a list of items whose total weight does not exceed the given limit.

## How it works

The utility sorts a predefined list of survival items by their utility‑to‑weight ratio and then greedily picks items while staying under the weight limit.

