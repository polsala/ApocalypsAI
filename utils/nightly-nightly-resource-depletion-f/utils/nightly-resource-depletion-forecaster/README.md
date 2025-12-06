# Nightly Resource Depletion Forecaster

## 🔮 Overview

The `nightly-resource-depletion-forecaster` is a crucial utility for any post-apocalyptic (or just highly chaotic) environment. It helps you keep track of vital resources by predicting how many 'days until depletion' based on their current stock and estimated daily consumption. No more nasty surprises when your last can of 'Nutrient Paste 7' runs out!

## ✨ Features

-   **Configurable Resources**: Define any number of resources, their current quantity, and daily consumption rate.
-   **Depletion Forecast**: Calculates the estimated days remaining for each resource.
-   **Visual Indicators**: Uses a simple emoji system to give you an at-a-glance status:
    -   🟢 Plenty (more than 30 days left, or infinite)
    -   🟡 Stable (15-30 days left)
    -   🟠 Warning (5-14 days left)
    -   🔴 Critical (1-4 days left)
    -   💀 Depleted (0 days left or negative)
-   **Self-Contained**: Written in Python, requires `PyYAML` for YAML config files.

## 🚀 Usage

1.  **Create a configuration file** (e.g., `resources.yaml`):

    ```yaml
    resources:
      - name: Water Rations
        current_amount: 150
        daily_consumption: 5
      - name: Power Cells
        current_amount: 30
        daily_consumption: 2
      - name: Medical Supplies
        current_amount: 10
        daily_consumption: 0.5
      - name: Scrap Metal
        current_amount: 500
        daily_consumption: 100
      - name: Ancient Knowledge Scrolls
        current_amount: 3
        daily_consumption: 0
      - name: Last Hope Fuel
        current_amount: 2
        daily_consumption: 1
      - name: Broken Drones
        current_amount: 0
        daily_consumption: 1
    ```

2.  **Run the forecaster**:

    ```bash
    python src/forecaster.py --config resources.yaml
    ```

    Or, if you want to use a different config file (JSON is also supported):

    ```bash
    python src/forecaster.py --config path/to/your/custom_config.json
    ```

## 📊 Example Output

```
Resource                  | Current | Consump. | Days Left | Status
--------------------------|---------|----------|-----------|--------
Water Rations             | 150.0   | 5.0      | 30.0      | 🟡 Stable
Power Cells               | 30.0    | 2.0      | 15.0      | 🟡 Stable
Medical Supplies          | 10.0    | 0.5      | 20.0      | 🟡 Stable
Scrap Metal               | 500.0   | 100.0    | 5.0       | 🟠 Warning
Ancient Knowledge Scrolls | 3.0     | 0.0      | ∞         | 🟢 Plenty
Last Hope Fuel            | 2.0     | 1.0      | 2.0       | 🔴 Critical
Broken Drones             | 0.0     | 1.0      | 0.0       | 💀 Depleted
```

## 🛠️ Development

### Requirements

-   Python 3.6+
-   `PyYAML` (for YAML config files, install with `pip install PyYAML`)

### Running Tests

```bash
python -m unittest tests/test_forecaster.py
```
