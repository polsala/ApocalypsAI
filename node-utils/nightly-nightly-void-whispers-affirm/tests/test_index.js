const { getRandomAffirmation } = require('../src/index');

// Mock rationale: We mock Math.random to return a fixed value to ensure deterministic test outcomes.
jest.spyOn(global.Math, 'random').mockReturnValue(0.1);

describe('Void Whispers Affirmations', () => {
  test('should return a fixed affirmation when Math.random is mocked', () => {
    const result = getRandomAffirmation();
    expect(result).toBe("Amidst the ruins, your resilience echoes louder than the silence.");
  });
});
