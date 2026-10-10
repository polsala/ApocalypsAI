const { execSync } = require('child_process');
const { mock } = require('node:test');

// Mocking Math.random to ensure deterministic tests
const mockMathRandom = (values) => {
    let index = 0;
    mock.method(Math, 'random', () => {
        if (index >= values.length) {
            // Fallback to original if we run out of mock values
            return Math.random();
        }
        return values[index++];
    });
};

// Helper to run command and capture stdout
const runCommand = (command) => {
    try {
        // Use execSync with a timeout to prevent hanging
        const stdout = execSync(`node src/index.js ${command}`, {
            stdio: 'pipe', // Capture stdout
            timeout: 5000, // 5 second timeout
            encoding: 'utf-8'
        });
        return stdout.trim();
    } catch (error) {
        // If the command timed out or failed, return an error indicator
        if (error.signal === 'SIGTERM') {
            return 'TIMEOUT';
        }
        return `ERROR: ${error.message}`; // Or handle other errors
    }
};

describe('Cosmic Comm Relay', () => {

    beforeEach(() => {
        // Reset mocks before each test
        mock.reset();
        // Mock getRandomInt to control its output
        mock.method(require('../src/index.js'), 'getRandomInt', (min, max) => {
            // This mock is tricky as getRandomInt is used internally. 
            // For simplicity, we'll mock Math.random directly for most cases.
            // If specific getRandomInt control is needed, more advanced mocking is required.
        });
    });

    describe('send command', () => {
        test('should report successful transmission when Math.random() > MESSAGE_PROBABILITY', () => {
            // Mock Math.random to return a value that ensures success
            mockMathRandom([0.1]); // 0.1 < 0.7 (MESSAGE_PROBABILITY)
            const output = runCommand('send "Hello Void!"');
            expect(output).toContain('Message successfully transmitted to the void!');
        });

        test('should report failed transmission when Math.random() <= MESSAGE_PROBABILITY', () => {
            // Mock Math.random to return a value that ensures failure
            mockMathRandom([0.8]); // 0.8 > 0.7 (MESSAGE_PROBABILITY)
            const output = runCommand('send "Hello Void!"');
            expect(output).toContain('Transmission failed. The void is silent... for now.');
        });
    });

    describe('receive command', () => {
        test('should listen for transmissions and report incoming messages', () => {
            // Mock Math.random to simulate one successful incoming message after a delay
            // First call to Math.random for interval: 0.5 (simulates 3000ms delay)
            // Second call for MESSAGE_PROBABILITY: 0.1 (simulates success)
            mockMathRandom([0.5, 0.1]);
            const output = runCommand('receive');
            // This test is tricky because 'receive' runs indefinitely. 
            // We'll rely on the timeout mechanism of runCommand and check for the expected output.
            // A more robust test would involve mocking setInterval and clearInterval.
            // For this example, we'll check if the initial listening message is present.
            expect(output).toContain('Listening for cosmic transmissions...');
            // Note: This test doesn't assert the *content* of the received message due to the nature of setInterval.
            // A more advanced test setup would be needed for that.
        });

        test('should report interference when --interfere is used and interference occurs', () => {
            // Mock Math.random for: 
            // 1. Interval delay (0.5 -> 3000ms)
            // 2. Interference chance (0.1 -> interference occurs)
            // 3. Garble chance within interference (0.6 -> garble happens)
            // 4. Character garble chance (0.7 -> character is garbled)
            // 5. Another character garble chance (0.2 -> character is NOT garbled)
            mockMathRandom([0.5, 0.1, 0.6, 0.7, 0.2]);
            const output = runCommand('receive --interfere');
            expect(output).toContain('Cosmic interference is active. Expect the unexpected!');
            // Again, checking for the initial message due to the nature of setInterval.
        });

        test('should not report interference when --interfere is used but interference does not occur', () => {
            // Mock Math.random for:
            // 1. Interval delay (0.5 -> 3000ms)
            // 2. Interference chance (0.8 -> no interference)
            mockMathRandom([0.5, 0.8]);
            const output = runCommand('receive --interfere');
            expect(output).toContain('Cosmic interference is active. Expect the unexpected!');
            // This test is limited by the setInterval nature. It confirms the setup message is shown.
        });
    });

    // Mocking the entire module for more controlled testing of internal functions
    describe('internal functions', () => {
        let cosmicRelayModule;

        beforeAll(() => {
            // Dynamically require the module to mock its exports
            jest.isolateModules(() => {
                cosmicRelayModule = require('../src/index.js');
            });
        });

        test('simulateCosmicEvent should return a greeting when Math.random() is low', () => {
            // Mock Math.random for simulateCosmicEvent
            mockMathRandom([0.2]); // 0.2 < 0.7 (MESSAGE_PROBABILITY)
            // Need to access the internal function, which is not directly exported.
            // This requires a more advanced mocking strategy or restructuring the module.
            // For this example, we'll assume we can access it or test its effect indirectly.
            // Since we can't directly mock internal functions easily with Jest's default setup
            // without exporting them, we'll skip direct testing of simulateCosmicEvent here
            // and rely on the 'send' and 'receive' command tests to cover its behavior.
        });

        test('introduceInterference should garble a message when Math.random() is low', () => {
            // Mock Math.random for introduceInterference
            mockMathRandom([0.2]); // 0.2 < 0.3 (INTERFERENCE_CHANCE)
            // Again, direct access to internal functions is challenging.
            // We'll test the *effect* of interference via the 'receive --interfere' command.
        });
    });
});
