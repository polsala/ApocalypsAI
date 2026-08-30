const { CosmicCommRelay } = require('../src/index.js');

// Mock setTimeout to control delays and make tests deterministic
let mockTimeoutCallback = null;
let mockTimeoutDelay = 0;

const originalSetTimeout = global.setTimeout;
global.setTimeout = (callback, delay) => {
  mockTimeoutCallback = callback;
  mockTimeoutDelay = delay;
  return 123; // Mock timer ID
};

// Mock Math.random to control random outcomes
let mockRandomValues = [];
let mockRandomIndex = 0;

const originalMathRandom = Math.random;
Math.random = () => {
  if (mockRandomIndex >= mockRandomValues.length) {
    // Fallback to original if we run out of mock values, or throw error
    // For deterministic tests, we expect all values to be provided.
    throw new Error("Not enough mock random values provided.");
  }
  return mockRandomValues[mockRandomIndex++];
};

// Helper to reset mocks between tests
function resetMocks() {
  mockTimeoutCallback = null;
  mockTimeoutDelay = 0;
  mockRandomValues = [];
  mockRandomIndex = 0;
}

describe('CosmicCommRelay', () => {
  beforeEach(() => {
    resetMocks();
  });

  afterAll(() => {
    // Restore original functions after all tests
    global.setTimeout = originalSetTimeout;
    Math.random = originalMathRandom;
  });

  test('should instantiate with default options', () => {
    const relay = new CosmicCommRelay();
    expect(relay.baseDelayMs).toBe(500);
    expect(relay.delayVariance).toBe(200);
    expect(relay.corruptionChance).toBe(0.1);
  });

  test('should instantiate with custom options', () => {
    const options = { baseDelayMs: 100, delayVariance: 50, corruptionChance: 0.5 };
    const relay = new CosmicCommRelay(options);
    expect(relay.baseDelayMs).toBe(100);
    expect(relay.delayVariance).toBe(50);
    expect(relay.corruptionChance).toBe(0.5);
  });

  test('should send message with no corruption and expected delay', async () => {
    // Mock rationale: Ensure deterministic delay and no corruption.
    mockRandomValues = [0.0, 0.0]; // Ensure Math.random() always returns 0.0 for delay calculation and corruption check
    const relay = new CosmicCommRelay({ baseDelayMs: 100, delayVariance: 0 });
    const message = "Hello, Earth!";

    const sendPromise = relay.send(message);

    // Trigger the setTimeout callback
    expect(mockTimeoutCallback).not.toBeNull();
    expect(mockTimeoutDelay).toBe(100);
    mockTimeoutCallback(); // Simulate delay completion

    const receivedMessage = await sendPromise;
    expect(receivedMessage).toBe(message);
    expect(mockRandomIndex).toBe(2); // Used one for delay, one for corruption check
  });

  test('should send message with corruption', async () => {
    // Mock rationale: Simulate a 50% chance of corruption for each character.
    // First random value (0.5) for delay variance (adds 100ms to base 500ms = 600ms total delay)
    // Subsequent random values (0.6, 0.4, 0.7) for corruption checks.
    // 0.6 > 0.5 (corrupt), 0.4 < 0.5 (no corrupt), 0.7 > 0.5 (corrupt)
    mockRandomValues = [0.5, 0.6, 0.4, 0.7];
    const relay = new CosmicCommRelay({ baseDelayMs: 500, delayVariance: 100, corruptionChance: 0.5 });
    const message = "Test";

    const sendPromise = relay.send(message);

    // Trigger the setTimeout callback
    expect(mockTimeoutCallback).not.toBeNull();
    expect(mockTimeoutDelay).toBe(600);
    mockTimeoutCallback(); // Simulate delay completion

    const receivedMessage = await sendPromise;

    // Expected corrupted message: 'T' corrupted, 'e' not, 's' corrupted.
    // The corrupted characters will be random ASCII characters.
    // We can't predict the exact corrupted characters, but we can check length and that it's not the original.
    expect(receivedMessage.length).toBe(message.length);
    expect(receivedMessage).not.toBe(message);
    expect(mockRandomIndex).toBe(4); // Used one for delay, three for corruption checks
  });

  test('should handle empty message', async () => {
    // Mock rationale: Ensure empty messages are handled gracefully.
    mockRandomValues = [0.0]; // For delay
    const relay = new CosmicCommRelay({ baseDelayMs: 10 });
    const message = "";

    const sendPromise = relay.send(message);
    expect(mockTimeoutCallback).not.toBeNull();
    mockTimeoutCallback();

    const receivedMessage = await sendPromise;
    expect(receivedMessage).toBe("");
    expect(mockRandomIndex).toBe(1);
  });

  test('should handle high corruption chance', async () => {
    // Mock rationale: Ensure all characters are corrupted.
    mockRandomValues = [0.0, 1.0, 1.0, 1.0]; // 1.0 for corruption chance means always corrupt
    const relay = new CosmicCommRelay({ baseDelayMs: 10, corruptionChance: 1.0 });
    const message = "ABC";

    const sendPromise = relay.send(message);
    expect(mockTimeoutCallback).not.toBeNull();
    mockTimeoutCallback();

    const receivedMessage = await sendPromise;
    expect(receivedMessage.length).toBe(message.length);
    expect(receivedMessage).not.toBe(message);
    expect(mockRandomIndex).toBe(4);
  });
});
