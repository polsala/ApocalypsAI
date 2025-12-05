# Nightly Scavenger Stash Sorter

A crucial utility for any discerning post-apocalyptic scavenger! The Nightly Scavenger Stash Sorter helps you quickly categorize your daily haul, assign priority, and suggest optimal storage locations or disposal methods. No more guessing where that "mysterious glowing rock" should go!

## Features

*   **Automated Categorization**: Uses predefined keywords to sort items into categories like Food, Tools, Materials, Medical, and Junk.
*   **Priority Assignment**: Each category comes with a suggested priority (High, Medium, Low).
*   **Storage Suggestions**: Get recommendations for where to stash your treasures (or trash).
*   **Flexible Input**: Process items from a direct list or a file.

## Usage

### Prerequisites

*   Python 3.6+ (standard library only)

### Running the Sorter

You can run the sorter in two ways:

1.  **Directly with a comma-separated list of items:**

    ```bash
    python src/sorter.py --items "apple,rusty wrench,scrap metal,bandages,broken toy,purified water"
    ```

2.  **With a file containing one item per line:**

    First, create a file named `haul.txt` (or any name you prefer):

    ```
    # haul.txt
    old boot
    can of beans
    copper wire
    painkillers
    hammer
    strange glowing mushroom
    ```

    Then, run the sorter:

    ```bash
    python src/sorter.py --file haul.txt
    ```

### Example Output

```
--- Scavenger's Stash Report ---

Item: apple
  Category: Food
  Priority: High
  Location: Pantry

Item: rusty wrench
  Category: Tools
  Priority: Medium
  Location: Workshop

Item: scrap metal
  Category: Materials
  Priority: Medium
  Location: Storage Shed

Item: bandages
  Category: Medical
  Priority: High
  Location: Infirmary

Item: broken toy
  Category: Junk
  Priority: Low
  Location: Disposal Pile

Item: purified water
  Category: Food
  Priority: High
  Location: Pantry

Item: strange glowing mushroom
  Category: Uncategorized
  Priority: Unknown
  Location: Undetermined

--- End of Report ---
```

## Customization

The categorization rules are embedded within `src/sorter.py`. For advanced users, you can modify the `CATEGORIZATION_RULES` dictionary in the `StashSorter` class to add new categories, keywords, priorities, or locations to better suit your specific post-apocalyptic needs.
