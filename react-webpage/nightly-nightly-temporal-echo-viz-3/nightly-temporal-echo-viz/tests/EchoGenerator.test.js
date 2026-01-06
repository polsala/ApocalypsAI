import { generateEcho } from '../src/EchoGenerator';

describe('EchoGenerator', () => {
  const originalMathRandom = Math.random;

  beforeEach(() => {
    // Mock rationale: Math.random is used for probabilistic transformations in generateEcho.
    // To ensure deterministic test results, Math.random is mocked to return a fixed sequence or value.
    // This allows us to predict the output of the echo generation functions.
    let mockRandomCalls = 0;
    Math.random = jest.fn(() => {
      mockRandomCalls++;
      // Provide a sequence of predictable random numbers for different scenarios
      if (mockRandomCalls === 1) return 0.1; // For whisper (remove/replace)
      if (mockRandomCalls === 2) return 0.7; // For whisper (keep)
      if (mockRandomCalls === 3) return 0.2; // For whisper (remove/replace)
      if (mockRandomCalls === 4) return 0.9; // For whisper (keep)
      if (mockRandomCalls === 5) return 0.5; // For shift (replace)
      if (mockRandomCalls === 6) return 0.8; // For shift (keep)
      if (mockRandomCalls === 7) return 0.1; // For void (add phrase)
      if (mockRandomCalls === 8) return 0.5; // For void (keep)
      if (mockRandomCalls === 9) return 0.1; // For reverb (add echo)
      if (mockRandomCalls === 10) return 0.9; // For reverb (keep)
      return 0.5; // Default for subsequent calls if needed
    });
  });

  afterEach(() => {
    Math.random = originalMathRandom; // Restore original Math.random
  });

  test('should generate a whisper echo correctly', () => {
    const text = 'The quick brown fox jumps over the lazy dog.';
    const expected = '... quick brown ... jumps over the lazy dog.'; // Based on mock random values
    expect(generateEcho(text, 'whisper')).toBe(expected);
  });

  test('should generate a temporal shift echo correctly', () => {
    const text = 'The message of time will echo in the void.';
    const expected = 'The signal of era will echo in the abyss.'; // Based on mock random values
    expect(generateEcho(text, 'shift')).toBe(expected);
  });

  test('should generate a void distortion echo correctly', () => {
    const text = 'A faint light in the darkness.';
    const expected = '[STATIC] A faint light in the darkness.'; // Based on mock random values
    expect(generateEcho(text, 'void')).toBe(expected);
  });

  test('should generate a reverb echo correctly', () => {
    const text = 'Hello world, this is a test.';
    const expected = 'Hello...hello... world, this is a test.'; // Based on mock random values
    expect(generateEcho(text, 'reverb')).toBe(expected);
  });

  test('should return original text for unknown type', () => {
    const text = 'This is original.';
    expect(generateEcho(text, 'unknown')).toBe(text);
  });

  test('should handle empty string input gracefully', () => {
    expect(generateEcho('', 'whisper')).toBe('');
    expect(generateEcho('   ', 'shift')).toBe('   ');
  });

  test('should handle text with only spaces', () => {
    expect(generateEcho('   ', 'whisper')).toBe('   ');
  });
});
