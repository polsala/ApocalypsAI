# Apocalypse Scavenger List Generator

This utility helps you prepare for the inevitable by generating a prioritized list of items to scavenge in a post-apocalyptic scenario. Whether you're focused on survival, comfort, or just a good laugh, this tool can help you plan your next supply run.

## Features

-   **Category-based filtering**: Focus on specific needs like 'survival', 'food', 'tools', 'morale', or 'luxury'.
-   **Priority sorting**: Items are ranked by their inherent usefulness in a dire situation.
-   **Customizable output**: Specify the number of items you need.
-   **Whimsical yet practical**: A curated list of items ranging from life-saving essentials to important morale boosters (like rubber ducks).

## Usage

To generate a list, run the `scavenger.py` script with desired categories and an optional item count.

```bash
python src/scavenger.py --categories survival food tools --count 10
python src/scavenger.py --categories morale luxury --count 5
python src/scavenger.py --categories all
```

### Arguments

-   `--categories <category1> <category2> ...`: Space-separated list of categories to include. Use `all` for all available categories. Available categories include: `survival`, `food`, `water`, `medical`, `tools`, `shelter`, `communication`, `defense`, `knowledge`, `comfort`, `morale`, `entertainment`, `luxury`.
-   `--count <int>`: (Optional) The maximum number of items to display. Defaults to all matching items.

## Example Output

```
--- Apocalypse Scavenging List (Categories: survival, food, tools) ---
1. Water Purification Tablets (Survival, Priority: 10)
2. Canned Beans (Food, Priority: 9)
3. First Aid Kit (Medical, Priority: 9)
4. Multi-tool (Tools, Priority: 8)
5. Duct Tape (Tools, Priority: 7)
6. Hand-crank Radio (Communication, Priority: 7)
7. Sleeping Bag (Shelter, Priority: 6)
8. Flashlight (Tools, Priority: 6)
9. Rope (Tools, Priority: 5)
10. Manual Coffee Maker (Comfort, Priority: 5)
```

## Development

The item database is stored in `src/items.json`. Feel free to expand it with your own post-apocalyptic essentials and oddities!
