const { getAttireSuggestion, getRandomElement, weatherConditions, moods } = require('../src/index');
const { attireRules } = require('../src/data');

// Mock rationale: Math.random is mocked to ensure getRandomElement returns predictable values for deterministic tests.
// This prevents tests from failing due to random selection.
describe('getAttireSuggestion', () => {
  test('should return correct attire for valid weather and mood', () => {
    const weather = "Acid Rain";
    const mood = "Scavenging";
    const expected = attireRules[weather][mood];
    expect(getAttireSuggestion(weather, mood)).toBe(expected);
  });

  test('should return correct attire for valid weather and mood (case-insensitive)', () => {
    const weather = "acid rain";
    const mood = "scavenging";
    const expected = attireRules["Acid Rain"]["Scavenging"];
    expect(getAttireSuggestion(weather, mood)).toBe(expected);
  });

  test('should return an error message for unknown weather', () => {
    const weather = "Volcanic Ashfall";
    const mood = "Bunker Formal";
    const expected = `Unknown weather condition: "Volcanic Ashfall". Available: ${weatherConditions.join(', ')}.`;
    expect(getAttireSuggestion(weather, mood)).toBe(expected);
  });

  test('should return an error message for unknown mood', () => {
    const weather = "Irradiated Haze";
    const mood = "Disco Party";
    const expected = `Unknown mood/occasion: "Disco Party". Available: ${moods.join(', ')}.`;
    expect(getAttireSuggestion(weather, mood)).toBe(expected);
  });

  test('should return a generic message if no weather or mood is provided', () => {
    expect(getAttireSuggestion(null, null)).toBe("Please provide both a weather condition and a mood, or let me choose for you!");
    expect(getAttireSuggestion("Irradiated Haze", null)).not.toBe("Please provide both a weather condition and a mood, or let me choose for you!");
  });
});

describe('getRandomElement', () => {
  // Mock rationale: Math.random is mocked to ensure getRandomElement returns predictable values for deterministic tests.
  // This prevents tests from failing due to random selection.
  const mockMath = Object.create(global.Math);
  mockMath.random = () => 0.5; // Always return the middle element for an odd-length array, or second half for even.
  global.Math = mockMath;

  test('should return a random element from an array', () => {
    const arr = ['a', 'b', 'c', 'd', 'e'];
    expect(getRandomElement(arr)).toBe('c'); // 0.5 * 5 = 2.5, floor is 2, arr[2] is 'c'
  });

  test('should return a random element from a different array', () => {
    const arr = [10, 20, 30, 40];
    expect(getRandomElement(arr)).toBe(30); // 0.5 * 4 = 2, floor is 2, arr[2] is 30
  });

  test('should handle single-element array', () => {
    const arr = ['single'];
    expect(getRandomElement(arr)).toBe('single'); // 0.5 * 1 = 0.5, floor is 0, arr[0] is 'single'
  });

  test('should handle empty array', () => {
    const arr = [];
    expect(getRandomElement(arr)).toBeUndefined();
  });
});

// Test CLI output by mocking console.log and process.argv
describe('CLI functionality', () => {
  let consoleSpy;
  let originalArgv;

  beforeEach(() => {
    consoleSpy = jest.spyOn(console, 'log').mockImplementation(() => {});
    originalArgv = process.argv;
    // Mock rationale: process.argv is mocked to simulate different command-line inputs
    // without actually running the process with different arguments.
    process.argv = ['node', 'index.js']; // Base arguments
  });

  afterEach(() => {
    consoleSpy.mockRestore();
    process.argv = originalArgv;
    jest.clearAllMocks();
  });

  test('should display help message with --help', () => {
    process.argv.push('--help');
    require('../src/index').runCli(); // Call the CLI function directly
    expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('Usage:'));
    expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('Options:'));
  });

  test('should display help message with -h', () => {
    process.argv.push('-h');
    require('../src/index').runCli();
    expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('Usage:'));
  });

  test('should list weather conditions and moods with --list', () => {
    process.argv.push('--list');
    require('../src/index').runCli();
    expect(consoleSpy).toHaveBeenCalledWith("Available Weather Conditions:");
    expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('- Irradiated Haze'));
    expect(consoleSpy).toHaveBeenCalledWith("\nAvailable Moods/Occasions:");
    expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('- Scavenging'));
  });

  test('should provide a specific suggestion when weather and mood are given', () => {
    process.argv.push('Acid Rain', 'Raid Prep');
    require('../src/index').runCli();
    expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('For "Acid Rain" and "Raid Prep", you should wear:'));
    expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining(attireRules["Acid Rain"]["Raid Prep"]));
  });

  test('should provide a random suggestion with --random', () => {
    // Mock rationale: Math.random is mocked to ensure getRandomElement returns predictable values for deterministic tests.
    // This prevents tests from failing due to random selection.
    const mockMath = Object.create(global.Math);
    mockMath.random = () => 0; // Always pick the first element
    global.Math = mockMath;

    process.argv.push('--random');
    require('../src/index').runCli();
    expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining(`Randomly selected: Weather "${weatherConditions[0]}", Mood "${moods[0]}"`));
    expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining(attireRules[weatherConditions[0]][moods[0]]));
  });

  test('should choose random mood if only weather is provided', () => {
    // Mock rationale: Math.random is mocked to ensure getRandomElement returns predictable values for deterministic tests.
    // This prevents tests from failing due to random selection.
    const mockMath = Object.create(global.Math);
    mockMath.random = () => 0; // Always pick the first element
    global.Math = mockMath;

    process.argv.push('Dust Storm');
    require('../src/index').runCli();
    expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('No mood provided. Choosing a random one.'));
    expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining(`For "Dust Storm" and "${moods[0]}", you should wear:`));
    expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining(attireRules["Dust Storm"][moods[0]]));
  });

  test('should choose random weather and mood if none are provided', () => {
    // Mock rationale: Math.random is mocked to ensure getRandomElement returns predictable values for deterministic tests.
    // This prevents tests from failing due to random selection.
    const mockMath = Object.create(global.Math);
    mockMath.random = () => 0; // Always pick the first element
    global.Math = mockMath;

    require('../src/index').runCli();
    expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('No weather provided. Choosing a random one.'));
    expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('No mood provided. Choosing a random one.'));
    expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining(`For "${weatherConditions[0]}" and "${moods[0]}", you should wear:`));
    expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining(attireRules[weatherConditions[0]][moods[0]]));
  });
});
