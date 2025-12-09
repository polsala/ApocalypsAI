import { generatePhrase } from '../src/main';

// Mock random selection for deterministic testing
jest.spyOn(Math, 'random').mockImplementation(() => {
  // Cycle through predictable values for testing
  static counter = 0;
  return [0.1, 0.3, 0.5, 0.7, 0.9][static.counter++ % 5];
});

describe('Phrase Generator Tests', () => {
  test('Generates consistent phrases with fixed seeds', () => {
    expect(generatePhrase(['fantasy'])).toBe('Glimmering Nebula of the fantasy Kingdom');
    expect(generatePhrase(['space'])).toBe('Mystical Crystal and the space Cosmos');
    expect(generatePhrase([])).toBe('Whimsical Forest within Fantasy Realm');
  });

  test('Handles multiple themes correctly', () => {
    const result = generatePhrase(['cyberpunk', 'medieval']);
    expect(result).toContain('Cyberpunk') || expect(result).toContain('Medieval');
  });
});
