const { CosmicCommRelay } = require('../src/main.js');

// Mock setTimeout to control time for tests
let realSetTimeout;
let fakeTimers = {};
let timerIdCounter = 1;

beforeAll(() => {
  realSetTimeout = global.setTimeout;
  global.setTimeout = (callback, delay, ...args) => {
    const id = timerIdCounter++;
    fakeTimers[id] = { callback, delay, args };
    return id;
  };
  global.clearTimeout = (id) => {
    delete fakeTimers[id];
  };
});

afterAll(() => {
  global.setTimeout = realSetTimeout;
  global.clearTimeout = realSetTimeout;
});

// Helper to advance timers
const advanceTimersByTime = (ms) => {
  const startTime = Date.now();
  const endTime = startTime + ms;
  let executedTimers = [];

  while (Date.now() < endTime) {
    let earliestTimerId = null;
    let earliestDelay = Infinity;

    for (const id in fakeTimers) {
      if (fakeTimers[id].delay < earliestDelay) {
        earliestDelay = fakeTimers[id].delay;
        earliestTimerId = id;
      }
    }

    if (earliestTimerId === null) break; // No timers left

    const timer = fakeTimers[earliestTimerId];
    const timeToAdvance = Math.min(timer.delay, ms - (Date.now() - startTime));

    // Simulate advancing time
    for (const id in fakeTimers) {
      fakeTimers[id].delay -= timeToAdvance;
    }

    if (fakeTimers[earliestTimerId].delay <= 0) {
      const { callback, args } = fakeTimers[earliestTimerId];
      delete fakeTimers[earliestTimerId];
      executedTimers.push({ callback, args });
    }
  }
  executedTimers.forEach(({ callback, args }) => callback(...args));
};

describe('CosmicCommRelay', () => {
  // Mock rationale: We are mocking setTimeout and clearTimeout to control the passage of time
  // in our tests, allowing us to deterministically test the delay behavior of the relay.

  test('should send a message with a delay', async () => {
    const relay = new CosmicCommRelay({ distance: 10 });
    const message = 'Test message';
    let receivedMessage = null;

    relay.sendMessage(message).then(msg => {
      receivedMessage = msg;
    });

    // Advance timers by a duration slightly longer than the expected minimum delay
    // (distance * baseDelayPerUnit = 10 * 50 = 500ms)
    advanceTimersByTime(600);

    expect(receivedMessage).toBe(message);
  });

  test('should introduce static noise to the message', async () => {
    const relay = new CosmicCommRelay({ distance: 5 });
    const message = 'Another test';
    let receivedMessage = null;

    // We need to mock Math.random to ensure static is introduced for this test
    // Mock rationale: Mocking Math.random to force the static condition for deterministic testing.
    const originalMathRandom = Math.random;
    Math.random = jest.fn()
      .mockReturnValueOnce(0.5) // For delay fluctuation
      .mockReturnValueOnce(0.4) // For static chance (30% threshold)
      .mockReturnValueOnce(0.1); // For signal degradation chance

    relay.sendMessage(message).then(msg => {
      receivedMessage = msg;
    });

    advanceTimersByTime(300); // 5 * 50 = 250ms base delay

    expect(receivedMessage).not.toBeNull();
    expect(receivedMessage).toContain('...crackle...'); // Or any other static string
    expect(receivedMessage).not.toBe(message);

    Math.random = originalMathRandom; // Restore original Math.random
  });

  test('should handle different distances for delay', async () => {
    const shortDistanceRelay = new CosmicCommRelay({ distance: 2 });
    const longDistanceRelay = new CosmicCommRelay({ distance: 20 });
    const message = 'Distance check';

    let shortReceived = null;
    let longReceived = null;

    shortDistanceRelay.sendMessage(message).then(msg => shortReceived = msg);
    longDistanceRelay.sendMessage(message).then(msg => longReceived = msg);

    // Advance timers to cover the longer delay (20 * 50 = 1000ms)
    advanceTimersByTime(1100);

    expect(shortReceived).toBe(message);
    expect(longReceived).toBe(message);
  });

  test('should not introduce static if random chance is low', async () => {
    const relay = new CosmicCommRelay({ distance: 1 });
    const message = 'No static please';
    let receivedMessage = null;

    // Mock rationale: Mocking Math.random to ensure static is NOT introduced for deterministic testing.
    const originalMathRandom = Math.random;
    Math.random = jest.fn()
      .mockReturnValueOnce(0.1) // For delay fluctuation
      .mockReturnValueOnce(0.2) // For static chance (below 0.3 threshold)
      .mockReturnValueOnce(0.05); // For signal degradation chance

    relay.sendMessage(message).then(msg => {
      receivedMessage = msg;
    });

    advanceTimersByTime(100);

    expect(receivedMessage).toBe(message);

    Math.random = originalMathRandom;
  });
});
