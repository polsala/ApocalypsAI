# Nightly Scavenger Knapsack

A whimsical CLI tool to help post‑apocalypse scavengers decide which items to carry given a weight limit. Uses the classic 0/1 knapsack algorithm.

## Installation

```sh
cargo install --path .
```

## Usage

Provide the capacity (maximum total weight) as the sole argument and feed a list of items via **stdin**. Each line should contain three whitespace‑separated fields:

```
<name> <weight> <value>
```

* **name** – Identifier for the item (no spaces)
* **weight** – Positive integer representing how heavy the item is
* **value** – Positive integer representing the usefulness of the item

### Example

Create a file `items.txt`:

```
water 3 10
food 2 9
medkit 5 15
radio 1 4
```

Run the tool with a capacity of 10:

```sh
cat items.txt | nightly-scavenger-knapsack 10
```

Expected output:

```
Total value: 34
Selected items:
- water
- food
- radio
```

## License

MIT
