const { CosmicCommRelay } = require('../src/index.js');

// Mocking the global fetch API for deterministic testing.
// Mock rationale: This allows us to control the behavior of fetch without making actual network requests.
let mockFetchImpl = jest.fn();

// Mocking setTimeout to control delays.
// Mock rationale: This allows us to speed up tests by instantly resolving setTimeout promises.
jest.useFakeTimers();

describe('CosmicCommRelay', () => {
  let relay;

  beforeEach(() => {
    // Reset mocks before each test
    mockFetchImpl.mockClear();
    jest.clearAllTimers();

    // Set up the global fetch mock
    global.fetch = mockFetchImpl;

    // Initialize relay with default options for most tests
    relay = new CosmicCommRelay();
  });

  afterEach(() => {
    // Restore original global fetch if it existed, or remove it.
    // Mock rationale: Clean up the global scope after tests.
    delete global.fetch;
  });

  describe('constructor', () => {
    test('should initialize with default options', () => {
      expect(relay.minDelayMs).toBe(100);
      expect(relay.maxDelayMs).toBe(1000);
      expect(relay.packetLossRate).toBe(0.05);
    });

    test('should initialize with custom options', () => {
      const customRelay = new CosmicCommRelay({
        minDelayMs: 500,
        maxDelayMs: 5000,
        packetLossRate: 0.25
      });
      expect(customRelay.minDelayMs).toBe(500);
      expect(customRelay.maxDelayMs).toBe(5000);
      expect(customRelay.packetLossRate).toBe(0.25);
    });

    test('should throw error for invalid minDelayMs', () => {
      expect(() => new CosmicCommRelay({ minDelayMs: -100 })).toThrow('Invalid delay options');
    });

    test('should throw error for invalid maxDelayMs', () => {
      expect(() => new CosmicCommRelay({ maxDelayMs: -1000 })).toThrow('Invalid delay options');
    });

    test('should throw error if minDelayMs > maxDelayMs', () => {
      expect(() => new CosmicCommRelay({ minDelayMs: 2000, maxDelayMs: 1000 })).toThrow('Invalid delay options');
    });

    test('should throw error for invalid packetLossRate < 0', () => {
      expect(() => new CosmicCommRelay({ packetLossRate: -0.1 })).toThrow('Invalid packetLossRate');
    });

    test('should throw error for invalid packetLossRate > 1', () => {
      expect(() => new CosmicCommRelay({ packetLossRate: 1.1 })).toThrow('Invalid packetLossRate');
    });
  });

  describe('simulateDelay', () => {
    test('should call setTimeout with a delay within the configured range', async () => {
      const min = 500;
      const max = 1500;
      relay = new CosmicCommRelay({ minDelayMs: min, maxDelayMs: max });

      // Mock Math.random to control the delay
      // Mock rationale: Ensure the delay calculation is predictable for testing.
      jest.spyOn(Math, 'random').mockReturnValue(0.5); // This should result in a delay of 1000ms

      const delayPromise = relay.simulateDelay();
      expect(setTimeout).toHaveBeenCalledTimes(1);
      expect(setTimeout).toHaveBeenCalledWith(expect.any(Function), 1000);

      // Advance timers to resolve the delay
      jest.advanceTimersByTime(1000);
      await delayPromise;

      jest.spyOn(Math, 'random').mockRestore(); // Restore Math.random
    });
  });

  describe('simulatePacketLoss', () => {
    test('should return true when Math.random is less than packetLossRate', () => {
      relay = new CosmicCommRelay({ packetLossRate: 0.8 });
      // Mock Math.random to ensure packet loss occurs
      // Mock rationale: Force packet loss for testing the error path.
      jest.spyOn(Math, 'random').mockReturnValue(0.7);
      expect(relay.simulatePacketLoss()).toBe(true);
      jest.spyOn(Math, 'random').mockRestore();
    });

    test('should return false when Math.random is greater than or equal to packetLossRate', () => {
      relay = new CosmicCommRelay({ packetLossRate: 0.2 });
      // Mock Math.random to ensure no packet loss occurs
      // Mock rationale: Ensure the success path is tested.
      jest.spyOn(Math, 'random').mockReturnValue(0.3);
      expect(relay.simulatePacketLoss()).toBe(false);
      jest.spyOn(Math, 'random').mockRestore();
    });
  });

  describe('fetch', () => {
    const testUrl = 'http://example.com/data';

    test('should call fetch with the correct URL and options', async () => {
      // Mock Math.random to ensure no packet loss and a specific delay
      // Mock rationale: Control both delay and packet loss for predictable fetch behavior.
      jest.spyOn(Math, 'random').mockReturnValue(0.1); // No packet loss
      jest.spyOn(relay, 'simulateDelay').mockResolvedValue(); // Mock delay to resolve immediately for this test

      const mockResponse = { ok: true, json: async () => ({ message: 'success' }) };
      mockFetchImpl.mockResolvedValue(mockResponse);

      await relay.fetch(testUrl, { method: 'GET' });

      expect(mockFetchImpl).toHaveBeenCalledTimes(1);
      expect(mockFetchImpl).toHaveBeenCalledWith(testUrl, { method: 'GET' });

      jest.spyOn(Math, 'random').mockRestore();
    });

    test('should throw an error if packet loss occurs', async () => {
      // Mock Math.random to ensure packet loss
      // Mock rationale: Force packet loss to test the error handling.
      jest.spyOn(Math, 'random').mockReturnValue(0.9);
      jest.spyOn(relay, 'simulateDelay').mockResolvedValue();

      await expect(relay.fetch(testUrl)).rejects.toThrow('Cosmic interference: Packet lost to');
      expect(mockFetchImpl).not.toHaveBeenCalled();

      jest.spyOn(Math, 'random').mockRestore();
    });

    test('should throw an error for non-ok HTTP responses', async () => {
      // Mock Math.random to ensure no packet loss
      // Mock rationale: Ensure fetch is called, but the response is handled as an error.
      jest.spyOn(Math, 'random').mockReturnValue(0.1);
      jest.spyOn(relay, 'simulateDelay').mockResolvedValue();

      const mockResponse = { ok: false, status: 404 };
      mockFetchImpl.mockResolvedValue(mockResponse);

      await expect(relay.fetch(testUrl)).rejects.toThrow('Cosmic anomaly: HTTP error 404');
      expect(mockFetchImpl).toHaveBeenCalledTimes(1);
    });

    test('should propagate errors from the underlying fetch', async () => {
      // Mock Math.random to ensure no packet loss
      // Mock rationale: Test that errors originating from the actual fetch call are passed through.
      jest.spyOn(Math, 'random').mockReturnValue(0.1);
      jest.spyOn(relay, 'simulateDelay').mockResolvedValue();

      const fetchError = new Error('Network error from fetch');
      mockFetchImpl.mockRejectedValue(fetchError);

      await expect(relay.fetch(testUrl)).rejects.toThrow('Network error from fetch');
      expect(mockFetchImpl).toHaveBeenCalledTimes(1);
    });
  });
});
