import { generateQuest, getAllMoods } from '../src/questGenerator';
import { Mood, Quest } from '../src/types';

// Mock rationale: Math.random is used internally by generateQuest to pick a random quest.
// To make tests deterministic, we mock Math.random to always return a predictable value (e.g., 0).
// This ensures that generateQuest always picks the first item from the filtered list for a given mood.
const mockMathRandom = (returnValue: number) => {
  const originalMathRandom = Math.random;
  Math.random = () => returnValue;
  return () => { Math.random = originalMathRandom; }; // Restore original
};

describe('questGenerator', () => {
  let restoreMathRandom: () => void;

  beforeEach(() => {
    restoreMathRandom = mockMathRandom(0); // Always pick the first quest for deterministic tests
  });

  afterEach(() => {
    restoreMathRandom(); // Restore Math.random after each test
  });

  it('should return a quest for a valid mood', () => {
    const mood: Mood = 'energetic';
    const quest = generateQuest(mood);
    expect(quest).toBeDefined();
    expect(quest?.mood).toBe(mood);
    expect(typeof quest?.title).toBe('string');
    expect(typeof quest?.description).toBe('string');
  });

  it('should return a specific quest when Math.random is mocked to 0', () => {
    const mood: Mood = 'energetic';
    const quest = generateQuest(mood);
    // Based on the current quest list, the first energetic quest is 'The Sparkle & Conquer Protocol'
    expect(quest?.title).toBe('The Sparkle & Conquer Protocol');
  });

  it('should return a different specific quest for another mood when Math.random is mocked to 0', () => {
    const mood: Mood = 'tired';
    const quest = generateQuest(mood);
    // Based on the current quest list, the first tired quest is 'The Great Pillow Expedition'
    expect(quest?.title).toBe('The Great Pillow Expedition');
  });

  it('should return a neutral quest if an unknown mood is requested (fallback behavior)', () => {
    const unknownMood = 'unknown' as Mood; // Cast to Mood for type compatibility, though it's invalid
    const quest = generateQuest(unknownMood);
    expect(quest).toBeDefined();
    expect(quest?.mood).toBe('neutral'); // Expect fallback to neutral
    // Based on the current quest list, the first neutral quest is 'The Path of the Curious Explorer'
    expect(quest?.title).toBe('The Path of the Curious Explorer');
  });

  it('should return a quest with actionable steps if available', () => {
    const mood: Mood = 'energetic';
    const quest = generateQuest(mood);
    expect(quest?.actionableSteps).toBeDefined();
    expect(Array.isArray(quest?.actionableSteps)).toBe(true);
    expect(quest?.actionableSteps?.length).toBeGreaterThan(0);
  });

  it('getAllMoods should return an array of unique moods', () => {
    const moods = getAllMoods();
    expect(Array.isArray(moods)).toBe(true);
    expect(moods.length).toBeGreaterThan(0);
    // Check for expected moods
    expect(moods).toContain('energetic');
    expect(moods).toContain('tired');
    expect(moods).toContain('creative');
    expect(moods).toContain('procrastinating');
    expect(moods).toContain('neutral');
    expect(moods).toContain('anxious');
    expect(moods).toContain('playful');
    // Ensure no duplicates
    expect(new Set(moods).size).toBe(moods.length);
  });
});
