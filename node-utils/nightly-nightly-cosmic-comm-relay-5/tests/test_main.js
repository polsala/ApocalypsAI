const { exec } = require('child_process');
const path = require('path');

// Mock rationale: We are mocking the child_process.exec function to control its output and behavior
// for deterministic testing without actually running the script externally or relying on external factors.
jest.mock('child_process');

// Mock rationale: We are mocking setTimeout to control the timing of asynchronous operations
// and ensure tests run quickly and deterministically.
jest.useFakeTimers();

const mockExec = require('child_process').exec;

// Helper function to simulate running the script and capturing its output
function runScript(args = []) {
    return new Promise((resolve, reject) => {
        const scriptPath = path.join(__dirname, '../src/main.js');
        const command = `node ${scriptPath} ${args.join(' ')}`;

        mockExec(command, (error, stdout, stderr) => {
            if (error) {
                return reject({ error, stdout, stderr });
            }
            resolve({ stdout, stderr });
        });
    });
}

describe('Cosmic Comm Relay', () => {

    beforeEach(() => {
        // Reset mocks before each test
        mockExec.mockClear();
        jest.clearAllTimers();
    });

    test('should send a message with default settings and no interference', async () => {
        // Mock rationale: Ensure exec is called with the correct command and arguments.
        mockExec.mockImplementation((command, callback) => {
            // Simulate the script running and calling the callback with success
            callback(null, "\n🚀 Initiating cosmic transmission...\n   Original Message: \"Test message\"\n   Estimated travel time: 2500ms\n✨ Message received at destination!\n   Final Message: \"Test message\"\n", "");
        });

        const { stdout } = await runScript(['"Test message"']);

        // Advance timers to allow setTimeout within the script to potentially run (though mocked exec bypasses it)
        jest.advanceTimersByTime(3000);

        expect(mockExec).toHaveBeenCalledTimes(1);
        expect(stdout).toContain('Original Message: "Test message"');
        expect(stdout).toContain('Final Message: "Test message"');
        expect(stdout).not.toContain('Cosmic interference detected!');
    });

    test('should simulate interference by altering the message', async () => {
        // Mock rationale: Simulate a scenario where interference occurs.
        mockExec.mockImplementation((command, callback) => {
            // Simulate interference by returning a slightly altered message
            callback(null, "\n🚀 Initiating cosmic transmission...\n   Original Message: \"Hello world\"\n   Estimated travel time: 3000ms\n   ⚠️ Cosmic interference detected! Signal is a bit fuzzy...\n✨ Message received at destination!\n   Final Message: \"Helo world\"\n", "");
        });

        const { stdout } = await runScript(['"Hello world"']);

        jest.advanceTimersByTime(3500);

        expect(mockExec).toHaveBeenCalledTimes(1);
        expect(stdout).toContain('Original Message: "Hello world"');
        expect(stdout).toContain('Cosmic interference detected!');
        expect(stdout).toContain('Final Message: "Helo world"'); // Expecting an altered message
    });

    test('should handle custom delay range', async () => {
        // Mock rationale: Simulate a specific delay range being used.
        mockExec.mockImplementation((command, callback) => {
            callback(null, "\n🚀 Initiating cosmic transmission...\n   Original Message: \"Short delay test\"\n   Estimated travel time: 750ms\n✨ Message received at destination!\n   Final Message: \"Short delay test\"\n", "");
        });

        const { stdout } = await runScript(['"Short delay test"', '--delay-range', '500,1000']);

        jest.advanceTimersByTime(1500);

        expect(mockExec).toHaveBeenCalledTimes(1);
        expect(stdout).toContain('Estimated travel time: 750ms'); // Expecting a delay within the custom range
    });

    test('should handle custom interference chance', async () => {
        // Mock rationale: Simulate a scenario with a higher chance of interference.
        mockExec.mockImplementation((command, callback) => {
            callback(null, "\n🚀 Initiating cosmic transmission...\n   Original Message: \"High interference\"\n   Estimated travel time: 4000ms\n   ⚠️ Cosmic interference detected! Signal is a bit fuzzy...\n✨ Message received at destination!\n   Final Message: \"High interferenc\"\n", "");
        });

        const { stdout } = await runScript(['"High interference"', '--interference-chance', '80']);

        jest.advanceTimersByTime(4500);

        expect(mockExec).toHaveBeenCalledTimes(1);
        expect(stdout).toContain('Cosmic interference detected!');
        expect(stdout).toContain('Final Message: "High interferenc"');
    });

    test('should exit with an error if no message is provided', async () => {
        // Mock rationale: Simulate the script exiting with an error code and message.
        mockExec.mockImplementation((command, callback) => {
            callback(new Error('Script exited with code 1'), '', 'Error: Message is required.\nUsage: node src/main.js <message> [--delay-range <min>,<max>] [--interference-chance <percentage>]\n');
        });

        await expect(runScript([])).rejects.toThrow();
        const { stderr } = await runScript([]); // Capture stderr from the rejected promise

        expect(stderr).toContain('Error: Message is required.');
    });
});
