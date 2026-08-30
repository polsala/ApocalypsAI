export type Mood = 'energetic' | 'tired' | 'creative' | 'procrastinating' | 'neutral' | 'anxious' | 'playful';

export interface Quest {
  mood: Mood;
  title: string;
  description: string;
  actionableSteps?: string[];
}
