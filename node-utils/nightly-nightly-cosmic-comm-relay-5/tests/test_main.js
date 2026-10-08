const { exec } = require('child_process');
const path = require('path');

// Mock rationale: We are mocking the child_process.exec function to control its output and avoid actual command execution.
// This allows for deterministic testing of the utility's behavior based on simulated command-line arguments and expected outputs.
jest.mock('child_process');

// Mock rationale: We are mocking the 'commander' library to control argument parsing and prevent actual command execution.
// This allows us to simulate different command-line inputs and verify how the utility processes them without relying on the actual CLI parsing.
jest.mock('commander', () => ({
    program: {
        argument: jest.fn().mockReturnThis(),
        option: jest.fn().mockReturnThis(),
        action: jest.fn(),
        parse: jest.fn()
    }
}));

// Mock rationale: We are mocking setTimeout to control time-based operations and ensure tests run quickly and deterministically.
// This allows us to simulate delays and asynchronous behavior without waiting for real-time delays.
const mockSetTimeout = jest.fn(callback => callback());
global.setTimeout = mockSetTimeout;

// Mock rationale: We are mocking Math.random to control the outcome of random operations like delays and interference.
// This ensures that tests produce consistent results by providing predictable random values.
let mockRandomValues = [];
let mockRandomIndex = 0;
const originalMathRandom = Math.random;

const setMockRandomValues = (values) => {
    mockRandomValues = values;
    mockRandomIndex = 0;
    Math.random = jest.fn(() => {
        if (mockRandomIndex >= mockRandomValues.length) {
            // If we run out of mock values, fall back to original Math.random or throw an error
            // For deterministic tests, it's better to ensure enough values are provided.
            console.warn("Ran out of mock Math.random values. Falling back to original Math.random.");
            return originalMathRandom();
        }
        return mockRandomValues[mockRandomIndex++];
    });
};

const restoreMathRandom = () => {
    Math.random = originalMathRandom;
};

// Mock console.log and console.error to capture output
let consoleOutput = [];
const mockConsoleLog = jest.fn((...args) => {
    consoleOutput.push(args.join(' '));
});
const mockConsoleError = jest.fn((...args) => {
    consoleOutput.push(`ERROR: ${args.join(' ')}`);
});

// Mock commander's action to capture arguments and simulate execution
let mockActionCallback;

// Re-require the module after mocking
let mainModule;

describe('Cosmic Comm Relay', () => {

    beforeEach(() => {
        jest.clearAllMocks();
        consoleOutput = [];
        global.console.log = mockConsoleLog;
        global.console.error = mockConsoleError;

        // Mock commander's argument, option, and parse methods
        const commander = require('commander');
        commander.program.argument.mockImplementation((name, description) => commander.program);
        commander.program.option.mockImplementation((flags, description, defaultValue) => commander.program);
        commander.program.action.mockImplementation((callback) => {
            mockActionCallback = callback;
            return commander.program;
        });
        commander.program.parse.mockImplementation((argv) => {
            if (mockActionCallback) {
                // Simulate parsing and calling the action callback
                // This is a simplified simulation. In a real scenario, you'd parse argv more thoroughly.
                // For these tests, we'll directly call the callback with simulated arguments.
            }
        });

        // Load the module after mocks are set up
        jest.resetModules();
        mainModule = require('../src/main');
    });

    afterEach(() => {
        restoreMathRandom();
        global.console.log = console.log; // Restore original console.log
        global.console.error = console.error; // Restore original console.error
    });

    test('should transmit a message successfully with default options', async () => {
        setMockRandomValues([0.2, 0.1]); // Simulate delay variation and no interference
        const message = "Hello, void!";
        const expectedDelay = 1000 + (1000 * 0.2 * 0.5); // Base + variation

        // Simulate calling the action callback with parsed arguments
        await mockActionCallback(message, { delay: '1000', errorRate: '0.05' });

        expect(mockConsoleLog).toHaveBeenCalledWith(`\n🚀 Initiating transmission of: "${message}"`);
        expect(mockConsoleLog).toHaveBeenCalledWith('  - Base delay set to: 1000ms');
        expect(mockConsoleLog).toHaveBeenCalledWith('  - Cosmic interference rate: 5%');
        expect(mockSetTimeout).toHaveBeenCalledWith(expect.any(Function), expectedDelay);
        expect(mockConsoleLog).toHaveBeenCalledWith(`✅ Transmission successful! Received: "${message}"`);
        expect(mockConsoleLog).toHaveBeenCalledWith('🌌 Transmission cycle complete.');
    });

    test('should handle message corruption with specified error rate', async () => {
        setMockRandomValues([0.3, 0.6]); // Simulate delay variation and interference (corruption)
        const message = "Test message";
        const expectedDelay = 1000 + (1000 * 0.3 * 0.5);

        await mockActionCallback(message, { delay: '1000', errorRate: '0.7' });

        expect(mockConsoleLog).toHaveBeenCalledWith(`\n🚀 Initiating transmission of: "${message}"`);
        expect(mockConsoleLog).toHaveBeenCalledWith('  - Base delay set to: 1000ms');
        expect(mockConsoleLog).toHaveBeenCalledWith('  - Cosmic interference rate: 70%');
        expect(mockSetTimeout).toHaveBeenCalledWith(expect.any(Function), expectedDelay);
        expect(mockConsoleLog).toHaveBeenCalledWith('✨ Cosmic interference detected! Message was corrupted.');
        // The exact corrupted message depends on the random indices chosen for swapping.
        // We'll check if it's different from the original and has the same length.
        const logEntries = consoleOutput.join('\n');
        expect(logEntries).toContain('Received garbled transmission:');
        const garbledLog = consoleOutput.find(line => line.includes('Received garbled transmission:'));
        expect(garbledLog).not.toBeUndefined();
        const receivedMessage = garbledLog.split('"')[1];
        expect(receivedMessage).not.toBe(message);
        expect(receivedMessage.length).toBe(message.length);
        expect(mockConsoleLog).toHaveBeenCalledWith('🌌 Transmission cycle complete.');
    });

    test('should handle message loss with specified error rate', async () => {
        setMockRandomValues([0.1, 0.9]); // Simulate delay variation and interference (loss)
        const message = "Lost in space";
        const expectedDelay = 1000 + (1000 * 0.1 * 0.5);

        await mockActionCallback(message, { delay: '1000', errorRate: '0.9' });

        expect(mockConsoleLog).toHaveBeenCalledWith(`\n🚀 Initiating transmission of: "${message}"`);
        expect(mockConsoleLog).toHaveBeenCalledWith('  - Base delay set to: 1000ms');
        expect(mockConsoleLog).toHaveBeenCalledWith('  - Cosmic interference rate: 90%');
        expect(mockSetTimeout).toHaveBeenCalledWith(expect.any(Function), expectedDelay);
        expect(mockConsoleLog).toHaveBeenCalledWith('✨ Cosmic interference detected! Message was lost.');
        expect(mockConsoleLog).toHaveBeenCalledWith('  - Transmission failed to arrive.');
        expect(mockConsoleLog).toHaveBeenCalledWith('🌌 Transmission cycle complete.');
    });

    test('should use custom delay and error rate', async () => {
        setMockRandomValues([0.4, 0.05]); // Simulate delay variation and no interference
        const message = "Custom settings";
        const customDelay = 500;
        const customErrorRate = 0.1;
        const expectedDelay = customDelay + (customDelay * 0.4 * 0.5);

        await mockActionCallback(message, { delay: `${customDelay}`, errorRate: `${customErrorRate}` });

        expect(mockConsoleLog).toHaveBeenCalledWith(`\n🚀 Initiating transmission of: "${message}"`);
        expect(mockConsoleLog).toHaveBeenCalledWith(`  - Base delay set to: ${customDelay}ms`);
        expect(mockConsoleLog).toHaveBeenCalledWith(`  - Cosmic interference rate: ${customErrorRate * 100}%`);
        expect(mockSetTimeout).toHaveBeenCalledWith(expect.any(Function), expectedDelay);
        expect(mockConsoleLog).toHaveBeenCalledWith(`✅ Transmission successful! Received: "${message}"`);
        expect(mockConsoleLog).toHaveBeenCalledWith('🌌 Transmission cycle complete.');
    });

    test('should handle short messages for corruption', async () => {
        setMockRandomValues([0.1, 0.5]); // Simulate delay and interference
        const message = "Hi";
        const expectedDelay = 1000 + (1000 * 0.1 * 0.5);

        await mockActionCallback(message, { delay: '1000', errorRate: '0.5' });

        expect(mockConsoleLog).toHaveBeenCalledWith(`\n🚀 Initiating transmission of: "${message}"`);
        expect(mockConsoleLog).toHaveBeenCalledWith('  - Base delay set to: 1000ms');
        expect(mockConsoleLog).toHaveBeenCalledWith('  - Cosmic interference rate: 50%');
        expect(mockSetTimeout).toHaveBeenCalledWith(expect.any(Function), expectedDelay);
        expect(mockConsoleLog).toHaveBeenCalledWith('✨ Cosmic interference detected! Message was corrupted.');
        const logEntries = consoleOutput.join('\n');
        expect(logEntries).toContain('Received garbled transmission:');
        const garbledLog = consoleOutput.find(line => line.includes('Received garbled transmission:'));
        expect(garbledLog).not.toBeUndefined();
        const receivedMessage = garbledLog.split('"')[1];
        expect(receivedMessage.length).toBe(message.length);
        expect(mockConsoleLog).toHaveBeenCalledWith('🌌 Transmission cycle complete.');
    });

    test('should exit with error for invalid delay', async () => {
        setMockRandomValues([0.1]);
        const message = "Invalid delay test";

        await mockActionCallback(message, { delay: '-100', errorRate: '0.1' });

        expect(mockConsoleError).toHaveBeenCalledWith('Error: Invalid delay value. Must be a non-negative number.');
        expect(mockConsoleLog).not.toHaveBeenCalledWith(expect.stringContaining('Transmission successful'));
    });

    test('should exit with error for invalid error rate (too high)', async () => {
        setMockRandomValues([0.1]);
        const message = "Invalid rate test";

        await mockActionCallback(message, { delay: '1000', errorRate: '1.1' });

        expect(mockConsoleError).toHaveBeenCalledWith('Error: Invalid error rate. Must be between 0.0 and 1.0.');
        expect(mockConsoleLog).not.toHaveBeenCalledWith(expect.stringContaining('Transmission successful'));
    });

    test('should exit with error for invalid error rate (too low)', async () => {
        setMockRandomValues([0.1]);
        const message = "Invalid rate test";

        await mockActionCallback(message, { delay: '1000', errorRate: '-0.1' });

        expect(mockConsoleError).toHaveBeenCalledWith('Error: Invalid error rate. Must be between 0.0 and 1.0.');
        expect(mockConsoleLog).not.toHaveBeenCalledWith(expect.stringContaining('Transmission successful'));
    });
});
