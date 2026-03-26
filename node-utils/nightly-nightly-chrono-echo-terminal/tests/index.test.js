const { echoWithTemporalEffects, parseArgs } = require('../src/index');

describe('parseArgs', () => {
  test('should parse message and default options', () => {
    const args = ['Hello'];
    const { message, delay, glitchProbability, reverseProbability } = parseArgs(args);
    expect(message).toBe('Hello');
    expect(delay).toBe(50);
    expect(glitchProbability).toBe(0.05);
    expect(reverseProbability).toBe(0.01);
  });

  test('should parse custom delay', () => {
    const args = ['-d', '100', 'World'];
    const { message, delay } = parseArgs(args);
    expect(message).toBe('World');
    expect(delay).toBe(100);
  });

  test('should parse custom glitch probability', () => {
    const args = ['--glitch-probability', '0.5', 'Test'];
    const { message, glitchProbability } = parseArgs(args);
    expect(message).toBe('Test');
    expect(glitchProbability).toBe(0.5);
  });

  test('should parse custom reverse probability', () => {
    const args = ['Message', '-r', '0.1'];
    const { message, reverseProbability } = parseArgs(args);
    expect(message).toBe('Message');
    expect(reverseProbability).toBe(0.1);
  });

  test('should handle mixed arguments', () => {
    const args = ['-d', '10', 'Mixed', '-g', '0.2', '-r', '0.05'];
    const { message, delay, glitchProbability, reverseProbability } = parseArgs(args);
    expect(message).toBe('Mixed');
    expect(delay).toBe(10);
    expect(glitchProbability).toBe(0.2);
    expect(reverseProbability).toBe(0.05);
  });

  test('should exit with error if no message is provided', () => {
    const mockExit = jest.spyOn(process, 'exit').mockImplementation(() => {});
    const mockError = jest.spyOn(console, 'error').mockImplementation(() => {});
    parseArgs(['-d', '100']);
    expect(mockError).toHaveBeenCalledWith(expect.stringContaining('Usage:'));
    expect(mockExit).toHaveBeenCalledWith(1);
    mockExit.mockRestore();
    mockError.mockRestore();
  });

  test('should exit with error on unknown argument', () => {
    const mockExit = jest.spyOn(process, 'exit').mockImplementation(() => {});
    const mockError = jest.spyOn(console, 'error').mockImplementation(() => {});
    parseArgs(['Hello', '--unknown-arg']);
    expect(mockError).toHaveBeenCalledWith(expect.stringContaining('Unknown argument'));
    expect(mockExit).toHaveBeenCalledWith(1);
    mockExit.mockRestore();
    mockError.mockRestore();
  });
});

describe('echoWithTemporalEffects', () => {
  let mockStdoutWrite;
  let output = '';

  beforeEach(() => {
    jest.useFakeTimers(); // Mock rationale: Allows controlling setTimeout for deterministic testing of delays.
    output = '';
    mockStdoutWrite = jest.fn((chunk) => {
      output += chunk;
    });
  });

  afterEach(() => {
    jest.runOnlyPendingTimers(); // Ensure all timers are cleared
    jest.clearAllTimers();
    jest.useRealTimers();
  });

  test('should echo a simple message with delay', async () => {
    const message = 'Hi';
    const delay = 10;
    const promise = echoWithTemporalEffects(message, delay, 0, 0, mockStdoutWrite);

    jest.advanceTimersByTime(delay); // H
    expect(output).toBe('H');
    jest.advanceTimersByTime(delay); // i
    expect(output).toBe('Hi');
    jest.advanceTimersByTime(delay); // \n
    expect(output).toBe('Hi\n');

    await promise; // Wait for the promise to resolve after all timers are run
    expect(mockStdoutWrite).toHaveBeenCalledTimes(message.length + 1); // 2 chars + 1 newline
  });

  test('should apply glitches based on probability', async () => {
    const message = 'Test';
    const delay = 1;
    // Mock rationale: Control Math.random to deterministically trigger glitches.
    jest.spyOn(Math, 'random')
      .mockReturnValueOnce(0.6) // T - no glitch
      .mockReturnValueOnce(0.01) // e - glitch
      .mockReturnValueOnce(0.6) // s - no glitch
      .mockReturnValueOnce(0.01) // t - glitch
      .mockReturnValue(0.6); // For any subsequent calls (e.g., reverse prob)

    const promise = echoWithTemporalEffects(message, delay, 0.5, 0, mockStdoutWrite);

    jest.advanceTimersByTime(delay * message.length + delay); // Run all timers
    await promise;

    // We expect 'T' and 's' to be original, 'e' and 't' to be glitched.
    // Since we don't know *what* the glitched char will be, we check length and non-originality.
    expect(output.length).toBe(message.length + 1); // 4 chars + newline
    expect(output[0]).toBe('T');
    expect(output[1]).not.toBe('e'); // Glitched
    expect(output[2]).toBe('s');
    expect(output[3]).not.toBe('t'); // Glitched
    expect(output[4]).toBe('\n');

    Math.random.mockRestore();
  });

  test('should apply segment reversal based on probability', async () => {
    const message = 'ABCDEF';
    const delay = 1;
    // Mock rationale: Control Math.random to deterministically trigger a reversal.
    jest.spyOn(Math, 'random')
      .mockReturnValueOnce(0.005) // Trigger reverse for 'ABC'
      .mockReturnValue(0.9); // No glitches or further reversals

    const promise = echoWithTemporalEffects(message, delay, 0, 0.01, mockStdoutWrite);

    // Await the full execution
    jest.advanceTimersByTime(delay * (message.length + 1)); // (3 reversed + 3 normal) + newline
    await promise;

    // 'ABC' should become 'CBA'
    // 'DEF' should remain 'DEF'
    expect(output).toBe('CBADEF\n');
    expect(mockStdoutWrite).toHaveBeenCalledTimes(message.length + 1); // 6 chars + 1 newline

    Math.random.mockRestore();
  });

  test('should handle empty message', async () => {
    const message = '';
    const delay = 10;
    const promise = echoWithTemporalEffects(message, delay, 0, 0, mockStdoutWrite);

    jest.advanceTimersByTime(delay); // Only for the final newline
    await promise;

    expect(output).toBe('\n');
    expect(mockStdoutWrite).toHaveBeenCalledTimes(1); // Only the newline
  });

  test('should not glitch or reverse if probabilities are 0', async () => {
    const message = 'Hello';
    const delay = 1;
    // Mock rationale: Ensure Math.random is not called for glitch/reverse logic when probabilities are 0.
    const randomSpy = jest.spyOn(Math, 'random');

    const promise = echoWithTemporalEffects(message, delay, 0, 0, mockStdoutWrite);
    jest.advanceTimersByTime(delay * message.length + delay);
    await promise;

    expect(output).toBe('Hello\n');
    expect(randomSpy).not.toHaveBeenCalled(); // No random calls expected
    randomSpy.mockRestore();
  });
});
