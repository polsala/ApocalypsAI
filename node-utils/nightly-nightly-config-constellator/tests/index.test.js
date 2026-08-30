// tests/index.test.js
const assert = require('assert');
const sinon = require('sinon');
const { parseEnvContent, compareConfigs, main } = require('../src/index');
const fs = require('fs');
const path = require('path');

// Mock console.log and console.error for testing output
let consoleLogStub;
let consoleErrorStub;
let processExitStub;

function setupStubs() {
    consoleLogStub = sinon.stub(console, 'log');
    consoleErrorStub = sinon.stub(console, 'error');
    processExitStub = sinon.stub(process, 'exit');
}

function restoreStubs() {
    consoleLogStub.restore();
    consoleErrorStub.restore();
    processExitStub.restore();
}

// --- Test parseEnvContent ---
console.log('Running parseEnvContent tests...');

// Test 1: Basic .env file parsing
const basicEnvContent = `
KEY1=value1
KEY2=value2
# A comment
KEY3=value with spaces
KEY4=value=with=equals
`;
const expectedBasicEnv = {
    KEY1: 'value1',
    KEY2: 'value2',
    KEY3: 'value with spaces',
    KEY4: 'value=with=equals'
};
assert.deepStrictEqual(parseEnvContent(basicEnvContent), expectedBasicEnv, 'Test 1 Failed: Basic parsing');
console.log('  Test 1 Passed: Basic parsing');

// Test 2: Empty content
assert.deepStrictEqual(parseEnvContent(''), {}, 'Test 2 Failed: Empty content');
console.log('  Test 2 Passed: Empty content');

// Test 3: Only comments and empty lines
const commentOnlyContent = `
# Comment 1

  # Comment 2
`;
assert.deepStrictEqual(parseEnvContent(commentOnlyContent), {}, 'Test 3 Failed: Only comments');
console.log('  Test 3 Passed: Only comments');

// Test 4: Values with leading/trailing spaces
const spacedValueContent = `
KEY=  value with spaces  
`;
assert.deepStrictEqual(parseEnvContent(spacedValueContent), { KEY: 'value with spaces' }, 'Test 4 Failed: Spaced value');
console.log('  Test 4 Passed: Spaced value');

console.log('All parseEnvContent tests passed!\n');

// --- Test compareConfigs ---
console.log('Running compareConfigs tests...');

// Test 5: Two identical configs
const config5_1 = { 'FILE_A': { A: '1', B: '2' }, 'FILE_B': { A: '1', B: '2' } };
const expected5 = { missing: {}, drifting: {}, harmonized: ['A', 'B'] };
assert.deepStrictEqual(compareConfigs(config5_1), expected5, 'Test 5 Failed: Identical configs');
console.log('  Test 5 Passed: Identical configs');

// Test 6: One missing key
const config6_1 = { 'FILE_A': { A: '1', B: '2' }, 'FILE_B': { A: '1' } };
const expected6 = { missing: { 'FILE_B': ['B'] }, drifting: {}, harmonized: ['A'] };
assert.deepStrictEqual(compareConfigs(config6_1), expected6, 'Test 6 Failed: One missing key');
console.log('  Test 6 Passed: One missing key');

// Test 7: One drifting key (present in all, different values)
const config7_1 = { 'FILE_A': { A: '1', B: '2' }, 'FILE_B': { A: '1', B: '3' } };
const expected7 = { missing: {}, drifting: { B: { 'FILE_A': '2', 'FILE_B': '3' } }, harmonized: ['A'] };
assert.deepStrictEqual(compareConfigs(config7_1), expected7, 'Test 7 Failed: One drifting key');
console.log('  Test 7 Passed: One drifting key');

// Test 8: Multiple missing and drifting keys
const config8_1 = {
    'dev.env': { API_KEY: 'dev_key', DEBUG_MODE: 'true', PORT: '3000', FEATURE_FLAG: 'enabled' },
    'prod.env': { API_KEY: 'prod_key', PORT: '8080', DATABASE_URL: 'postgres://user:pass@host:5432/db' }
};
const expected8 = {
    missing: {
        'dev.env': ['DATABASE_URL'],
        'prod.env': ['DEBUG_MODE', 'FEATURE_FLAG']
    },
    drifting: {
        API_KEY: { 'dev.env': 'dev_key', 'prod.env': 'prod_key' },
        PORT: { 'dev.env': '3000', 'prod.env': '8080' }
    },
    harmonized: []
};
assert.deepStrictEqual(compareConfigs(config8_1), expected8, 'Test 8 Failed: Complex scenario');
console.log('  Test 8 Passed: Complex scenario');

// Test 9: Three files, various states (corrected logic: drifting only if in ALL files)
const config9_1 = {
    'file1.env': { A: '1', B: '2', C: '3' },
    'file2.env': { A: '1', B: '20', D: '4' },
    'file3.env': { A: '1', C: '30', D: '4' }
};
const expected9_corrected = {
    missing: {
        'file3.env': ['B'],
        'file2.env': ['C'],
        'file1.env': ['D']
    },
    drifting: {}, // No keys are present in ALL files AND have different values
    harmonized: ['A']
};
assert.deepStrictEqual(compareConfigs(config9_1), expected9_corrected, 'Test 9 Failed: Three files, corrected logic');
console.log('  Test 9 Passed: Three files, corrected logic');

console.log('All compareConfigs tests passed!\n');

// --- Test main function (CLI behavior) ---
console.log('Running main function tests...');

// Mock fs.readFileSync
let readFileSyncStub;

// Test 10: Successful comparison with two files
setupStubs();
readFileSyncStub = sinon.stub(fs, 'readFileSync');
readFileSyncStub.withArgs('mock_dev.env', 'utf8').returns('API_KEY=dev_key\nPORT=3000');
readFileSyncStub.withArgs('mock_prod.env', 'utf8').returns('API_KEY=prod_key\nPORT=8080');
// Mock rationale: Simulates reading .env files from disk without actual file I/O.
// This ensures deterministic tests regardless of the file system state.

main(['mock_dev.env', 'mock_prod.env']);

assert.strictEqual(consoleLogStub.callCount > 0, true, 'Test 10 Failed: console.log should be called');
assert.strictEqual(consoleLogStub.calledWithMatch('🌌 Aligning Config Constellations 🌌'), true, 'Test 10 Failed: Expected header not found');
assert.strictEqual(consoleLogStub.calledWithMatch('API_KEY:'), true, 'Test 10 Failed: API_KEY drifting not reported');
assert.strictEqual(consoleLogStub.calledWithMatch('PORT:'), true, 'Test 10 Failed: PORT drifting not reported');
assert.strictEqual(processExitStub.notCalled, true, 'Test 10 Failed: process.exit should not be called on success');

restoreStubs();
readFileSyncStub.restore();
console.log('  Test 10 Passed: Successful comparison');

// Test 11: Error reading a file
setupStubs();
readFileSyncStub = sinon.stub(fs, 'readFileSync');
readFileSyncStub.withArgs('non_existent.env', 'utf8').throws(new Error('File not found'));
// Mock rationale: Simulates a file read error, ensuring the utility handles it gracefully.

main(['non_existent.env']);

assert.strictEqual(consoleErrorStub.calledWithMatch('Error reading file non_existent.env: File not found'), true, 'Test 11 Failed: Error message not displayed');
assert.strictEqual(processExitStub.calledWith(1), true, 'Test 11 Failed: process.exit(1) should be called on error');

restoreStubs();
readFileSyncStub.restore();
console.log('  Test 11 Passed: Error reading file');

// Test 12: Not enough arguments
setupStubs();

main([]);

assert.strictEqual(consoleErrorStub.calledWithMatch('Usage: node src/index.js <path/to/env1> <path/to/env2> [path/to/env3 ...]'), true, 'Test 12 Failed: Usage message not displayed');
assert.strictEqual(processExitStub.calledWith(1), true, 'Test 12 Failed: process.exit(1) should be called for insufficient args');

restoreStubs();
console.log('  Test 12 Passed: Not enough arguments');

console.log('All main function tests passed!\n');

console.log('All tests completed successfully!');
