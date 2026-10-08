import { Item, ApocalypticCategory, CategorizedItem, Scarcity } from './types';

export const DEFAULT_CATEGORIES: ApocalypticCategory[] = [
  { name: 'Survival Essentials', minScore: 80, maxScore: 100, priority: 1, description: 'Critical for immediate survival and well-being.' },
  { name: 'Tactical Gear', minScore: 60, maxScore: 79, priority: 2, description: 'Useful for defense, offense, or strategic movement.' },
  { name: 'Resource & Crafting', minScore: 40, maxScore: 59, priority: 3, description: 'Materials for building, repairing, or creating new items.' },
  { name: 'Barter & Trade', minScore: 20, maxScore: 39, priority: 4, description: 'Items with value for exchange, but not direct survival.' },
  { name: 'Curiosities & Morale', minScore: 0, maxScore: 19, priority: 5, description: 'Provides comfort, entertainment, or historical insight, but low practical utility.' },
];

/**
 * Categorizes a single item based on its raw utility score.
 * @param item The item to categorize.
 * @param categories The list of available categories.
 * @returns The item paired with its assigned category.
 * @throws Error if no suitable category is found for the item's score.
 */
export function categorizeItem(item: Item, categories: ApocalypticCategory[] = DEFAULT_CATEGORIES): CategorizedItem {
  const category = categories.find(cat =>
    item.rawUtilityScore >= cat.minScore && item.rawUtilityScore <= cat.maxScore
  );

  if (!category) {
    throw new Error(`Item "${item.name}" with score ${item.rawUtilityScore} could not be assigned to a category.`);
  }

  return { item, category };
}

/**
 * Sorts a list of items into categories and then by priority and utility.
 * @param items The list of items to sort.
 * @param categories The list of available categories.
 * @returns A sorted list of categorized items.
 */
export function sortStash(items: Item[], categories: ApocalypticCategory[] = DEFAULT_CATEGORIES): CategorizedItem[] {
  const categorized = items.map(item => categorizeItem(item, categories));

  // Sort by category priority (lower number = higher priority), then by item utility score (higher = better)
  return categorized.sort((a, b) => {
    if (a.category.priority !== b.category.priority) {
      return a.category.priority - b.category.priority;
    }
    return b.item.rawUtilityScore - a.item.rawUtilityScore;
  });
}

/**
 * Formats a categorized item for display.
 * @param categorizedItem The item to format.
 * @returns A formatted string.
 */
export function formatCategorizedItem(categorizedItem: CategorizedItem): string {
  const { item, category } = categorizedItem;
  return `[${category.name} (Prio: ${category.priority})] ${item.name} (Score: ${item.rawUtilityScore}, Scarcity: ${item.scarcity}) - ${item.description}`;
}

/**
 * Runs the CLI application.
 * Expects arguments in the format: <name>|<description>|<utility_score>|<scarcity>
 * Example: node dist/index.js "Water Purifier|Filters contaminated water|95|Scarce" "Rusty Spoon|Good for digging|10|Abundant"
 */
export function runCli(args: string[]): void {
  if (args.length === 0) {
    console.log("Usage: npm start \"<name>|<description>|<utility_score>|<scarcity>\" [\"<name>|...\"]");
    console.log("\nExample: npm start \"Water Purifier|Filters contaminated water|95|Scarce\" \"Rusty Spoon|Good for digging|10|Abundant\"");
    return;
  }

  const items: Item[] = [];
  for (const arg of args) {
    const parts = arg.split('|');
    if (parts.length !== 4) {
      console.error(`Error: Invalid item format for "${arg}". Expected "name|description|utility_score|scarcity".`);
      return;
    }
    const [name, description, scoreStr, scarcityStr] = parts;
    const rawUtilityScore = parseInt(scoreStr, 10);
    if (isNaN(rawUtilityScore) || rawUtilityScore < 0 || rawUtilityScore > 100) {
      console.error(`Error: Invalid utility score for "${name}". Must be a number between 0 and 100.`);
      return;
    }
    const scarcity: Scarcity = scarcityStr as Scarcity;
    if (!['Abundant', 'Common', 'Scarce', 'Rare', 'Legendary'].includes(scarcity)) {
        console.error(`Error: Invalid scarcity for "${name}". Must be one of: Abundant, Common, Scarce, Rare, Legendary.`);
        return;
    }

    items.push({ name, description, rawUtilityScore, scarcity });
  }

  try {
    const sortedStash = sortStash(items);
    console.log("\n--- Your Sorted Scavenger's Stash ---");
    sortedStash.forEach(item => console.log(formatCategorizedItem(item)));
    console.log("-------------------------------------\n");
  } catch (error: any) {
    console.error(`An error occurred: ${error.message}`);
  }
}

// This block ensures runCli is called when the script is executed directly
if (require.main === module) {
  // process.argv[0] is 'node', process.argv[1] is 'dist/index.js'
  runCli(process.argv.slice(2));
}
