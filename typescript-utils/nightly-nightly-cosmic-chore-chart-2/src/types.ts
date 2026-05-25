export type ChoreCategory = 'Daily' | 'Weekly' | 'Errand' | 'Self-Care';

export interface Chore {
  id: string;
  description: string;
  category: ChoreCategory;
  effort: 'low' | 'medium' | 'high';
}

export type CosmicInfluence = 'LunarLull' | 'MartianMomentum' | 'VenusianVibe' | 'JovianJolt' | 'SolarSurge';

export interface CosmicGuidance {
  influence: CosmicInfluence;
  message: string;
  suggestedChores: Chore[];
}
