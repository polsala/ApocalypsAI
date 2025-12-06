# Chronicle Keeper

## A Survivor's Daily Log Generator

In the grim future of the ApocalypsAI, keeping a record of your daily struggles and triumphs is paramount. The `chronicle-keeper` is a simple, whimsical utility designed to help survivors document their experiences, resource status, morale, and observations in a structured Markdown format.

Whether you're fending off rogue AI drones or simply trying to remember where you stashed that last can of beans, this tool ensures your legacy (or at least your daily inventory) is preserved.

## How to Use

1.  Navigate to the `utils/chronicle-keeper/` directory.
2.  Run the Python script:
    ```bash
    python src/chronicle_keeper.py
    ```
3.  Follow the prompts to enter your daily events, resource updates, morale rating, and any other observations.
4.  A new Markdown file will be created in the `logs/` directory (which will be created if it doesn't exist) with the format `YYYY-MM-DD-chronicle.md`.

## Example Output (`logs/2023-10-27-chronicle.md`)

```markdown
# Chronicle Entry - 2023-10-27

## Key Events:

*   Scavenged Sector 7. Encountered a pack of feral drones. Managed to evade.
*   Repaired the perimeter fence near the west gate.

## Resource Status:

*   **Food**: 3 days remaining (found 2 cans of nutrient paste).
*   **Water**: 5 days remaining (purified 10 liters).
*   **Ammo**: 17 rounds (used 3 on a rogue squirrel).
*   **Medical Supplies**: Low (1 bandage, 0 painkillers).

## Morale:

★★★☆☆ (3/5 - A bit weary, but hopeful after finding food.)

## Observations & Reflections:

Saw strange lights in the northern sky tonight. Could be a new AI patrol, or perhaps a glimmer of hope? Must investigate tomorrow if resources allow. The silence is getting louder.
```
