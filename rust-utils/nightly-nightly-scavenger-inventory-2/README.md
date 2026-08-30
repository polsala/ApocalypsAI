# nightly-scavenger-inventory

**Nightly Scavenger Inventory** is a tiny Rust command‑line utility that helps post‑apocalypse wanderers keep track of their loot.

It reads a CSV file describing items you have collected and prints:

* Total quantity per category (e.g., food, medicine, tools)
* Items that will expire within the next 7 days
* A random, whimsical survival tip to keep morale high

## CSV format

The input file must be UTF‑8 encoded and contain a header row with the following columns:

```
name,category,quantity,expiration_date
```

* `name` – free‑form description of the item
* `category` – one word categorising the item (e.g., `food`, `medicine`, `tool`)
* `quantity` – integer amount you possess
* `expiration_date` – ISO‑8601 date (`YYYY‑MM‑DD`). Use `9999‑12‑31` for non‑perishable items.

Example:

```
name,category,quantity,expiration_date
Canned Beans,food,12,2024-12-01
Bandage,medicine,5,2025-01-15
Rope,tool,2,9999-12-31
```

## Installation

```bash
# Install Rust toolchain if you haven't already
curl https://sh.rustup.rs -sSf | sh
# Clone the repository and build
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/rust-utils/nightly-scavenger-inventory
cargo build --release
```

The binary will be located at `target/release/nightly-scavenger-inventory`.

## Usage

```bash
# Print help
./nightly-scavenger-inventory --help

# Generate a report from inventory.csv
./nightly-scavenger-inventory inventory.csv
```

The program writes the report to standard output.

## Testing

```bash
cargo test
```

All tests are deterministic and run offline.

## License

MIT – see the root LICENSE file.
