Nightly Scavenger Knapsack
==========================

Overview
--------
In a post‑apocalyptic world every gram counts.  This tiny Rust command‑line tool helps you decide which scavenged items to carry by solving the classic 0/1 knapsack problem.  Give it a weight capacity and a list of items (name, weight, value) and it will tell you the maximum total value you can fit.

Build & Run
-----------
```sh
# Build the binary (requires Rust toolchain)
cargo build --release

# Run the program
# Provide the capacity as the sole argument and feed items via stdin.
# Each line must contain: <name> <weight> <value>
# Example:
cat <<EOF | cargo run --release -- 7
water 3 10
food 2 7
medkit 5 12
EOF
```

Output
------
The program prints the maximum achievable value for the given capacity.

Example Output
--------------
```
Maximum value: 19
```

Explanation
-----------
For the example above the best combination is `food` (weight 2, value 7) and `medkit` (weight 5, value 12) which fits exactly into the capacity of 7 and yields a total value of 19.

Testing
-------
Run the test suite with:
```sh
cargo test
```
All tests are deterministic and run offline.
