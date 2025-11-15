# Pre-Apocalypse Resource Allocator

A whimsical-yet-useful command-line utility designed to help you strategically distribute vital resources among your survival group in a hypothetical pre-apocalyptic scenario. Optimize your chances of survival by ensuring everyone gets what they need, from food and water to specialized tools and medical supplies.

## Philosophy

In the face of impending doom, efficient resource management is paramount. This tool provides a simple, deterministic algorithm to allocate resources based on individual needs and specialized skills, bringing a touch of order to the chaos of the end times.

## Features

*   **Needs-Based Allocation**: Prioritizes essential resources like water and food based on declared survivor needs.
*   **Skill-Based Assignments**: Automatically assigns specialized items (e.g., medkits to medics, tools to engineers) if available.
*   **Scarcity Handling**: Gracefully manages situations where resources are limited, highlighting unmet needs.
*   **Clear Output**: Provides a detailed allocation plan, remaining resources, and a list of any unfulfilled requirements.

## Installation

This utility is self-contained and written in Python 3.11+. No external dependencies are required beyond the standard library.

1.  Navigate to the `utils/pre-apocalypse-resource-allocator/` directory.
2.  Ensure you have Python 3.11 or newer installed.

## Usage

The `allocator.py` script can be run directly from the command line.

```bash
python src/allocator.py
```

### Customizing Resources and Survivors

To use the allocator with your own data, modify the `resources` and `survivors` dictionaries within the `main()` function of `src/allocator.py`.

**Example `resources` dictionary:**

```python
resources = {
    "food_rations": 100,      # Total units of food available
    "water_bottles": 50,      # Total units of water available
    "medkits": 10,            # Total medkits available (skill-assigned)
    "tools": 5                # Total tools available (skill-assigned)
}
```

**Example `survivors` list:**

```python
survivors = [
    {
        "name": "Alice",
        "needs": {"food_rations": 10, "water_bottles": 5}, # Daily needs
        "skills": ["medic"]                               # Specialized skills
    },
    {
        "name": "Bob",
        "needs": {"food_rations": 8, "water_bottles": 4},
        "skills": ["engineer"]
    },
    {
        "name": "Charlie",
        "needs": {"food_rations": 12, "water_bottles": 6},
        "skills": ["scavenger"] # Skills not explicitly handled by item assignment are ignored for now
    },
]
```

The script will then print the allocation plan, remaining resources, and any unmet needs to the console.

## Development and Testing

To run the automated tests for this utility:

1.  Navigate to the `utils/pre-apocalypse-resource-allocator/` directory.
2.  Run the tests using `unittest`:

    ```bash
    python -m unittest tests/test_allocator.py
    ```

All tests are deterministic and run offline, ensuring consistent results.
