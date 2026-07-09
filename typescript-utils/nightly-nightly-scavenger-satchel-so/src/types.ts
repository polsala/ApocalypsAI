export interface Item {
  name: string;
  weight: number; // e.g., in kilograms
  volume: number; // e.g., in liters
  survival_score: number; // arbitrary points, higher is better
}

export interface SatchelConfig {
  maxWeight: number;
  maxVolume: number;
}
