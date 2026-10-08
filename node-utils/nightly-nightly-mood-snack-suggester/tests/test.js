const { getSnackSuggestion } = require('../src/snackSuggester');
const { run } = require('../src/index'); // To test the CLI output
const yargs = require('yargs'); // Mock yargs for CLI tests

// Mock rationale: We need to capture console output and control CLI arguments
// without actually running the full CLI process or affecting the real console.
// This ensures tests are deterministic and isolated.

describe('getSnackSuggestion', () => {
  test('should return correct snack for "grumpy" mood', () => {
    const suggestion = getSnackSuggestion('grumpy');
    expect(suggestion.name).toBe('Irradiated Twinkie');
    expect(suggestion.description).toContain('eternal grumpiness');
  });

  test('should return correct snack for "energetic" mood', () => {
    const suggestion = getSnackSuggestion('energetic');
    expect(suggestion.name).toBe('Mutant Berry Blend');
    expect(suggestion.description).toContain('potent burst of energy');
  });

  test('should return correct snack for "contemplative" mood (case-insensitive)', () => {
    const suggestion = getSnackSuggestion('CoNtEmPlAtIvE');
    expect(suggestion.name).toBe('Dusty Can of Beans (vintage 2042)');
    expect(suggestion.description).toContain('quiet reflection');
  });

  test('should return default snack for unknown mood', () => {
    const suggestion = getSnackSuggestion('confused');
    expect(suggestion.name).toBe('Dehydrated Nutrient Paste');
    expect(suggestion.description).toContain('universal sustenance');
  });

  test('should return default snack for empty mood', () => {
    const suggestion = getSnackSuggestion('');
    expect(suggestion.name).toBe('Dehydrated Nutrient Paste');
  });
});

describe('CLI Integration', () => {
  let consoleSpy;
  let exitSpy;

  beforeEach(() => {
    consoleSpy = jest.spyOn(console, 'log').mockImplementation(() => {});
    exitSpy = jest.spyOn(process, 'exit').mockImplementation(() => {});
    // Mock rationale: Prevent actual console output during tests and prevent process from exiting.
    // This allows us to assert on the output and control test flow.
  });

  afterEach(() => {
    consoleSpy.mockRestore();
    exitSpy.mockRestore();
  });

  test('should output correct snack for a valid mood via CLI', async () => {
    // Mock rationale: Simulate yargs parsing command-line arguments.
    // This allows us to test the `run` function as if it were called from the CLI.
    jest.spyOn(yargs, 'argv', 'get').mockReturnValue({ mood: 'hopeful' });

    await run();

    expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('Mood: hopeful'));
    expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('Suggested Snack: Foraged Mushroom Surprise'));
    expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('Description: A rare find! Hopefully, it\'s the edible kind. A gamble, much like hope itself. Chew thoroughly.'));
    expect(exitSpy).not.toHaveBeenCalled();
  });

  test('should output default snack for an unknown mood via CLI', async () => {
    jest.spyOn(yargs, 'argv', 'get').mockReturnValue({ mood: 'ecstatic' });

    await run();

    expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('Mood: ecstatic'));
    expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('Suggested Snack: Dehydrated Nutrient Paste'));
    expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('Description: When your mood is beyond classification, or simply \'meh\', this universal sustenance will do. It\'s... food.'));
    expect(exitSpy).not.toHaveBeenCalled();
  });

  test('should prompt for mood and exit if no mood is provided via CLI', async () => {
    jest.spyOn(yargs, 'argv', 'get').mockReturnValue({}); // No mood provided

    await run();

    expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('Please specify your mood.'));
    expect(exitSpy).toHaveBeenCalledWith(1);
  });
});
