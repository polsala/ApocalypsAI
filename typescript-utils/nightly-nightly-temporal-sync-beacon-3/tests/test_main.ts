import axios from 'axios';
import { execSync } from 'child_process';
import { main } from '../src/main'; // Assuming main is exported for testing, or adjust import path

// Mocking axios and child_process
jest.mock('axios');
jest.mock('child_process');

const mockAxios = axios as jest.Mocked<typeof axios>;
const mockExecSync = execSync as jest.Mock;

// Mock rationale: These mocks are essential for deterministic and offline testing.
// They allow us to simulate network responses and system command executions without
// actual network calls or modifying the system's time during tests.

describe('Temporal Sync Beacon', () => {
  const mockBeaconUrl = 'http://mock-beacon.com/time';
  const mockBeaconTimestamp = 1678886400000; // March 15, 2023 12:00:00 PM UTC
  const mockLocalTimestamp = 1678886405000; // March 15, 2023 12:00:05 PM UTC (5 seconds later)
  const mockOffsetMs = mockBeaconTimestamp - mockLocalTimestamp; // -5000ms

  beforeEach(() => {
    // Reset mocks before each test
    mockAxios.get.mockClear();
    mockExecSync.mockClear();
    // Mock Date.now() to return a consistent value for local timestamp
    jest.spyOn(Date, 'now').mockReturnValue(mockLocalTimestamp);
  });

  afterEach(() => {
    // Restore Date.now() after all tests
    jest.restoreAllMocks();
  });

  test('should fetch time from beacon and report offset', async () => {
    mockAxios.get.mockResolvedValue({
      data: { timestamp: mockBeaconTimestamp },
      status: 200,
      statusText: 'OK',
      headers: {},
      config: {},
    });

    // Mock console.log to capture output
    const consoleSpy = jest.spyOn(console, 'log').mockImplementation(() => {});

    // Simulate command line arguments
    process.argv = ['node', 'src/main.ts', '--beacon-url', mockBeaconUrl];

    await main();

    expect(mockAxios.get).toHaveBeenCalledWith(mockBeaconUrl);
    expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('Temporal Sync Beacon Status:'));
    expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining(`Beacon URL: ${mockBeaconUrl}`));
    expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('Temporal Offset: -5000ms'));
    expect(mockExecSync).not.toHaveBeenCalled(); // Not adjusting time in this test

    consoleSpy.detroy(); // Clean up spy
  });

  test('should adjust local time if --adjust flag is provided and offset is significant', async () => {
    mockAxios.get.mockResolvedValue({
      data: { timestamp: mockBeaconTimestamp },
      status: 200,
      statusText: 'OK',
      headers: {},
      config: {},
    });

    // Mock console.log and console.warn
    const consoleSpy = jest.spyOn(console, 'log').mockImplementation(() => {});
    const consoleWarnSpy = jest.spyOn(console, 'warn').mockImplementation(() => {});

    // Simulate command line arguments with --adjust
    process.argv = ['node', 'src/main.ts', '--beacon-url', mockBeaconUrl, '--adjust'];

    await main();

    expect(mockAxios.get).toHaveBeenCalledWith(mockBeaconUrl);
    // The exact command might vary based on OS, so we check for the presence of 'sudo date -s'
    expect(mockExecSync).toHaveBeenCalledWith(expect.stringContaining('sudo date -s @'));
    expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('Local time adjusted successfully.'));

    consoleSpy.mockRestore();
    consoleWarnSpy.mockRestore();
  });

  test('should not adjust local time if offset is not significant', async () => {
    const smallOffsetTimestamp = 1678886400500; // 500ms difference
    jest.spyOn(Date, 'now').mockReturnValue(smallOffsetTimestamp);

    mockAxios.get.mockResolvedValue({
      data: { timestamp: mockBeaconTimestamp },
      status: 200,
      statusText: 'OK',
      headers: {},
      config: {},
    });

    const consoleSpy = jest.spyOn(console, 'log').mockImplementation(() => {});

    process.argv = ['node', 'src/main.ts', '--beacon-url', mockBeaconUrl, '--adjust'];

    await main();

    expect(mockAxios.get).toHaveBeenCalledWith(mockBeaconUrl);
    expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('Local time is already within acceptable synchronization range. No adjustment needed.'));
    expect(mockExecSync).not.toHaveBeenCalled();

    consoleSpy.mockRestore();
  });

  test('should handle invalid timestamp format from beacon', async () => {
    mockAxios.get.mockResolvedValue({
      data: { timestamp: 'not a number' },
      status: 200,
      statusText: 'OK',
      headers: {},
      config: {},
    });

    const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});

    process.argv = ['node', 'src/main.ts', '--beacon-url', mockBeaconUrl];

    await expect(main()).rejects.toThrow('Invalid timestamp format from beacon.');
    expect(mockAxios.get).toHaveBeenCalledWith(mockBeaconUrl);
    expect(consoleErrorSpy).toHaveBeenCalledWith(expect.stringContaining('Invalid timestamp format from beacon.'));

    consoleErrorSpy.mockRestore();
  });

  test('should handle network errors when fetching from beacon', async () => {
    const networkError = new Error('Network Error');
    mockAxios.get.mockRejectedValue(networkError);

    const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});

    process.argv = ['node', 'src/main.ts', '--beacon-url', mockBeaconUrl];

    await expect(main()).rejects.toThrow('Network Error');
    expect(mockAxios.get).toHaveBeenCalledWith(mockBeaconUrl);
    expect(consoleErrorSpy).toHaveBeenCalledWith(expect.stringContaining(`Error fetching time from beacon at ${mockBeaconUrl}: Network Error`));

    consoleErrorSpy.mockRestore();
  });

  test('should exit with error if beacon-url is not provided', () => {
    const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
    const processExitSpy = jest.spyOn(process, 'exit').mockImplementation((code?: number) => { throw new Error(`process.exit(${code})`) });

    process.argv = ['node', 'src/main.ts']; // No beacon URL

    try {
      main();
    } catch (e: any) {
      expect(e.message).toBe('process.exit(1)');
      expect(consoleErrorSpy).toHaveBeenCalledWith('Error: --beacon-url is required.');
    }

    consoleErrorSpy.mockRestore();
    processExitSpy.mockRestore();
  });
});
