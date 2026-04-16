const assert = require('assert');

// Mock the main script's behavior for testing
const mockMain = require('../src/main.js');

// Mock console.log and process.argv for isolated testing
let consoleOutput = [];
let mockArgv = [];

const originalConsoleLog = console.log;
const originalProcessArgv = process.argv;

// Mock console.log to capture output
console.log = (message) => {
    consoleOutput.push(message);
};

// Mock process.argv to control command-line arguments
process.argv = ['node', 'src/main.js']; // Base arguments

// Helper to run a specific command with given arguments
function runTestCommand(args) {
    consoleOutput = []; // Clear previous output
    mockArgv = ['node', 'src/main.js', ...args];
    process.argv = mockArgv;

    // Dynamically require and run the main function
    // This is a bit hacky, but allows us to re-run main with mocked argv
    const mainModule = require('../src/main.js');
    mainModule.main(); // Assuming main is exported or globally available

    // Restore original process.argv for subsequent tests
    process.argv = originalProcessArgv;
}

// --- Test Cases ---

// Test 1: Basic encoding and decoding
console.log('\n--- Test 1: Basic Encoding/Decoding ---');
runTestCommand(['encode', 'Hello']);
const encodedHello = consoleOutput[0].replace('Cosmic Pulses: ', '');
consoleOutput = []; // Clear for decode test
runTestCommand(['decode', encodedHello]);
const decodedHello = consoleOutput[0].replace('Decoded Message: ', '');
assert.strictEqual(decodedHello, 'Hello', 'Test 1 Failed: Basic encode/decode mismatch');
console.log('Test 1 Passed');

// Test 2: Encoding with spaces and punctuation
console.log('\n--- Test 2: Spaces and Punctuation ---');
runTestCommand(['encode', 'ApocalypsAI is fun!']);
const encodedApoc = consoleOutput[0].replace('Cosmic Pulses: ', '');
consoleOutput = [];
runTestCommand(['decode', encodedApoc]);
const decodedApoc = consoleOutput[0].replace('Decoded Message: ', '');
assert.strictEqual(decodedApoc, 'ApocalypsAI is fun!', 'Test 2 Failed: Spaces/punctuation mismatch');
console.log('Test 2 Passed');

// Test 3: Empty message encoding
console.log('\n--- Test 3: Empty Message Encoding ---');
runTestCommand(['encode', '']);
const encodedEmpty = consoleOutput[0].replace('Cosmic Pulses: ', '');
assert.strictEqual(encodedEmpty, '', 'Test 3 Failed: Empty message encoding incorrect');
consoleOutput = [];
runTestCommand(['decode', '']);
const decodedEmpty = consoleOutput[0].replace('Decoded Message: ', '');
assert.strictEqual(decodedEmpty, '', 'Test 3 Failed: Empty message decoding incorrect');
console.log('Test 3 Passed');

// Test 4: Message with special characters (should still work via ASCII)
console.log('\n--- Test 4: Special Characters ---');
runTestCommand(['encode', '€£¥']);
const encodedSpecial = consoleOutput[0].replace('Cosmic Pulses: ', '');
consoleOutput = [];
runTestCommand(['decode', encodedSpecial]);
const decodedSpecial = consoleOutput[0].replace('Decoded Message: ', '');
assert.strictEqual(decodedSpecial, '€£¥', 'Test 4 Failed: Special characters mismatch');
console.log('Test 4 Passed');

// Test 5: Longer message to check modulation consistency
console.log('\n--- Test 5: Longer Message Consistency ---');
const longMessage = 'This is a much longer message to test the cosmic modulation algorithm thoroughly.';
runTestCommand(['encode', longMessage]);
const encodedLong = consoleOutput[0].replace('Cosmic Pulses: ', '');
consoleOutput = [];
runTestCommand(['decode', encodedLong]);
const decodedLong = consoleOutput[0].replace('Decoded Message: ', '');
assert.strictEqual(decodedLong, longMessage, 'Test 5 Failed: Longer message mismatch');
console.log('Test 5 Passed');

// Test 6: Ensure different messages produce different pulse sequences (highly probable)
console.log('\n--- Test 6: Different Messages, Different Pulses ---');
runTestCommand(['encode', 'abc']);
const pulses1 = consoleOutput[0].replace('Cosmic Pulses: ', '');
consoleOutput = [];
runTestCommand(['encode', 'abd']);
const pulses2 = consoleOutput[0].replace('Cosmic Pulses: ', '');
assert.notStrictEqual(pulses1, pulses2, 'Test 6 Failed: Identical pulses for different messages');
console.log('Test 6 Passed');

// Restore original console.log and process.argv
console.log = originalConsoleLog;
process.argv = originalProcessArgv;

console.log('\nAll tests completed.');
