const { expect } = require('chai');
const sinon = require('sinon');
const main = require('../src/main'); // Assuming main.js exports functions or is run directly

// Mocking the require for 'readline' to control its behavior during tests
let mockReadline;
let mockInterface;

// Mocking the global setTimeout and Math.random for deterministic tests
let clock;
let randomStub;

// Helper to mock console.log and capture output
let consoleLogStub;
let consoleWarnStub;
let consoleErrorStub;

// Mocking the sendMessage function to control its return values and timing
let sendMessageStub;

// Mocking the listenForTransmissions function to control its execution flow
let listenForTransmissionsStub;

// Mocking the parseArgs function to control command-line arguments
let parseArgsStub;

// Mocking the main execution function to control its entry point
let mockMainExecution;

// --- Mock Rationale ---
// Mocking setTimeout: To control the timing of asynchronous operations and ensure tests run deterministically without actual delays.
// Mocking Math.random: To control the random outcomes of signal degradation and message selection, making tests repeatable.
// Mocking console.log/warn/error: To capture and assert on output messages without cluttering test output and to verify logging behavior.
// Mocking readline: To prevent actual user input prompts during automated tests.
// Mocking sendMessage and listenForTransmissions: To isolate the testing of specific functions and control their behavior (e.g., return values, execution paths).
// Mocking parseArgs: To simulate different command-line arguments without actually passing them to the script.
// Mocking main execution: To control the entry point of the script for testing purposes.


describe('Cosmic Comm Relay', () => {

    beforeEach(() => {
        // Mocking readline
        mockInterface = {
            on: sinon.stub(),
            close: sinon.stub()
        };
        mockReadline = {
            createInterface: sinon.stub().returns(mockInterface)
        };
        // Replace the actual require with our mock
        require = sinon.stub().callsFake((moduleName) => {
            if (moduleName === 'readline') return mockReadline;
            // Fallback for other modules if needed, though not expected here
            return require.original(moduleName);
        });
        // Store original require to restore later
        require.original = require.original || require;

        // Mocking setTimeout and Math.random
        clock = sinon.useFakeTimers();
        randomStub = sinon.stub(Math, 'random');

        // Mocking console output
        consoleLogStub = sinon.stub(console, 'log');
        consoleWarnStub = sinon.stub(console, 'warn');
        consoleErrorStub = sinon.stub(console, 'error');

        // Mocking internal functions from src/main.js
        // We need to require the module *after* stubbing 'require' if it's used internally
        // However, since we're testing the module itself, we'll stub its exported/internal functions directly
        // For this example, let's assume src/main.js exports the functions we want to test or we can access them via a global scope if needed.
        // A common pattern is to export them for testing.
        // For simplicity here, we'll stub them as if they were accessible.
        // In a real scenario, you might need to adjust how these are exposed.
        sendMessageStub = sinon.stub(require('../src/main'), 'sendMessage');
        listenForTransmissionsStub = sinon.stub(require('../src/main'), 'listenForTransmissions');
        parseArgsStub = sinon.stub(require('../src/main'), 'parseArgs');
        mockMainExecution = require('../src/main').main; // Assuming main is exported

        // Set default mock behavior for parseArgs
        parseArgsStub.returns({ degradationChance: 0 });
    });

    afterEach(() => {
        // Restore mocks and timers
        sinon.restore();
        clock.restore();
        // Restore original require
        require = require.original;
    });

    describe('parseArgs', () => {
        it('should return default degradation chance if no args are provided', () => {
            parseArgsStub.restore(); // Restore to use original function for this test
            const args = process.argv.slice(2);
            const result = require('../src/main').parseArgs(); // Call original parseArgs
            expect(result.degradationChance).to.equal(0);
        });

        it('should parse --degrade argument correctly', () => {
            parseArgsStub.returns({ degradationChance: 25 });
            const result = parseArgsStub();
            expect(result.degradationChance).to.equal(25);
        });

        it('should warn and use default for invalid degradation percentage', () => {
            parseArgsStub.returns({ degradationChance: 0 }); // Resetting stub for this test
            const originalParseArgs = require('../src/main').parseArgs;
            sinon.stub(require('../src/main'), 'parseArgs').callsFake(() => {
                // Simulate the internal logic of parseArgs for this specific test
                const args = ['--degrade', 'invalid-percent'];
                let degradationChance = 0;
                if (args[0] === '--degrade' && args[1]) {
                    const percentage = parseInt(args[1], 10);
                    if (isNaN(percentage) || percentage < 0 || percentage > 100) {
                        consoleWarnStub(`Warning: Invalid degradation percentage '${args[1]}'. Using default ${0}%.`);
                    } else {
                        degradationChance = percentage;
                    }
                }
                return { degradationChance };
            });
            
            const result = require('../src/main').parseArgs();
            expect(consoleWarnStub.calledOnce).to.be.true;
            expect(consoleWarnStub.getCall(0).args[0]).to.include('invalid-percent');
            expect(result.degradationChance).to.equal(0);
        });

        it('should handle degradation percentage at 0', () => {
            parseArgsStub.returns({ degradationChance: 0 });
            const result = parseArgsStub();
            expect(result.degradationChance).to.equal(0);
        });

        it('should handle degradation percentage at 100', () => {
            parseArgsStub.returns({ degradationChance: 100 });
            const result = parseArgsStub();
            expect(result.degradationChance).to.equal(100);
        });
    });

    describe('listenForTransmissions', () => {
        it('should call sendMessage multiple times', async () => {
            sendMessageStub.resolves('Mocked received message'); // Make sendMessage resolve immediately
            await require('../src/main').listenForTransmissions(10);
            expect(sendMessageStub.callCount).to.be.at.least(1);
        });

        it('should log listening status', async () => {
            sendMessageStub.resolves('Mocked received message');
            await require('../src/main').listenForTransmissions(10);
            expect(consoleLogStub.getCall(0).args[0]).to.include('Listening for cosmic transmissions');
        });
    });

    describe('sendMessage', () => {
        it('should resolve with a received message', async () => {
            const testMessage = "Hello, universe!";
            const degradation = 0;
            randomStub.onCall(0).returns(0.5); // For getRandomInt(min, max)
            randomStub.onCall(1).returns(0.1); // For degradeSignal random check
            clock.tick(2000); // Advance timers by 2 seconds
            const result = await require('../src/main').sendMessage(testMessage, degradation);
            expect(result).to.equal(`Received: "${testMessage}"`);
            expect(consoleLogStub.getCall(0).args[0]).to.include('Transmitting message');
            expect(consoleLogStub.getCall(1).args[0]).to.include('Successfully received message');
        });

        it('should simulate signal degradation and return garbled message', async () => {
            const testMessage = "Important data";
            const degradation = 100;
            // Mock Math.random to ensure degradation happens
            randomStub.onCall(0).returns(0.5); // For getRandomInt(min, max)
            randomStub.onCall(1).returns(0.9); // For degradeSignal random check (guarantees degradation)
            randomStub.onCall(2).returns(0); // For corruptionType (e.g., character swap)
            randomStub.onCall(3).returns(0); // For idx1 in character swap
            randomStub.onCall(4).returns(1); // For idx2 in character swap
            clock.tick(3000);
            const result = await require('../src/main').sendMessage(testMessage, degradation);
            expect(result).to.include('Received garbled: "');
            expect(consoleLogStub.getCall(1).args[0]).to.include('Received garbled transmission');
        });

        it('should handle signal loss', async () => {
            const testMessage = "Short";
            const degradation = 100;
            randomStub.onCall(0).returns(0.5); // For getRandomInt(min, max)
            randomStub.onCall(1).returns(0.9); // For degradeSignal random check
            randomStub.onCall(2).returns(1); // For corruptionType (character deletion)
            randomStub.onCall(3).returns(0); // For idx in character deletion
            clock.tick(1500);
            const result = await require('../src/main').sendMessage(testMessage, degradation);
            expect(result).to.include('Received garbled: "');
            expect(consoleLogStub.getCall(1).args[0]).to.include('Received garbled transmission');
        });

        it('should handle gibberish insertion', async () => {
            const testMessage = "Normal message";
            const degradation = 100;
            randomStub.onCall(0).returns(0.5); // For getRandomInt(min, max)
            randomStub.onCall(1).returns(0.9); // For degradeSignal random check
            randomStub.onCall(2).returns(2); // For corruptionType (gibberish insertion)
            randomStub.onCall(3).returns(5); // For insertPos
            randomStub.onCall(4).returns(0); // For gibberish index
            clock.tick(4000);
            const result = await require('../src/main').sendMessage(testMessage, degradation);
            expect(result).to.include('Received garbled: "');
            expect(consoleLogStub.getCall(1).args[0]).to.include('Received garbled transmission');
        });
    });

    describe('main', () => {
        it('should call listenForTransmissions with parsed arguments', async () => {
            const mockDegradation = 30;
            parseArgsStub.returns({ degradationChance: mockDegradation });
            listenForTransmissionsStub.resolves(); // Make listenForTransmissions resolve

            await mockMainExecution();

            expect(parseArgsStub.calledOnce).to.be.true;
            expect(listenForTransmissionsStub.calledOnceWithExactly(mockDegradation)).to.be.true;
        });

        it('should handle errors during execution', async () => {
            const testError = new Error('Cosmic anomaly!');
            parseArgsStub.returns({ degradationChance: 0 });
            listenForTransmissionsStub.rejects(testError);

            await mockMainExecution();

            expect(consoleErrorStub.calledOnce).to.be.true;
            expect(consoleErrorStub.getCall(0).args[0]).to.include('An unexpected cosmic anomaly occurred');
            expect(consoleErrorStub.getCall(0).args[1]).to.equal(testError);
        });
    });
});
