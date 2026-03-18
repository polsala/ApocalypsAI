# nightly-scavenger-inventory

**What it does**

A tiny Rust command‑line tool for post‑apocalyptic survivors. It reads a CSV list of scavenged supplies (name, quantity, expiration date) and:

1. Sorts the items so the ones that will expire soonest appear first.
2. Prints a friendly suggestion of the *best* item to use right now.

The utility is deliberately whimsical – it pretends you’re managing a bunker pantry – but the underlying logic (CSV parsing, date handling, sorting) is genuinely useful for any small inventory‑tracking script.

**How to build**

```bash
# Clone the repository (or copy the generated folder) and cd into it
cargo build --release
```

**How to run**

```bash
# Provide a CSV file (or pipe via stdin)
cat supplies.csv | cargo run --quiet
```

**CSV format**

```
name,quantity,expiration_date
Water Bottle,10,2025-12-31
Canned Beans,5,2024-03-15
Radiated Fruit,2,2023-09-01
```

* `expiration_date` must be in ISO‑8601 (YYYY‑MM‑DD).

**Example output**

```
Sorted inventory (soonest expiry first):
1. Radiated Fruit – 2 pcs – expires 2023-09-01
2. Canned Beans – 5 pcs – expires 2024-03-15
3. Water Bottle – 10 pcs – expires 2025-12-31

Suggestion: Use "Radiated Fruit" first!
```

**Testing**

Run the bundled tests with:

```bash
cargo test
```

The tests use mock CSV strings, so they run offline and deterministically.
