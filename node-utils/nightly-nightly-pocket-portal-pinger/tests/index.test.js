import { checkPortal, main } from '../src/index.js';
import assert from 'assert';
import { promises as fs } from 'fs'; // Import fs/promises for mocking
import fetch from 'node-fetch'; // Import node-fetch for mocking

// Mock rationale: We need to control file system and network operations
// to ensure tests are deterministic and offline. This involves replacing
// fs.readFile, fs.access, and global.fetch with controlled functions.

const originalFsReadFile = fs.readFile;
const originalFsAccess = fs.access;
const originalFetch = global.fetch; // node-fetch usually patches global.fetch

let consoleOutput = [];
const originalConsoleLog = console.log;
const originalConsoleError = console.error;

function mockConsole() {
    consoleOutput = [];
    console.log = (...args) => consoleOutput.push(args.join(' '));
    console.error = (...args) => consoleOutput.push(args.join(' '));
}

function restoreConsole() {
    console.log = originalConsoleLog;
    console.error = originalConsoleError;
}

function setupMocks() {
    // Mock fs.access for file checks
    fs.access = async (path, mode) => {
        if (path === 'valid-local-file.txt') {
            return; // File exists
        }
        if (path === 'non-existent-local-file.txt') {
            const error = new Error('File not found');
            error.code = 'ENOENT'; // Standard Node.js error code for file not found
            throw error;
        }
        if (path === 'error-local-file.txt') {
            const error = new Error('Permission denied');
            error.code = 'EACCES'; // Standard Node.js error code for permission denied
            throw error;
        }
        throw new Error(`Mock fs.access: Unknown file path for mock: ${path}`);
    };

    // Mock fs.readFile for reading portal list
    fs.readFile = async (filePath, encoding) => {
        if (filePath === 'mock-portal-list.txt') {
            return 'https://example.com/stable\nhttp://example.com/fluctuating\nvalid-local-file.txt\nhttps://example.com/collapsed\nhttps://example.com/unreachable\nnon-existent-local-file.txt';
        }
        if (filePath === 'empty-portal-list.txt') {
            return '';
        }
        if (filePath === 'single-portal.txt') {
            return 'https://example.com/stable';
        }
        const error = new Error(`Mock readFile: Unknown file path ${filePath}`);
        error.code = 'ENOENT';
        throw error;
    };

    // Mock node-fetch (or global.fetch if node-fetch patches it)
    global.fetch = async (url, options) => {
        if (url === 'https://example.com/stable') {
            return { ok: true, status: 200, headers: new Map(), text: async () => 'OK' };
        }
        if (url === 'http://example.com/fluctuating') {
            return { ok: false, status: 404, headers: new Map(), text: async () => 'Not Found' };
        }
        if (url === 'https://example.com/collapsed') {
            return { ok: false, status: 500, headers: new Map(), text: async () => 'Server Error' };
        }
        if (url === 'https://example.com/unreachable') {
            throw new Error('Network error');
        }
        throw new Error(`Mock fetch: Unknown URL ${url}`);
    };
}

function restoreMocks() {
    fs.readFile = originalFsReadFile;
    fs.access = originalFsAccess;
    global.fetch = originalFetch;
}

async function runTests() {
    console.log('Running tests for nightly-pocket-portal-pinger...');

    // Test checkPortal function
    console.log('\n--- Testing checkPortal ---');

    // Mock setup for checkPortal
    setupMocks();

    // Test 1: Stable URL
    let result = await checkPortal('https://example.com/stable');
    assert.deepStrictEqual(result, { status: 'Stable', code: 200, type: 'URL' }, 'Test 1 Failed: Stable URL');
    console.log('Test 1 Passed: Stable URL');

    // Test 2: Fluctuating URL (404)
    result = await checkPortal('http://example.com/fluctuating');
    assert.deepStrictEqual(result, { status: 'Fluctuating', code: 404, type: 'URL' }, 'Test 2 Failed: Fluctuating URL (404)');
    console.log('Test 2 Passed: Fluctuating URL (404)');

    // Test 3: Collapsed URL (500)
    result = await checkPortal('https://example.com/collapsed');
    assert.deepStrictEqual(result, { status: 'Collapsed', code: 500, type: 'URL' }, 'Test 3 Failed: Collapsed URL (500)');
    console.log('Test 3 Passed: Collapsed URL (500)');

    // Test 4: Unreachable URL (network error)
    result = await checkPortal('https://example.com/unreachable');
    assert.strictEqual(result.status, 'Unreachable', 'Test 4 Failed: Unreachable URL (status)');
    assert.ok(result.error.includes('Network error'), 'Test 4 Failed: Unreachable URL (error message)');
    console.log('Test 4 Passed: Unreachable URL (network error)');

    // Test 5: Stable local file
    result = await checkPortal('valid-local-file.txt');
    assert.deepStrictEqual(result, { status: 'Stable', type: 'File' }, 'Test 5 Failed: Stable local file');
    console.log('Test 5 Passed: Stable local file');

    // Test 6: Fluctuating local file (not found)
    result = await checkPortal('non-existent-local-file.txt');
    assert.strictEqual(result.status, 'Fluctuating', 'Test 6 Failed: Fluctuating local file (status)');
    assert.ok(result.error.includes('File not found'), 'Test 6 Failed: Fluctuating local file (error message)');
    console.log('Test 6 Passed: Fluctuating local file (not found)');

    restoreMocks(); // Restore mocks after checkPortal tests

    // Test main function
    console.log('\n--- Testing main function ---');

    // Mock process.argv for main function
    const originalArgv = process.argv;

    // Test 7: No arguments
    mockConsole();
    process.argv = ['node', 'index.js'];
    let exitCode = 0;
    const originalProcessExit = process.exit;
    process.exit = (code) => { exitCode = code; throw new Error('process.exit called'); }; // Mock exit
    try {
        await main();
    } catch (e) {
        // Expected to catch the mocked process.exit
    }
    assert.strictEqual(exitCode, 1, 'Test 7 Failed: No arguments should exit with 1');
    assert.ok(consoleOutput[0].includes('Usage:'), 'Test 7 Failed: Usage message not displayed');
    console.log('Test 7 Passed: No arguments');
    restoreConsole();
    process.exit = originalProcessExit; // Restore exit

    // Test 8: Valid portal list file
    mockConsole();
    setupMocks(); // Re-setup mocks for main
    process.argv = ['node', 'index.js', 'mock-portal-list.txt'];
    await main();
    assert.ok(consoleOutput.some(line => line.includes('https://example.com/stable: Dimensional Stability: Stable (HTTP 200)')), 'Test 8 Failed: Stable URL not reported');
    assert.ok(consoleOutput.some(line => line.includes('http://example.com/fluctuating: Dimensional Stability: Fluctuating (HTTP 404)')), 'Test 8 Failed: Fluctuating URL not reported');
    assert.ok(consoleOutput.some(line => line.includes('valid-local-file.txt: Dimensional Stability: Stable')), 'Test 8 Failed: Local file not reported');
    assert.ok(consoleOutput.some(line => line.includes('https://example.com/collapsed: Dimensional Stability: Collapsed (HTTP 500)')), 'Test 8 Failed: Collapsed URL not reported');
    assert.ok(consoleOutput.some(line => line.includes('https://example.com/unreachable: Dimensional Stability: Unreachable (Error: Network error)')), 'Test 8 Failed: Unreachable URL not reported');
    assert.ok(consoleOutput.some(line => line.includes('non-existent-local-file.txt: Dimensional Stability: Fluctuating (Error: File not found)')), 'Test 8 Failed: Non-existent local file not reported');
    console.log('Test 8 Passed: Valid portal list file');
    restoreConsole();
    restoreMocks();

    // Test 9: Non-existent portal list file
    mockConsole();
    process.argv = ['node', 'index.js', 'non-existent-list.txt'];
    exitCode = 0;
    process.exit = (code) => { exitCode = code; throw new Error('process.exit called'); };
    try {
        await main();
    } catch (e) {
        // Expected
    }
    assert.strictEqual(exitCode, 1, 'Test 9 Failed: Non-existent list should exit with 1');
    assert.ok(consoleOutput[0].includes('Error reading portal list file: Mock readFile: Unknown file path non-existent-list.txt'), 'Test 9 Failed: Error message for non-existent list not displayed');
    console.log('Test 9 Passed: Non-existent portal list file');
    restoreConsole();
    process.exit = originalProcessExit;

    // Test 10: Empty portal list file
    mockConsole();
    setupMocks(); // Re-setup mocks for main
    process.argv = ['node', 'index.js', 'empty-portal-list.txt'];
    await main();
    assert.ok(consoleOutput.some(line => line.includes('Pocket Portal Pinger complete.')), 'Test 10 Failed: Empty list should complete');
    assert.ok(!consoleOutput.some(line => line.includes('Dimensional Stability')), 'Test 10 Failed: No portals should be checked');
    console.log('Test 10 Passed: Empty portal list file');
    restoreConsole();
    restoreMocks();

    // Test 11: Single portal in list
    mockConsole();
    setupMocks(); // Re-setup mocks for main
    process.argv = ['node', 'index.js', 'single-portal.txt'];
    await main();
    assert.ok(consoleOutput.some(line => line.includes('https://example.com/stable: Dimensional Stability: Stable (HTTP 200)')), 'Test 11 Failed: Single portal not reported');
    console.log('Test 11 Passed: Single portal in list');
    restoreConsole();
    restoreMocks();

    process.argv = originalArgv; // Restore original argv

    console.log('\nAll tests completed.');
}

// Set NODE_ENV to 'test' to prevent main() from running automatically
process.env.NODE_ENV = 'test';

runTests().catch(error => {
    console.error('An error occurred during testing:', error);
    process.exit(1);
});
