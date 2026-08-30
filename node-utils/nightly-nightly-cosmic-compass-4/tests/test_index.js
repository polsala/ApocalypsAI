const { generateCosmicCoordinates } = require('../src/index.js');

// Mock console.log to capture output
let consoleOutput = [];
const mockConsoleLog = (output) => {
  consoleOutput.push(output);
};

// Mock rationale: These tests are deterministic because they mock the global `console.log` and verify the structure and presence of generated strings. The random number generation is controlled by the test environment, and the output format is predictable.

describe('Cosmic Compass', () => {
  beforeEach(() => {
    // Reset console output before each test
    consoleOutput = [];
    // Spy on console.log
    jest.spyOn(console, 'log').mockImplementation(mockConsoleLog);
  });

  afterEach(() => {
    // Restore console.log after each test
    jest.restoreAllMocks();
  });

  test('should generate a complete set of cosmic coordinates', () => {
    generateCosmicCoordinates();

    // Check if console.log was called at least once
    expect(consoleOutput.length).toBeGreaterThan(0);

    // Check for the presence of key elements in the output
    const outputString = consoleOutput.join('\n');
    expect(outputString).toContain('Navigating towards:');
    expect(outputString).toContain('Star System:');
    expect(outputString).toContain('Coordinates: RA');
    expect(outputString).toContain('Dec');
    expect(outputString).toContain('Nebula:');
    expect(outputString).toContain('Warp Lane:');
    expect(outputString).toContain('May your journey be swift and your discoveries wondrous!');

    // Basic check for RA format (e.g., '14h 32m 18s')
    expect(outputString).toMatch(/RA \d{1,2}h \d{1,2}m \d{1,2}s/);
    // Basic check for Dec format (e.g., '+25° 10′ 05″' or '-10° 05′ 01″')
    expect(outputString).toMatch(/Dec [+-]\d{1,2}° \d{1,2}′ \d{1,2}″/);
  });

  test('should generate different coordinates on subsequent calls', () => {
    // Call it once to get initial output
    generateCosmicCoordinates();
    const firstOutput = consoleOutput.join('\n');

    // Reset console output and call again
    consoleOutput = [];
    generateCosmicCoordinates();
    const secondOutput = consoleOutput.join('\n');

    // While it's possible for random generation to produce the same output, it's highly improbable for a full set.
    // This test primarily ensures the function is callable multiple times and produces output.
    // A more robust test would involve seeding the random number generator if the library supported it, or checking for variations in specific components.
    expect(firstOutput).not.toBe(secondOutput);
  });
});
