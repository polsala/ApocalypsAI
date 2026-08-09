import * as fs from 'fs';
import * as path from 'path';
import { generateCosmicInfluence, assignChores } from '../src/index';
import { Chore, CosmicInfluence, AssignedChore } from '../src/types';

// Mock rationale: We need to control the random selection of cosmic influences
// and chore sorting for deterministic tests. Math.random is mocked to return
// a predictable sequence or a fixed value.
const mockMathRandom = (values: number[]) => {
  let i = 0;
  const mock = jest.spyOn(Math, 'random').mockImplementation(() => {
    if (i >= values.length) {
      i = 0; // Loop if more random numbers are needed than provided
    }
    return values[i++];
  });
  return mock;
};

// Mock rationale: We need to provide a consistent set of chores without relying
// on actual file system operations, making tests fast and isolated.
const mockChores: Chore[] = [
  { id: 'c1', name: 'Scavenge for Water', baseDifficulty: 4, tags: ['survival', 'physical', 'outdoor'] },
  { id: 'c2', name: 'Repair Shelter Wall', baseDifficulty: 3, tags: ['maintenance', 'physical'] },
  { id: 'c3', name: 'Inventory Supplies', baseDifficulty: 2, tags: ['logistics', 'mental'] },
  { id: 'c4', name: 'Clean Contamination Zone', baseDifficulty: 5, tags: ['danger', 'physical', 'hygiene'] },
  { id: 'c5', name: 'Tend to Hydroponics', baseDifficulty: 3, tags: ['farming', 'maintenance'] },
  { id: 'c6', name: 'Sharpen Tools', baseDifficulty: 1, tags: ['maintenance', 'crafting'] },
  { id: 'c7', name: 'Monitor Perimeter Sensors', baseDifficulty: 2, tags: ['security', 'mental'] }
];

describe('Nightly Cosmic Chore Chart', () => {
  let randomMock: jest.SpyInstance;

  beforeEach(() => {
    // Reset mocks before each test
    jest.clearAllMocks();
  });

  afterEach(() => {
    if (randomMock) {
      randomMock.mockRestore();
    }
  });

  describe('generateCosmicInfluence', () => {
    test('should return a cosmic influence deterministically based on mock random', () => {
      randomMock = mockMathRandom([0.01]); // Should pick the first influence
      const influence = generateCosmicInfluence();
      expect(influence.name).toBe('Solar Flare Surge');

      randomMock = mockMathRandom([0.99]); // Should pick the last influence (assuming 5 influences)
      const influence2 = generateCosmicInfluence();
      expect(influence2.name).toBe('Temporal Ripple');
    });
  });

  describe('assignChores', () => {
    const mockCosmicInfluence: CosmicInfluence = {
      name: "Void Whisper",
      modifier: 0.8,
      favoredTags: ["mental", "logistics"],
      hinderedTags: ["physical", "danger"],
      message: "The void whispers secrets of efficiency. Focus your mind, not your muscle."
    };

    test('should return an empty array if no chores are provided', () => {
      const assigned = assignChores([], mockCosmicInfluence, 3);
      expect(assigned).toEqual([]);
    });

    test('should assign the correct number of chores', () => {
      randomMock = mockMathRandom([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]); // For sorting ties
      const assigned = assignChores(mockChores, mockCosmicInfluence, 3);
      expect(assigned.length).toBe(3);
    });

    test('should assign fewer chores if numChoresToAssign is greater than available chores', () => {
      randomMock = mockMathRandom([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]); // For sorting ties
      const assigned = assignChores(mockChores.slice(0, 2), mockCosmicInfluence, 5);
      expect(assigned.length).toBe(2);
    });

    test('should correctly calculate effective difficulty and apply boosts/hindrances', () => {
      randomMock = mockMathRandom([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]); // For sorting ties
      const assigned = assignChores(mockChores, mockCosmicInfluence, mockChores.length);

      // Chore c3: Inventory Supplies (baseDifficulty: 2, tags: ['logistics', 'mental'])
      // Favored tags: ['mental', 'logistics'] -> 2 * 0.8 (modifier) * 0.8 (favored) = 1.28
      const c3 = assigned.find(c => c.id === 'c3');
      expect(c3?.effectiveDifficulty).toBe(1.28);
      expect(c3?.cosmicBoost).toBe(true);
      expect(c3?.cosmicHindrance).toBe(false);

      // Chore c7: Monitor Perimeter Sensors (baseDifficulty: 2, tags: ['security', 'mental'])
      // Favored tags: ['mental'] -> 2 * 0.8 (modifier) * 0.8 (favored) = 1.28
      const c7 = assigned.find(c => c.id === 'c7');
      expect(c7?.effectiveDifficulty).toBe(1.28);
      expect(c7?.cosmicBoost).toBe(true);
      expect(c7?.cosmicHindrance).toBe(false);

      // Chore c1: Scavenge for Water (baseDifficulty: 4, tags: ['survival', 'physical', 'outdoor'])
      // Hindered tags: ['physical'] -> 4 * 0.8 (modifier) * 1.2 (hindered) = 3.84
      const c1 = assigned.find(c => c.id === 'c1');
      expect(c1?.effectiveDifficulty).toBe(3.84);
      expect(c1?.cosmicBoost).toBe(false);
      expect(c1?.cosmicHindrance).toBe(true);

      // Chore c5: Tend to Hydroponics (baseDifficulty: 3, tags: ['farming', 'maintenance'])
      // No favored/hindered tags -> 3 * 0.8 (modifier) = 2.4
      const c5 = assigned.find(c => c.id === 'c5');
      expect(c5?.effectiveDifficulty).toBe(2.4);
      expect(c5?.cosmicBoost).toBe(false);
      expect(c5?.cosmicHindrance).toBe(false);
    });

    test('should sort chores by effective difficulty (easiest first)', () => {
      randomMock = mockMathRandom([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]); // For sorting ties
      const assigned = assignChores(mockChores, mockCosmicInfluence, mockChores.length);

      // Expected order based on calculations above and tie-breaking
      // c3 (1.28), c7 (1.28), c6 (1.6), c5 (2.4), c2 (2.88), c1 (3.84), c4 (4.8)
      expect(assigned[0].id).toBe('c3'); // Inventory Supplies (1.28)
      expect(assigned[1].id).toBe('c7'); // Monitor Perimeter Sensors (1.28)
      expect(assigned[2].id).toBe('c6'); // Sharpen Tools (1.6)
      expect(assigned[3].id).toBe('c5'); // Tend to Hydroponics (2.4)
      expect(assigned[4].id).toBe('c2'); // Repair Shelter Wall (2.88)
      expect(assigned[5].id).toBe('c1'); // Scavenge for Water (3.84)
      expect(assigned[6].id).toBe('c4'); // Clean Contamination Zone (4.8)
    });
  });
});
