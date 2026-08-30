export type MoodFactor = 'food' | 'shelter' | 'social' | 'weather' | 'safety' | 'anomaly' | 'resource_gain' | 'resource_loss';

export interface MoodEntry {
  timestamp: number; // Unix timestamp
  moodScore: 1 | 2 | 3 | 4 | 5; // 1: Dire, 5: Radiant
  factors: MoodFactor[];
  notes?: string;
}

export interface EmotionalReport {
  date: string; // YYYY-MM-DD
  averageMood: number; // Calculated average
  moodTrend: 'rising' | 'falling' | 'stable';
  dominantPositiveFactors: MoodFactor[];
  dominantNegativeFactors: MoodFactor[];
  recommendation: string;
}
