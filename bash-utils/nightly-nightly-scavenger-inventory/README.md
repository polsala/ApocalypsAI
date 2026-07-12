# Nightly Scavenger Inventory Generator

A whimsical Bash utility that reads a list of scavenged items (name, weight per unit, quantity) and produces a nicely formatted inventory report, total weight, and a tongue‑in‑cheek survival rating.

## Usage

```sh
cat items.txt | ./src/inventory.sh
```

`items.txt` format (one item per line):

```
<name> <weight_per_unit> <quantity>
```

**Example**:

```
water 2 5
canned_food 1 10
medkit 0.5 2
```

**Output**:

```
Scavenger Inventory:
- water x5 (2 each) = 10.00
- canned_food x10 (1 each) = 10.00
- medkit x2 (0.5 each) = 1.00
Total weight: 21.00 units
Survival rating: Sturdy
```

### Rating thresholds
- **< 20** → Feeble
- **20‑50** → Sturdy
- **> 50** → Titanic
