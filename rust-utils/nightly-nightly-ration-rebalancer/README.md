# Nightly Ration Rebalancer

`nightly-ration-rebalancer` is a high-performance CLI tool crafted in Rust to help survivors optimize and rebalance their precious food rations. In a world where every calorie counts, this utility ensures you meet your daily caloric needs while strategically prioritizing less perishable items, extending the life of your vital supplies.

## Features

*   **Calorie-based Optimization**: Calculates the most efficient way to meet a target caloric intake.
*   **Perishability Prioritization**: Automatically suggests consuming more perishable items first.
*   **Inventory Management**: Provides an updated inventory after the suggested consumption.
*   **CSV Input/Output**: Easy integration with existing inventory spreadsheets.

## Usage

```bash
nightly-ration-rebalancer <INPUT_CSV_FILE> --target-calories <CALORIES> [--output-csv <OUTPUT_CSV_FILE>]
```

### Arguments:

*   `<INPUT_CSV_FILE>`: Path to the CSV file containing your current ration inventory.
*   `--target-calories <CALORIES>`: The desired daily caloric intake (e.g., `2000`).
*   `--output-csv <OUTPUT_CSV_FILE>` (Optional): Path to save the updated inventory after rebalancing. If not provided, the updated inventory is printed to stdout.

## Input CSV Format

The input CSV file should have the following columns, in this exact order:

`name,calories_per_unit,units_available,perishability_score`

*   `name`: (String) The name of the food item (e.g., "Canned Beans", "Dried Fruit").
*   `calories_per_unit`: (Integer) Calories provided by one unit of the item.
*   `units_available`: (Integer) How many units of this item you currently possess.
*   `perishability_score`: (Integer, 1-5) A score indicating how quickly the item spoils.
    *   `1`: Very low perishability (e.g., MREs, canned goods).
    *   `2`: Low perishability (e.g., dried goods, jerky).
    *   `3`: Medium perishability (e.g., root vegetables, hard cheese).
    *   `4`: High perishability (e.g., fresh fruits, some dairy).
    *   `5`: Very high perishability (e.g., fresh meat, leafy greens).

### Example `inventory.csv`:

```csv
Canned Beans,200,10,1
Dried Fruit,50,20,2
Fresh Apple,95,3,5
MRE,1200,5,1
Survival Bar,300,15,2
```

## Output

The tool will print a daily ration plan to `stdout` and, if `--output-csv` is specified, save the remaining inventory to the specified file.

### Example Output (to stdout):

```
--- Daily Ration Plan (Target: 2000 Calories) ---
Consume 3 units of Fresh Apple (285 calories)
Consume 1 unit of MRE (1200 calories)
Consume 2 units of Canned Beans (400 calories)
Total Consumed: 1885 calories (Remaining: 115 calories to target)

--- Remaining Inventory ---
Canned Beans,8,200,1
Dried Fruit,20,50,2
MRE,4,1200,1
Survival Bar,15,300,2
```

## Building and Running

To build the utility, navigate to its directory and run:

```bash
cargo build --release
```

Then, you can run it from the `target/release/` directory:

```bash
./target/release/nightly-ration-rebalancer inventory.csv --target-calories 2000
```

## Tests

To run the tests, use:

```bash
cargo test
```
