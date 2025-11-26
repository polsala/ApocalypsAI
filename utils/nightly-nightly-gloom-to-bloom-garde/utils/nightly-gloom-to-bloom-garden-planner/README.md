# Nightly Gloom-to-Bloom Garden Planner

## 🌻 Transform Desolation into Cultivation 🌻

In the grim aftermath, every patch of fertile ground is a treasure. The `Nightly Gloom-to-Bloom Garden Planner` is your trusty companion for turning barren lands into bountiful harvests. This utility helps you strategically plan your survival garden, optimizing plant placement based on available space, prevailing climate conditions, and your precious seed inventory.

Maximize your yield, diversify your crops, and ensure your community thrives, one carefully planted seed at a time!

## Usage

Run the planner from your terminal, providing the total available area, the dominant climate zone, and a path to your seed inventory JSON file.

```bash
python src/planner.py \
  --area <total_area_in_sq_meters> \
  --climate <climate_zone> \
  --seeds <path_to_seeds_json_file>
```

### Arguments:

*   `--area`: Total available garden area in square meters (e.g., `10.5`).
*   `--climate`: The dominant climate zone for your region (e.g., `temperate`, `arid`, `cold`, `warm`). This helps filter for suitable plants.
*   `--seeds`: Path to a JSON file containing your seed inventory. See `Example seeds.json` below.

### Example:

```bash
python src/planner.py --area 15.0 --climate temperate --seeds my_seeds.json
```

### Example `my_seeds.json` format:

```json
[
  {
    "name": "Carrot",
    "space_sqm": 0.1,
    "yield_units": 5,
    "climate_zones": ["temperate", "cold"]
  },
  {
    "name": "Potato",
    "space_sqm": 0.5,
    "yield_units": 20,
    "climate_zones": ["temperate"]
  },
  {
    "name": "Tomato",
    "space_sqm": 0.3,
    "yield_units": 12,
    "climate_zones": ["temperate", "warm"]
  },
  {
    "name": "Cactus Fruit",
    "space_sqm": 1.0,
    "yield_units": 1,
    "climate_zones": ["arid"]
  }
]
```

## Output

The planner will output a detailed planting plan, including the number of each plant to sow, the total space they will occupy, and their estimated total yield. It will also provide a summary of total space utilized and any remaining unused area.

```
--- Gloom-to-Bloom Garden Plan ---
Available Area: 15.00 sqm
Climate Zone: Temperate

Planting Details:
  - 100x Carrot (uses 10.00 sqm, est. yield: 500 units)
  - 10x Potato (uses 5.00 sqm, est. yield: 200 units)

Summary:
  Total estimated yield: 700 units
  Total space utilized: 15.00 sqm
  Remaining unused space: 0.00 sqm
```
