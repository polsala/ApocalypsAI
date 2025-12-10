import { TemporalSyncBeacon } from '../src/main';
import axios from 'axios';

// Mock axios to control network responses
jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

// Mock the setInterval and clearInterval to control timers
jest.useFakeTimers();

describe('TemporalSyncBeacon', () => {
  const mockBeaconUrl = 'http://mock-beacon.com/time';
  const mockInterval = 1000; // 1 second for faster testing

  beforeEach(() => {
    // Clear all mocks and timers before each test
    mockedAxios.get.mockClear();
    jest.clearAllTimers();
  });

  it('should throw an error if beacon URL is not provided', () => {
    expect(() => new TemporalSyncBeacon('')).toThrow('Beacon URL is required.');
  });

  it('should initialize with default interval if not provided', () => {
    const beacon = new TemporalSyncBeacon(mockBeaconUrl);
    // Accessing private property for test, not ideal but works for this case
    // @ts-ignore
    expect(beacon.intervalSeconds).toBe(300);
  });

  it('should start and perform an initial sync', async () => {
    const mockTimestamp = Date.now();
    mockedAxios.get.mockResolvedValue({
      data: { timestamp: mockTimestamp },
      status: 200,
      statusText: 'OK',
      headers: {},
      config: {},
    });

    const beacon = new TemporalSyncBeacon(mockBeaconUrl, mockInterval);
    const syncSpy = jest.spyOn(beacon as any, 'syncTime');

    await beacon.start();

    expect(mockedAxios.get).toHaveBeenCalledTimes(1);
    expect(mockedAxios.get).toHaveBeenCalledWith(mockBeaconUrl);
    expect(syncSpy).toHaveBeenCalledTimes(1);
  });

  it('should emit a "synced" event with the correct time', (done) => {
    const mockTimestamp = Date.now();
    mockedAxios.get.mockResolvedValue({
      data: { timestamp: mockTimestamp },
      status: 200,
      statusText: 'OK',
      headers: {},
      config: {},
    });

    const beacon = new TemporalSyncBeacon(mockBeaconUrl, mockInterval);

    beacon.on('synced', (syncedTime: Date) => {
      expect(syncedTime.getTime()).toBe(mockTimestamp);
      done(); // Signal that the test is complete
    });

    beacon.start().catch(done.fail);
  });

  it('should emit an "error" event on failed sync', async () => {
    const errorMessage = 'Network Error';
    mockedAxios.get.mockRejectedValue(new Error(errorMessage));

    const beacon = new TemporalSyncBeacon(mockBeaconUrl, mockInterval);
    const errorSpy = jest.spyOn(beacon, 'emit');

    await beacon.start();

    // Wait for the interval to potentially trigger (though start() already called syncTime)
    // If the initial sync fails, the error should be emitted.
    expect(errorSpy).toHaveBeenCalledWith('error', expect.any(Error));
    expect(errorSpy).toHaveBeenCalledWith('error', expect.objectContaining({ message: expect.stringContaining('Failed to sync time') }));
  });

  it('should resynchronize at the specified interval', async () => {
    const mockTimestamp1 = Date.now();
    const mockTimestamp2 = Date.now() + 5000;

    mockedAxios.get
      .mockResolvedValueOnce({ data: { timestamp: mockTimestamp1 }, status: 200, statusText: 'OK', headers: {}, config: {} })
      .mockResolvedValueOnce({ data: { timestamp: mockTimestamp2 }, status: 200, statusText: 'OK', headers: {}, config: {} });

    const beacon = new TemporalSyncBeacon(mockBeaconUrl, mockInterval);
    const syncSpy = jest.spyOn(beacon as any, 'syncTime');

    await beacon.start();

    // Advance timers by the interval to trigger the next sync
    jest.advanceTimersByTime(mockInterval);

    // syncTime should have been called twice: once on start, once after interval
    expect(syncSpy).toHaveBeenCalledTimes(2);
    expect(mockedAxios.get).toHaveBeenCalledTimes(2);
  });

  it('should stop the synchronization timer', () => {
    const beacon = new TemporalSyncBeacon(mockBeaconUrl, mockInterval);
    const syncSpy = jest.spyOn(beacon as any, 'syncTime');

    beacon.start();
    beacon.stop();

    jest.advanceTimersByTime(mockInterval);

    expect(syncSpy).toHaveBeenCalledTimes(1); // Only the initial sync should have happened
  });

  it('should handle invalid timestamp format from beacon', async () => {
    mockedAxios.get.mockResolvedValue({
      data: { time: 'not a number' }, // Incorrect format
      status: 200,
      statusText: 'OK',
      headers: {},
      config: {},
    });

    const beacon = new TemporalSyncBeacon(mockBeaconUrl, mockInterval);
    const errorSpy = jest.spyOn(beacon, 'emit');

    await beacon.start();

    expect(errorSpy).toHaveBeenCalledWith('error', expect.any(Error));
    expect(errorSpy).toHaveBeenCalledWith('error', expect.objectContaining({ message: expect.stringContaining('Invalid timestamp format') }));
  });

  it('should handle non-200 status codes from beacon', async () => {
    mockedAxios.get.mockResolvedValue({
      data: 'Internal Server Error',
      status: 500,
      statusText: 'Internal Server Error',
      headers: {},
      config: {},
    });

    const beacon = new TemporalSyncBeacon(mockBeaconUrl, mockInterval);
    const errorSpy = jest.spyOn(beacon, 'emit');

    await beacon.start();

    expect(errorSpy).toHaveBeenCalledWith('error', expect.any(Error));
    expect(errorSpy).toHaveBeenCalledWith('error', expect.objectContaining({ message: expect.stringContaining('500 - Internal Server Error') }));
  });
});
