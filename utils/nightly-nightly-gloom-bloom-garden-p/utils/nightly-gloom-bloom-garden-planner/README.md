# Nightly Gloom & Bloom Garden Planner

## 🌻 Overview

In the grim aftermath, every patch of soil is precious. The "Gloom & Bloom Garden Planner" is your AI-powered horticultural assistant, designed to help survivors make the most of their limited resources. This utility takes your available climate, soil type, and planting space, then suggests an optimal planting plan from a catalog of resilient crops, prioritizing fast-growing and high-yield options to keep you fed and your spirits up!

## ✨ Features

*   **Intelligent Crop Selection**: Filters plants based on your specific climate and soil conditions.
*   **Space Optimization**: Calculates how many of each suitable plant can fit into your available square footage.
*   **Yield Estimation**: Provides an estimated yield in kilograms for your planned garden.
*   **Fast-Growth Priority**: Automatically prioritizes crops with shorter growth cycles for quicker harvests.
*   **JSON Output**: Delivers a structured plan for easy integration with other survival systems (or just for reading!).

## 🚀 How to Use

The utility is a Python 3.11 script.

### Prerequisites

*   Python 3.11 or higher

### Running the Planner

Navigate to the `src` directory and run the `planner.py` script with the required arguments:

```bash
python src/planner.py --climate <climate_zone> --soil <soil_type> --space <available_space_sqft>
```

**Arguments:**

*   `--climate`: The current climate zone. Examples: `warm`, `temperate`, `cool`.
*   `--soil`: The type of soil available. Examples: `loamy`, `sandy`, `clay`, `any`.
*   `--space`: The total square footage (float) available for planting.

### Example

Let's plan a garden for a `temperate` climate with `loamy` soil and `15.0` square feet of space:

```bash
python src/planner.py --climate temperate --soil loamy --space 15.0
```

**Example Output:**

```json
{
  "climate_zone": "temperate",
  "soil_type": "loamy",
  "available_space_sqft": 15.0,
  "planting_plan": [
    {
      "name": "Radish",
      "quantity": 75,
      "space_used_sqft": 15.0,
      "estimated_yield_kg": 37.5,
      "notes": "Fast-growing, good for quick harvests."
    }
  ],
  "total_space_used_sqft": 15.0,
  "total_estimated_yield_kg": 37.5,
  "remaining_space_sqft": 0.0,
  "notes": "Plan prioritizes faster-growing plants suitable for specified conditions. Yields are estimates."
}
```

## 🧪 Testing

To ensure the planner is always ready for the next planting season, run the self-contained tests:

```bash
python -m unittest tests/test_planner.py
```

## 📜 Plant Catalog

The planner uses an internal catalog of resilient plants. This catalog can be extended or modified directly within `src/planner.py` to adapt to new discoveries or mutations in the post-apocalyptic flora. Each plant entry includes:

*   `name`: Common name of the plant.
*   `type`: Category (e.g., `vegetable`, `herb`, `flower`).
*   `growth_time_days`: Approximate days from planting to harvest.
*   `preferred_climate`: List of suitable climate zones.
*   `preferred_soil`: List of suitable soil types.
*   `space_required_sqft`: Square footage needed per plant.
*   `yield_per_sqft`: Estimated yield in kilograms per square foot.
*   `notes`: Any special considerations or benefits.
