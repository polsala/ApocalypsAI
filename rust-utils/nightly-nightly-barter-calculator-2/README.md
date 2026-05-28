# nightly-barter-calculator

Utility to calculate barter exchange rates between items in a post‑apocalyptic setting.

## Usage

```sh
cargo run -- <ITEM_A> <ITEM_B> <VALUE_A> <VALUE_B>
```

- **ITEM_A** – Name of the first item (e.g., `water`).
- **ITEM_B** – Name of the second item (e.g., `canned-food`).
- **VALUE_A** – Barter value of one unit of ITEM_A (numeric).
- **VALUE_B** – Barter value of one unit of ITEM_B (numeric).

### Example

```sh
cargo run -- water canned-food 3 5
```

Output:
```
You need 1.67 water to equal 1 canned‑food
```

## Build & Test

```sh
cargo build --release
cargo test
```

The tool is deliberately lightweight and has no external dependencies beyond the Rust standard library.
