const { sendCosmicMessage } = require('../src/index');

// Mock setTimeout to control delays and test timing
jest.useFakeTimers();

// Mock Math.random to control corruption outcomes
let mockRandom = jest.fn();
global.Math.random = mockRandom;

describe('Cosmic Communication Relay', () => {

    beforeEach(() => {
        // Reset mocks before each test
        jest.clearAllTimers();
        mockRandom.mockClear();
    });

    test('should send a message with default options', async () => {
        const message = "Hello, void!";
        // Mock random to ensure no corruption occurs
        mockRandom.mockReturnValue(0.01); // Probability of corruption is 0.05, so 0.01 should not trigger

        const promise = sendCosmicMessage(message);

        // Advance timers by default delay + jitter
        jest.advanceTimersByTime(100 + 500); // Max possible delay

        const receivedMessage = await promise;
        expect(receivedMessage).toBe(message);
    });

    test('should apply substitution corruption when probability is met', async () => {
        const message = "Test message";
        // Mock random to trigger corruption
        mockRandom.mockReturnValueOnce(0.06); // Triggers corruption (default prob 0.05)
        mockRandom.mockReturnValueOnce(0.5);  // For choosing index to substitute
        mockRandom.mockReturnValueOnce(0.1);  // For choosing replacement character

        const promise = sendCosmicMessage(message, {
            corruptionProbability: 0.05,
            corruptionType: 'substitute'
        });

        jest.advanceTimersByTime(100 + 500);
        const receivedMessage = await promise;

        // The exact corrupted message depends on the random choices, but it should not be the original.
        // We can't assert the exact string without more complex mockRandom control, but we can assert it's different.
        expect(receivedMessage).not.toBe(message);
        expect(receivedMessage.length).toBe(message.length);
    });

    test('should apply deletion corruption when probability is met', async () => {
        const message = "Delete me";
        // Mock random to trigger corruption
        mockRandom.mockReturnValueOnce(0.06); // Triggers corruption
        mockRandom.mockReturnValueOnce(0.3);  // For choosing index to delete

        const promise = sendCosmicMessage(message, {
            corruptionProbability: 0.05,
            corruptionType: 'delete'
        });

        jest.advanceTimersByTime(100 + 500);
        const receivedMessage = await promise;

        expect(receivedMessage).not.toBe(message);
        expect(receivedMessage.length).toBe(message.length - 1);
    });

    test('should apply insertion corruption when probability is met', async () => {
        const message = "Insert";
        // Mock random to trigger corruption
        mockRandom.mockReturnValueOnce(0.06); // Triggers corruption
        mockRandom.mockReturnValueOnce(0.5);  // For choosing index to insert
        mockRandom.mockReturnValueOnce(0.2);  // For choosing inserted character

        const promise = sendCosmicMessage(message, {
            corruptionProbability: 0.05,
            corruptionType: 'insert'
        });

        jest.advanceTimersByTime(100 + 500);
        const receivedMessage = await promise;

        expect(receivedMessage).not.toBe(message);
        expect(receivedMessage.length).toBe(message.length + 1);
    });

    test('should not corrupt if random value is above probability', async () => {
        const message = "Safe message";
        // Mock random to ensure no corruption occurs
        mockRandom.mockReturnValue(0.99); // Probability of corruption is 0.05, so 0.99 should not trigger

        const promise = sendCosmicMessage(message, {
            corruptionProbability: 0.05,
            corruptionType: 'substitute'
        });

        jest.advanceTimersByTime(100 + 500);
        const receivedMessage = await promise;
        expect(receivedMessage).toBe(message);
    });

    test('should handle empty message gracefully', async () => {
        const message = "";
        mockRandom.mockReturnValue(0.06); // Trigger corruption

        const promise = sendCosmicMessage(message, {
            corruptionProbability: 0.05,
            corruptionType: 'substitute'
        });
        jest.advanceTimersByTime(100 + 500);
        const receivedMessage = await promise;
        expect(receivedMessage).toBe(""); // Empty message remains empty
    });

    test('should use custom delay', async () => {
        const message = "Delayed message";
        const customDelay = 1500;
        mockRandom.mockReturnValue(0.01); // No corruption

        const promise = sendCosmicMessage(message, {
            delay: customDelay,
            corruptionProbability: 0.05
        });

        // Advance timers by custom delay + jitter
        jest.advanceTimersByTime(customDelay + 500);

        const receivedMessage = await promise;
        expect(receivedMessage).toBe(message);
    });

    test('should handle unknown corruption type by not corrupting', async () => {
        const message = "Unknown type";
        mockRandom.mockReturnValue(0.06); // Trigger corruption attempt

        const promise = sendCosmicMessage(message, {
            corruptionProbability: 0.05,
            corruptionType: 'unknown'
        });

        jest.advanceTimersByTime(100 + 500);
        const receivedMessage = await promise;
        expect(receivedMessage).toBe(message);
    });
});
