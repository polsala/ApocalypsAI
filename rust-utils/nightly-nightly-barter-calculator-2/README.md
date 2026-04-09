# Nightly Barter Calculator

A whimsical command‑line utility for the post‑apocalyptic trader in you. It assigns a simple numeric value to items based on their rarity and utility, then suggests a fair exchange ratio between two items.

## Installation

```sh
cargo install --path .
```

## Usage

```sh
nightly-barter-calculator <item1> <rarity1> <utility1> <item2> <rarity2> <utility2>
```

All numeric arguments must be integers from 1 to 10.

### Example

```sh
nightly-barter-calculator "Rusty Pipe" 7 5 "Canned Beans" 3 8
```

Output:

```
1 Rusty Pipe ≈ 2.33 Canned Beans
```

## How it works

Each item gets a value = rarity × utility. The exchange ratio is the quotient of the two values, rounded to two decimal places.

## Testing

```sh
cargo test
```
