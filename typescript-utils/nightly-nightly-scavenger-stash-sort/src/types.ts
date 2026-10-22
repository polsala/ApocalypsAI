export type Scarcity = 'Abundant' | 'Common' | 'Scarce' | 'Rare' | 'Legendary';

export interface Item {
  name: string;
  description: string;
  rawUtilityScore: number; // 0-100, higher is more useful
  scarcity: Scarcity;
}

export interface ApocalypticCategory {
  name: string;
  minScore: number;
  maxScore: number;
  priority: number; // Lower number means higher priority (e.g., 1 for Essentials, 5 for Curiosities)
  description: string;
}

export interface CategorizedItem {
  item: Item;
  category: ApocalypticCategory;
}
