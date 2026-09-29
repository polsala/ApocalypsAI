# Nightly Scavenger's Stash Sorter

A type-safe utility to categorize and prioritize your post-apocalyptic inventory items based on their survival utility and scarcity. Never wonder what to grab first from your hoard again!

## Features

*   **Type-Safe Item Management**: Define your items with clear types for name, description, utility score, and scarcity.
*   **Configurable Categories**: Items are automatically assigned to predefined "apocalyptic utility" categories (e.g., Survival Essentials, Tactical Gear, Curiosities).
*   **Prioritized Sorting**: Your stash is sorted first by category priority, then by individual item utility score, giving you a clear hierarchy of importance.
*   **CLI Interface**: Quickly input items and get an organized output directly in your terminal.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/typescript-utils/nightly-scavenger-stash-sorter
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    ```
3.  **Build the TypeScript project:**
    ```bash
    npm run build
    ```

## Usage

The utility can be run directly from the command line, providing item details as arguments.

**Format:** `"Name|Description|UtilityScore(0-100)|Scarcity"`

**Scarcity options:** `Abundant`, `Common`, `Scarce`, `Rare`, `Legendary`

```bash
npm start "Water Purifier|Filters contaminated water|95|Scarce" "Rusty Spoon|Good for digging|10|Abundant" "Medkit|Heals wounds|88|Rare" "Old Map|Shows pre-apocalypse roads|45|Common" "Can of Beans|Edible food|65|Common"
```

### Example Output

```
--- Your Sorted Scavenger's Stash ---
[Survival Essentials (Prio: 1)] Water Purifier (Score: 95, Scarcity: Scarce) - Filters contaminated water
[Survival Essentials (Prio: 1)] Medkit (Score: 88, Scarcity: Rare) - Heals wounds
[Resource & Crafting (Prio: 3)] Can of Beans (Score: 65, Scarcity: Common) - Edible food
[Resource & Crafting (Prio: 3)] Old Map (Score: 45, Scarcity: Common) - Shows pre-apocalypse roads
[Curiosities & Morale (Prio: 5)] Rusty Spoon (Score: 10, Scarcity: Abundant) - Good for digging
-------------------------------------
```

## Development & Testing

To run the tests:

```bash
npm test
```

To rebuild after changes:

```bash
npm run build
```

## Customization

You can modify the `DEFAULT_CATEGORIES` array in `src/index.ts` to define your own apocalyptic utility categories, their score ranges, and priorities.

```typescript
// src/index.ts
export const CUSTOM_CATEGORIES: ApocalypticCategory[] = [
  { name: 'Ultra-Rare Artifacts', minScore: 90, maxScore: 100, priority: 1, description: 'Items of immense value or power.' },
  // ... more categories
];
```
You would then need to pass `CUSTOM_CATEGORIES` to `sortStash` if you're using it programmatically. The CLI currently uses `DEFAULT_CATEGORIES`.

## License

This project is licensed under the MIT License.
