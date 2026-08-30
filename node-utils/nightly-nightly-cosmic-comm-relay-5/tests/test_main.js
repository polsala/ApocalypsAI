const { exec } = require('child_process');
const path = require('path');
const sinon = require('sinon');

// Mock the readline module to control input/output
let mockReadline;
let mockInterface;

// Mock the simulateCosmicDelay function
let mockSimulateCosmicDelay;

// Helper to simulate user input
function simulateInput(inputs) {
    let inputIndex = 0;
    mockInterface.question.callsFake((query, callback) => {
        console.log(`Mocking input for: ${query.trim()}`);
        if (inputIndex < inputs.length) {
            callback(inputs[inputIndex++]);
        } else {
            callback(''); // Default empty input if not enough provided
        }
    });
}

// Helper to capture console output
function captureConsoleOutput(callback) {
    const logSpy = sinon.spy(console, 'log');
    const errorSpy = sinon.spy(console, 'error');
    const warnSpy = sinon.spy(console, 'warn');

    callback();

    const logs = {
        log: logSpy.getCalls().map(call => call.args[0]),
        error: errorSpy.getCalls().map(call => call.args[0]),
        warn: warnSpy.getCalls().map(call => call.args[0])
    };

    logSpy.restore();
    errorSpy.restore();
    warnSpy.restore();

    return logs;
}

describe('Cosmic Comm Relay', () => {
    beforeEach(() => {
        // Mock readline
        mockInterface = {
            question: sinon.stub(),
            close: sinon.stub()
        };
        mockReadline = {
            createInterface: sinon.stub().returns(mockInterface)
        };
        sinon.stub(require('readline'), 'createInterface').returns(mockInterface);

        // Mock simulateCosmicDelay
        mockSimulateCosmicDelay = sinon.stub().resolves(); // Make it resolve immediately for tests
        sinon.stub(require('./main'), 'simulateCosmicDelay').callsFake(mockSimulateCosmicDelay);

        // Mock the main function to be testable
        sinon.stub(require('./main'), 'runCosmicCommRelay').callsFake(async () => {
            // Re-implement the core logic here for isolation, or ensure the original is called correctly
            // For simplicity, we'll assume the original `runCosmicCommRelay` is called and we mock its dependencies.
            // If `runCosmicCommRelay` itself needs to be stubbed, we'd do it here.
        });
    });

    afterEach(() => {
        sinon.restore(); // Restore all mocks
    });

    it('should encrypt and send a message correctly', (done) => {
        const mockInputs = ['send', 'mySecretKey', 'Hello Cosmic World!', '10000'];
        simulateInput(mockInputs);

        const logs = captureConsoleOutput(() => {
            require('./main'); // Execute the script
        });

        // Wait for async operations to complete
        setTimeout(() => {
            // Check if readline.close was called
            sinon.assert.calledOnce(mockInterface.close);

            // Check if simulateCosmicDelay was called with the correct distance
            sinon.assert.calledOnce(mockSimulateCosmicDelay);
            sinon.assert.calledWith(mockSimulateCosmicDelay, 10000);

            // Check console output for key messages
            expect(logs.log).to.include('Welcome to the Cosmic Comm Relay!');
            expect(logs.log).to.include('Choose mode (send/receive):');
            expect(logs.log).to.include('Enter your secret key:');
            expect(logs.log).to.include('Enter your message:');
            expect(logs.log).to.include('Enter simulated cosmic distance (e.g., 10000):');
            expect(logs.log).to.include('Transmitting message...');
            expect(logs.log).to.include('Message encrypted and sent across the void!');
            expect(logs.log).to.include('Transmission complete.');

            done();
        }, 100); // Small delay to allow async operations
    });

    it('should decrypt a received message correctly', (done) => {
        const mockInputs = ['receive', 'mySecretKey'];
        simulateInput(mockInputs);

        // Mock the internal xorEncryptDecrypt to return a predictable encrypted string
        const originalXorEncryptDecrypt = require('./main').xorEncryptDecrypt;
        const mockEncryptedMessage = originalXorEncryptDecrypt('Greetings from a distant star!', 'mySecretKey');
        sinon.stub(require('./main'), 'xorEncryptDecrypt').callsFake((text, key) => {
            // For receiving, we expect the original message to be passed in for encryption
            // and we want to return a pre-defined encrypted string for decryption.
            // This is a bit tricky: we're testing the decryption path.
            // Let's assume the mock data is already encrypted.
            if (text === 'Greetings from a distant star!') return mockEncryptedMessage; // This is for the mock data generation
            return originalXorEncryptDecrypt(text, key); // For actual encryption if needed elsewhere
        });

        // We need to mock the 'incoming transmission' part more directly
        // The current `runCosmicCommRelay` simulates this internally.
        // Let's stub the internal simulation to return our known encrypted message.
        const originalRunCosmicCommRelay = require('./main').runCosmicCommRelay;
        sinon.stub(require('./main'), 'runCosmicCommRelay').callsFake(async () => {
            console.log('Welcome to the Cosmic Comm Relay!');
            rl.question('Choose mode (send/receive): ', async (mode) => {
                rl.question('Enter your secret key: ', async (key) => {
                    console.log('\nListening for transmissions...');
                    const mockDistance = 50000; // Arbitrary mock distance
                    await simulateCosmicDelay(mockDistance);
                    console.log('Incoming transmission detected!');
                    // Manually call the decryption part with our known encrypted message
                    const decryptedMessage = xorEncryptDecrypt(mockEncryptedMessage, key);
                    console.log(`Message decrypted: ${decryptedMessage}`);
                    rl.close();
                });
            });
        });

        const logs = captureConsoleOutput(() => {
            require('./main'); // Execute the script
        });

        setTimeout(() => {
            sinon.assert.calledOnce(mockInterface.close);
            sinon.assert.calledOnce(mockSimulateCosmicDelay);

            expect(logs.log).to.include('Welcome to the Cosmic Comm Relay!');
            expect(logs.log).to.include('Choose mode (send/receive):');
            expect(logs.log).to.include('Enter your secret key:');
            expect(logs.log).to.include('Listening for transmissions...');
            expect(logs.log).to.include('Incoming transmission detected!');
            expect(logs.log).to.include('Message decrypted: Greetings from a distant star!');

            done();
        }, 100);
    });

    it('should handle invalid mode input', (done) => {
        const mockInputs = ['fly'];
        simulateInput(mockInputs);

        const logs = captureConsoleOutput(() => {
            require('./main');
        });

        setTimeout(() => {
            sinon.assert.calledOnce(mockInterface.close);
            expect(logs.log).to.include('Invalid mode. Please choose "send" or "receive".');
            done();
        }, 50);
    });

    it('should handle missing secret key', (done) => {
        const mockInputs = ['send', ''];
        simulateInput(mockInputs);

        const logs = captureConsoleOutput(() => {
            require('./main');
        });

        setTimeout(() => {
            sinon.assert.calledOnce(mockInterface.close);
            expect(logs.log).to.include('A secret key is required.');
            done();
        }, 50);
    });

    it('should handle invalid distance input', (done) => {
        const mockInputs = ['send', 'key', 'message', 'not-a-number'];
        simulateInput(mockInputs);

        const logs = captureConsoleOutput(() => {
            require('./main');
        });

        setTimeout(() => {
            sinon.assert.calledOnce(mockInterface.close);
            expect(logs.log).to.include('Invalid distance. Please enter a positive number.');
            done();
        }, 50);
    });
});
