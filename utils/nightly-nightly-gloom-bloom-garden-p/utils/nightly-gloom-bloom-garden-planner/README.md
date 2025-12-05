# Nightly Gloom & Bloom Garden Planner

## 🌻 Cultivating Hope in the Rubble 🌻

The world might be a bit... dusty, but life finds a way! The Gloom & Bloom Garden Planner is your trusty companion for cultivating sustenance and beauty in the post-apocalyptic landscape. This utility helps you maximize your yield by suggesting resilient plants tailored to your garden's specific conditions.

### Features

*   **Intelligent Plant Suggestions**: Recommends hardy, apocalypse-proof plants based on your garden's light and soil conditions.
*   **Space Optimization**: Calculates how many of each suggested plant can fit in your available garden area.
*   **Simple & Self-Contained**: A lightweight Python script, easy to run and integrate into your survival toolkit.

### How to Use

1.  **Navigate** to the `nightly-gloom-bloom-garden-planner` directory.
2.  **Run** the `planner.py` script from your terminal:

    ```bash
    python src/planner.py --width <garden_width> --length <garden_length> --light <sun|partial|shade> --soil <sandy|loamy|clay>
    ```

    *   `<garden_width>`: The width of your garden plot in arbitrary units (e.g., meters, feet). Must be a positive number.
    *   `<garden_length>`: The length of your garden plot in arbitrary units. Must be a positive number.
    *   `<light>`: The predominant light condition: `sun` (6+ hours direct), `partial` (3-6 hours direct), or `shade` (<3 hours direct).
    *   `<soil>`: The primary soil type: `sandy`, `loamy`, or `clay`.

### Example

```bash
python src/planner.py --width 5 --length 10 --light sun --soil loamy
```

This will output a list of suitable plants and their estimated quantities for a 5x10 unit garden with full sun and loamy soil.

### Plant Data

The planner uses a built-in database of resilient plants. Each plant has preferences for light, soil, and requires a certain amount of "space units".

### Development

Contributions are welcome! If you have suggestions for new resilient plants or improvements to the planning algorithm, feel free to open an issue or PR.

### License

This utility is released under the MIT License.
