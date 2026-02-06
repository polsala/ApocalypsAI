export type Rarity = 'Common' | 'Uncommon' | 'Rare' | 'Legendary' | 'Mythic';

export interface Relic {
  name: string;
  description?: string;
}

export interface ClassificationResult {
  relic: Relic;
  rarity: Rarity;
  utilityScore: number;
  reason: string[];
}

export interface KeywordRule {
  keywords: string[];
  rarityBoost?: Rarity; // e.g., 'Rare'
  utilityBoost?: number; // e.g., 3
  description?: string; // for explanation
}
