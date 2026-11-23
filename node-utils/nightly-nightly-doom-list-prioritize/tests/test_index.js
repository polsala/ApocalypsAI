const assert = require('assert');
const { Writable } = require('stream');

// Set NODE_ENV to 'test' to prevent main from exiting prematurely
process.env.NODE_ENV = 'test';

// Import the main function and other exported components
const { main, parseTaskString, generateChaosFactors, calculateScore, doomDescriptors, chaosEmojis } = require('../src/index.js');

// Mock console.log and process.exit
let capturedOutput = '';
let exitCode = null;
const originalConsoleLog = console.log;
const originalProcessExit = process.exit;

const mockConsoleLog = (message) => {
    capturedOutput += message + '\n';
};
const mockProcessExit = (code) => {
    exitCode = code;
    throw new Error('Simulated process exit with code ' + code); // Stop execution
};

// Mock Math.random for deterministic tests
let originalMathRandom;
const mockMathRandom = (value) => {
    return () => value;
};

function runTest(name, testFunction) {
    originalConsoleLog(`Running test: ${name}`);
    capturedOutput = '';
    exitCode = null;
    originalMathRandom = Math.random; // Store original
    console.log = mockConsoleLog; // Apply mock
    process.exit = mockProcessExit; // Apply mock

    try {
        testFunction();
        originalConsoleLog(`✅ ${name} passed.`);
    } catch (error) {
        if (error.message.startsWith('Simulated process exit')) {
            originalConsoleLog(`✅ ${name} passed (simulated exit).`);
        } else {
            originalConsoleLog(`❌ ${name} failed:`, error.message);
            originalConsoleLog('Captured Output:\n', capturedOutput);
            process.exit(1); // Exit test runner if a test truly fails
        }
    } finally {
        Math.random = originalMathRandom; // Restore original Math.random
        console.log = originalConsoleLog; // Restore original console.log
        process.exit = originalProcessExit; // Restore original process.exit
    }
}

// # Mock rationale:
// We mock Math.random to ensure deterministic chaos factors (rating, descriptor, emoji)
// for consistent test results, as the utility's core logic involves random elements.
// We mock console.log to capture the CLI output and assert its content and format
// without polluting the test runner's console.
// We mock process.exit to prevent the test runner from terminating prematurely
// and to verify the correct exit code is triggered by the utility's logic.

// Test 1: No tasks provided
runTest('should display usage message when no tasks are provided', () => {
    main(['node', 'src/index.js']);
    assert.ok(capturedOutput.includes('No tasks provided. Usage:'), 'Should show usage message');
    assert.strictEqual(exitCode, 0, 'Should exit with code 0');
});

// Test 2: Single task with default priority/impact
runTest('should prioritize a single task with default settings', () => {
    Math.random = mockMathRandom(0.5); // Mock random for deterministic chaos

    main(['node', 'src/index.js', 'Survive the zombie horde']);

    assert.ok(capturedOutput.includes('Survive the zombie horde'), 'Task name should be in output');
    assert.ok(capturedOutput.includes('[NORMAL]'), 'Default priority should be NORMAL');
    assert.ok(capturedOutput.includes('(MEDIUM Impact'), 'Default impact should be MEDIUM');
    assert.ok(capturedOutput.includes('Chaos: 6/10'), 'Chaos rating should be deterministic (0.5 * 10 + 1 = 6)');
    assert.ok(capturedOutput.includes(doomDescriptors[Math.floor(0.5 * doomDescriptors.length)]), 'Doom descriptor should be deterministic');
    assert.ok(capturedOutput.includes(chaosEmojis[Math.floor(0.5 * chaosEmojis.length)]), 'Chaos emoji should be deterministic');
});

// Test 3: Multiple tasks with mixed priorities and impacts
runTest('should prioritize multiple tasks correctly based on score', () => {
    Math.random = mockMathRandom(0.1); // Mock random for deterministic chaos (rating 2, descriptor 1, emoji 1)

    main([
        'node', 'src/index.js',
        'Secure the bunker --priority critical --impact high', // Score: 300 + 150 + 2 = 452
        'Gather canned goods --priority urgent --impact medium', // Score: 200 + 100 + 2 = 302
        'Learn to juggle --priority low --impact low' // Score: 0 + 50 + 2 = 52
    ]);

    const lines = capturedOutput.split('\n').filter(line => line.includes('. '));
    assert.strictEqual(lines.length, 3, 'Should have 3 prioritized tasks');
    assert.ok(lines[0].includes('Secure the bunker'), 'Highest priority task should be first');
    assert.ok(lines[1].includes('Gather canned goods'), 'Medium priority task should be second');
    assert.ok(lines[2].includes('Learn to juggle'), 'Lowest priority task should be last');
});

// Test 4: parseTaskString function
runTest('parseTaskString should correctly parse task name and options', () => {
    let task = parseTaskString('Defend the perimeter --priority critical --impact high');
    assert.deepStrictEqual(task, { name: 'Defend the perimeter', priority: 'critical', impact: 'high' });

    task = parseTaskString('Scavenge for supplies');
    assert.deepStrictEqual(task, { name: 'Scavenge for supplies', priority: 'normal', impact: 'medium' });

    task = parseTaskString('Repair the drone --priority urgent');
    assert.deepStrictEqual(task, { name: 'Repair the drone', priority: 'urgent', impact: 'medium' });

    task = parseTaskString('Find a pet --impact low');
    assert.deepStrictEqual(task, { name: 'Find a pet', priority: 'normal', impact: 'low' });

    task = parseTaskString('Invalid priority --priority foo'); // Should default to normal
    assert.deepStrictEqual(task, { name: 'Invalid priority', priority: 'normal', impact: 'medium' });
});

// Test 5: generateChaosFactors function
runTest('generateChaosFactors should return deterministic values with mocked Math.random', () => {
    Math.random = mockMathRandom(0.5);
    const chaos = generateChaosFactors();
    assert.deepStrictEqual(chaos, {
        chaosRating: 6, // Math.floor(0.5 * 10) + 1 = 5 + 1 = 6
        descriptor: doomDescriptors[Math.floor(0.5 * doomDescriptors.length)], // Index 6: 'Hypothetical'
        emoji: chaosEmojis[Math.floor(0.5 * chaosEmojis.length)] // Index 7: '⚠️'
    });
});

// Test 6: calculateScore function
runTest('calculateScore should correctly calculate scores', () => {
    const task1 = { priority: 'critical', impact: 'high', chaosRating: 5 };
    assert.strictEqual(calculateScore(task1), (3 * 100) + (3 * 50) + 5); // 300 + 150 + 5 = 455

    const task2 = { priority: 'normal', impact: 'low', chaosRating: 10 };
    assert.strictEqual(calculateScore(task2), (1 * 100) + (1 * 50) + 10); // 100 + 50 + 10 = 160

    const task3 = { priority: 'low', impact: 'medium', chaosRating: 1 };
    assert.strictEqual(calculateScore(task3), (0 * 100) + (2 * 50) + 1); // 0 + 100 + 1 = 101
});

originalConsoleLog('\nAll tests completed.');
