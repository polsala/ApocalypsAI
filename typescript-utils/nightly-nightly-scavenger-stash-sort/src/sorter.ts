import { Item, StashCategory, SortedStash } from './types';

export function sortItemsIntoStashes(items: Item[], categories: StashCategory[]): SortedStash {
  const sortedStash: SortedStash = {};

  // Initialize categories in the result, sorted by priority (highest first)
  const sortedCategories = [...categories].sort((a, b) => b.priority - a.priority);
  sortedCategories.forEach(cat => {
    sortedStash[cat.name] = [];
  });

  items.forEach(item => {
    let assigned = false;
    for (const category of sortedCategories) {
      const matchesAllRules = category.rules.every(rule => rule(item));
      if (matchesAllRules) {
        sortedStash[category.name].push(item);
        assigned = true;
        break; // Item assigned, move to next item
      }
    }
    // If an item doesn't match any category, it's not added to any stash.
    // For this utility, we assume all items should eventually fit *somewhere*
    // or the rules need to be adjusted. Could add an "Unsorted" category if needed.
  });

  return sortedStash;
}
