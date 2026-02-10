const { generateBeacon, parseArgs } = require('../src/index');
const crypto = require('crypto');

// Mock rationale: We need deterministic timestamps for consistent test results.
// Without mocking, `new Date().toISOString()` would produce different values
// on each test run, making signature comparison impossible.
const MOCK_ISO_TIMESTAMP = '2023-10-27T10:30:00.000Z';

describe('parseArgs', () => {
  test('should return default context if no args are provided', () => {
    const args = [];
    const { context } = parseArgs(args);
    expect(context).toBe('');
  });

  test('should parse --context argument correctly', () => {
    const args = ['--context', 'test-context'];
    const { context } = parseArgs(args);
    expect(context).toBe('test-context');
  });

  test('should parse -c argument correctly', () => {
    const args = ['-c', 'short-context'];
    const { context } = parseArgs(args);
    expect(context).toBe('short-context');
  });

  test('should handle other arguments gracefully (ignore them)', () => {
    const args = ['--other-arg', 'value', '-c', 'my-context'];
    const { context } = parseArgs(args);
    expect(context).toBe('my-context');
  });

  test('should exit with error if --context is missing a value', () => {
    const mockExit = jest.spyOn(process, 'exit').mockImplementation(() => {});
    const mockError = jest.spyOn(console, 'error').mockImplementation(() => {});

    parseArgs(['--context']);

    expect(mockError).toHaveBeenCalledWith('Error: --context requires a value.');
    expect(mockExit).toHaveBeenCalledWith(1);

    mockExit.mockRestore();
    mockError.mockRestore();
  });
});

describe('generateBeacon', () => {
  let dateSpy;

  beforeEach(() => {
    dateSpy = jest.spyOn(Date.prototype, 'toISOString').mockReturnValue(MOCK_ISO_TIMESTAMP);
    // Mock rationale: Ensures `new Date().toISOString()` always returns a fixed value
    // for deterministic testing of the timestamp and signature.
  });

  afterEach(() => {
    dateSpy.mockRestore();
  });

  test('should generate a beacon with a timestamp and signature', () => {
    const beacon = generateBeacon();
    expect(beacon).toHaveProperty('timestamp');
    expect(beacon).toHaveProperty('signature');
    expect(beacon.timestamp).toBe(MOCK_ISO_TIMESTAMP);
    
    const expectedDataToHash = MOCK_ISO_TIMESTAMP + '';
    const expectedSignature = crypto.createHash('sha256').update(expectedDataToHash).digest('hex');
    expect(beacon.signature).toBe(expectedSignature);
  });

  test('should generate a beacon with context and a different signature', () => {
    const context = 'test-context';
    const beacon = generateBeacon(context);
    expect(beacon).toHaveProperty('timestamp');
    expect(beacon).toHaveProperty('signature');
    expect(beacon).toHaveProperty('context', context);
    expect(beacon.timestamp).toBe(MOCK_ISO_TIMESTAMP);

    const expectedDataToHash = MOCK_ISO_TIMESTAMP + context;
    const expectedSignature = crypto.createHash('sha256').update(expectedDataToHash).digest('hex');
    expect(beacon.signature).toBe(expectedSignature);
  });

  test('signatures should be different for different contexts', () => {
    const beacon1 = generateBeacon('context1');
    const beacon2 = generateBeacon('context2');
    expect(beacon1.signature).not.toBe(beacon2.signature);
  });

  test('signatures should be the same for identical contexts and timestamps', () => {
    const beacon1 = generateBeacon('same-context');
    const beacon2 = generateBeacon('same-context');
    expect(beacon1.signature).toBe(beacon2.signature);
  });
});

describe('CLI execution', () => {
  let logSpy;
  let dateSpy;

  beforeEach(() => {
    logSpy = jest.spyOn(console, 'log').mockImplementation(() => {});
    dateSpy = jest.spyOn(Date.prototype, 'toISOString').mockReturnValue(MOCK_ISO_TIMESTAMP);
    // Mock rationale: Captures console output for verification and ensures deterministic timestamps.
  });

  afterEach(() => {
    logSpy.mockRestore();
    dateSpy.mockRestore();
  });

  test('should print JSON output to console when run as CLI', () => {
    // Mock rationale: Simulate command line arguments for the main script.
    const originalArgv = process.argv;
    process.argv = ['node', 'src/index.js']; 
    
    // Clear module cache to re-require and trigger CLI execution block
    jest.resetModules();
    require('../src/index'); 

    expect(logSpy).toHaveBeenCalledTimes(1);
    const output = JSON.parse(logSpy.mock.calls[0][0]);
    expect(output).toHaveProperty('timestamp', MOCK_ISO_TIMESTAMP);
    expect(output).toHaveProperty('signature');

    process.argv = originalArgv; // Restore original argv
  });

  test('should print JSON output with context when run as CLI with --context', () => {
    const originalArgv = process.argv;
    process.argv = ['node', 'src/index.js', '--context', 'cli-test'];

    jest.resetModules();
    require('../src/index');

    expect(logSpy).toHaveBeenCalledTimes(1);
    const output = JSON.parse(logSpy.mock.calls[0][0]);
    expect(output).toHaveProperty('timestamp', MOCK_ISO_TIMESTAMP);
    expect(output).toHaveProperty('context', 'cli-test');
    expect(output).toHaveProperty('signature');

    process.argv = originalArgv;
  });
});
