const { reRollThought, keywordMap, voidWhispers } = require('../src/reRoller');

describe('reRollThought', () => {
  // Mock rationale: Math.random is non-deterministic. To ensure tests are repeatable
  // and predictable, we mock it to always return a specific index, allowing us to
  // test the exact output with a known void whisper.
  const mockMath = Object.create(global.Math);
  mockMath.random = () => 0.5; // Always pick the middle whisper for deterministic tests
  global.Math = mockMath;

  // Calculate the expected whisper based on the mocked Math.random
  const expectedWhisper = voidWhispers[Math.floor(0.5 * voidWhispers.length)];

  test('should replace keywords and append a void whisper', () => {
    const originalThought = "I'm worried about this difficult problem.";
    const expectedReRolled = `I'm considering about this intriguing puzzle. ${expectedWhisper}`;
    expect(reRollThought(originalThought)).toBe(expectedReRolled);
  });

  test('should handle multiple occurrences of the same keyword', () => {
    const originalThought = "I'm worried, very worried, about the problem.";
    const expectedReRolled = `I'm considering, very considering, about the puzzle. ${expectedWhisper}`;
    expect(reRollThought(originalThought)).toBe(expectedReRolled);
  });

  test('should be case-insensitive for keyword replacement', () => {
    const originalThought = "I feel ANXIOUS and stressed.";
    const expectedReRolled = `I feel anticipating and energized. ${expectedWhisper}`;
    expect(reRollThought(originalThought)).toBe(expectedReRolled);
  });

  test('should not alter words that are not keywords', () => {
    const originalThought = "The cat sat on the mat.";
    const expectedReRolled = `The cat sat on the mat. ${expectedWhisper}`;
    expect(reRollThought(originalThought)).toBe(expectedReRolled);
  });

  test('should capitalize the first letter of the re-rolled thought', () => {
    const originalThought = "i am feeling lonely.";
    const expectedReRolled = `I am feeling reflective. ${expectedWhisper}`;
    expect(reRollThought(originalThought)).toBe(expectedReRolled);
  });

  test('should handle thoughts with no keywords, only appending whisper', () => {
    const originalThought = "The sky is blue today.";
    const expectedReRolled = `The sky is blue today. ${expectedWhisper}`;
    expect(reRollThought(originalThought)).toBe(expectedReRolled);
  });

  test('should handle empty string input gracefully (after trimming and lowercasing)', () => {
    const originalThought = "";
    const expectedReRolled = `. ${expectedWhisper}`;
    expect(reRollThought(originalThought)).toBe(expectedReRolled);
  });

  test('should handle thought with only keywords', () => {
    const originalThought = "Worried problem.";
    const expectedReRolled = `Considering puzzle. ${expectedWhisper}`;
    expect(reRollThought(originalThought)).toBe(expectedReRolled);
  });
});
