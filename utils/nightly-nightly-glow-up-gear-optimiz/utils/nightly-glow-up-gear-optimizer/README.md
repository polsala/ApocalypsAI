# Nightly Glow-Up Gear Optimizer

## 🌟 Optimize Your Post-Apocalyptic Loadout! 🌟

The wasteland is harsh, and every ounce counts. The Nightly Glow-Up Gear Optimizer helps you select the perfect set of gear for your next perilous expedition, ensuring you're always prepared without being overburdened. Whether you're scavenging for scraps, fending off mutated critters, or just trying to look fabulous in the ruins, this utility has your back!

### Features:
- **Intelligent Loadout Selection**: Prioritizes gear based on utility, condition, and relevance to your mission.
- **Weight Management**: Ensures your chosen gear stays within your carrying capacity.
- **Task-Specific Optimization**: Tailors recommendations for different post-apocalyptic activities.

### How to Use:

1.  **Prepare your gear data**: Create a JSON file (e.g., `gear_data.json`) containing a list of your available gear items. Each item should be a dictionary with `name`, `weight`, `base_utility`, `condition` (0.0-1.0), and `tags` (list of strings).

    Example `gear_data.json`:
    ```json
    [
      {"name": "Rusty Machete", "weight": 1.5, "base_utility": 7, "condition": 0.6, "tags": ["combat", "scavenging"]},
      {"name": "Duct Tape Roll", "weight": 0.2, "base_utility": 9, "condition": 1.0, "tags": ["repair", "utility"]},
      {"name": "Water Purifier (Broken)", "weight": 0.8, "base_utility": 8, "condition": 0.1, "tags": ["survival", "hydration"]},
      {"name": "Radiation Suit (Patched)", "weight": 5.0, "base_utility": 10, "condition": 0.7, "tags": ["protection", "survival"]},
      {"name": "Shiny Bottlecaps", "weight": 0.1, "base_utility": 1, "condition": 1.0, "tags": ["currency", "trade"]},
      {"name": "Medical Kit (Basic)", "weight": 0.7, "base_utility": 8, "condition": 0.9, "tags": ["medical", "survival"]}
    ]
    ```

2.  **Run the optimizer**: Execute the `optimizer.py` script with your gear data file, maximum weight capacity, and desired task tags.

    ```bash
    python src/optimizer.py --gear-file gear_data.json --max-weight 5.0 --task-tags scavenging combat
    ```

    Or for a general loadout:
    ```bash
    python src/optimizer.py --gear-file gear_data.json --max-weight 3.0
    ```

### Arguments:
- `--gear-file <path>`: Path to the JSON file containing your gear inventory. (Required)
- `--max-weight <float>`: Your maximum carrying capacity in arbitrary units (e.g., kg, lbs). (Required)
- `--task-tags <tag1> <tag2> ...`: Space-separated list of tags relevant to your current mission (e.g., `scavenging`, `combat`, `medical`). (Optional)

### Output:
The script will print the optimized loadout, including total weight and total effective utility.

```
Optimized Loadout for task(s) ['scavenging', 'combat'] (Max Weight: 5.0):
- Rusty Machete (Weight: 1.5, Utility: 4.2)
- Duct Tape Roll (Weight: 0.2, Utility: 9.0)
- Medical Kit (Basic) (Weight: 0.7, Utility: 7.2)
Total Weight: 2.4
Total Effective Utility: 20.4
```
