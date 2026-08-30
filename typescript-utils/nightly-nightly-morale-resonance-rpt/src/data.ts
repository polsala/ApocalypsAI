import { MoodEntry } from './types';

// # Mock rationale: In a real scenario, this would persist to a file or database.
// For deterministic, offline tests, we use an in-memory array.
let moodEntries: MoodEntry[] = [];

export const addMoodEntry = (entry: MoodEntry): void => {
  moodEntries.push(entry);
};

export const getMoodEntries = (): MoodEntry[] => {
  return [...moodEntries]; // Return a copy to prevent external modification
};

export const clearMoodEntries = (): void => {
  moodEntries = []; // For testing purposes
};
