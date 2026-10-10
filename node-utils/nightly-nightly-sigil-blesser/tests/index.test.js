const { test, mock } = require('node:test');
const assert = require('node:assert');
const path = require('node:path');
const fs = require('node:fs'); // Use node:fs for mocking

// Mock the entire 'fs' module for isolation
mock.mockModule('node:fs', {
    ...fs, // Keep original fs functions that are not mocked
    readFileSync: mock.fn((filePath, encoding) => {
        // Mock rationale: Simulate file content without actual disk access.
        if (filePath.includes('test_file.txt')) {
            return 'This is a test file content.';
        }
        if (filePath.includes('empty_file.txt')) {
            return '';
        }
        if (filePath.includes('sigils.json')) {
            // Mock rationale: Simulate existing log file content.
            return JSON.stringify([
                {
                    "timestamp": "2023-01-01T00:00:00.000Z",
                    "filePath": "/mock/path/old_file.txt",
                    "sigil": "oldhash-Old-Entry"
                }
            ]);
        }
        throw new Error(`ENOENT: no such file or directory, open '${filePath}'`);
    }),
    writeFileSync: mock.fn((filePath, data, encoding) => {
        // Mock rationale: Prevent actual disk writes during tests.
        // Store the written content in a mock variable for assertion.
        mock.writeFileSync.mock.calls.push({ filePath, data, encoding });
    }),
    existsSync: mock.fn((filePath) => {
        // Mock rationale: Control existence of files for test scenarios.
        if (filePath.includes('test_file.txt') || filePath.includes('empty_file.txt')) {
            return true;
        }
        if (filePath.includes('sigils.json')) {
            // Assume sigils.json exists if readSigilLog is called
            return true;
        }
        return false;
    })
});

// Import the module after mocking fs
const { generateSigil, readSigilLog, writeSigilLog, blessFile, _adjectives, _nouns } = require('../src/index.js');

test('generateSigil creates a correct sigil', () => {
    // Mock rationale: Ensure deterministic random word selection for consistent test results.
    mock.method(Math, 'random', () => 0); // Always pick the first adjective and noun

    const content = 'hello world';
    const expectedHashPart = '5d41402a'; // MD5 hash of 'hello world' starts with this
    const expectedAdjective = _adjectives[0]; // Whispering
    const expectedNoun = _nouns[0]; // Orb
    const expectedSigil = `${expectedHashPart}-${expectedAdjective}-${expectedNoun}`;

    const sigil = generateSigil(content);
    assert.strictEqual(sigil, expectedSigil, 'Sigil should match expected format and content');

    mock.restoreAll(); // Restore Math.random
});

test('readSigilLog reads existing log file', () => {
    const log = readSigilLog();
    assert.deepStrictEqual(log, [
        {
            "timestamp": "2023-01-01T00:00:00.000Z",
            "filePath": "/mock/path/old_file.txt",
            "sigil": "oldhash-Old-Entry"
        }
    ], 'Should read and parse existing log entries');
});

test('readSigilLog returns empty array if log file does not exist', () => {
    // Mock rationale: Simulate a scenario where the log file is absent.
    mock.mockImplementationOnce(fs.existsSync, (filePath) => false);
    const log = readSigilLog();
    assert.deepStrictEqual(log, [], 'Should return an empty array if log file does not exist');
});

test('writeSigilLog writes log entries to file', () => {
    const testEntries = [{ timestamp: "now", filePath: "/test", sigil: "test-sigil" }];
    writeSigilLog(testEntries);

    const calls = mock.writeFileSync.mock.calls;
    assert.strictEqual(calls.length, 1, 'writeFileSync should be called once');
    assert.strictEqual(calls[0].filePath, path.join(__dirname, '..', 'sigils.json'), 'Should write to the correct log file path');
    assert.strictEqual(calls[0].data, JSON.stringify(testEntries, null, 2), 'Should write correct JSON content');
});

test('blessFile successfully processes a file and updates log', async () => {
    // Mock rationale: Ensure deterministic random word selection for consistent test results.
    mock.method(Math, 'random', () => 0.5); // Pick middle adjective and noun

    // Clear previous write calls for this test
    mock.writeFileSync.mock.calls = [];

    const filePath = 'test_file.txt';
    const expectedFileContent = 'This is a test file content.';
    const expectedHashPart = '25529f52'; // MD5 hash of 'This is a test file content.'
    const expectedAdjective = _adjectives[Math.floor(0.5 * _adjectives.length)]; // Glimmering
    const expectedNoun = _nouns[Math.floor(0.5 * _nouns.length)]; // Shard
    const expectedSigil = `${expectedHashPart}-${expectedAdjective}-${expectedNoun}`;

    const sigil = await blessFile(filePath);

    assert.strictEqual(sigil, expectedSigil, 'blessFile should return the correct sigil');

    const readCalls = mock.readFileSync.mock.calls;
    assert.strictEqual(readCalls.length, 2, 'readFileSync should be called twice (file content + log)');
    assert.ok(readCalls[0].args[0].includes(filePath), 'Should read the specified file content');

    const writeCalls = mock.writeFileSync.mock.calls;
    assert.strictEqual(writeCalls.length, 1, 'writeFileSync should be called once to update log');

    const writtenLog = JSON.parse(writeCalls[0].data);
    assert.strictEqual(writtenLog.length, 2, 'Log should contain old entry and new entry');
    assert.strictEqual(writtenLog[1].sigil, expectedSigil, 'New log entry should have the correct sigil');
    assert.ok(writtenLog[1].filePath.includes(path.resolve(filePath)), 'New log entry should have the correct absolute file path');

    mock.restoreAll(); // Restore Math.random
});

test('blessFile handles non-existent file gracefully', async () => {
    const originalProcessExit = process.exit;
    const originalConsoleError = console.error;
    let exitCode = null;
    let errorMessage = '';

    // Mock rationale: Prevent actual process exit and capture error output.
    process.exit = mock.fn((code) => { exitCode = code; });
    console.error = mock.fn((message) => { errorMessage += message; });

    const nonExistentFilePath = 'non_existent_file.txt';
    await blessFile(nonExistentFilePath);

    assert.strictEqual(exitCode, 1, 'Process should exit with code 1');
    assert.ok(errorMessage.includes(`Error: File not found at '${path.resolve(nonExistentFilePath)}'`), 'Should log file not found error');

    process.exit = originalProcessExit; // Restore original
    console.error = originalConsoleError; // Restore original
});

test('blessFile handles empty file content', async () => {
    // Mock rationale: Ensure deterministic random word selection for consistent test results.
    mock.method(Math, 'random', () => 0.9); // Pick last adjective and noun

    mock.writeFileSync.mock.calls = []; // Clear previous write calls

    const filePath = 'empty_file.txt';
    const expectedFileContent = '';
    const expectedHashPart = 'd41d8cd9'; // MD5 hash of '' (empty string)
    const expectedAdjective = _adjectives[_adjectives.length - 1]; // Void-touched
    const expectedNoun = _nouns[_nouns.length - 1]; // Chronicle
    const expectedSigil = `${expectedHashPart}-${expectedAdjective}-${expectedNoun}`;

    const sigil = await blessFile(filePath);

    assert.strictEqual(sigil, expectedSigil, 'blessFile should return the correct sigil for empty file');

    const writeCalls = mock.writeFileSync.mock.calls;
    const writtenLog = JSON.parse(writeCalls[0].data);
    assert.strictEqual(writtenLog[1].sigil, expectedSigil, 'New log entry should have the correct sigil for empty file');

    mock.restoreAll(); // Restore Math.random
});

test('blessFile handles no file path argument', async () => {
    const originalProcessExit = process.exit;
    const originalConsoleError = console.error;
    let exitCode = null;
    let errorMessage = '';

    // Mock rationale: Prevent actual process exit and capture error output.
    process.exit = mock.fn((code) => { exitCode = code; });
    console.error = mock.fn((message) => { errorMessage += message; });

    await blessFile(null); // Call with no path

    assert.strictEqual(exitCode, 1, 'Process should exit with code 1');
    assert.ok(errorMessage.includes("Error: Please provide a file path."), 'Should log error for missing file path');

    process.exit = originalProcessExit; // Restore original
    console.error = originalConsoleError; // Restore original
});
