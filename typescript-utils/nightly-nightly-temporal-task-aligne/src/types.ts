export interface Task {
  id: string;
  name: string;
  urgency: number; // 1 (low) to 5 (high)
  energyCost: number; // 1 (low) to 5 (high)
  temporalAlignment?: number; // Calculated score
}
