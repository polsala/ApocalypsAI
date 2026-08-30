# Nightly Chrono-Clutter Sorter

A type-safe TypeScript CLI tool designed to help you organize your digital detritus into whimsical, apocalypse-themed temporal categories. Define your own categories and rules in a JSON configuration file, then feed it a list of items (tasks, links, notes, etc.) to get them sorted into a more manageable, if slightly anachronistic, order.

## Features

*   **Whimsical Categorization**: Sort items into categories like 'Urgent Void', 'Temporal Drift', 'Future Echo', and 'Forgotten Relic'.
*   **Customizable Rules**: Define keywords or phrases that automatically assign items to specific categories.
*   **Type-Safe**: Built with TypeScript for robust and predictable behavior.
*   **CLI Interface**: Easily integrate into your workflow.

## Installation

1.  Navigate to the `nightly-chrono-clutter-sorter` directory.
2.  Install dependencies:
    ```bash
    npm install
    ```

## Usage

First, create a configuration file (e.g., `config.json`) that defines your categories and sorting rules. Each rule consists of a `keyword` and a `targetCategoryId`.

**`example-config.json`:**
```json
{
  "categories": [
    { "id": "urgent-void", "name": "Urgent Void", "description": "Critical tasks requiring immediate attention before temporal collapse.", "priority": 1 },
    { "id": "temporal-drift", "name": "Temporal Drift", "description": "Important but not immediate; can float for a bit.", "priority": 2 },
    { "id": "future-echo", "name": "Future Echo", "description": "Long-term plans, ideas, or things to consider for the distant future.", "priority": 3 },
    { "id": "forgotten-relic", "name": "Forgotten Relic", "description": "Low priority, archival, or items that might never be revisited.", "priority": 4 }
  ],
  "rules": [
    { "keyword": "urgent", "targetCategoryId": "urgent-void" },
    { "keyword": "critical", "targetCategoryId": "urgent-void" },
    { "keyword": "bug", "targetCategoryId": "urgent-void" },
    { "keyword": "review", "targetCategoryId": "temporal-drift" },
    { "keyword": "plan", "targetCategoryId": "future-echo" },
    { "keyword": "idea", "targetCategoryId": "future-echo" },
    { "keyword": "archive", "targetCategoryId": "forgotten-relic" }
  ],
  "defaultCategoryId": "temporal-drift"
}
```

Then, run the CLI tool, providing the path to your configuration file and the items you want to sort:

```bash
# Sort items using the example configuration
npx ts-node src/index.ts --config example-config.json "Fix critical time-loop bug" "Review PR for new temporal anomaly detector" "Plan next week's resource scavenging run" "Old notes on pre-apocalypse tech" "Urgent: replenish water supply"
```

**Expected Output:**

```
--- Chrono-Clutter Sorting Report ---

Category: Urgent Void (Critical tasks requiring immediate attention before temporal collapse.)
  - Fix critical time-loop bug
  - Urgent: replenish water supply

Category: Temporal Drift (Important but not immediate; can float for a bit.)
  - Review PR for new temporal anomaly detector
  - Old notes on pre-apocalypse tech

Category: Future Echo (Long-term plans, ideas, or things to consider for the distant future.)
  - Plan next week's resource scavenging run

Category: Forgotten Relic (Low priority, archival, or items that might never be revisited.)

-------------------------------------
```

## Development

To run tests:

```bash
npm test
```
