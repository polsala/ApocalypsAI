# Nightly Relic Identifier

## Summary
This utility helps survivors identify mysterious pre-apocalypse relics, suggests their original purpose, and offers whimsical post-apocalypse repurposing ideas. Ever found a 'shiny metal disc with a hole' and wondered what it was? This tool is for you!

## Usage

### Prerequisites
- Node.js (v14 or higher)

### Installation
1. Navigate to the `node-utils/nightly-relic-identifier` directory.
2. Run `npm install` to install dependencies (primarily `sinon` for testing).

### Running the utility
To identify an item, run the script with your item's description as an argument:

```bash
node src/index.js "shiny metal disc with a hole"
```

Example Output:
```
Relic Identified: Ancient Data Storage Disc (CD/DVD)
Original Purpose: Used to store digital information, music, or movies.
Repurposing Idea: Sharpen edges for a makeshift blade, use as a reflective signal mirror, or as a very durable coaster.
Survival Rating: Moderate
```

If no specific relic is identified, it will provide a generic response:

```bash
node src/index.js "odd glowing rock"
```

Example Output:
```
Relic Identified: Unknown Anomaly
Original Purpose: Lost to the mists of time, or perhaps never had one.
Repurposing Idea: Use as a paperweight, a conversation starter, or a very slow-acting poison (handle with care).
Survival Rating: Unpredictable
```

## How it Works
The utility uses a simple keyword matching system against an internal database of known relics (`src/relics.json`). The more keywords from a relic's definition match your description, the higher the chance of a correct identification.

## Extending the Relic Database
You can add new relics or modify existing ones by editing `src/relics.json`. Each entry should have:
- `keywords`: An array of strings that describe the item.
- `name`: The identified name of the relic.
- `purpose`: Its original pre-apocalypse function.
- `repurpose`: Whimsical or practical post-apocalypse uses.
- `survival_rating`: A rating of its general usefulness (e.g., Low, Moderate, High, Unpredictable).
