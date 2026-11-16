import { strict as assert } from 'assert';
import { analyzeText, Mood } from '../src/index';
import * as fs from 'fs'; // Import fs to mock it

// # Mock rationale: fs.readFileSync is mocked to prevent actual file system access
// during tests, ensuring determinism and offline execution. This allows testing
// the CLI's file input parsing logic without needing real files.
const mockFsReadFileSync = jest.spyOn(fs, 'readFileSync');

describe('analyzeText', () => {
  it('should correctly analyze text with GloomDoom keywords', () => {
    const text = "The apocalypse is nigh, bringing despair and ruin.";
    const result = analyzeText(text);
    assert.equal(result.dominantMood, Mood.GloomDoom);
    assert.equal(result.moodCounts[Mood.GloomDoom], 3);
    assert.equal(result.moodCounts[Mood.HopeSpark], 0);
  });

  it('should correctly analyze text with HopeSpark keywords', () => {
    const text = "A spark of hope for the future, let's build and grow.";
    const result = analyzeText(text);
    assert.equal(result.dominantMood, Mood.HopeSpark);
    assert.equal(result.moodCounts[Mood.HopeSpark], 3);
    assert.equal(result.moodCounts[Mood.GloomDoom], 0);
  });

  it('should correctly analyze text with ChaosChuckle keywords', () => {
    const text = "Embrace the chaos, a whimsical giggle in the unpredictable disorder.";
    const result = analyzeText(text);
    assert.equal(result.dominantMood, Mood.ChaosChuckle);
    assert.equal(result.moodCounts[Mood.ChaosChuckle], 4);
  });

  it('should correctly analyze text with VoidZen keywords', () => {
    const text = "Find peace in the void, a serene stillness and calm.";
    const result = analyzeText(text);
    assert.equal(result.dominantMood, Mood.VoidZen);
    assert.equal(result.moodCounts[Mood.VoidZen], 3);
  });

  it('should return Neutral for text with no recognized keywords', () => {
    const text = "This is a plain sentence with no special words.";
    const result = analyzeText(text);
    assert.equal(result.dominantMood, Mood.Neutral);
    assert.equal(result.moodCounts[Mood.GloomDoom], 0);
    assert.equal(result.totalWords, 9);
  });

  it('should return Mixed for text with multiple dominant moods', () => {
    const text = "The doom of the apocalypse, yet a spark of hope and a whimsical chaos.";
    const result = analyzeText(text);
    assert.equal(result.dominantMood, Mood.Mixed);
    assert.equal(result.moodCounts[Mood.GloomDoom], 2);
    assert.equal(result.moodCounts[Mood.HopeSpark], 1);
    assert.equal(result.moodCounts[Mood.ChaosChuckle], 1);
  });

  it('should handle empty input gracefully', () => {
    const text = "";
    const result = analyzeText(text);
    assert.equal(result.dominantMood, Mood.Neutral);
    assert.equal(result.totalLines, 0);
    assert.equal(result.totalWords, 0);
    assert.deepStrictEqual(result.moodCounts, {
      [Mood.GloomDoom]: 0,
      [Mood.HopeSpark]: 0,
      [Mood.ChaosChuckle]: 0,
      [Mood.VoidZen]: 0,
      [Mood.Neutral]: 0,
      [Mood.Mixed]: 0
    });
  });

  it('should calculate mood distribution correctly', () => {
    const text = "Doom and despair, but also hope for the future.";
    const result = analyzeText(text);
    const totalMoodScore = result.moodCounts[Mood.GloomDoom] + result.moodCounts[Mood.HopeSpark];
    assert.equal(result.moodDistribution[Mood.GloomDoom], result.moodCounts[Mood.GloomDoom] / totalMoodScore);
    assert.equal(result.moodDistribution[Mood.HopeSpark], result.moodCounts[Mood.HopeSpark] / totalMoodScore);
    assert.equal(result.moodDistribution[Mood.ChaosChuckle], 0);
  });

  it('should be case-insensitive for keywords', () => {
    const text = "Apocalypse and HOpe and chAoS and vOiD.";
    const result = analyzeText(text);
    assert.equal(result.moodCounts[Mood.GloomDoom], 1);
    assert.equal(result.moodCounts[Mood.HopeSpark], 1);
    assert.equal(result.moodCounts[Mood.ChaosChuckle], 1);
    assert.equal(result.moodCounts[Mood.VoidZen], 1);
    assert.equal(result.dominantMood, Mood.Mixed);
  });

  it('should count multiple occurrences of the same keyword', () => {
    const text = "Doom, doom, and more doom. Despair, despair.";
    const result = analyzeText(text);
    assert.equal(result.moodCounts[Mood.GloomDoom], 5); // 3x doom, 2x despair
    assert.equal(result.dominantMood, Mood.GloomDoom);
  });
});

// Mocking global objects for CLI tests is more complex and often involves child_process.
// For this self-contained utility, we focus on testing the core `analyzeText` function.
// The `main` function's interaction with `fs` and `process.stdin` is assumed to be correct
// if `analyzeText` is robust. However, for completeness, a basic mock for `fs.readFileSync`
// is included to demonstrate how external dependencies would be handled if `main` were tested directly.

describe('CLI behavior (simulated)', () => {
  // Reset mocks before each test
  beforeEach(() => {
    mockFsReadFileSync.mockClear();
  });

  it('should read from file when --file argument is provided', async () => {
    // # Mock rationale: Simulates reading a file without actual disk I/O.
    mockFsReadFileSync.mockReturnValueOnce("The void is calm.");

    // Temporarily modify process.argv to simulate CLI input
    const originalArgv = process.argv;
    process.argv = ['node', 'index.js', '--file', 'dummy.txt'];

    // Mock console.log to capture output
    const originalConsoleLog = console.log;
    let capturedOutput = '';
    console.log = (msg: string) => { capturedOutput += msg; };

    // Dynamically import and run main to avoid module caching issues with process.argv changes
    const { main } = await import('../src/index');
    await main();

    assert.ok(mockFsReadFileSync.calledWith('dummy.txt', 'utf8'));
    const result = JSON.parse(capturedOutput);
    assert.equal(result.dominantMood, Mood.VoidZen);
    assert.equal(result.moodCounts[Mood.VoidZen], 1);

    // Restore original process.argv and console.log
    process.argv = originalArgv;
    console.log = originalConsoleLog;

    // Clear module cache for subsequent tests if needed, though not strictly necessary for this setup
    // delete require.cache[require.resolve('../src/index')];
  });

  // Note: Mocking process.stdin for piped input in a synchronous test environment is significantly
  // more complex and typically requires a separate test runner or child process execution.
  // The `analyzeText` function covers the core logic, and the `main` function's stdin handling
  // is a standard Node.js pattern.
});
