const { analyzeMood, runCli } = require('../src/index');
const assert = require('assert');

// Mock rationale: We need to capture console output and prevent process.exit for testing CLI behavior.
// Mocking console.log, console.error, and process.exit allows us to test the CLI's output and exit conditions deterministically
// without affecting the actual console or terminating the test runner.
let consoleOutput = [];
const mockConsoleLog = (message) => consoleOutput.push(message);
const mockConsoleError = (message) => consoleOutput.push(message); // Capture errors too
let mockExitCode = null;
const mockProcessExit = (code) => { mockExitCode = code; };

// Helper to reset mocks before each test
const setupMocks = () => {
  consoleOutput = [];
  mockExitCode = null;
  global.console.log = mockConsoleLog;
  global.console.error = mockConsoleError;
  global.process.exit = mockProcessExit;
};

// Helper to restore original console/process after tests
const restoreMocks = () => {
  global.console.log = console.log;
  global.console.error = console.error;
  global.process.exit = process.exit;
};

console.log('Running tests for nightly-mood-ring-cli...');

// Test cases for analyzeMood function
assert.deepStrictEqual(analyzeMood('I am so happy today, it is wonderful!'), { color: 'Rose Quartz', description: 'Radiant with optimism, a beacon of hope!' }, 'Test Case 1 Failed: Positive text');
assert.deepStrictEqual(analyzeMood('This is a terrible problem, I feel sad.'), { color: 'Obsidian Black', description: 'Reflecting deep contemplation, perhaps a touch of cosmic gloom.' }, 'Test Case 2 Failed: Negative text');
assert.deepStrictEqual(analyzeMood('The quick brown fox jumps over the lazy dog.'), { color: 'Moonstone Grey', description: 'Calm and collected, observing the cosmic dance with serene detachment.' }, 'Test Case 3 Failed: Neutral text');
assert.deepStrictEqual(analyzeMood('I love this, but it is a difficult problem.'), { color: 'Amethyst Purple', description: 'A swirl of emotions, a truly complex cosmic tapestry.' }, 'Test Case 4 Failed: Mixed text');
assert.deepStrictEqual(analyzeMood('Great success, no problems!'), { color: 'Rose Quartz', description: 'Radiant with optimism, a beacon of hope!' }, 'Test Case 5 Failed: Positive with negative keyword present but positive dominant');
assert.deepStrictEqual(analyzeMood('Awful failure, but I have hope.'), { color: 'Obsidian Black', description: 'Reflecting deep contemplation, perhaps a touch of cosmic gloom.' }, 'Test Case 6 Failed: Negative with positive keyword present but negative dominant');
assert.deepStrictEqual(analyzeMood('Joy and despair.'), { color: 'Amethyst Purple', description: 'A swirl of emotions, a truly complex cosmic tapestry.' }, 'Test Case 7 Failed: Equal positive and negative');
assert.deepStrictEqual(analyzeMood('A bright future, no dark clouds.'), { color: 'Rose Quartz', description: 'Radiant with optimism, a beacon of hope!' }, 'Test Case 8 Failed: Positive with negative keyword present but positive dominant (bright/dark)');


// Test cases for CLI behavior (runCli)
// Mock rationale: process.argv is a global variable that needs to be manipulated to simulate CLI arguments.
// We save and restore the original to ensure tests are isolated and don't affect other parts of the system.
const originalArgv = process.argv;

// Test 1: CLI with positive argument
setupMocks();
process.argv = [...originalArgv.slice(0, 2), 'I feel happy and wonderful today!'];
runCli();
assert.deepStrictEqual(consoleOutput, ['Color: Rose Quartz', 'Description: Radiant with optimism, a beacon of hope!'], 'CLI Test 1 Failed: Positive argument');
assert.strictEqual(mockExitCode, null, 'CLI Test 1 Failed: Should not exit');
restoreMocks();

// Test 2: CLI with negative argument
setupMocks();
process.argv = [...originalArgv.slice(0, 2), 'This is a terrible day, full of problems.'];
runCli();
assert.deepStrictEqual(consoleOutput, ['Color: Obsidian Black', 'Description: Reflecting deep contemplation, perhaps a touch of cosmic gloom.'], 'CLI Test 2 Failed: Negative argument');
assert.strictEqual(mockExitCode, null, 'CLI Test 2 Failed: Should not exit');
restoreMocks();

// Test 3: CLI with neutral argument
setupMocks();
process.argv = [...originalArgv.slice(0, 2), 'Just a regular day.'];
runCli();
assert.deepStrictEqual(consoleOutput, ['Color: Moonstone Grey', 'Description: Calm and collected, observing the cosmic dance with serene detachment.'], 'CLI Test 3 Failed: Neutral argument');
assert.strictEqual(mockExitCode, null, 'CLI Test 3 Failed: Should not exit');
restoreMocks();

// Test 4: CLI with mixed argument
setupMocks();
process.argv = [...originalArgv.slice(0, 2), 'I love the idea, but it has difficult problems.'];
runCli();
assert.deepStrictEqual(consoleOutput, ['Color: Amethyst Purple', 'Description: A swirl of emotions, a truly complex cosmic tapestry.'], 'CLI Test 4 Failed: Mixed argument');
assert.strictEqual(mockExitCode, null, 'CLI Test 4 Failed: Should not exit');
restoreMocks();

// Test 5: CLI with no arguments (should show usage and exit 1)
setupMocks();
process.argv = originalArgv.slice(0, 2); // No arguments
runCli();
assert.deepStrictEqual(consoleOutput, ['Usage: nightly-mood-ring <text> or echo "text" | nightly-mood-ring'], 'CLI Test 5 Failed: No arguments - usage message');
assert.strictEqual(mockExitCode, 1, 'CLI Test 5 Failed: No arguments - should exit with code 1');
restoreMocks();


console.log('All tests passed!');
