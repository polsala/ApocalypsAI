export type Mood = "Radiant as a Supernova" | "Hopeful as a Seedling" | "Neutral as a Deactivated Sentry" | "Anxious as a Scavenger" | "Gloomy as a Nuclear Winter";

export interface MoraleEntry {
  date: string; // YYYY-MM-DD
  mood: Mood;
  notes?: string;
}

export interface MoraleData {
  entries: MoraleEntry[];
}
