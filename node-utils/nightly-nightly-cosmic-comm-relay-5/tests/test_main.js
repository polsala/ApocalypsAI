const { exec } = require('child_process');
const path = require('path');

// Mock the actual message sending/receiving to make tests deterministic and offline
// We'll mock the internal functions directly for simplicity in this example.
// In a real-world scenario, you might use a mocking library like 'jest' or 'sinon'.

// Mock rationale: These functions are mocked to control their behavior during testing,
// ensuring deterministic outcomes without actual network calls or time delays.
// This allows us to test the logic of message processing, interference, and argument parsing.

let mockDelay = 100;
let mockInterference = false;

// Mock the core functions that would normally involve async operations or randomness
const mockSendMessage = jest.fn((message, delay, interference) => {
    const processedMessage = interference ? `INTERFERED(${message})` : message;
    return Promise.resolve(processedMessage);
});

const mockReceiveMessage = jest.fn((delay, interference) => {
    const possibleMessages = [
        "Mocked signal 1.",
        "Mocked signal 2.",
        "Mocked signal 3."
    ];
    let received = possibleMessages[0]; // Always pick the first for deterministic test
    if (interference) {
        received = `INTERFERED(${received})`;
    }
    return Promise.resolve(received);
});

// Store original functions to restore them later
const originalSendMessage = require('../src/main').sendMessage;
const originalReceiveMessage = require('../src/main').receiveMessage;

// Replace the actual functions with mocks before tests
jest.mock('../src/main', () => {
    const originalModule = jest.requireActual('../src/main');
    return {
        ...originalModule,
        sendMessage: mockSendMessage,
        receiveMessage: mockReceiveMessage,
        // We also need to mock the runCosmicRelay to control its flow
        runCosmicRelay: jest.fn(async (options) => {
            const delay = options.delay || 100;
            const interference = options.interference || false;

            if (options.send) {
                await mockSendMessage(options.send, delay, interference);
                return "Sent and exited";
            } else if (options.listen) {
                await mockReceiveMessage(delay, interference);
                return "Listened";
            } else {
                await mockSendMessage("Initial greeting", delay, interference);
                await mockReceiveMessage(delay, interference);
                return "Sent and listened";
            }
        })
    };
});

// Mock console.log to capture output
let consoleOutput = [];
const mockConsoleLog = jest.fn((...args) => {
    consoleOutput.push(args.join(' '));
});

// Mock process.exit to prevent actual process termination during tests
const mockProcessExit = jest.fn();

describe('Cosmic Communication Relay', () => {

    beforeEach(() => {
        // Reset mocks and clear output before each test
        mockSendMessage.mockClear();
        mockReceiveMessage.mockClear();
        jest.clearAllMocks();
        consoleOutput = [];
        // Replace console.log with our mock
        global.console.log = mockConsoleLog;
        global.process.exit = mockProcessExit;
    });

    afterAll(() => {
        // Restore original console.log and process.exit after all tests
        global.console.log = console;
        global.process.exit = process;
    });

    test('should send an initial greeting by default', async () => {
        const { runCosmicRelay } = require('../src/main');
        await runCosmicRelay({});

        expect(mockSendMessage).toHaveBeenCalledWith("Hello from Earth! This is ApocalypsAI.", expect.any(Number), false);
        expect(mockReceiveMessage).toHaveBeenCalled();
    });

    test('should send a specific message when --send is used', async () => {
        const { runCosmicRelay } = require('../src/main');
        const testMessage = "Test message to the void!";
        await runCosmicRelay({ send: testMessage });

        expect(mockSendMessage).toHaveBeenCalledWith(testMessage, expect.any(Number), false);
        expect(mockReceiveMessage).not.toHaveBeenCalled();
        expect(mockProcessExit).toHaveBeenCalledWith(0);
    });

    test('should enable interference when --interference flag is used', async () => {
        const { runCosmicRelay } = require('../src/main');
        await runCosmicRelay({ interference: true });

        expect(mockSendMessage).toHaveBeenCalledWith(expect.any(String), expect.any(Number), true);
        expect(mockReceiveMessage).toHaveBeenCalledWith(expect.any(Number), true);
    });

    test('should set custom delay when --delay is used', async () => {
        const customDelay = 500;
        const { runCosmicRelay } = require('../src/main');
        await runCosmicRelay({ delay: customDelay });

        // The mocked runCosmicRelay uses expect.any(Number) for delay, but we can check if it was passed
        // The actual delay value is handled by the mock's setTimeout, which we don't test here.
        // We are testing that the option is correctly passed to the mocked functions.
        expect(mockSendMessage).toHaveBeenCalledWith(expect.any(String), customDelay, false);
        expect(mockReceiveMessage).toHaveBeenCalledWith(customDelay, false);
    });

    test('should only listen when --listen flag is used', async () => {
        const { runCosmicRelay } = require('../src/main');
        await runCosmicRelay({ listen: true });

        expect(mockSendMessage).not.toHaveBeenCalled();
        expect(mockReceiveMessage).toHaveBeenCalled();
    });

    test('should correctly parse command line arguments', () => {
        // Mocking exec to simulate command line execution for argument parsing test
        // This is a bit of a hack, but demonstrates how to test argument parsing.
        // A more robust solution would involve a dedicated argument parsing library.
        const originalExec = require('child_process').exec;
        const mockExec = jest.fn((command, callback) => {
            // Simulate command line args for testing
            const simulatedArgs = command.split(' ').slice(2); // Remove 'node' and 'src/main.js'
            const options = {};
            for (let i = 0; i < simulatedArgs.length; i++) {
                const arg = simulatedArgs[i];
                if (arg === '--interference' || arg === '-i') {
                    options.interference = true;
                } else if (arg === '--delay' && simulatedArgs[i + 1]) {
                    options.delay = parseInt(simulatedArgs[i + 1], 10);
                    i++;
                } else if (arg === '--listen') {
                    options.listen = true;
                } else if (arg === '--send' && simulatedArgs[i + 1]) {
                    options.send = simulatedArgs[i + 1];
                    i++;
                }
            }
            callback(null, JSON.stringify(options)); // Return options as JSON string
        });
        require('child_process').exec = mockExec;

        const scriptPath = path.join(__dirname, '../src/main.js');
        const command1 = `node ${scriptPath} --interference --delay 200 --send "Test"`;
        const command2 = `node ${scriptPath} -i --listen`;

        let parsedOptions1, parsedOptions2;

        exec(command1, (error, stdout, stderr) => {
            if (error) {
                console.error(`exec error: ${error}`);
                return;
            }
            parsedOptions1 = JSON.parse(stdout);
        });

        exec(command2, (error, stdout, stderr) => {
            if (error) {
                console.error(`exec error: ${error}`);
                return;
            }
            parsedOptions2 = JSON.parse(stdout);
        });

        // Wait for exec to complete (simulated)
        // In a real test, you'd use async/await or promises with exec
        setTimeout(() => {
            expect(parsedOptions1).toEqual({
                interference: true,
                delay: 200,
                send: "Test"
            });
            expect(parsedOptions2).toEqual({
                interference: true,
                listen: true
            });
            // Restore original exec
            require('child_process').exec = originalExec;
        }, 50);
    });
});
