import axios from 'axios';
import { checkTemporalSync, getNodeTimestamp } from '../src/index'; // Assuming index.ts exports these

// Mock axios for testing
jest.mock('axios');
const mockAxios = axios as jest.Mocked<typeof axios>;

// Mock console.log and console.error to capture output
let consoleLogSpy: jest.SpyInstance;
let consoleErrorSpy: jest.SpyInstance;

beforeEach(() => {
  consoleLogSpy = jest.spyOn(console, 'log').mockImplementation(() => {});
  consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
  // Reset mock before each test
  mockAxios.get.mockClear();
});

afterEach(() => {
  consoleLogSpy.mockRestore();
  consoleErrorSpy.mockRestore();
});

describe('getNodeTimestamp', () => {
  it('should return timestamp and no error for a valid response', async () => {
    // Mock rationale: Simulates a successful API call to a temporal node.
    mockAxios.get.mockResolvedValue({
      data: { timestamp: 1678886400000 },
      status: 200,
      statusText: 'OK',
      headers: {},
      config: {},
    });

    const result = await getNodeTimestamp('http://mock-node.com/time');
    expect(result).toEqual({
      url: 'http://mock-node.com/time',
      timestamp: 1678886400000,
      error: null,
    });
    expect(mockAxios.get).toHaveBeenCalledWith('http://mock-node.com/time', { timeout: 5000 });
  });

  it('should return null timestamp and an error for network issues', async () => {
    // Mock rationale: Simulates a network error (e.g., connection refused) when trying to reach a node.
    const error = new Error('Network Error');
    (error as any).response = { status: 500 }; // Add mock response details if needed
    mockAxios.get.mockRejectedValue(error);

    const result = await getNodeTimestamp('http://mock-node.com/time');
    expect(result).toEqual({
      url: 'http://mock-node.com/time',
      timestamp: null,
      error: 'Network Error',
    });
  });

  it('should return null timestamp and an error for invalid timestamp format', async () => {
    // Mock rationale: Simulates a node returning data in an unexpected format.
    mockAxios.get.mockResolvedValue({
      data: { timestamp: 'not-a-number' },
      status: 200,
      statusText: 'OK',
      headers: {},
      config: {},
    });

    const result = await getNodeTimestamp('http://mock-node.com/time');
    expect(result).toEqual({
      url: 'http://mock-node.com/time',
      timestamp: null,
      error: 'Invalid timestamp format received',
    });
  });
});

describe('checkTemporalSync', () => {
  const mockNodeUrls = ['http://node1.test', 'http://node2.test', 'http://node3.test'];
  const mockTolerance = 5;

  it('should report synced status when all nodes are within tolerance', async () => {
    const currentTime = Date.now();
    // Mock rationale: Simulates multiple nodes reporting timestamps that are very close to each other and within tolerance.
    mockAxios.get.mockImplementation(async (url) => {
      if (url === 'http://node1.test') return { data: { timestamp: currentTime }, status: 200 };
      if (url === 'http://node2.test') return { data: { timestamp: currentTime + 100 }, status: 200 };
      if (url === 'http://node3.test') return { data: { timestamp: currentTime - 50 }, status: 200 };
      return { data: {}, status: 500 }; // Should not happen
    });

    await checkTemporalSync(mockNodeUrls, mockTolerance);

    expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining('Checking temporal sync'));
    expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining('http://node1.test: Timestamp'));
    expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining('http://node2.test: Timestamp'));
    expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining('http://node3.test: Timestamp'));
    expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining('Maximum temporal drift detected: 150ms')); // Max diff between +100 and -50 from first
    expect(consoleLogSpy).toHaveBeenCalledWith('Overall sync status: SYNCED');
    expect(process.exitCode).toBeUndefined(); // No error exit
  });

  it('should report desynced status when nodes exceed tolerance', async () => {
    const currentTime = Date.now();
    // Mock rationale: Simulates nodes with timestamps significantly different, exceeding the tolerance.
    mockAxios.get.mockImplementation(async (url) => {
      if (url === 'http://node1.test') return { data: { timestamp: currentTime }, status: 200 };
      if (url === 'http://node2.test') return { data: { timestamp: currentTime + 6000 }, status: 200 }; // 6 seconds difference
      if (url === 'http://node3.test') return { data: { timestamp: currentTime - 1000 }, status: 200 };
      return { data: {}, status: 500 };
    });

    await checkTemporalSync(mockNodeUrls, mockTolerance);

    expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining('Checking temporal sync'));
    expect(consoleLogSpy).toHaveBeenCalledWith('Overall sync status: DESYNCED');
    expect(process.exitCode).toBe(1); // Indicate failure
  });

  it('should report errors for unreachable nodes', async () => {
    const currentTime = Date.now();
    // Mock rationale: Simulates one node being unreachable while others are fine.
    mockAxios.get.mockImplementation(async (url) => {
      if (url === 'http://node1.test') return { data: { timestamp: currentTime }, status: 200 };
      if (url === 'http://node2.test') return { data: { timestamp: currentTime + 100 }, status: 200 };
      if (url === 'http://node3.test') throw new Error('Connection refused');
      return { data: {}, status: 500 };
    });

    await checkTemporalSync(mockNodeUrls, mockTolerance);

    expect(consoleErrorSpy).toHaveBeenCalledWith(expect.stringContaining('--- Errors Encountered ---'));
    expect(consoleErrorSpy).toHaveBeenCalledWith(expect.stringContaining('http://node3.test: Connection refused'));
    expect(consoleLogSpy).toHaveBeenCalledWith('Overall sync status: SYNCED'); // Sync check still happens with valid nodes
  });

  it('should report if not enough valid nodes are available', async () => {
    // Mock rationale: Simulates a scenario where all nodes fail or return invalid data.
    mockAxios.get.mockImplementation(async (url) => {
      if (url === 'http://node1.test') throw new Error('Node offline');
      if (url === 'http://node2.test') return { data: { timestamp: 'invalid' }, status: 200 };
      if (url === 'http://node3.test') throw new Error('Node offline');
      return { data: {}, status: 500 };
    });

    await checkTemporalSync(mockNodeUrls, mockTolerance);

    expect(consoleErrorSpy).toHaveBeenCalledWith(expect.stringContaining('Not enough valid nodes to perform sync check.'));
    expect(process.exitCode).toBeUndefined(); // No error exit from checkTemporalSync itself, but no sync report
  });
});
