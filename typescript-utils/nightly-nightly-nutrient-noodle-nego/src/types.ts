export interface NutrientPaste {
  id: string;
  name: string;
  tags: string[];
}

export interface ConsumptionRecord {
  lastConsumedId: string | null;
  history: string[]; // To track recent consumption for mood-based avoidance
}
