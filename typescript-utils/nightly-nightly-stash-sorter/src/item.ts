export type ItemCategory = 'food' | 'water' | 'tool' | 'weapon' | 'medical' | 'misc';
export type ItemRarity = 'common' | 'uncommon' | 'rare' | 'legendary';
export type ItemCondition = 'pristine' | 'good' | 'worn' | 'damaged' | 'broken';

export interface ScavengedItem {
  id: string;
  name: string;
  category: ItemCategory;
  rarity: ItemRarity;
  condition: ItemCondition;
  weight_kg: number;
  value_units: number; // Abstract survival value
  perishable?: boolean;
}

export interface SurvivalPriority {
  sortBy?: keyof ScavengedItem;
  sortOrder?: 'asc' | 'desc';
  filterCategory?: ItemCategory[];
  filterRarity?: ItemRarity[];
  filterConditionMin?: ItemCondition;
  limit?: number;
}

const conditionOrder: Record<ItemCondition, number> = {
  'broken': 0,
  'damaged': 1,
  'worn': 2,
  'good': 3,
  'pristine': 4
};

export function sortAndFilterItems(items: ScavengedItem[], priority: SurvivalPriority): ScavengedItem[] {
  let filteredItems = [...items];

  // 1. Filter by category
  if (priority.filterCategory && priority.filterCategory.length > 0) {
    filteredItems = filteredItems.filter(item => priority.filterCategory!.includes(item.category));
  }

  // 2. Filter by rarity
  if (priority.filterRarity && priority.filterRarity.length > 0) {
    filteredItems = filteredItems.filter(item => priority.filterRarity!.includes(item.rarity));
  }

  // 3. Filter by minimum condition
  if (priority.filterConditionMin) {
    const minConditionRank = conditionOrder[priority.filterConditionMin];
    filteredItems = filteredItems.filter(item => conditionOrder[item.condition] >= minConditionRank);
  }

  // 4. Sort
  if (priority.sortBy) {
    const sortBy = priority.sortBy;
    const sortOrder = priority.sortOrder || 'asc';

    filteredItems.sort((a, b) => {
      let valA: any = a[sortBy];
      let valB: any = b[sortBy];

      // Handle specific sorting for condition
      if (sortBy === 'condition') {
        valA = conditionOrder[valA as ItemCondition];
        valB = conditionOrder[valB as ItemCondition];
      }

      if (valA < valB) return sortOrder === 'asc' ? -1 : 1;
      if (valA > valB) return sortOrder === 'asc' ? 1 : -1;
      return 0;
    });
  }

  // 5. Limit
  if (priority.limit !== undefined && priority.limit >= 0) {
    filteredItems = filteredItems.slice(0, priority.limit);
  }

  return filteredItems;
}
