export interface Item {
  id: string;
  name: string;
  description?: string;
  tags?: string[];
  basePriority?: number; // 0-100, default 50
}

export interface Factor {
  name: string;
  weight: number; // Multiplier, e.g., 1.5 for high importance, 0.5 for low
  keywords: string[]; // Keywords that trigger this factor
  type: 'positive' | 'negative'; // Does this factor increase or decrease priority?
}

export interface Config {
  factors: Factor[];
  defaultBasePriority: number; // Default base priority if not specified in item
}

export interface PrioritizedItem {
  item: Item;
  score: number;
  rationale: string[];
}
