const cosmicRelay = require('../src/index.js');

// Mocking setTimeout to control delays and test asynchronous behavior
let mockTimeoutCallback = null;
let mockTimeoutDelay = 0;

global.setTimeout = (callback, delay) => {
  mockTimeoutCallback = callback;
  mockTimeoutDelay = delay;
  // We don't actually execute the timeout here, it will be triggered manually in tests
  return 123; // Mock timer ID
};

// Mocking Math.random to control random outcomes
let mockRandomValues = [];
let mockRandomIndex = 0;

const originalMathRandom = Math.random;

const mockMathRandom = () => {
  if (mockRandomIndex < mockRandomValues.length) {
    return mockRandomValues[mockRandomIndex++];
  }
  return originalMathRandom(); // Fallback to real random if mocks run out
};

describe('Cosmic Comm Relay', () => {

  beforeEach(() => {
    // Reset mocks before each test
    mockTimeoutCallback = null;
    mockTimeoutDelay = 0;
    mockRandomValues = [];
    mockRandomIndex = 0;
    Math.random = mockMathRandom;
  });

  afterEach(() => {
    // Restore original Math.random after all tests
    Math.random = originalMathRandom;
  });

  describe('send', () => {
    it('should resolve with a message after a simulated delay', async () => {
      const message = "Hello, Earth!";
      const options = { delayRange: [100, 200], corruptionChance: 0 };

      // Mock Math.random to ensure a specific delay is chosen (e.g., 150ms)
      // Math.random() * (max - min + 1) + min
      // For 150ms, if min=100, max=200, we need a value that results in 150.
      // (150 - 100) / (200 - 100 + 1) = 50 / 101 ≈ 0.495
      mockRandomValues = [0.495]; // This will result in a delay of 150ms

      const sendPromise = cosmicRelay.send(message, options);

      // Manually trigger the setTimeout callback
      expect(mockTimeoutCallback).not.toBeNull();
      expect(mockTimeoutDelay).toBe(150);
      mockTimeoutCallback();

      const receivedMessage = await sendPromise;
      expect(receivedMessage).toBe(message);
    });

    it('should not corrupt the message if corruptionChance is 0', async () => {
      const message = "No corruption here.";
      const options = { corruptionChance: 0 };

      const sendPromise = cosmicRelay.send(message, options);

      // Trigger the timeout
      expect(mockTimeoutCallback).not.toBeNull();
      mockTimeoutCallback();

      const receivedMessage = await sendPromise;
      expect(receivedMessage).toBe(message);
    });

    it('should corrupt the message if corruptionChance is 1 and a corruption occurs', async () => {
      const message = "This is a test message.";
      const options = { corruptionChance: 1 };

      // Mock Math.random to force corruption (e.g., substitution)
      // First random for corruption type (0 for substitution)
      // Second random for index (e.g., 0)
      // Third random for character code (e.g., '!' which is ASCII 33)
      mockRandomValues = [0, 0, 0.01]; // 0.01 is arbitrary for char code, will result in '!'

      const sendPromise = cosmicRelay.send(message, options);

      // Trigger the timeout
      expect(mockTimeoutCallback).not.toBeNull();
      mockTimeoutCallback();

      const receivedMessage = await sendPromise;
      // The exact corrupted message depends on the mocked random values for char code and index.
      // We expect it to be different from the original.
      expect(receivedMessage).not.toBe(message);
      expect(receivedMessage.length).toBe(message.length);
    });

    it('should handle message deletion corruption', async () => {
      const message = "Delete me!";
      const options = { corruptionChance: 1 };

      // Mock Math.random for deletion
      // 1 for deletion type
      // 0 for index to delete
      mockRandomValues = [1, 0];

      const sendPromise = cosmicRelay.send(message, options);

      // Trigger the timeout
      expect(mockTimeoutCallback).not.toBeNull();
      mockTimeoutCallback();

      const receivedMessage = await sendPromise;
      expect(receivedMessage).not.toBe(message);
      expect(receivedMessage.length).toBe(message.length - 1);
      expect(receivedMessage).toBe("Delete me");
    });

    it('should handle message insertion corruption', async () => {
      const message = "Insert here.";
      const options = { corruptionChance: 1 };

      // Mock Math.random for insertion
      // 2 for insertion type
      // 0 for index to insert at
      // arbitrary value for character code (e.g., 'X' which is ASCII 88)
      mockRandomValues = [2, 0, 0.8]; // 0.8 will result in 'X'

      const sendPromise = cosmicRelay.send(message, options);

      // Trigger the timeout
      expect(mockTimeoutCallback).not.toBeNull();
      mockTimeoutCallback();

      const receivedMessage = await sendPromise;
      expect(receivedMessage).not.toBe(message);
      expect(receivedMessage.length).toBe(message.length + 1);
      expect(receivedMessage).toBe("XInsert here.");
    });

    it('should use default options if none are provided', async () => {
      const message = "Default test.";

      // Mock Math.random to ensure a specific delay within default range (e.g., 1000ms)
      // Default range: [100, 2000]
      // (1000 - 100) / (2000 - 100 + 1) = 900 / 1901 ≈ 0.473
      mockRandomValues = [0.473]; // This will result in a delay of 1000ms

      const sendPromise = cosmicRelay.send(message);

      // Trigger the timeout
      expect(mockTimeoutCallback).not.toBeNull();
      expect(mockTimeoutDelay).toBe(1000);
      mockTimeoutCallback();

      const receivedMessage = await sendPromise;
      expect(receivedMessage).toBe(message);
    });
  });
});
