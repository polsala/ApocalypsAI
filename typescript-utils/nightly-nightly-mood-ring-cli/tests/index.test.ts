import * as readline from 'readline';
import chalk from 'chalk';
import { classifyMood, moods } from '../src/moods';

// Mock rationale: We need to simulate user input and capture console output
// to test the CLI's interactive behavior and output correctness without actual I/O.
// This ensures deterministic and offline testing.

// Mock readline.createInterface and its methods
const mockQuestion = jest.fn();
const mockClose = jest.fn();
const mockCreateInterface = jest.fn(() => ({
  question: mockQuestion,
  close: mockClose,
}));

jest.mock('readline', () => ({
  createInterface: mockCreateInterface,
}));

// Mock console.log to capture output
const mockConsoleLog = jest.spyOn(console, 'log').mockImplementation(() => {});

// Dynamically import the main module after mocks are set up
// This is necessary because `src/index.ts` calls `readline.createInterface` at the top level
// and `runMoodRing()` immediately if `require.main === module`.
let runMoodRing: () => Promise<void>;

beforeAll(async () => {
  const mainModule = await import('../src/index');
  runMoodRing = mainModule.runMoodRing; // Assuming runMoodRing is exported for testing
});

beforeEach(() => {
  mockQuestion.mockClear();
  mockClose.mockClear();
  mockCreateInterface.mockClear();
  mockConsoleLog.mockClear();
});

describe('classifyMood', () => {
  it('should classify "calm" as Serene Sapphire', () => {
    const mood = classifyMood('I feel calm');
    expect(mood.type).toBe('Serene Sapphire');
  });

  it('should classify "happy" as Vibrant Verdant', () => {
    const mood = classifyMood('I am very happy today!');
    expect(mood.type).toBe('Vibrant Verdant');
  });

  it('should classify "stressed" as Obsidian Shadow', () => {
    const mood = classifyMood('Feeling quite stressed out.');
    expect(mood.type).toBe('Obsidian Shadow');
  });

  it('should classify "confused" as Rainbow Shimmer', () => {
    const mood = classifyMood('I am so confused about everything.');
    expect(mood.type).toBe('Rainbow Shimmer');
  });

  it('should classify "frustrated" as Crimson Ember', () => {
    const mood = classifyMood('This is so frustrating!');
    expect(mood.type).toBe('Crimson Ember');
  });

  it('should classify "sad" as Azure Abyss', () => {
    const mood = classifyMood('Feeling a bit sad.');
    expect(mood.type).toBe('Azure Abyss');
  });

  it('should classify "hopeful" as Golden Glow', () => {
    const mood = classifyMood('I feel hopeful for the future.');
    expect(mood.type).toBe('Golden Glow');
  });

  it('should classify "introspective" as Amethyst Aura', () => {
    const mood = classifyMood('Just feeling introspective.');
    expect(mood.type).toBe('Amethyst Aura');
  });

  it('should return Rainbow Shimmer for unknown input', () => {
    const mood = classifyMood('I feel like a potato.');
    expect(mood.type).toBe('Rainbow Shimmer');
  });

  it('should be case-insensitive', () => {
    const mood = classifyMood('CALM');
    expect(mood.type).toBe('Serene Sapphire');
  });

  it('should handle multiple keywords, picking the first match', () => {
    // 'happy' comes before 'stressed' in the moods array's keyword check order
    const mood = classifyMood('I am happy but also stressed');
    expect(mood.type).toBe('Vibrant Verdant'); // 'happy' is found first
  });
});

describe('runMoodRing', () => {
  it('should prompt the user and display the correct mood and insight', async () => {
    // Simulate user input 'calm'
    mockQuestion.mockImplementationOnce((_question, callback) => {
      callback('I feel calm');
    });

    await runMoodRing();

    expect(mockCreateInterface).toHaveBeenCalledTimes(1);
    expect(mockQuestion).toHaveBeenCalledTimes(1);
    expect(mockQuestion).toHaveBeenCalledWith(
      expect.stringContaining('How are you feeling right now, wanderer of the digital wastes?'),
      expect.any(Function)
    );

    // Find the Serene Sapphire mood from the actual moods array
    const sereneMood = moods.find(m => m.type === 'Serene Sapphire');
    if (!sereneMood) throw new Error('Serene Sapphire mood not found');

    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('✨ The Nightly Mood Ring hums softly... ✨'));
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining(`Your aura glows with ${sereneMood.color(sereneMood.type)}!`));
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining(`"${sereneMood.insight}"`));
    expect(mockClose).toHaveBeenCalledTimes(1);
  });

  it('should handle an unknown feeling and default to Rainbow Shimmer', async () => {
    // Simulate user input 'blarg'
    mockQuestion.mockImplementationOnce((_question, callback) => {
      callback('blarg');
    });

    await runMoodRing();

    const rainbowMood = moods.find(m => m.type === 'Rainbow Shimmer');
    if (!rainbowMood) throw new Error('Rainbow Shimmer mood not found');

    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining(`Your aura glows with ${rainbowMood.color(rainbowMood.type)}!`));
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining(`"${rainbowMood.insight}"`));
    expect(mockClose).toHaveBeenCalledTimes(1);
  });

  it('should correctly classify and display for a "stressed" input', async () => {
    mockQuestion.mockImplementationOnce((_question, callback) => {
      callback('I am feeling very stressed today.');
    });

    await runMoodRing();

    const stressedMood = moods.find(m => m.type === 'Obsidian Shadow');
    if (!stressedMood) throw new Error('Obsidian Shadow mood not found');

    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining(`Your aura glows with ${stressedMood.color(stressedMood.type)}!`));
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining(`"${stressedMood.insight}"`));
    expect(mockClose).toHaveBeenCalledTimes(1);
  });
});
