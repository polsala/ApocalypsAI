const assert = require('assert');
const sinon = require('sinon');
const { simulateCosmicCommunication } = require('../src/main');

describe('Cosmic Communication Relay', () => {
  let randomStub;

  beforeEach(() => {
    // Mock Math.random to ensure deterministic tests
    randomStub = sinon.stub(Math, 'random');
  });

  afterEach(() => {
    // Restore Math.random after each test
    randomStub.restore();
  });

  it('should return the original message with no delay and no corruption for zero distance', () => {
    // Mock rationale: Math.random is stubbed, so no actual random events occur.
    // We explicitly set it to return values that would result in no corruption.
    randomStub.onCall(0).returns(0.001); // For corruption chance check (0.001 < 0.005 * 0)
    randomStub.onCall(1).returns(0); // For character corruption logic (not reached)

    const message = "Hello";
    const distance = 0;
    const result = simulateCosmicCommunication(message, distance);

    assert.strictEqual(result.originalMessage, message, 'Original message mismatch');
    assert.strictEqual(result.receivedMessage, message, 'Received message should be original for zero distance');
    assert.strictEqual(result.delayMs, 0, 'Delay should be 0 for zero distance');
    assert.strictEqual(result.corrupted, false, 'Message should not be corrupted for zero distance');
  });

  it('should simulate delay for a given distance', () => {
    // Mock rationale: Math.random is stubbed, so no actual random events occur.
    randomStub.onCall(0).returns(0.001); // For corruption chance check (0.001 < 0.005 * 10)
    randomStub.onCall(1).returns(0); // For character corruption logic (not reached)

    const message = "Test";
    const distance = 10;
    const expectedDelay = 10 * 50;
    const result = simulateCosmicCommunication(message, distance);

    assert.strictEqual(result.originalMessage, message, 'Original message mismatch');
    assert.strictEqual(result.delayMs, expectedDelay, 'Delay calculation is incorrect');
    assert.strictEqual(result.corrupted, false, 'Message should not be corrupted in this specific mock scenario');
  });

  it('should simulate message corruption when corruption chance is met', () => {
    // Mock rationale: We force Math.random to return a value that triggers corruption.
    // The subsequent random calls are mocked to ensure predictable corruption.
    randomStub.onCall(0).returns(0.01); // For corruption chance check (0.01 > 0.005 * 10)
    randomStub.onCall(1).returns(0.5); // For numCharsToCorrupt (0.5 * 5 = 2.5 -> floor = 2)
    randomStub.onCall(2).returns(0); // For randomIndex (first char)
    randomStub.onCall(3).returns(0); // For corruptionType (replace)
    randomStub.onCall(4).returns(0.1); // For randomChar (0.1 -> 'b')
    randomStub.onCall(5).returns(2); // For randomIndex (third char)
    randomStub.onCall(6).returns(1); // For corruptionType (delete)

    const message = "abcdef";
    const distance = 10;
    const result = simulateCosmicCommunication(message, distance);

    assert.strictEqual(result.originalMessage, message, 'Original message mismatch');
    assert.strictEqual(result.corrupted, true, 'Message should be corrupted');
    // Based on mocks: 'a' replaced with 'b', 'c' deleted.
    // Original: a b c d e f
    // After replace 'a' with 'b': b b c d e f
    // After delete 'c': b b d e f
    assert.strictEqual(result.receivedMessage, "bbdef", 'Received message is not as expected after corruption');
  });

  it('should handle maximum delay cap', () => {
    // Mock rationale: Math.random is stubbed, so no actual random events occur.
    randomStub.onCall(0).returns(0.001); // For corruption chance check
    randomStub.onCall(1).returns(0); // For character corruption logic (not reached)

    const message = "Short";
    const distance = 200; // Distance that would exceed the cap
    const MAX_ALLOWED_DELAY = 5000;
    const result = simulateCosmicCommunication(message, distance);

    assert.strictEqual(result.delayMs, MAX_ALLOWED_DELAY, 'Delay should be capped');
  });

  it('should handle maximum corruption chance cap', () => {
    // Mock rationale: We force Math.random to return a value that triggers corruption.
    // The subsequent random calls are mocked to ensure predictable corruption.
    randomStub.onCall(0).returns(0.6); // For corruption chance check (0.6 > 0.5 cap)
    randomStub.onCall(1).returns(0); // For numCharsToCorrupt (0.5 * 5 = 2.5 -> floor = 2)
    randomStub.onCall(2).returns(0); // For randomIndex (first char)
    randomStub.onCall(3).returns(0); // For corruptionType (replace)
    randomStub.onCall(4).returns(0.1); // For randomChar (0.1 -> 'b')
    randomStub.onCall(5).returns(1); // For randomIndex (second char)
    randomStub.onCall(6).returns(2); // For corruptionType (swap)

    const message = "abcde";
    const distance = 200; // Distance that would exceed the cap
    const result = simulateCosmicCommunication(message, distance);

    assert.strictEqual(result.corrupted, true, 'Message should be corrupted');
    // Based on mocks: 'a' replaced with 'b', 'b' and 'c' swapped.
    // Original: a b c d e
    // After replace 'a' with 'b': b b c d e
    // After swap 'b' and 'c': b c b d e
    assert.strictEqual(result.receivedMessage, "bcbde", 'Received message is not as expected after capped corruption');
  });
});
