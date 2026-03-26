const assert = require('assert');
const CosmicRelay = require('../src/main'); // Assuming main.js is in ../src/

// Mocking setTimeout and Math.random for deterministic tests
let mockDelay = (ms) => Promise.resolve();
let mockRandomValue = 0.5; // Default to a value that won't trigger anomaly

// Mock the global setTimeout
const originalSetTimeout = global.setTimeout;
global.setTimeout = (callback, ms) => {
    // Mock rationale: This mock ensures that delay() calls resolve immediately
    // or with a controlled delay, making tests deterministic and preventing
    // them from waiting for actual time to pass.
    if (ms === 1000) { // Specific delay for retries
        return originalSetTimeout(callback, 10); // Short delay for retry simulation
    }
    return originalSetTimeout(callback, 10); // Short delay for other delays
};

// Mock the global Math.random
const originalMathRandom = global.Math.random;
global.Math.random = () => mockRandomValue;

describe('CosmicRelay', () => {
    let relay;

    beforeEach(() => {
        relay = new CosmicRelay();
        // Reset mocks before each test
        mockDelay = (ms) => Promise.resolve();
        mockRandomValue = 0.5;
        relay.isRelayActive = true; // Ensure relay is active for tests
        relay.MAX_RETRIES = 2; // Lower retries for faster tests
        relay.ANOMALY_CHANCE = 0.1; // Lower anomaly chance for easier control
    });

    afterEach(() => {
        // Clean up mocks after each test
        global.setTimeout = originalSetTimeout;
        global.Math.random = originalMathRandom;
        clearInterval(relay.relayInterval);
    });

    it('should start the relay and emit relayStarted event', (done) => {
        relay.once('relayStarted', () => {
            assert.strictEqual(relay.isRelayActive, true, 'Relay should be active');
            done();
        });
        relay.startRelay();
    });

    it('should stop the relay and emit relayStopped event', (done) => {
        relay.startRelay();
        relay.once('relayStopped', () => {
            assert.strictEqual(relay.isRelayActive, false, 'Relay should be inactive');
            done();
        });
        relay.stopRelay();
    });

    it('should successfully send a message without anomalies', async () => {
        mockRandomValue = 0.05; // Ensure anomaly doesn't trigger
        let messageSent = false;
        relay.on('messageSent', () => {
            messageSent = true;
        });

        await relay.sendMessage('Hello, universe!');
        assert.strictEqual(messageSent, true, 'messageSent event should be emitted');
    });

    it('should handle transmission failures after multiple retries', async () => {
        mockRandomValue = 0.9; // High chance to trigger anomaly
        relay.MAX_RETRIES = 2;
        let transmissionFailed = false;
        relay.on('transmissionFailed', () => {
            transmissionFailed = true;
        });

        await relay.sendMessage('Urgent distress signal!');
        assert.strictEqual(transmissionFailed, true, 'transmissionFailed event should be emitted');
    });

    it('should queue messages for reception', () => {
        const testMessage = { message: 'Incoming transmission', time: new Date().toISOString() };
        relay.messageQueue.push(testMessage);
        assert.strictEqual(relay.messageQueue.length, 1, 'Message should be added to queue');
    });

    it('should receive a message from the queue', (done) => {
        const testMessage = { message: 'Incoming transmission', time: new Date().toISOString() };
        relay.messageQueue.push(testMessage);

        relay.once('messageReceived', (receivedMsg) => {
            assert.deepStrictEqual(receivedMsg, testMessage, 'Received message should match queued message');
            assert.strictEqual(relay.messageQueue.length, 0, 'Message should be removed from queue');
            done();
        });
        relay.receiveMessage();
    });

    it('should emit an error if trying to send when relay is offline', (done) => {
        relay.stopRelay();
        relay.once('error', (err) => {
            assert.strictEqual(err, 'Relay is offline. Cannot send message.', 'Error message should be correct');
            done();
        });
        relay.sendMessage('Offline test');
    });
});
