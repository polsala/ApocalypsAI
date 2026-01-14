import { getCosmicGuidance } from '../src/index';
import { CardinalDirection } from '../src/types';

// Mock rationale: Math.random() is used to select a random phrase.
// To ensure deterministic tests, we mock Math.random() to always return a specific value,
// allowing us to predict which phrase will be chosen.
describe('getCosmicGuidance', () => {
  const mockRandom = jest.spyOn(Math, 'random');

  beforeEach(() => {
    // Reset mock before each test
    mockRandom.mockRestore();
  });

  it('should return a valid guidance for North', () => {
    mockRandom.mockReturnValue(0.1); // Always pick the first phrase
    const guidance = getCosmicGuidance('N');
    expect(guidance.direction).toBe('N');
    expect(guidance.message).toBe("To the N: Follow the faint echo of the void, where forgotten stars hum.");
  });

  it('should return a valid guidance for South (case-insensitive)', () => {
    mockRandom.mockReturnValue(0.5); // Always pick the second phrase
    const guidance = getCosmicGuidance('s');
    expect(guidance.direction).toBe('S');
    expect(guidance.message).toBe("To the S: Embrace the warmth of the Southern Cross, finding comfort in the unknown.");
  });

  it('should return a valid guidance for East', () => {
    mockRandom.mockReturnValue(0.9); // Always pick the last phrase
    const guidance = getCosmicGuidance('E');
    expect(guidance.direction).toBe('E');
    expect(guidance.message).toBe("To the E: Unravel the threads of destiny, where the first light touches.");
  });

  it('should return a valid guidance for West', () => {
    mockRandom.mockReturnValue(0.0); // Always pick the first phrase
    const guidance = getCosmicGuidance('W');
    expect(guidance.direction).toBe('W');
    expect(guidance.message).toBe("To the W: Veer slightly towards the shimmering nebula, seeking nascent truths.");
  });

  it('should throw an error for an invalid direction', () => {
    expect(() => getCosmicGuidance('X' as CardinalDirection)).toThrow('Invalid direction: X. Please use N, S, E, or W.');
  });

  it('should throw an error for an empty direction', () => {
    expect(() => getCosmicGuidance('' as CardinalDirection)).toThrow('Invalid direction: . Please use N, S, E, or W.');
  });
});

// Test CLI execution separately
describe('CLI execution', () => {
  const mockConsoleError = jest.spyOn(console, 'error').mockImplementation(() => {});
  const mockConsoleLog = jest.spyOn(console, 'log').mockImplementation(() => {});
  const mockProcessExit = jest.spyOn(process, 'exit').mockImplementation((code?: number) => { throw new Error(`process.exit: ${code}`); });
  const mockRandom = jest.spyOn(Math, 'random');

  beforeEach(() => {
    mockConsoleError.mockClear();
    mockConsoleLog.mockClear();
    mockProcessExit.mockClear();
    mockRandom.mockRestore(); // Restore Math.random for CLI tests, as it's less critical to mock for output string matching
    jest.resetModules(); // CRITICAL: Clear module cache to re-import index.ts and re-run top-level CLI logic
  });

  afterAll(() => {
    mockConsoleError.mockRestore();
    mockConsoleLog.mockRestore();
    mockProcessExit.mockRestore();
    mockRandom.mockRestore();
  });

  it('should log guidance for a valid direction', () => {
    mockRandom.mockReturnValue(0.1); // Ensure consistent output for this test
    process.argv = ['node', 'index.ts', 'N'];
    try {
      require('../src/index'); // Re-import to trigger CLI logic
    } catch (e) {
      // Expected if process.exit is called, but not for valid execution
    }
    expect(mockConsoleLog).toHaveBeenCalledWith("To the N: Follow the faint echo of the void, where forgotten stars hum.");
    expect(mockConsoleError).not.toHaveBeenCalled();
    expect(mockProcessExit).not.toHaveBeenCalled();
  });

  it('should log an error and exit for no direction', () => {
    process.argv = ['node', 'index.ts'];
    expect(() => require('../src/index')).toThrow('process.exit: 1');
    expect(mockConsoleError).toHaveBeenCalledWith("Error: Please provide a cardinal direction (N, S, E, W).");
    expect(mockProcessExit).toHaveBeenCalledWith(1);
    expect(mockConsoleLog).not.toHaveBeenCalled();
  });

  it('should log an error and exit for an invalid direction', () => {
    process.argv = ['node', 'index.ts', 'INVALID'];
    expect(() => require('../src/index')).toThrow('process.exit: 1');
    expect(mockConsoleError).toHaveBeenCalledWith("Error: Invalid direction: INVALID. Please use N, S, E, or W.");
    expect(mockProcessExit).toHaveBeenCalledWith(1);
    expect(mockConsoleLog).not.toHaveBeenCalled();
  });
});
