import { TemporalSyncBeacon } from '../src/main';
import fetch from 'node-fetch';

// Mock node-fetch
jest.mock('node-fetch');
const mockFetch = fetch as jest.Mock;

// Mock EventEmitter
jest.mock('events');

// Mock Date.now() to control time for deterministic tests
const mockDateNow = jest.spyOn(Date, 'now');

describe('TemporalSyncBeacon', () => {
  const MOCK_BEACON_URL = 'http://mock.beacon.com/time';
  const SYNC_INTERVAL = 100; // Short interval for testing

  beforeEach(() => {
    // Reset mocks before each test
    mockFetch.mockClear();
    mockDateNow.mockClear();
    jest.useFakeTimers(); // Enable fake timers for setInterval/clearInterval
  });

  afterEach(() => {
    jest.useRealTimers(); // Restore real timers after tests
  });

  it('should initialize with default interval', () => {
    const beacon = new TemporalSyncBeacon(MOCK_BEACON_URL);
    // Accessing private property for test, not ideal but for demonstration
    // In a real scenario, you might expose a getter or use a different testing strategy.
    // For this example, we'll rely on the start() method to trigger the interval.
    expect(beacon).toBeDefined();
  });

  it('should synchronize time and emit a synced event', async () => {
    const mockBeaconTimestamp = 1678886400000; // A fixed point in time
    const mockLocalTimestamp1 = 1678886400050; // 50ms after beacon time
    const mockLocalTimestamp2 = 1678886400100; // 100ms after beacon time
    const expectedOffset = mockBeaconTimestamp - mockLocalTimestamp1;

    // Mock fetch to return a successful response
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ timestamp: mockBeaconTimestamp })
    });
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ timestamp: mockBeaconTimestamp })
    });

    // Mock Date.now() for deterministic local timestamps
    mockDateNow.mockReturnValueOnce(mockLocalTimestamp1);
    mockDateNow.mockReturnValueOnce(mockLocalTimestamp2);

    const beacon = new TemporalSyncBeacon(MOCK_BEACON_URL, SYNC_INTERVAL);
    const syncedSpy = jest.fn();
    beacon.on('synced', syncedSpy);

    await beacon.start(); // This will call synchronize once immediately

    // Advance timers to allow the first setInterval to potentially run (though start() calls it directly)
    jest.advanceTimersByTime(SYNC_INTERVAL);

    // Wait for the promise from start() to resolve
    await Promise.resolve();

    expect(mockFetch).toHaveBeenCalledTimes(1);
    expect(mockFetch).toHaveBeenCalledWith(MOCK_BEACON_URL);
    expect(syncedSpy).toHaveBeenCalledTimes(1);
    expect(syncedSpy).toHaveBeenCalledWith(expectedOffset);

    // Advance timers to trigger the next interval sync
    jest.advanceTimersByTime(SYNC_INTERVAL);
    await Promise.resolve(); // Wait for the next sync to complete

    expect(mockFetch).toHaveBeenCalledTimes(2);
    expect(syncedSpy).toHaveBeenCalledTimes(2);
    // The offset should be the same if Date.now() is mocked consistently
    expect(syncedSpy).toHaveBeenNthCalledWith(2, expectedOffset);

    beacon.stop();
  });

  it('should emit an error event on fetch failure', async () => {
    const fetchError = new Error('Network error');
    mockFetch.mockRejectedValueOnce(fetchError);

    const beacon = new TemporalSyncBeacon(MOCK_BEACON_URL, SYNC_INTERVAL);
    const errorSpy = jest.fn();
    beacon.on('error', errorSpy);

    await beacon.start();
    await Promise.resolve(); // Wait for the promise from start() to resolve

    expect(mockFetch).toHaveBeenCalledTimes(1);
    expect(errorSpy).toHaveBeenCalledTimes(1);
    expect(errorSpy).toHaveBeenCalledWith(fetchError);

    beacon.stop();
  });

  it('should emit an error event on non-ok HTTP response', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: false,
      status: 500,
      statusText: 'Internal Server Error'
    });

    const beacon = new TemporalSyncBeacon(MOCK_BEACON_URL, SYNC_INTERVAL);
    const errorSpy = jest.fn();
    beacon.on('error', errorSpy);

    await beacon.start();
    await Promise.resolve(); // Wait for the promise from start() to resolve

    expect(mockFetch).toHaveBeenCalledTimes(1);
    expect(errorSpy).toHaveBeenCalledTimes(1);
    expect(errorSpy.mock.calls[0][0]).toBeInstanceOf(Error);
    expect(errorSpy.mock.calls[0][0].message).toContain('HTTP error! status: 500');

    beacon.stop();
  });

  it('should stop synchronization when stop() is called', async () => {
    const mockBeaconTimestamp = 1678886400000;
    const mockLocalTimestamp = 1678886400050;

    mockFetch.mockResolvedValue({ ok: true, json: async () => ({ timestamp: mockBeaconTimestamp }) });
    mockDateNow.mockReturnValue(mockLocalTimestamp);

    const beacon = new TemporalSyncBeacon(MOCK_BEACON_URL, SYNC_INTERVAL);
    const syncedSpy = jest.fn();
    beacon.on('synced', syncedSpy);

    await beacon.start();
    await Promise.resolve(); // Wait for initial sync

    expect(mockFetch).toHaveBeenCalledTimes(1);
    expect(syncedSpy).toHaveBeenCalledTimes(1);

    beacon.stop();

    jest.advanceTimersByTime(SYNC_INTERVAL);
    await Promise.resolve(); // Wait for potential next sync

    expect(mockFetch).toHaveBeenCalledTimes(1); // Should not have been called again
    expect(syncedSpy).toHaveBeenCalledTimes(1); // Should not have been called again
  });

  it('should return the current offset', async () => {
    const mockBeaconTimestamp = 1678886400000;
    const mockLocalTimestamp = 1678886400050;
    const expectedOffset = mockBeaconTimestamp - mockLocalTimestamp;

    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ timestamp: mockBeaconTimestamp })
    });
    mockDateNow.mockReturnValue(mockLocalTimestamp);

    const beacon = new TemporalSyncBeacon(MOCK_BEACON_URL, SYNC_INTERVAL);
    await beacon.start();
    await Promise.resolve(); // Wait for initial sync

    expect(beacon.getOffset()).toBe(expectedOffset);

    beacon.stop();
  });

  it('should reset offset to 0 on error', async () => {
    const mockBeaconTimestamp = 1678886400000;
    const mockLocalTimestamp = 1678886400050;
    const expectedOffset = mockBeaconTimestamp - mockLocalTimestamp;

    // First sync succeeds
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ timestamp: mockBeaconTimestamp })
    });
    mockDateNow.mockReturnValue(mockLocalTimestamp);

    const beacon = new TemporalSyncBeacon(MOCK_BEACON_URL, SYNC_INTERVAL);
    await beacon.start();
    await Promise.resolve();
    expect(beacon.getOffset()).toBe(expectedOffset);

    // Second sync fails
    const fetchError = new Error('Network error');
    mockFetch.mockRejectedValueOnce(fetchError);
    jest.advanceTimersByTime(SYNC_INTERVAL);
    await Promise.resolve();

    expect(beacon.getOffset()).toBe(0); // Offset should be reset

    beacon.stop();
  });
});
