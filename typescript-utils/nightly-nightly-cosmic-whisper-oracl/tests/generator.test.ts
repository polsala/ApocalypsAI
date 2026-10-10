import { generateWhisper } from '../src/generator';
import { WhisperCategory, WhisperOutcome } from '../src/types';
import { WHISPER_PROMPTS } from '../src/data';

describe('generateWhisper', () => {
  let mockMathRandom: jest.SpyInstance;

  beforeEach(() => {
    // Mock rationale: Ensure deterministic test results by controlling Math.random().
    // This allows us to predict which prompt will be selected from the data array.
    mockMathRandom = jest.spyOn(Math, 'random').mockReturnValue(0.5); // Always pick the middle element if possible
  });

  afterEach(() => {
    mockMathRandom.mockRestore(); // Restore original Math.random() after each test
  });

  it('should generate a whisper with a valid structure', () => {
    const whisper = generateWhisper();
    expect(whisper).toHaveProperty('category');
    expect(whisper).toHaveProperty('prompt');
    expect(whisper).toHaveProperty('action');
    expect(whisper).toHaveProperty('risk');
    expect(whisper).toHaveProperty('timestamp');
    expect(typeof whisper.category).toBe('string');
    expect(typeof whisper.prompt).toBe('string');
    expect(typeof whisper.action).toBe('string');
    expect(typeof whisper.risk).toBe('string');
    expect(typeof whisper.timestamp).toBe('string');
    expect(new Date(whisper.timestamp).toISOString()).toBe(whisper.timestamp); // Check valid ISO string
  });

  it('should generate a whisper from a specific category when provided', () => {
    const category: WhisperCategory = "Resource";
    const resourcePrompts = WHISPER_PROMPTS.filter(p => p.category === category);
    mockMathRandom.mockReturnValue(0.0); // Pick the first resource prompt (index 0)

    const whisper = generateWhisper(category);
    expect(whisper.category).toBe(category);
    expect(whisper.prompt).toBe(resourcePrompts[0].prompt);
    expect(whisper.action).toBe(resourcePrompts[0].actionVerb);
  });

  it('should throw an error if no whispers are found for a given category', () => {
    const invalidCategory = "NonExistent" as WhisperCategory; // Cast to test error handling
    expect(() => generateWhisper(invalidCategory)).toThrow(`No whispers found for category: ${invalidCategory}`);
  });

  it('should select a random prompt when no category is specified', () => {
    // With mockMathRandom at 0.5, and 18 prompts, it should pick index 9 (Math.floor(0.5 * 18) = 9)
    const expectedPrompt = WHISPER_PROMPTS[9]; // Index 9 is 'exp-1'
    const whisper = generateWhisper();
    expect(whisper.prompt).toBe(expectedPrompt.prompt);
    expect(whisper.category).toBe(expectedPrompt.category);
  });

  it('should select a random prompt within a category', () => {
    const category: WhisperCategory = "Shelter";
    const shelterPrompts = WHISPER_PROMPTS.filter(p => p.category === category);
    mockMathRandom.mockReturnValue(0.99); // Pick the last shelter prompt (index 2 of 3)

    const whisper = generateWhisper(category);
    expect(whisper.category).toBe(category);
    expect(whisper.prompt).toBe(shelterPrompts[shelterPrompts.length - 1].prompt);
  });
});
