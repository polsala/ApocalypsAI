# Nightly Priority Scrambler

A whimsical-yet-useful CLI tool to help you prioritize your post-apocalyptic inventory, tasks, or anything else, based on configurable "survival factors" and keywords. Ever wondered if that 'Shiny Rock' is more important than a 'Broken Radio'? This tool will tell you!

## Features

*   **Type-Safe**: Built with TypeScript for robust data handling.
*   **Configurable Factors**: Define your own survival factors, their weights, and associated keywords.
*   **Detailed Rationale**: Understand *why* an item received its score.
*   **Flexible Input**: Prioritize anything from physical items to abstract tasks.

## Installation

1.  **Prerequisites**: Ensure you have Node.js (v18+) and npm/yarn installed.
2.  **Navigate**: Change into the `nightly-priority-scrambler` directory.
3.  **Install Dependencies**:
    ```bash
    npm install
    # or yarn install
    ```
4.  **Build (Optional, for production)**:
    ```bash
    npm run build
    ```

## Usage

Run the tool using `ts-node` (for development/quick runs) or `node` (after building):

```bash
# Using ts-node (requires ts-node to be installed globally or locally)
./node_modules/.bin/ts-node src/index.ts --items path/to/your_items.json --config path/to/your_config.json

# After building (npm run build)
node dist/index.js --items path/to/your_items.json --config path/to/your_config.json
```

### Input Files

#### `items.json` (Array of `Item` objects)

Each item should have an `id`, `name`, and optionally `description`, `tags`, and `basePriority`.

```json
[
  {
    "id": "1",
    "name": "Canned Beans",
    "description": "A staple, lasts forever.",
    "tags": ["food", "survival", "nutrition"],
    "basePriority": 70
  },
  {
    "id": "2",
    "name": "First Aid Kit",
    "tags": ["medical", "survival", "health"],
    "basePriority": 90
  },
  {
    "id": "3",
    "name": "Broken Radio",
    "description": "Needs repair, might get news from the outside.",
    "tags": ["communication", "electronics"],
    "basePriority": 30
  },
  {
    "id": "4",
    "name": "Shiny Rock",
    "description": "Looks pretty, no practical use, but good for morale.",
    "tags": ["trinket", "morale"],
    "basePriority": 10
  }
]
```

#### `config.json` (Single `Config` object)

Defines your survival factors, their weights, keywords, and whether they add or subtract from priority. Also sets a `defaultBasePriority`.

```json
{
  "factors": [
    {
      "name": "Survival Essential",
      "weight": 20,
      "keywords": ["survival", "food", "water", "medical"],
      "type": "positive"
    },
    {
      "name": "Communication Need",
      "weight": 15,
      "keywords": ["radio", "communication", "signal"],
      "type": "positive"
    },
    {
      "name": "Repair Required",
      "weight": 10,
      "keywords": ["broken", "needs repair", "damaged"],
      "type": "negative"
    },
    {
      "name": "Morale Boost",
      "weight": 5,
      "keywords": ["pretty", "shiny", "trinket", "comfort"],
      "type": "positive"
    },
    {
      "name": "Outdated Info",
      "weight": 8,
      "keywords": ["old", "outdated", "unreliable"],
      "type": "negative"
    }
  ],
  "defaultBasePriority": 50
}
```

### Example Output

```
--- Apocalyptic Priority Scramble Results ---

1. First Aid Kit (Score: 130)
   Rationale:
     - Base priority: 90
     - +40.00 from "Survival Essential" (keywords: medical, survival)

2. Canned Beans (Score: 110)
   Description: A staple, lasts forever.
   Rationale:
     - Base priority: 70
     - +40.00 from "Survival Essential" (keywords: food, survival)

3. Broken Radio (Score: 50)
   Description: Needs repair, might get news from the outside.
   Rationale:
     - Base priority: 30
     - +30.00 from "Communication Need" (keywords: radio, communication)
     - -10.00 from "Repair Required" (keywords: broken)

4. Shiny Rock (Score: 20)
   Description: Looks pretty, no practical use, but good for morale.
   Rationale:
     - Base priority: 10
     - +10.00 from "Morale Boost" (keywords: shiny, trinket)

-------------------------------------------
```

## Development

### Running Tests

```bash
npm test
# or yarn test
```

### Project Structure

```
.gitignore
package.json
tsconfig.json
src/
  index.ts    # Main application logic
  types.ts    # TypeScript interfaces
tests/
  index.test.ts # Jest tests
```
