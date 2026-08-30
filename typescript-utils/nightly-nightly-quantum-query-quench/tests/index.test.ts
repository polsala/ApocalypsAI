import { QuantumQuencher } from '../src';

describe('QuantumQuencher', () => {
  let consoleWarnSpy: jest.SpyInstance;
  let consoleErrorSpy: jest.SpyInstance;

  beforeEach(() => {
    jest.useFakeTimers();
    consoleWarnSpy = jest.spyOn(console, 'warn').mockImplementation(() => {});
    consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
  });

  afterEach(() => {
    jest.runOnlyPendingTimers();
    jest.useRealTimers();
    consoleWarnSpy.mockRestore();
    consoleErrorSpy.mockRestore();
  });

  // Mock rationale: `setTimeout` and `Date.now` are global browser/Node APIs that introduce non-determinism and real-time delays. Mocking them allows for instant, predictable testing of asynchronous logic and time-based features like delays and rate limiting without waiting for actual time to pass.

  it('should execute an operation successfully on the first attempt', async () => {
    const quencher = new QuantumQuencher();
    const mockOperation = jest.fn().mockResolvedValue('Success');

    const promise = quencher.query(mockOperation, 'Test Op');
    jest.runAllTimers(); // Advance timers for any potential internal delays (e.g., rate limit check)

    await expect(promise).resolves.toBe('Success');
    expect(mockOperation).toHaveBeenCalledTimes(1);
    expect(consoleWarnSpy).not.toHaveBeenCalled();
  });

  it('should retry a failing operation and succeed', async () => {
    const quencher = new QuantumQuencher({
      retryStrategy: { maxRetries: 2, initialDelayMs: 10, backoffFactor: 2 },
    });
    let callCount = 0;
    const mockOperation = jest.fn(() => {
      callCount++;
      if (callCount < 3) {
        throw new Error('Transient error');
      }
      return Promise.resolve('Eventual Success');
    });

    const promise = quencher.query(mockOperation, 'Flaky Op');

    // First call fails
    jest.advanceTimersByTime(0);
    // Second call fails after initial delay
    jest.advanceTimersByTime(10);
    // Third call succeeds after backoff delay
    jest.advanceTimersByTime(20);

    await expect(promise).resolves.toBe('Eventual Success');
    expect(mockOperation).toHaveBeenCalledTimes(3);
    expect(consoleWarnSpy).toHaveBeenCalledTimes(2);
    expect(consoleWarnSpy).toHaveBeenCalledWith(expect.stringContaining('Flaky Op failed (attempt 1/3)'));
    expect(consoleWarnSpy).toHaveBeenCalledWith(expect.stringContaining('Flaky Op failed (attempt 2/3)'));
  });

  it('should fail after exhausting all retries', async () => {
    const quencher = new QuantumQuencher({
      retryStrategy: { maxRetries: 2, initialDelayMs: 10, backoffFactor: 2 },
    });
    const mockOperation = jest.fn().mockRejectedValue(new Error('Persistent error'));

    const promise = quencher.query(mockOperation, 'Failing Op');

    // First call fails
    jest.advanceTimersByTime(0);
    // Second call fails after initial delay
    jest.advanceTimersByTime(10);
    // Third call fails after backoff delay
    jest.advanceTimersByTime(20);

    await expect(promise).rejects.toThrow('Failing Op failed after 3 attempts: Persistent error');
    expect(mockOperation).toHaveBeenCalledTimes(3);
    expect(consoleWarnSpy).toHaveBeenCalledTimes(3);
    expect(consoleWarnSpy).toHaveBeenCalledWith(expect.stringContaining('Failing Op failed (attempt 1/3)'));
    expect(consoleWarnSpy).toHaveBeenCalledWith(expect.stringContaining('Failing Op failed (attempt 2/3)'));
    expect(consoleWarnSpy).toHaveBeenCalledWith(expect.stringContaining('Failing Op failed (attempt 3/3)'));
  });

  it('should respect rate limits by delaying subsequent calls', async () => {
    const quencher = new QuantumQuencher({
      rateLimitStrategy: { maxRequests: 1, intervalMs: 1000 },
    });
    const mockOperation = jest.fn().mockResolvedValue('Rate Limited Success');

    jest.setSystemTime(new Date('2023-01-01T00:00:00.000Z'));

    const promise1 = quencher.query(mockOperation, 'RL Op 1');
    jest.advanceTimersByTime(0); // Execute first call immediately

    const promise2 = quencher.query(mockOperation, 'RL Op 2');
    jest.advanceTimersByTime(0); // Try to execute second call immediately

    // At this point, promise2 should be pending, waiting for rate limit
    expect(mockOperation).toHaveBeenCalledTimes(1);

    jest.advanceTimersByTime(999); // Advance almost to the end of the interval
    expect(mockOperation).toHaveBeenCalledTimes(1); // Still only one call

    jest.advanceTimersByTime(1); // Advance past the interval (total 1000ms)
    // Now the second call should execute

    await Promise.all([promise1, promise2]);

    expect(mockOperation).toHaveBeenCalledTimes(2);
    expect(await promise1).toBe('Rate Limited Success');
    expect(await promise2).toBe('Rate Limited Success');
  });

  it('should handle multiple concurrent rate-limited calls correctly', async () => {
    const quencher = new QuantumQuencher({
      rateLimitStrategy: { maxRequests: 2, intervalMs: 2000 },
    });
    const mockOperation = jest.fn().mockResolvedValue('Concurrent Success');

    jest.setSystemTime(new Date('2023-01-01T00:00:00.000Z'));

    const p1 = quencher.query(mockOperation, 'C Op 1');
    jest.advanceTimersByTime(0);
    const p2 = quencher.query(mockOperation, 'C Op 2');
    jest.advanceTimersByTime(0);
    const p3 = quencher.query(mockOperation, 'C Op 3');
    jest.advanceTimersByTime(0);

    // First two should execute immediately
    expect(mockOperation).toHaveBeenCalledTimes(2);

    // Third should be pending due to rate limit
    jest.advanceTimersByTime(1999); // Almost 2 seconds
    expect(mockOperation).toHaveBeenCalledTimes(2);

    jest.advanceTimersByTime(1); // 2 seconds passed
    // Now the third call should execute
    expect(mockOperation).toHaveBeenCalledTimes(3);

    await Promise.all([p1, p2, p3]);
    expect(await p1).toBe('Concurrent Success');
    expect(await p2).toBe('Concurrent Success');
    expect(await p3).toBe('Concurrent Success');
  });

  it('should use default strategies if none are provided', async () => {
    const quencher = new QuantumQuencher(); // Uses defaults
    const mockOperation = jest.fn().mockResolvedValue('Default Success');

    const promise = quencher.query(mockOperation, 'Default Op');
    jest.runAllTimers();

    await expect(promise).resolves.toBe('Default Success');
    expect(mockOperation).toHaveBeenCalledTimes(1);
  });

  it('should merge provided strategies with defaults', async () => {
    const quencher = new QuantumQuencher({
      retryStrategy: { maxRetries: 1 }, // Override maxRetries, keep other defaults
    });
    let callCount = 0;
    const mockOperation = jest.fn(() => {
      callCount++;
      if (callCount < 2) {
        throw new Error('Merge error');
      }
      return Promise.resolve('Merged Success');
    });

    const promise = quencher.query(mockOperation, 'Merge Op');

    jest.advanceTimersByTime(0);
    jest.advanceTimersByTime(100); // Default initialDelayMs

    await expect(promise).resolves.toBe('Merged Success');
    expect(mockOperation).toHaveBeenCalledTimes(2); // 1 initial + 1 retry = 2 attempts
    expect(consoleWarnSpy).toHaveBeenCalledTimes(1);
  });
});
