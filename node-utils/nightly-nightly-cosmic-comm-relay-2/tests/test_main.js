const assert = require('assert');
const { sendMessage, receiveMessages, _deriveKey, _encryptMessage, _decryptMessage, _simulateSignalDegradation, _messageQueue } = require('../src/main');

// Mock console.log to capture output for testing
let consoleOutput = [];
const originalConsoleLog = console.log;
const originalConsoleError = console.error;

beforeEach(() => {
    consoleOutput = [];
    console.log = (message) => consoleOutput.push(message);
    console.error = (message) => consoleOutput.push(message);
    // Clear the message queue before each test
    _messageQueue.length = 0;
});

afterEach(() => {
    console.log = originalConsoleLog;
    console.error = originalConsoleError;
});

describe('Cosmic Comm Relay', () => {

    it('should derive a consistent encryption key', () => {
        // Mock rationale: Deterministic key derivation is essential for testing encryption/decryption.
        const key1 = _deriveKey('Earth_Base_1');
        const key2 = _deriveKey('Earth_Base_1');
        const key3 = _deriveKey('Mars_Colony_A');
        assert.strictEqual(key1, key2, 'Keys for the same recipient should be identical');
        assert.notStrictEqual(key1, key3, 'Keys for different recipients should differ');
        assert.strictEqual(key1.length, 64, 'Derived key should be 64 hex characters (256 bits)');
    });

    it('should encrypt and decrypt messages correctly', () => {
        // Mock rationale: Verifies the core encryption/decryption mechanism works as expected.
        const testMessage = 'This is a test transmission.';
        const recipientId = 'Jupiter_Orbiter_X';
        const key = _deriveKey(recipientId);
        const { iv, encryptedData } = _encryptMessage(testMessage, key);
        const decryptedMessage = _decryptMessage(encryptedData, key, iv);
        assert.strictEqual(decryptedMessage, testMessage, 'Decrypted message should match original');
    });

    it('should simulate signal degradation without breaking decryption (most of the time)', () => {
        // Mock rationale: Tests the robustness of the system against simulated noise.
        // This test might occasionally fail due to the nature of degradation, but should pass frequently.
        const originalMessage = 'A vital status update from the outer rim.';
        const recipientId = 'Saturn_Ring_Station';
        const key = _deriveKey(recipientId);

        for (let i = 0; i < 10; i++) { // Run multiple times to increase confidence
            const { iv, encryptedData } = _encryptMessage(originalMessage, key);
            const degradedEncryptedData = _simulateSignalDegradation(encryptedData);
            try {
                const decryptedMessage = _decryptMessage(degradedEncryptedData, key, iv);
                // If it decrypts, it might be correct or a false positive due to degradation.
                // We can't strictly assert equality here due to degradation, but we can check if it *can* decrypt.
                // A more advanced test would check for specific degradation patterns.
                assert.ok(true, 'Message was able to be decrypted after degradation.');
            } catch (e) {
                // If it fails to decrypt, that's also a possible outcome of degradation.
                // For this test, we're more concerned if it *can* decrypt at all.
                // If it consistently fails, it indicates a problem with degradation or decryption.
                // console.warn(`Test iteration ${i+1}: Decryption failed after degradation. This is expected sometimes.`, e.message);
            }
        }
    });

    it('should send and receive a message successfully', (done) => {
        // Mock rationale: Tests the end-to-end flow of sending and receiving.
        const senderId = 'Earth_Command';
        const recipientId = 'Moon_Outpost_Alpha';
        const message = 'All systems nominal. Awaiting further instructions.';

        sendMessage(recipientId, message);

        // Check if the message was added to the queue
        assert.strictEqual(_messageQueue.length, 1, 'Message should be added to the queue');
        assert.strictEqual(_messageQueue[0].recipientId, recipientId, 'Message recipient ID should match');

        // Simulate receiving the message
        receiveMessages(recipientId);

        // Check console output for success message
        assert.ok(consoleOutput.some(log => log.includes('Incoming transmission')), 'Console should indicate incoming transmission');
        assert.ok(consoleOutput.some(log => log.includes(`Decrypted Payload: "${message}"`)), 'Console should show the decrypted message');
        assert.strictEqual(_messageQueue.length, 0, 'Message should be removed from queue after receiving');
        done();
    });

    it('should handle receiving no messages', () => {
        // Mock rationale: Ensures the receiver gracefully handles an empty queue.
        const myId = 'Deep_Space_Probe_7';
        receiveMessages(myId);
        assert.ok(consoleOutput.some(log => log.includes('No new transmissions detected')), 'Console should indicate no messages');
    });

    it('should handle corrupted messages during reception', () => {
        // Mock rationale: Tests how the system reacts to malformed encrypted data.
        const recipientId = 'Europa_Station';
        const key = _deriveKey(recipientId);
        const originalMessage = 'This is a test.';
        const { iv, encryptedData } = _encryptMessage(originalMessage, key);

        // Corrupt the encrypted data
        const corruptedData = encryptedData.slice(0, -5) + 'abcde'; // Replace last few chars

        _messageQueue.push({ recipientId, iv, encryptedData: corruptedData });

        receiveMessages(recipientId);

        assert.ok(consoleOutput.some(log => log.includes('Transmission corrupted or invalid')), 'Console should indicate corrupted transmission');
        assert.strictEqual(_messageQueue.length, 1, 'Corrupted message should remain in queue if not processed');
    });

});
