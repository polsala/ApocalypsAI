# Nightly Scarcity Sentiment

## Overview
In the grim future of the ApocalypsAI, every item holds a story and a potential for survival. The `nightly-scarcity-sentiment` utility helps you quantify the emotional and practical value of your precious post-apocalyptic possessions. It calculates a "Scarcity Sentiment Score" for any item, considering its category, your perceived value, and how long you've managed to hold onto it.

This whimsical-yet-useful tool assists survivors in prioritizing their inventory, making tough decisions about what to keep, trade, or use immediately. A higher score indicates an item is more critical or valuable in your current context.

## How it Works
The utility uses a predefined set of scarcity factors for common item categories (e.g., food, medicine, tools). It combines these base factors with your subjective "perceived value" (on a scale of 1-10) and applies a decay factor based on how many days you've held the item. This decay simulates spoilage, wear-and-tear, or simply the diminishing novelty of an item over time.

## Installation
1. Navigate to the `node-utils/nightly-scarcity-sentiment` directory.
2. No external dependencies are required beyond Node.js itself.

## Usage
Run the utility from your terminal with the following arguments:

```bash
node src/index.js <itemName> <category> <perceivedValue(1-10)> <daysHeld>
```

### Arguments:
*   `<itemName>`: The name of the item (e.g., "Can of Beans", "Rusty Crowbar").
*   `<category>`: The general category of the item. Available categories are: `food`, `water`, `medicine`, `tools`, `ammo`, `fuel`, `luxury`, `information`, `components`, `shelter_material`, `misc`.
*   `<perceivedValue(1-10)>`: Your subjective rating of the item's value, from 1 (low) to 10 (high).
*   `<daysHeld>`: The number of days you've possessed the item (0 or more).

### Example:
```bash
node src/index.js 'Emergency Rations' food 9 15
```

## Development & Testing
To run the automated tests:

```bash
node tests/test_index.js
```
