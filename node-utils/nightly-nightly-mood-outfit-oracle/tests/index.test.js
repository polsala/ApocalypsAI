const { generateOutfit, moods, weatherConditions } = require('../src/index');

// Mock rationale: We need to test the CLI behavior without actually running it
// or affecting the global process.argv. By mocking process.argv, we can
// simulate different command-line inputs deterministically. Similarly, mocking
// console.log, console.error, and process.exit allows us to capture output
// and prevent the test runner from exiting prematurely.
const mockProcessArgv = (args) => {
  const originalArgv = process.argv;
  process.argv = ['node', 'src/index.js', ...args];
  return () => { process.argv = originalArgv; }; // Restore original
};

describe('generateOutfit', () => {
  test('should generate an outfit for a valid mood and weather', () => {
    const mood = 'resilient';
    const weather = 'ashfall';
    const output = generateOutfit(mood, weather);

    expect(output).toContain('--- Nightly Mood-Matching Outfit Oracle ---');
    expect(output).toContain('Desired Mood: Resilient');
    expect(output).toContain('Simulated Weather: Ashfall');
    expect(output).toContain('- Sturdy scavenged boots');
    expect(output).toContain('- Respirator mask');
    expect(output).toContain('Stay safe and stylish in the wastes!');
  });

  test('should return an error for an unknown mood', () => {
    const mood = 'unknown';
    const weather = 'clear skies';
    const output = generateOutfit(mood, weather);
    expect(output).toContain('Unknown mood: "unknown"');
    expect(output).toContain(`Available moods: ${Object.keys(moods).join(", ")}`);
  });

  test('should return an error for unknown weather', () => {
    const mood = 'optimistic';
    const weather = 'apocalyptic hail';
    const output = generateOutfit(mood, weather);
    expect(output).toContain('Unknown weather: "apocalyptic hail"');
    expect(output).toContain(`Available weather: ${Object.keys(weatherConditions).join(", ")}`);
  });

  test('should generate correct output for "mysterious" and "irradiated drizzle"', () => {
    const mood = 'mysterious';
    const weather = 'irradiated drizzle';
    const output = generateOutfit(mood, weather);

    expect(output).toContain('Desired Mood: Mysterious');
    expect(output).toContain('Simulated Weather: Irradiated Drizzle');
    expect(output).toContain('- Silent-tread sneakers');
    expect(output).toContain('- Darkened, flowing cloak');
    expect(output).toContain('- Waterproof outer shell (lead-lined if available)');
    expect(output).toContain('- Geiger counter pouch');
  });

  test('should handle different casing for mood and weather', () => {
    const mood = 'OPTIMISTIC';
    const weather = 'Solar Flare Advisory';
    const output = generateOutfit(mood, weather);

    expect(output).toContain('Desired Mood: OPTIMISTIC'); // Displayed as input
    expect(output).toContain('Simulated Weather: Solar Flare Advisory'); // Displayed as input
    expect(output).toContain('- Brightly patched overalls');
    expect(output).toContain('- UV-protective eyewear');
  });
});

describe('CLI execution', () => {
  let consoleLogSpy;
  let consoleErrorSpy;
  let exitSpy;
  let restoreArgv;

  beforeEach(() => {
    consoleLogSpy = jest.spyOn(console, 'log').mockImplementation(() => {});
    consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
    exitSpy = jest.spyOn(process, 'exit').mockImplementation(() => {});
  });

  afterEach(() => {
    consoleLogSpy.mockRestore();
    consoleErrorSpy.mockRestore();
    exitSpy.mockRestore();
    if (restoreArgv) restoreArgv();
  });

  test('should print usage to stderr and exit with 1 if no arguments are provided', () => {
    restoreArgv = mockProcessArgv([]);
    require('../src/index');
    expect(consoleErrorSpy).toHaveBeenCalledWith(expect.stringContaining('Usage: nightly-mood-outfit-oracle <mood> <weather>'));
    expect(exitSpy).toHaveBeenCalledWith(1);
  });

  test('should print usage to stderr and exit with 1 if only one argument is provided', () => {
    restoreArgv = mockProcessArgv(['resilient']);
    require('../src/index');
    expect(consoleErrorSpy).toHaveBeenCalledWith(expect.stringContaining('Usage: nightly-mood-outfit-oracle <mood> <weather>'));
    expect(exitSpy).toHaveBeenCalledWith(1);
  });

  test('should print outfit to stdout for valid arguments', () => {
    restoreArgv = mockProcessArgv(['daring', 'whispering winds']);
    require('../src/index');
    expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining('Desired Mood: daring'));
    expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining('Simulated Weather: whispering winds'));
    expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining('- Armored plating (lightweight)'));
    expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining('- Thick scarf or cowl'));
    expect(exitSpy).not.toHaveBeenCalled();
    expect(consoleErrorSpy).not.toHaveBeenCalled();
  });

  test('should print error message to stdout for unknown mood but not exit', () => {
    restoreArgv = mockProcessArgv(['unknown', 'clear skies']);
    require('../src/index');
    expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining('Unknown mood: "unknown"'));
    expect(exitSpy).not.toHaveBeenCalled();
    expect(consoleErrorSpy).not.toHaveBeenCalled();
  });

  test('should print error message to stdout for unknown weather but not exit', () => {
    restoreArgv = mockProcessArgv(['optimistic', 'apocalyptic hail']);
    require('../src/index');
    expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining('Unknown weather: "apocalyptic hail"'));
    expect(exitSpy).not.toHaveBeenCalled();
    expect(consoleErrorSpy).not.toHaveBeenCalled();
  });
});
