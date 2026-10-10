import { getQuest, getDetox, displayQuest, displayDetox, parseArgs, getRandomElement } from '../src/index';
import { microQuests, distractionDetoxes, Mood, MicroQuest, DistractionDetox } from '../src/quests';

// Mock rationale: Math.random is non-deterministic. Mocking it ensures tests always pick the same element,
// making tests reliable and repeatable without external factors.
const mockMathRandom = (returnValue: number) => {
  const originalMathRandom = Math.random;
  Math.random = () => returnValue;
  return () => { Math.random = originalMathRandom; }; // Restore original
};

describe('nightly-focus-flicker-fixer', () => {

  let consoleSpy: jest.SpyInstance;

  beforeEach(() => {
    consoleSpy = jest.spyOn(console, 'log').mockImplementation(() => {});
    jest.spyOn(console, 'warn').mockImplementation(() => {}); // Mock warn too
  });

  afterEach(() => {
    consoleSpy.mockRestore();
    jest.restoreAllMocks();
  });

  describe('getRandomElement', () => {
    it('should return the first element when Math.random is 0', () => {
      const restore = mockMathRandom(0);
      const arr = [1, 2, 3];
      expect(getRandomElement(arr)).toBe(1);
      restore();
    });

    it('should return the last element when Math.random is just under 1', () => {
      const restore = mockMathRandom(0.999999999);
      const arr = [1, 2, 3];
      expect(getRandomElement(arr)).toBe(3);
      restore();
    });

    it('should return a valid element from the array', () => {
      const restore = mockMathRandom(0.5); // Should pick the middle element if odd length
      const arr = ['a', 'b', 'c', 'd', 'e'];
      expect(getRandomElement(arr)).toBe('c');
      restore();
    });
  });

  describe('getQuest', () => {
    it('should return a quest', () => {
      const quest = getQuest();
      expect(microQuests).toContain(quest);
    });

    it('should return a quest filtered by mood "low"', () => {
      const restore = mockMathRandom(0); // Ensure consistent selection
      const quest = getQuest('low');
      expect(quest.moods).toContain('low');
      restore();
    });

    it('should return a quest filtered by mood "high"', () => {
      const restore = mockMathRandom(0); // Ensure consistent selection
      const quest = getQuest('high');
      expect(quest.moods).toContain('high');
      restore();
    });

    it('should return a quest even if no specific mood quests match (fallback)', () => {
      // Temporarily filter out all quests that match 'high' to test fallback
      const originalQuests = [...microQuests];
      (microQuests as MicroQuest[]) = microQuests.filter(q => !q.moods.includes('high'));
      const restore = mockMathRandom(0); // Mock rationale: Ensures deterministic selection for fallback test.
      const quest = getQuest('high'); // Should still return a quest from the filtered list
      expect(quest).toBeDefined();
      restore();
      (microQuests as MicroQuest[]) = originalQuests; // Restore original quests
    });
  });

  describe('getDetox', () => {
    it('should return a distraction detox', () => {
      const detox = getDetox();
      expect(distractionDetoxes).toContain(detox);
    });
  });

  describe('displayQuest', () => {
    it('should log the quest details to console', () => {
      const quest: MicroQuest = {
        id: 'test-quest',
        title: 'Test Quest',
        description: 'This is a test description.',
        moods: ['any'],
        durationMinutes: 1,
      };
      displayQuest(quest);
      expect(consoleSpy).toHaveBeenCalledTimes(5);
      expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('✨ Micro-Quest Initiated: Test Quest ✨'));
      expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('Objective: This is a test description.'));
      expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('Estimated Duration: 1 minutes'));
    });
  });

  describe('displayDetox', () => {
    it('should log the detox details to console', () => {
      const detox: DistractionDetox = {
        id: 'test-detox',
        title: 'Test Detox',
        description: 'This is a test detox description.',
        durationMinutes: 5,
      };
      displayDetox(detox);
      expect(consoleSpy).toHaveBeenCalledTimes(5);
      expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('🚫 Distraction-Detox Protocol: Test Detox 🚫'));
      expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('Action: This is a test detox description.'));
      expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('Recommended Duration: 5 minutes'));
    });
  });

  describe('parseArgs', () => {
    it('should default to quest with mood "any" if no args', () => {
      const args = [];
      const result = parseArgs(args);
      expect(result).toEqual({ type: 'quest', mood: 'any' });
    });

    it('should parse --detox correctly', () => {
      const args = ['--detox'];
      const result = parseArgs(args);
      expect(result).toEqual({ type: 'detox' });
    });

    it('should parse --quest with mood correctly', () => {
      const args = ['--quest', '--mood', 'low'];
      const result = parseArgs(args);
      expect(result).toEqual({ type: 'quest', mood: 'low' });
    });

    it('should parse --mood without --quest explicitly', () => {
      const args = ['--mood', 'high'];
      const result = parseArgs(args);
      expect(result).toEqual({ type: 'quest', mood: 'high' });
    });

    it('should handle invalid mood gracefully', () => {
      const args = ['--mood', 'invalid'];
      const result = parseArgs(args);
      expect(result).toEqual({ type: 'quest', mood: 'any' });
      expect(console.warn).toHaveBeenCalledWith(expect.stringContaining('Invalid mood: "invalid". Using \'any\'.'));
    });

    it('should prioritize --detox over --quest and --mood', () => {
      const args = ['--detox', '--quest', '--mood', 'high'];
      const result = parseArgs(args);
      expect(result).toEqual({ type: 'detox' });
    });
  });
});
