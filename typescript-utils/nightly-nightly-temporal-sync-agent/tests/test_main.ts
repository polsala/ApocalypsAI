import { createClient } from 'ntp-client';
import { startSyncAgent } from '../src/main'; // Assuming startSyncAgent is exported for testing

// Mock the ntp-client library
jest.mock('ntp-client', () => ({
  createClient: jest.fn(),
}));

const mockNtpClient = {
  on: jest.fn(),
  query: jest.fn(),
};

const mockCreateClient = createClient as jest.Mock;

describe('Temporal Sync Agent', () => {
  let originalNodeEnv: string | undefined;
  let consoleSpy: jest.SpyInstance;

  beforeAll(() => {
    originalNodeEnv = process.env.NODE_ENV;
    process.env.NODE_ENV = 'test'; // Set to test environment to enable mock
    // Mock the console methods to prevent actual logging during tests
    consoleSpy = jest.spyOn(console, 'log').mockImplementation(() => {});
    jest.spyOn(console, 'error').mockImplementation(() => {});
  });

  beforeEach(() => {
    // Reset mocks before each test
    mockCreateClient.mockClear();
    (mockNtpClient.on as jest.Mock).mockClear();
    (mockNtpClient.query as jest.Mock).mockClear();
    mockCreateClient.mockReturnValue(mockNtpClient);
    // Reset interval mocks
    jest.useFakeTimers();
  });

  afterAll(() => {
    process.env.NODE_ENV = originalNodeEnv; // Restore original NODE_ENV
    consoleSpy.clearInterval();
    consoleSpy.mockRestore();
  });

  test('should initialize with default NTP server and interval', () => {
    startSyncAgent();

    expect(mockCreateClient).toHaveBeenCalledWith('pool.ntp.org');
    expect(mockNtpClient.on).toHaveBeenCalledWith('error', expect.any(Function));
    expect(mockNtpClient.on).toHaveBeenCalledWith('message', expect.any(Function));
    expect(mockNtpClient.query).toHaveBeenCalledTimes(1);
    expect(setInterval).toHaveBeenCalledTimes(1);
    expect(setInterval).toHaveBeenCalledWith(expect.any(Function), 3600000);
  });

  test('should use custom NTP server and interval from environment variables', () => {
    process.env.NTP_SERVER = 'time.google.com';
    process.env.UPDATE_INTERVAL_MS = '1800000'; // 30 minutes

    startSyncAgent();

    expect(mockCreateClient).toHaveBeenCalledWith('time.google.com');
    expect(setInterval).toHaveBeenCalledWith(expect.any(Function), 1800000);
  });

  test('should handle invalid UPDATE_INTERVAL_MS', () => {
    process.env.UPDATE_INTERVAL_MS = 'invalid';
    const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});

    startSyncAgent();

    expect(consoleErrorSpy).toHaveBeenCalledWith('Invalid UPDATE_INTERVAL_MS. Using default.');
    expect(mockCreateClient).toHaveBeenCalledWith('pool.ntp.org'); // Should fall back to default
    expect(setInterval).toHaveBeenCalledTimes(1);
    expect(setInterval).toHaveBeenCalledWith(expect.any(Function), 3600000);

    consoleErrorSpy.mockRestore();
  });

  test('should call syncTime on interval', () => {
    startSyncAgent();
    jest.advanceTimersByTime(3600000);
    expect(mockCreateClient).toHaveBeenCalledTimes(2); // Initial call + 1 interval call
    expect(mockNtpClient.query).toHaveBeenCalledTimes(2);
  });

  test('NTP message handler should log time', () => {
    const messageHandler = mockNtpClient.on.mock.calls.find(call => call[0] === 'message')?.[1];
    const mockTxTimestamp = Date.now() / 1000;
    const expectedISOTime = new Date(mockTxTimestamp * 1000).toISOString();

    if (messageHandler) {
      messageHandler({ txTimestamp: mockTxTimestamp });
      expect(consoleSpy).toHaveBeenCalledWith(`NTP server time: ${expectedISOTime}`);
      expect(consoleSpy).toHaveBeenCalledWith('System time synchronization simulated successfully.');
    } else {
      fail('Message handler not found');
    }
  });

  test('NTP error handler should log error', () => {
    const errorHandler = mockNtpClient.on.mock.calls.find(call => call[0] === 'error')?.[1];
    const mockError = new Error('Simulated NTP error');

    if (errorHandler) {
      errorHandler(mockError);
      expect(consoleSpy).toHaveBeenCalledWith(`NTP client error: ${mockError.message}`);
    } else {
      fail('Error handler not found');
    }
  });
});
