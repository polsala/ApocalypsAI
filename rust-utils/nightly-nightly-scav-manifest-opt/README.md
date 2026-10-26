# Nightly Scavenger Manifest Optimizer

`nightly-scav-manifest-opt` is a high-performance CLI tool designed to help survivors optimize their packing strategy for scavenged items. Given a list of items with their value, weight, and volume, and the maximum capacity of your container, this tool will suggest the most efficient items to pack to maximize total value.

## Features

*   **Efficient Packing**: Uses a greedy algorithm to prioritize items with the best value-to-weight ratio, while respecting both weight and volume limits.
*   **CSV Input**: Easily define your scavenged items in a simple CSV format.
*   **Clear Output**: Provides a detailed report of packed items, total value, weight, and volume.

## Installation

To build and run this utility, you need Rust and Cargo installed.

```bash
cargo install --path .
```

Alternatively, you can build it directly:

```bash
cargo build --release
./target/release/nightly-scav-manifest-opt --help
```

## Usage

```bash
nightly-scav-manifest-opt --file <PATH_TO_CSV> --max-weight <MAX_WEIGHT_KG> --max-volume <MAX_VOLUME_L>
```

### Arguments

*   `--file <PATH_TO_CSV>`: Required. Path to the CSV file containing your item data.
*   `--max-weight <MAX_WEIGHT_KG>`: Required. The maximum weight (in kilograms) your container can hold.
*   `--max-volume <MAX_VOLUME_L>`: Required. The maximum volume (in liters) your container can hold.

### Input CSV Format

The CSV file must have a header row with `name`, `value`, `weight`, and `volume` columns. Each subsequent row represents an item.

*   `name`: (String) The name of the item.
*   `value`: (Integer) A numerical representation of the item's survival value or utility.
*   `weight`: (Float) The item's weight in kilograms.
*   `volume`: (Float) The item's volume in liters.

**Example `items.csv`:**

```csv
name,value,weight,volume
Rusty Spoon,1,0.1,0.05
Can of Beans,10,0.5,0.3
Water Bottle (empty),5,0.2,1.0
First Aid Kit,20,1.0,0.5
Tattered Blanket,8,2.0,5.0
Multi-tool,15,0.3,0.1
```

## Example Run

```bash
nightly-scav-manifest-opt --file items.csv --max-weight 2.0 --max-volume 2.0
```

**Expected Output:**

```
--- Scavenger Manifest Optimization Report ---
Container Capacity: Max Weight = 2.00kg, Max Volume = 2.00L
Packed Items:
  - Multi-tool (Value: 15, Weight: 0.30kg, Volume: 0.10L)
  - Water Bottle (empty) (Value: 5, Weight: 0.20kg, Volume: 1.00L)
  - Can of Beans (Value: 10, Weight: 0.50kg, Volume: 0.30L)
  - First Aid Kit (Value: 20, Weight: 1.00kg, Volume: 0.50L)
---------------------------------------------
Total Packed Value: 50
Total Packed Weight: 2.00kg
Total Packed Volume: 1.90L
```
