import { Item, SatchelConfig } from './types';

export function sortSatchel(items: Item[], config: SatchelConfig): Item[] {
  // Sort items by a combined score for a greedy approach.
  // Primary sort: survival_score (descending)
  // Secondary sort: density (survival_score / (weight + volume)) (descending)
  // Tertiary sort: total resource consumption (weight + volume) (ascending) to break ties for similar densities
  const sortedItems = [...items].sort((a, b) => {
    if (b.survival_score !== a.survival_score) {
      return b.survival_score - a.survival_score;
    }

    const densityA = a.survival_score / (a.weight + a.volume);
    const densityB = b.survival_score / (b.weight + b.volume);
    if (densityB !== densityA) {
      return densityB - densityA;
    }

    return (a.weight + a.volume) - (b.weight + b.volume);
  });

  let currentWeight = 0;
  let currentVolume = 0;
  const selectedItems: Item[] = [];

  for (const item of sortedItems) {
    if (
      currentWeight + item.weight <= config.maxWeight &&
      currentVolume + item.volume <= config.maxVolume
    ) {
      selectedItems.push(item);
      currentWeight += item.weight;
      currentVolume += item.volume;
    }
  }

  return selectedItems;
}
