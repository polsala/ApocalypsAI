import { distortText } from '../src/index';

describe('distortText', () => {
  let mockRandom: jest.SpyInstance;

  beforeEach(() => {
    // Mock rationale: Math.random() is non-deterministic. Mocking it ensures tests are repeatable.
    mockRandom = jest.spyOn(Math, 'random');
  });

  afterEach(() => {
    mockRandom.mockRestore();
  });

  it('should return the original text with no distortions if all chances are 0', () => {
    mockRandom.mockReturnValue(0.9); // Ensure all chances fail
    const options = {
      charOmissionChance: 0,
      charDuplicationChance: 0,
      wordEchoChance: 0,
      staticInsertionChance: 0,
    };
    const text = 'Hello world';
    expect(distortText(text, options)).toBe('Hello world');
  });

  it('should omit characters based on chance', () => {
    mockRandom.mockReturnValueOnce(0.01) // 'H' - omit
              .mockReturnValueOnce(0.9)  // 'e' - keep
              .mockReturnValueOnce(0.01) // 'l' - omit
              .mockReturnValueOnce(0.9)  // 'l' - keep
              .mockReturnValueOnce(0.9)  // 'o' - keep
              .mockReturnValueOnce(0.9)  // whitespace - keep
              .mockReturnValueOnce(0.9)  // 'w' - keep
              .mockReturnValueOnce(0.01) // 'o' - omit
              .mockReturnValueOnce(0.9)  // 'r' - keep
              .mockReturnValueOnce(0.9)  // 'l' - keep
              .mockReturnValueOnce(0.9); // 'd' - keep
    const options = {
      charOmissionChance: 0.05,
      charDuplicationChance: 0,
      wordEchoChance: 0,
      staticInsertionChance: 0,
    };
    const text = 'Hello world';
    // Expected: H (omit) e l (omit) l o -> elo
    //           w o (omit) r l d -> wrld
    expect(distortText(text, options)).toBe('elo wrld');
  });

  it('should duplicate characters based on chance', () => {
    mockRandom.mockReturnValueOnce(0.9)  // 'H' - keep
              .mockReturnValueOnce(0.01) // 'H' - duplicate
              .mockReturnValueOnce(0.9)  // 'e' - keep
              .mockReturnValueOnce(0.9)  // 'e' - no duplicate
              .mockReturnValueOnce(0.9)  // 'l' - keep
              .mockReturnValueOnce(0.01) // 'l' - duplicate
              .mockReturnValue(0.9);     // Rest no duplicates/omissions/echo/static
    const options = {
      charOmissionChance: 0,
      charDuplicationChance: 0.05,
      wordEchoChance: 0,
      staticInsertionChance: 0,
    };
    const text = 'Hello';
    // Expected: H (dup) e l (dup) o -> HHeello
    expect(distortText(text, options)).toBe('HHeello');
  });

  it('should echo words based on chance and minEchoLength', () => {
    mockRandom.mockReturnValueOnce(0.9) // 'Hello' - no char changes
              .mockReturnValueOnce(0.01) // 'Hello' - echo
              .mockReturnValueOnce(0.9) // whitespace - keep
              .mockReturnValueOnce(0.9) // 'world' - no char changes
              .mockReturnValueOnce(0.9) // 'world' - no echo
              .mockReturnValueOnce(0.9) // whitespace - keep
              .mockReturnValueOnce(0.9) // 'hi' - no char changes
              .mockReturnValueOnce(0.9); // 'hi' - no echo
    const options = {
      charOmissionChance: 0,
      charDuplicationChance: 0,
      wordEchoChance: 0.05,
      staticInsertionChance: 0,
      minEchoLength: 3,
    };
    const text = 'Hello world hi'; // 'hi' is < minEchoLength
    expect(distortText(text, options)).toBe('Hello...hel world hi');
  });

  it('should insert static content based on chance', () => {
    mockRandom.mockReturnValueOnce(0.9) // 'Hello' - no char changes
              .mockReturnValueOnce(0.9) // 'Hello' - no echo
              .mockReturnValueOnce(0.01) // Insert static after 'Hello'
              .mockReturnValueOnce(0.5) // Pick staticContent[0] (index 0 for 0.5 < 1)
              .mockReturnValueOnce(0.9) // whitespace - keep
              .mockReturnValueOnce(0.9) // 'world' - no char changes
              .mockReturnValueOnce(0.9) // 'world' - no echo
              .mockReturnValueOnce(0.9); // No static after 'world'
    const options = {
      charOmissionChance: 0,
      charDuplicationChance: 0,
      wordEchoChance: 0,
      staticInsertionChance: 0.05,
      staticContent: ['[STATIC_A]', '[STATIC_B]'],
    };
    const text = 'Hello world';
    expect(distortText(text, options)).toBe('Hello[STATIC_A] world');
  });

  it('should handle a combination of distortions', () => {
    mockRandom.mockReturnValueOnce(0.01) // 'T' - omit
              .mockReturnValueOnce(0.9)  // 'h' - keep
              .mockReturnValueOnce(0.01) // 'h' - duplicate
              .mockReturnValueOnce(0.9)  // 'i' - keep
              .mockReturnValueOnce(0.9)  // 'i' - no duplicate
              .mockReturnValueOnce(0.9)  // 's' - keep
              .mockReturnValueOnce(0.9)  // 's' - no duplicate
              .mockReturnValueOnce(0.01) // 'This' - echo
              .mockReturnValueOnce(0.01) // Insert static after 'This'
              .mockReturnValueOnce(0.1)  // Pick staticContent[0] (index 0 for 0.1 < 1)
              .mockReturnValueOnce(0.9)  // whitespace - keep
              .mockReturnValueOnce(0.9)  // 'i' - keep
              .mockReturnValueOnce(0.9)  // 'i' - no duplicate
              .mockReturnValueOnce(0.9)  // 's' - keep
              .mockReturnValueOnce(0.9)  // 's' - no duplicate
              .mockReturnValueOnce(0.9)  // 'is' - no echo
              .mockReturnValueOnce(0.9)  // whitespace - keep
              .mockReturnValueOnce(0.9)  // 'a' - keep
              .mockReturnValueOnce(0.9)  // 'a' - no duplicate
              .mockReturnValueOnce(0.9)  // 'a' - no echo
              .mockReturnValueOnce(0.9)  // whitespace - keep
              .mockReturnValueOnce(0.9)  // 't' - keep
              .mockReturnValueOnce(0.9)  // 't' - no duplicate
              .mockReturnValueOnce(0.9)  // 'e' - keep
              .mockReturnValueOnce(0.9)  // 'e' - no duplicate
              .mockReturnValueOnce(0.9)  // 's' - keep
              .mockReturnValueOnce(0.9)  // 's' - no duplicate
              .mockReturnValueOnce(0.9)  // 't' - keep
              .mockReturnValueOnce(0.9)  // 't' - no duplicate
              .mockReturnValueOnce(0.9)  // 'test' - no echo
              .mockReturnValueOnce(0.9); // No static after 'test'

    const options = {
      charOmissionChance: 0.05,
      charDuplicationChance: 0.05,
      wordEchoChance: 0.05,
      staticInsertionChance: 0.05,
      staticContent: ['[STATIC_A]', '[STATIC_B]'],
      minEchoLength: 3,
    };
    const text = 'This is a test';
    // 'This' -> 'hhis' (T omitted, h duplicated) -> 'hhis...hhi' (echo)
    // Static after 'hhis...hhi'
    // 'is' -> 'is'
    // 'a' -> 'a'
    // 'test' -> 'test'
    expect(distortText(text, options)).toBe('hhis...hhi[STATIC_A] is a test');
  });

  it('should handle empty string', () => {
    mockRandom.mockReturnValue(0.5);
    expect(distortText('', {})).toBe('');
  });

  it('should handle text with only spaces', () => {
    mockRandom.mockReturnValue(0.5);
    expect(distortText('   ', {})).toBe('   '); 
  });

  it('should use default options when none are provided', () => {
    mockRandom.mockReturnValueOnce(0.01) // 'H' - omit
              .mockReturnValueOnce(0.9)  // 'e' - keep
              .mockReturnValueOnce(0.9)  // 'l' - keep
              .mockReturnValueOnce(0.01) // 'l' - duplicate
              .mockReturnValueOnce(0.9)  // 'o' - keep
              .mockReturnValueOnce(0.01) // 'Hello' - echo
              .mockReturnValueOnce(0.01) // Insert static after 'Hello'
              .mockReturnValueOnce(0.5)  // Pick staticContent[1] from default (index 1 for 0.5 < 1)
              .mockReturnValueOnce(0.9)  // whitespace - keep
              .mockReturnValueOnce(0.9); // Rest no distortions
    const text = 'Hello world';
    // Default staticContent: ['[...void static...]', '[...temporal hum...]', '[...echo fade...]']
    // Expected: H (omit) e l (dup) o -> elo -> elo...elo
    // Static after 'elo...elo' (index 1 of default staticContent)
    // 'world' -> world
    expect(distortText(text, {})).toBe('elo...elo[...temporal hum...] world');
  });

  it('should insert static content before trailing whitespace if present', () => {
    mockRandom.mockReturnValueOnce(0.9) // 'Hello' - no char changes
              .mockReturnValueOnce(0.9) // 'Hello' - no echo
              .mockReturnValueOnce(0.01) // Insert static after 'Hello'
              .mockReturnValueOnce(0.01) // Pick staticContent[0]
              .mockReturnValueOnce(0.9) // 'world' - no char changes
              .mockReturnValueOnce(0.9) // 'world' - no echo
              .mockReturnValueOnce(0.9); // No static after 'world'

    const options = {
      charOmissionChance: 0,
      charDuplicationChance: 0,
      wordEchoChance: 0,
      staticInsertionChance: 0.05,
      staticContent: ['[STATIC_A]'],
    };
    const text = 'Hello  world'; // Two spaces between Hello and world
    expect(distortText(text, options)).toBe('Hello[STATIC_A]  world');
  });

  it('should not insert static content if the segment is only whitespace', () => {
    mockRandom.mockReturnValueOnce(0.9) // 'Hello' - no char changes
              .mockReturnValueOnce(0.9) // 'Hello' - no echo
              .mockReturnValueOnce(0.9) // No static after 'Hello'
              .mockReturnValueOnce(0.01) // This random value would trigger static if it were a word
              .mockReturnValueOnce(0.9) // whitespace - keep
              .mockReturnValueOnce(0.9) // 'world' - no char changes
              .mockReturnValueOnce(0.9) // 'world' - no echo
              .mockReturnValueOnce(0.9); // No static after 'world'

    const options = {
      charOmissionChance: 0,
      charDuplicationChance: 0,
      wordEchoChance: 0,
      staticInsertionChance: 0.05,
      staticContent: ['[STATIC_A]'],
    };
    const text = 'Hello  world';
    expect(distortText(text, options)).toBe('Hello  world');
  });
});
