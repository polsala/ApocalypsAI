export interface CosmicFactor {
  name: string;
  value: number; // e.g., 0.5 for half intensity, 2.0 for double
  impactMultiplier: number; // How much this factor influences priority
}

export interface Task {
  id: string;
  name: string;
  basePriority: number; // A baseline priority, higher is more urgent
  cosmicModifiers?: {
    [factorName: string]: number; // How much this specific task is affected by a cosmic factor
  };
  description?: string;
}

export interface PrioritizedTask extends Task {
  cosmicPriorityScore: number;
}
