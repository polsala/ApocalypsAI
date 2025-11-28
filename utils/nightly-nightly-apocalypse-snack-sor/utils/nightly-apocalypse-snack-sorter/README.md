# Nightly Apocalypse Snack Sorter

## Overview
In the grim future of the ApocalypsAI, every calorie counts and every day of shelf life is a victory. The 'Nightly Apocalypse Snack Sorter' is your trusty companion for organizing your vital food supplies. This utility helps you sort your provisions based on their shelf life and caloric density, ensuring you consume the most perishable and least calorically dense items first, or prioritize long-lasting, high-energy sustenance when needed.

## Features
- Sorts food items from a CSV file.
- Primary sort by 'Shelf Life' (descending).
- Secondary sort by 'Calories per Serving' (descending).
- Outputs sorted list to console or a new file.

## Usage

### Input File Format
Create a CSV file (e.g., `supplies.csv`) with the following columns:
`Item Name,Shelf Life (days),Calories per serving,Category`

Example `supplies.csv`:
```csv
Canned Beans,1825,200,Canned
Rice,3650,130,Dry Goods
Water Bottle,365,0,Beverage
MRE,1825,1200,Prepared Meal
Chocolate Bar,365,250,Snack
Dried Fruit,730,100,Snack
```

### Running the Sorter
```bash
python src/sorter.py --input supplies.csv --output sorted_supplies.csv
```

**Arguments:**
- `--input <file_path>`: Path to the input CSV file (required).
- `--output <file_path>`: Path to the output CSV file (optional). If not provided, output will be printed to stdout.

## Example Output (to stdout):
```
Sorted Supplies:
----------------
Item Name         | Shelf Life (days) | Calories per serving | Category
-----------------------------------------------------------------------
Rice              | 3650              | 130                  | Dry Goods
MRE               | 1825              | 1200                 | Prepared Meal
Canned Beans      | 1825              | 200                  | Canned
Dried Fruit       | 730               | 100                  | Snack
Chocolate Bar     | 365               | 250                  | Snack
Water Bottle      | 365               | 0                    | Beverage
```
