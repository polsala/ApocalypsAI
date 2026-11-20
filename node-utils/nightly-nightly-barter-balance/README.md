# nightly-barter-balance

Utility that suggests fair trade ratios between common post‑apocalypse supplies.

## Installation

```sh
# Clone the repository (or navigate to the generated folder)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/nightly-barter-balance
```

The utility is pure JavaScript and requires only Node.js (v14+).

## Usage

```sh
node src/main.js <item1> <quantity1> <item2> <quantity2>
```

Example:

```sh
node src/main.js water 10 ammo 5
```

The program will output a suggestion indicating whether the trade is balanced and, if not, how to adjust quantities to reach fairness.

## How it works

Each item has two hidden attributes:

- **rarity** – a score from 1 (common) to 5 (extremely rare)
- **utility** – a score from 1 (low usefulness) to 5 (high usefulness)

The **value** of an item is `rarity * utility`. The tool computes the total value on each side of the trade and, if the values differ, suggests the minimal number of additional items needed to balance the exchange.

## Supported items

| Item | Rarity | Utility |
|------|--------|---------|
| water | 1 | 5 |
| canned_food | 2 | 4 |
| ammo | 3 | 3 |
| medicine | 4 | 5 |
| fuel | 5 | 2 |

Feel free to extend the `items` map in `src/main.js` with your own supplies.
