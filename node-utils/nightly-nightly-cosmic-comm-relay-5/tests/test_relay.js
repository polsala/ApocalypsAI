const { exec } = require('child_process');
const path = require('path');

// Mock the messageQueue to control its state for testing
let mockMessageQueue = [];

// Mock the crypto module for deterministic encryption/decryption
jest.mock('crypto', () => ({
    randomBytes: jest.fn(() => Buffer.from('mockivmockivmockiv')), // Mock IV
    createCipheriv: jest.fn(() => ({
        update: jest.fn((text, inEnc, outEnc) => {
            // Simple XOR encryption for deterministic testing
            const keyBuffer = Buffer.from('testkey', 'utf8');
            const textBuffer = Buffer.from(text, inEnc);
            let encrypted = '';
            for (let i = 0; i < textBuffer.length; i++) {
                encrypted += String.fromCharCode(textBuffer[i] ^ keyBuffer[i % keyBuffer.length]);
            }
            return Buffer.from(encrypted).toString('hex');
        }),
        final: jest.fn(() => '')
    })),
    createDecipheriv: jest.fn(() => ({
        update: jest.fn((text, inEnc, outEnc) => {
            // Simple XOR decryption for deterministic testing
            const keyBuffer = Buffer.from('testkey', 'utf8');
            const textBuffer = Buffer.from(text, inEnc);
            let decrypted = '';
            for (let i = 0; i < textBuffer.length; i++) {
                decrypted += String.fromCharCode(textBuffer[i] ^ keyBuffer[i % keyBuffer.length]);
            }
            return Buffer.from(decrypted).toString('utf8');
        }),
        final: jest.fn(() => '')
    }))
}));

// Mock the Date.now() for deterministic arrival times
let mockDateNow = 1678886400000; // A fixed timestamp
const originalDateNow = Date.now;

// Mock the messageQueue and Date.now before each test
beforeEach(() => {
    // Mock the actual messageQueue in relay.js
    // This requires accessing the module scope, which can be tricky.
    // A more robust approach would be dependency injection, but for this
    // standalone utility, we'll try to override it directly if possible,
    // or simulate its behavior via command output parsing.
    // For simplicity in this example, we'll rely on parsing stdout.

    Date.now = jest.fn(() => mockDateNow);
});

// Restore original Date.now after all tests
afterAll(() => {
    Date.now = originalDateNow;
});

const relayScript = path.join(__dirname, '../src/relay.js');

// Helper function to execute the relay script and capture stdout/stderr
function runRelay(args) {
    return new Promise((resolve, reject) => {
        exec(`node ${relayScript} ${args.join(' ')}`, (error, stdout, stderr) => {
            if (error) {
                // Don't reject on expected errors like invalid commands, just return them
                // reject(error);
                // return;
            }
            resolve({ error, stdout, stderr });
        });
    });
}

// Mock rationale: The original implementation uses Date.now() and a global messageQueue.
// For deterministic tests, we need to mock these. We'll mock Date.now() directly.
// For the messageQueue, we'll simulate its behavior by parsing the stdout of the 'send' command
// and then checking the stdout of the 'receive' command to see if messages were processed.
// This is a pragmatic approach for a self-contained utility without complex dependency injection.

describe('Cosmic Comm Relay', () => {

    it('should send a message with default degradation and distance', async () => {
        const message = "Test message";
        const key = "testkey";
        const recipient = "Mars";

        const { stdout, stderr } = await runRelay(['send', `--message`, message, `--recipient`, recipient, `--key`, key]);

        expect(stderr).toBe('');
        expect(stdout).toContain(`Message sent to ${recipient}!`);
        expect(stdout).toContain(`Estimated Arrival:`); // Check if arrival time is calculated
    });

    it('should send a message with custom distance and degradation', async () => {
        const message = "Long range test";
        const key = "testkey";
        const recipient = "Jupiter";
        const distance = "50";
        const degradationRate = "0.2";

        const { stdout, stderr } = await runRelay(['send', `--message`, message, `--recipient`, recipient, `--key`, key, `--distance`, distance, `--degradationRate`, degradationRate]);

        expect(stderr).toBe('');
        expect(stdout).toContain(`Message sent to ${recipient}!`);
        expect(stdout).toContain(`Simulated Distance: ${distance} light-years`);
        expect(stdout).toContain(`Signal Degradation: ${parseFloat(degradationRate) * 100}%`);
        expect(stdout).toContain(`Estimated Arrival:`);
    });

    it('should receive a message that has arrived', async () => {
        const message = "Hello from the void!";
        const key = "testkey";
        const recipient = "Alpha Centauri";
        const distance = "5"; // This will set a travel time of 5 * 500 = 2500ms

        // First, send a message. This will add it to the queue.
        await runRelay(['send', `--message`, message, `--recipient`, recipient, `--key`, key, `--distance`, distance]);

        // Advance mock time to simulate message arrival
        // The message was sent at mockDateNow. It will arrive after distance * DEFAULT_DELAY_MULTIPLIER
        // Let's assume DEFAULT_DELAY_MULTIPLIER is 500ms/ly. So for 5 ly, it's 2500ms.
        mockDateNow += 5 * 500 + 100; // Add a bit extra to ensure it's past arrival time

        const { stdout, stderr } = await runRelay(['receive', `--key`, key]);

        expect(stderr).toBe('');
        expect(stdout).toContain(`--- Incoming Cosmic Transmissions (1) ---`);
        expect(stdout).toContain(`From: ${recipient} (Distance: ${distance} ly, Degradation: 1%)
  Message: ${message}`);
    });

    it('should indicate no messages have arrived if none have', async () => {
        const key = "testkey";

        // Ensure no messages are in the queue (or simulate an empty queue)
        // For this test, we'll just run receive without sending anything first.

        const { stdout, stderr } = await runRelay(['receive', `--key`, key]);

        expect(stderr).toBe('');
        expect(stdout).toContain("No messages have arrived yet. Keep waiting for cosmic signals...");
    });

    it('should handle degraded messages gracefully', async () => {
        const message = "Secret code";
        const key = "testkey";
        const recipient = "Nebula";
        const distance = "2";
        const degradationRate = "0.9"; // High degradation

        // Send a message with high degradation
        await runRelay(['send', `--message`, message, `--recipient`, recipient, `--key`, key, `--distance`, distance, `--degradationRate`, degradationRate]);

        // Advance mock time
        mockDateNow += 2 * 500 + 100;

        const { stdout, stderr } = await runRelay(['receive', `--key`, key]);

        expect(stderr).toBe('');
        // Due to the mocked crypto and high degradation, decryption might fail.
        // The test should check for the 'DEGRADED/UNREADABLE' message.
        expect(stdout).toContain(`From: ${recipient} (Distance: 2 ly, Degradation: 90%)
  Message: [DEGRADED/UNREADABLE] - Could not decrypt. The cosmic winds may have scrambled it too much!`);
    });

    it('should require a key for receiving messages', async () => {
        const { stdout, stderr } = await runRelay(['receive']);
        expect(stderr).toContain('Error: Key is required for receiving.');
        expect(stdout).toBe('');
    });

    it('should require a message and key for sending messages', async () => {
        const { stdout, stderr } = await runRelay(['send', '--recipient', 'Pluto']);
        expect(stderr).toContain('Error: Message and key are required for sending.');
        expect(stdout).toBe('');
    });
});
