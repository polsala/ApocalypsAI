export interface CosmicChoreConfig {
  tasks: string[];
  seed?: number; // Optional seed for deterministic "cosmic alignment"
}

export interface CosmicChoreSuggestion {
  chosenTask: string;
  rationale: string;
  cosmicAlignmentScore: number; // A number representing the "alignment"
}
