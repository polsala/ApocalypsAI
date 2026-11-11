# Nightly Ration Roulette

A containerized CLI tool designed to bring a touch of culinary adventure to the post-apocalyptic wasteland. It helps survivors make varied and balanced meal choices from their existing ration inventory, preventing the dreaded "flavor fatigue" that can set in when eating the same nutrient paste day after day.

## Features

*   **Randomized Meal Suggestions**: Based on user-defined meal compositions (e.g., "standard", "hearty", "snack").
*   **Category-Based Selection**: Ensures a balanced meal by picking items from categories like protein, carbs, fats, and veggies.
*   **Customizable Inventory**: Easily update your available rations and define new meal types via a simple JSON file.
*   **Containerized**: Runs in a Docker container for easy deployment and isolation.

## How to Use

### 1. Build the Docker Image

Navigate to the `nightly-ration-roulette` directory and build the Docker image:

```bash
docker build -t ration-roulette .
```

### 2. Customize Your Rations

The utility uses a `rations.json` file to manage your inventory and meal compositions. A template is provided at `src/rations_template.json`. You should copy this file, modify it to reflect your actual supplies, and mount it into the container.

**Example `rations.json` structure:**

```json
{
  "inventory": {
    "protein": [
      {"name": "Canned Tuna", "quantity": 5},
      {"name": "Dried Beef Jerky", "quantity": 10}
    ],
    "carb": [
      {"name": "Hardtack Biscuits", "quantity": 20}
    ],
    "veggie": [
      {"name": "Canned Green Beans", "quantity": 6}
    ]
  },
  "meal_composition": {
    "standard": ["protein", "carb", "veggie"],
    "snack": ["protein", "treat"]
  }
}
```

**Important:** Ensure `quantity` is greater than 0 for an item to be considered available.

### 3. Run the Ration Roulette

To get a meal suggestion, run the Docker container, mounting your custom `rations.json` file. You can specify a meal type as an argument (defaults to `standard`).

**Suggest a standard meal:**

```bash
docker run --rm -v "$(pwd)/my_rations.json:/app/rations.json" ration-roulette
```

**Suggest a hearty meal:**

```bash
docker run --rm -v "$(pwd)/my_rations.json:/app/rations.json" ration-roulette hearty
```

**Suggest a snack:**

```bash
docker run --rm -v "$(pwd)/my_rations.json:/app/rations.json" ration-roulette snack
```

Replace `my_rations.json` with the path to your customized inventory file.

## Development

### Local Setup

1.  **Prerequisites**: Python 3.9+.
2.  **Install dependencies**: None beyond standard library for this utility.
3.  **Run tests**: `python -m unittest tests/test_ration_roulette.py`

### Project Structure

```
. # nightly-ration-roulette/
├── README.md
├── Dockerfile
├── src/
│   ├── ration_roulette.py
│   └── rations_template.json
└── tests/
    └── test_ration_roulette.py
```

## Contributing

Feel free to suggest new features, meal types, or improvements! Just open an issue or pull request.
