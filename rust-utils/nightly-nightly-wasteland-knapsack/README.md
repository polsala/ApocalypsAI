# Nightly Wasteland Knapsack

**What it does**

A whimsical yet practical command‑line utility that helps post‑apocalyptic scavengers decide which items to carry.  Given a list of items (name, weight, value) and a maximum carry weight, it computes the optimal subset that maximizes total value using the classic 0/1 knapsack algorithm.

**Why it’s useful**

* No more guesswork when the radiation is rising.
* Works offline – pure Rust, no network calls.
* Perfect for role‑playing games, teaching algorithms, or real‑world budgeting of limited resources.

**Installation**

```bash
# From the utility directory
cargo build --release
# Binary will be at target/release/nightly-wasteland-knapsack
```

**Usage**

```bash
nightly-wasteland-knapsack <capacity> [input_file]
```

* `capacity` – maximum total weight you can carry (integer).
* `input_file` – optional path to a file containing items; if omitted, the program reads from **STDIN**.

Each line of the input must contain three whitespace‑separated fields:

```
<name> <weight> <value>
```

* `name` – identifier for the item (no spaces).
* `weight` – integer weight of the item.
* `value` – integer value (utility, rarity, etc.).

**Example**

```text
$ cat items.txt
apple 5 10
bread 4 7
candy 2 4

$ nightly-wasteland-knapsack 7 items.txt
Optimal total value: 14
Selected items:
- apple
- candy
```

**Testing**

Run the bundled tests with:

```bash
cargo test
```

---

*Feel free to adapt the utility for any kind of resource‑allocation puzzle – the apocalypse is just a theme!*
