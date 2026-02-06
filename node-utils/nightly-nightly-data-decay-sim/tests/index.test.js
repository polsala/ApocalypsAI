const assert = require('assert');
const { applyDecay, decayFile } = require('../src/index');
const fs = require('fs');
const path = require('path');

// Mock rationale: We need to control file system operations to make tests deterministic and offline.
// We don't want to actually read/write files during tests.
const mockReadFileContent = 'Hello, world!';
let mockWriteFileContent = '';
let mockWriteFilePath = '';

fs.promises = {
    readFile: async (filePath, encoding) => {
        if (filePath === 'mock_input.txt') {
            return mockReadFileContent;
        }
        throw new Error('File not found');
    },
    writeFile: async (filePath, content, encoding) => {
        mockWriteFilePath = filePath;
        mockWriteFileContent = content;
        return; // Simulate successful write
    }
};

// Mock console.log and process.exit to capture output and prevent actual exit during tests
let consoleOutput = [];
const originalConsoleLog = console.log;
const originalConsoleError = console.error;
const originalProcessExit = process.exit;

function mockConsole() {
    consoleOutput = [];
    console.log = (...args) => consoleOutput.push(args.join(' '));
    console.error = (...args) => consoleOutput.push(args.join(' '));
    process.exit = (code) => { throw new Error(`Process exited with code ${code}`); }; // Throw to stop execution
}

function restoreConsole() {
    console.log = originalConsoleLog;
    console.error = originalConsoleError;
    process.exit = originalProcessExit;
}

async function runTests() {
    console.log('Running tests for Nightly Data Decay Simulator...');

    // Test 1: applyDecay with no decay (decayRate = 0)
    let testInput = 'abc';
    let decayed = applyDecay(testInput, 0, () => 0.1); // randomFn always returns 0.1, higher than 0 decayRate
    assert.strictEqual(decayed, testInput, 'Test 1 Failed: No decay should result in original text');

    // Test 2: applyDecay with full decay (decayRate = 1) and controlled random for replacement
    // Mock randomFn to always trigger decay and always choose replacement (type 0)
    // and always pick the first corruption char '!'
    let mockRandomFnReplace = (() => {
        let calls = 0;
        return () => {
            calls++;
            if (calls % 3 === 1) return 0.0; // Trigger decay (randomFn() < decayRate)
            if (calls % 3 === 2) return 0.0; // Choose decayType 0 (replace)
            return 0.0; // Choose corruption char index 0 ('!')
        };
    })();
    decayed = applyDecay(testInput, 1, mockRandomFnReplace);
    assert.strictEqual(decayed, '!!!', 'Test 2 Failed: Full decay should replace all chars with "!"');

    // Test 3: applyDecay with full decay and controlled random for deletion
    // Mock randomFn to always trigger decay and always choose deletion (type 1)
    let mockRandomFnDelete = (() => {
        let calls = 0;
        return () => {
            calls++;
            if (calls % 2 === 1) return 0.0; // Trigger decay
            return 0.4; // Choose decayType 1 (delete)
        };
    })();
    decayed = applyDecay(testInput, 1, mockRandomFnDelete);
    assert.strictEqual(decayed, '', 'Test 3 Failed: Full decay should delete all chars');

    // Test 4: applyDecay with full decay and controlled random for insertion
    // Mock randomFn to always trigger decay and always choose insertion (type 2)
    // and always pick the first corruption char '!'
    let mockRandomFnInsert = (() => {
        let calls = 0;
        return () => {
            calls++;
            if (calls % 3 === 1) return 0.0; // Trigger decay
            if (calls % 3 === 2) return 0.8; // Choose decayType 2 (insert)
            return 0.0; // Choose corruption char index 0 ('!')
        };
    })();
    decayed = applyDecay(testInput, 1, mockRandomFnInsert);
    assert.strictEqual(decayed, '!a!b!c', 'Test 4 Failed: Full decay should insert "!" before each char');

    // Test 5: decayFile - read from mock, print to stdout
    mockConsole();
    try {
        await decayFile('mock_input.txt', 1, 0, null); // No decay
        assert.strictEqual(consoleOutput[0], mockReadFileContent, 'Test 5 Failed: decayFile should print original content with no decay');
    } finally {
        restoreConsole();
    }

    // Test 6: decayFile - read from mock, write to mock output file
    mockConsole();
    try {
        await decayFile('mock_input.txt', 1, 0, 'mock_output.txt'); // No decay
        assert.strictEqual(mockWriteFilePath, 'mock_output.txt', 'Test 6 Failed: decayFile should attempt to write to specified path');
        assert.strictEqual(mockWriteFileContent, mockReadFileContent, 'Test 6 Failed: decayFile should write original content with no decay');
        assert.ok(consoleOutput[0].includes('Decayed content written to mock_output.txt'), 'Test 6 Failed: Should log successful write');
    } finally {
        restoreConsole();
    }

    // Test 7: decayFile - invalid file path
    mockConsole();
    try {
        await decayFile('non_existent.txt');
        assert.fail('Test 7 Failed: decayFile should throw error for non-existent file');
    } catch (e) {
        assert.ok(e.message.includes('Process exited with code 1'), 'Test 7 Failed: Should exit with code 1 on file read error');
        assert.ok(consoleOutput[0].includes('Error reading file non_existent.txt'), 'Test 7 Failed: Should log file read error');
    } finally {
        restoreConsole();
    }

    console.log('All tests passed!');
}

runTests().catch(err => {
    console.error('Tests failed:', err);
    restoreConsole();
    process.exit(1);
});
