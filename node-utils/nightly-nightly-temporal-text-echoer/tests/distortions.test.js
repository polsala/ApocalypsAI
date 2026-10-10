const { applyFading, applyGlitch, applyEcho, GLITCH_SYMBOLS } = require('../src/distortions');

describe('Temporal Text Distortions', () => {
  let mockMathRandom;

  beforeEach(() => {
    // Mock rationale: Ensure deterministic output for random operations.
    mockMathRandom = jest.spyOn(Math, 'random').mockReturnValue(0.5);
  });

  afterEach(() => {
    mockMathRandom.mockRestore();
  });

  describe('applyFading', () => {
    test('should return original text if intensity is 0', () => {
      expect(applyFading("hello", 0)).toBe("hello");
    });

    test('should remove characters when Math.random() <= intensity', () => {
      // With mock Math.random returning 0.5, characters should be removed if intensity >= 0.5
      // Let's set specific mock values for a clear test.
      mockMathRandom.mockRestore();
      mockMathRandom = jest.spyOn(Math, 'random')
        .mockReturnValueOnce(0.6) // Keep 'a' (0.6 > 0.5)
        .mockReturnValueOnce(0.1) // Remove 'b' (0.1 <= 0.5)
        .mockReturnValueOnce(0.7); // Keep 'c' (0.7 > 0.5)
      // Mock rationale: Ensure deterministic output for random operations.
      expect(applyFading("abc", 0.5)).toBe("ac");
    });

    test('should remove all characters if intensity is 1', () => {
      mockMathRandom.mockRestore();
      mockMathRandom = jest.spyOn(Math, 'random').mockReturnValue(0.0); // Mock rationale: Ensure deterministic output for random operations.
      expect(applyFading("test", 1)).toBe("");
    });

    test('should keep all characters if intensity is 0', () => {
      mockMathRandom.mockRestore();
      mockMathRandom = jest.spyOn(Math, 'random').mockReturnValue(0.9); // Mock rationale: Ensure deterministic output for random operations.
      expect(applyFading("test", 0)).toBe("test");
    });
  });

  describe('applyGlitch', () => {
    test('should return original text if intensity is 0', () => {
      expect(applyGlitch("hello", 0)).toBe("hello");
    });

    test('should replace characters with glitch symbols based on intensity', () => {
      // With mock Math.random returning 0.5, characters should be glitched if intensity > 0.5
      // Let's set specific mock values for a clear test.
      mockMathRandom.mockRestore();
      mockMathRandom = jest.spyOn(Math, 'random')
        .mockReturnValueOnce(0.1) // Glitch 'a' (0.1 < 0.5)
        .mockReturnValueOnce(0.0) // Mock rationale: Deterministic glitch character selection (first symbol)
        .mockReturnValueOnce(0.6) // Keep 'b' (0.6 >= 0.5)
        .mockReturnValueOnce(0.2) // Glitch 'c' (0.2 < 0.5)
        .mockReturnValueOnce(1.0); // Mock rationale: Deterministic glitch character selection (last symbol)
      // Mock rationale: Ensure deterministic output for random operations.
      expect(applyGlitch("abc", 0.5)).toBe(`${GLITCH_SYMBOLS[0]}b${GLITCH_SYMBOLS[GLITCH_SYMBOLS.length - 1]}`);
    });

    test('should glitch all characters if intensity is 1', () => {
      mockMathRandom.mockRestore();
      mockMathRandom = jest.spyOn(Math, 'random')
        .mockReturnValueOnce(0.1) // Glitch 't'
        .mockReturnValueOnce(0.0) // Mock rationale: Deterministic glitch char selection
        .mockReturnValueOnce(0.2) // Glitch 'e'
        .mockReturnValueOnce(0.0) // Mock rationale: Deterministic glitch char selection
        .mockReturnValueOnce(0.3) // Glitch 's'
        .mockReturnValueOnce(0.0) // Mock rationale: Deterministic glitch char selection
        .mockReturnValueOnce(0.4) // Glitch 't'
        .mockReturnValueOnce(0.0); // Mock rationale: Deterministic glitch char selection
      // Mock rationale: Ensure deterministic output for random operations.
      expect(applyGlitch("test", 1)).toBe("!!!!"); // Assuming first symbol is '!'
    });
  });

  describe('applyEcho', () => {
    test('should return original text if intensity is 0', () => {
      expect(applyEcho("hello world", 0)).toBe("hello world");
    });

    test('should echo words based on intensity', () => {
      // With mock Math.random returning 0.5, words should be echoed if intensity > 0.5
      // Let's set specific mock values for a clear test.
      mockMathRandom.mockRestore();
      mockMathRandom = jest.spyOn(Math, 'random')
        .mockReturnValueOnce(0.6) // No echo for 'hello' (0.6 >= 0.5)
        .mockReturnValueOnce(0.1) // Echo 'world' (0.1 < 0.5)
        .mockReturnValueOnce(0.7); // No echo for 'again' (0.7 >= 0.5)
      // Mock rationale: Ensure deterministic output for random operations.
      expect(applyEcho("hello world again", 0.5)).toBe("hello world... world again");
    });

    test('should echo all eligible words if intensity is 1', () => {
      mockMathRandom.mockRestore();
      mockMathRandom = jest.spyOn(Math, 'random').mockReturnValue(0.1); // Mock rationale: Ensure deterministic output for random operations.
      expect(applyEcho("one two three", 1)).toBe("one... one two... two three... three");
    });

    test('should not echo short words or punctuation-only words', () => {
      mockMathRandom.mockRestore();
      mockMathRandom = jest.spyOn(Math, 'random').mockReturnValue(0.1); // Mock rationale: Ensure deterministic output for random operations.
      expect(applyEcho("a b c. d!", 1)).toBe("a b c. d!"); // Words 'a', 'b', 'c.', 'd!' are too short or not alphanumeric enough
    });

    test('should handle leading/trailing/multiple spaces correctly', () => {
      mockMathRandom.mockRestore();
      mockMathRandom = jest.spyOn(Math, 'random').mockReturnValue(0.1); // Mock rationale: Ensure deterministic output for random operations.
      expect(applyEcho("  hello   world  ", 1)).toBe("  hello... hello   world... world  ");
    });
  });

  describe('Combined Distortions', () => {
    test('should apply multiple distortions sequentially', () => {
      // Input: "Hello World"
      // Fading (0.5): Keep if random > 0.5. Remove if random <= 0.5.
      // Glitch (0.5): Glitch if random < 0.5. Keep if random >= 0.5.
      // Echo (0.5): Echo if random < 0.5. Keep if random >= 0.5.

      mockMathRandom.mockRestore();
      mockMathRandom = jest.spyOn(Math, 'random')
        // Fading "Hello World" (intensity 0.5)
        .mockReturnValueOnce(0.6) // Keep 'H'
        .mockReturnValueOnce(0.1) // Remove 'e'
        .mockReturnValueOnce(0.7) // Keep 'l'
        .mockReturnValueOnce(0.2) // Remove 'l'
        .mockReturnValueOnce(0.8) // Keep 'o'
        .mockReturnValueOnce(0.9) // Keep ' '
        .mockReturnValueOnce(0.3) // Remove 'W'
        .mockReturnValueOnce(0.4) // Remove 'o'
        .mockReturnValueOnce(0.5) // Remove 'r'
        .mockReturnValueOnce(0.6) // Keep 'l'
        .mockReturnValueOnce(0.7) // Keep 'd'
        // Faded result: "H o ld"

        // Glitching "H o ld" (intensity 0.5)
        .mockReturnValueOnce(0.1) // Glitch 'H'
        .mockReturnValueOnce(0.0) // Mock rationale: Deterministic glitch char selection (first symbol)
        .mockReturnValueOnce(0.6) // Keep ' '
        .mockReturnValueOnce(0.2) // Glitch 'o'
        .mockReturnValueOnce(0.0) // Mock rationale: Deterministic glitch char selection (first symbol)
        .mockReturnValueOnce(0.7) // Keep ' '
        .mockReturnValueOnce(0.3) // Glitch 'l'
        .mockReturnValueOnce(0.0) // Mock rationale: Deterministic glitch char selection (first symbol)
        .mockReturnValueOnce(0.8) // Keep 'd'
        // Glitched result: "! # !d"

        // Echoing "! # !d" (intensity 0.5)
        .mockReturnValueOnce(0.1) // Echo '!'
        .mockReturnValueOnce(0.2) // Echo '#'
        .mockReturnValueOnce(0.3); // Echo '!d'
      // Mock rationale: Ensure deterministic output for random operations across multiple distortions.
      const fadedText = applyFading("Hello World", 0.5);
      const glitchedText = applyGlitch(fadedText, 0.5);
      const echoedText = applyEcho(glitchedText, 0.5);

      expect(fadedText).toBe("H o ld");
      expect(glitchedText).toBe("! # !d");
      expect(echoedText).toBe("!... ! #... # !d... !d");
    });
  });
});
