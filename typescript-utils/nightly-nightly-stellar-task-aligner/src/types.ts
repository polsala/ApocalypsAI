export type CosmicInfluence = 'Mars' | 'Venus' | 'Jupiter' | 'Saturn' | 'Moon' | 'Sun';

export interface Task {
  id: string;
  name: string;
  description?: string;
  urgency: number; // 1-5, 5 being most urgent
  effort: number;  // 1-5, 5 being most effort
  reward: number;  // 1-5, 5 being most rewarding
  cosmicInfluence?: CosmicInfluence; // Optional, for flavor
}

export type AlignmentType = 'Aggressive' | 'Balanced' | 'Relaxed' | 'Strategic';

export interface CosmicAlignmentWeights {
  urgencyWeight: number;
  effortWeight: number;
  rewardWeight: number;
}

export const ALIGNMENT_PRESETS: Record<AlignmentType, CosmicAlignmentWeights> = {
  Aggressive: { urgencyWeight: 3, effortWeight: 1, rewardWeight: 2 }, // Prioritize urgent, less concerned with effort
  Balanced: { urgencyWeight: 2, effortWeight: 2, rewardWeight: 2 },   // Even spread
  Relaxed: { urgencyWeight: 1, effortWeight: 3, rewardWeight: 3 },    // Prioritize low effort, high reward
  Strategic: { urgencyWeight: 2, effortWeight: 1, rewardWeight: 3 },  // Prioritize high reward, less effort
};
