import { generateEchoes } from '../src/EchoGenerator';

describe('generateEchoes', () => {
  // Mock rationale: The `generateEchoes` function uses `Math.random()` internally,
  // which makes its output non-deterministic. To ensure tests are deterministic
  // and reliable, we mock `Math.random()` to return a predictable sequence of values.
  // This allows us to test the different branches of the echo generation logic.
  const mockMath = Object.create(global.Math);
  mockMath.random = jest.fn();
  global.Math = mockMath;

  beforeEach(() => {
    // Reset mock before each test
    mockMath.random.mockClear();
  });

  test('returns an empty array for empty or whitespace phrase', () => {
    expect(generateEchoes('', 5)).toEqual([]);
    expect(generateEchoes('   ', 5)).toEqual([]);
  });

  test('always includes the original phrase (or a variant) as one of the echoes', () => {
    mockMath.random.mockReturnValue(0.9); // Ensure a non-prefix/suffix path
    const echoes = generateEchoes('hello', 1);
    expect(echoes[0]).toMatch(/The Original: "hello"|Whisper: "hello"/); // Depending on random path
  });

  test('generates the specified number of echoes', () => {
    mockMath.random.mockReturnValue(0.1); // Always trigger prefix for simplicity
    const echoes = generateEchoes('test', 3);
    expect(echoes).toHaveLength(3);
  });

  test('generates echoes with whimsical prefixes', () => {
    mockMath.random
      .mockReturnValueOnce(0.1) // Trigger prefix
      .mockReturnValueOnce(0)   // Select first prefix "Whisper of"
      .mockReturnValueOnce(0.1) // Trigger prefix
      .mockReturnValueOnce(0.5) // Select a different prefix
      .mockReturnValueOnce(0.9); // Fallback to original
    const echoes = generateEchoes('dream', 3);
    expect(echoes).toContain('The Original: "dream"');
    expect(echoes).toContain(expect.stringMatching(/Whisper of the "dream"/));
    expect(echoes).toContain(expect.stringMatching(/Temporal Ripple of the "dream"/));
  });

  test('generates echoes with whimsical suffixes', () => {
    mockMath.random
      .mockReturnValueOnce(0.4) // Trigger suffix
      .mockReturnValueOnce(0)   // Select first suffix "past"
      .mockReturnValueOnce(0.4) // Trigger suffix
      .mockReturnValueOnce(0.5) // Select a different suffix
      .mockReturnValueOnce(0.9); // Fallback to original
    const echoes = generateEchoes('journey', 3);
    expect(echoes).toContain('The Original: "journey"');
    expect(echoes).toContain(expect.stringMatching(/"journey" from the past/));
    expect(echoes).toContain(expect.stringMatching(/"journey" from the dream/));
  });

  test('generates echoes with word replacements', () => {
    mockMath.random
      .mockReturnValueOnce(0.7) // Trigger word replacement
      .mockReturnValueOnce(0)   // Select first word "time"
      .mockReturnValueOnce(0)   // Select first replacement "chronos"
      .mockReturnValueOnce(0.9); // Fallback to original
    const echoes = generateEchoes('the time is now', 2);
    expect(echoes).toContain('The Original: "the time is now"');
    expect(echoes).toContain(expect.stringMatching(/Shifted: "the chronos is now"/));
  });

  test('generates echoes with simple distortions (word reverse)', () => {
    mockMath.random
      .mockReturnValueOnce(0.9) // Trigger distortion
      .mockReturnValueOnce(0)   // Select first word "hello"
      .mockReturnValueOnce(0.9); // Fallback to original
    const echoes = generateEchoes('hello world', 2);
    expect(echoes).toContain('The Original: "hello world"');
    expect(echoes).toContain(expect.stringMatching(/Distorted: "olleh world"/));
  });

  test('handles phrases with no replaceable words for word replacement path', () => {
    mockMath.random
      .mockReturnValueOnce(0.7) // Trigger word replacement
      .mockReturnValueOnce(0.9); // Fallback to original
    const echoes = generateEchoes('apple banana', 2);
    expect(echoes).toContain('The Original: "apple banana"');
    expect(echoes).toContain('Faint echo of "apple banana"'); // Fallback behavior
  });

  test('handles single word phrases for distortion path', () => {
    mockMath.random
      .mockReturnValueOnce(0.9) // Trigger distortion
      .mockReturnValueOnce(0)   // Select the single word
      .mockReturnValueOnce(0.9); // Fallback to original
    const echoes = generateEchoes('single', 2);
    expect(echoes).toContain('The Original: "single"');
    expect(echoes).toContain('Distorted: "elgnis"');
  });

  test('ensures unique echoes are generated up to count', () => {
    // Force all paths to generate the same echo initially, then vary
    mockMath.random
      .mockReturnValueOnce(0.1) // Prefix
      .mockReturnValueOnce(0)   // "Whisper of"
      .mockReturnValueOnce(0.1) // Prefix
      .mockReturnValueOnce(0)   // "Whisper of" (duplicate)
      .mockReturnValueOnce(0.4) // Suffix
      .mockReturnValueOnce(0)   // "past"
      .mockReturnValueOnce(0.9); // Fallback to original
    const echoes = generateEchoes('test', 3);
    // Expect 3 unique echoes, even if randomizer tries to create duplicates
    expect(echoes).toHaveLength(3);
    expect(new Set(echoes).size).toBe(3); // Verify uniqueness
  });
});
