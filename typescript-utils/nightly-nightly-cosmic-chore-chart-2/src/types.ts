export interface Chore {
  id: string;
  name: string;
  baseDifficulty: number; // 1-5
  tags: string[];
}

export interface CosmicInfluence {
  name: string;
  modifier: number; // Multiplier for difficulty (e.g., 0.8 for easier, 1.2 for harder)
  favoredTags: string[];
  hinderedTags: string[];
  message: string;
}

export interface AssignedChore extends Chore {
  effectiveDifficulty: number;
  cosmicBoost: boolean;
  cosmicHindrance: boolean;
}
