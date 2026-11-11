const assert = require('assert');
const path = require('path');

// --- Mocking Setup ---
// Mock rationale: We need to prevent actual file system operations during tests
// to ensure determinism, speed, and isolation. We simulate file reads and writes
// using an in-memory store.
let mockFileContent = '[]'; // Default empty array for tasks.json

// Mock rationale: Ensure consistent IDs for testing purposes.
// In a real scenario, this would be truly random.
let mockCryptoRandomBytesReturn = 'testID';

// Create mock objects for fs.promises and crypto
const mockFsPromises = {
    readFile: async (filePath, encoding) => {
        if (filePath === path.join(__dirname, '..', 'tasks.json')) {
            // Simulate ENOENT if mockFileContent is null
            if (mockFileContent === null) {
                const error = new Error('File not found');
                error.code = 'ENOENT';
                throw error;
            }
            return mockFileContent;
        }
        throw new Error(`Mock readFile: Unexpected file path ${filePath}`);
    },
    writeFile: async (filePath, data, encoding) => {
        if (filePath === path.join(__dirname, '..', 'tasks.json')) {
            mockFileContent = data;
            return;
        }
        throw new Error(`Mock writeFile: Unexpected file path ${filePath}`);
    }
};

const mockCrypto = {
    randomBytes: (size) => {
        if (size === 3) {
            return {
                toString: (encoding) => {
                    if (encoding === 'hex') {
                        return mockCryptoRandomBytesReturn;
                    }
                    return 'mocked_buffer_string';
                }
            };
        }
        return { toString: () => 'mocked_random_bytes' };
    }
};

// Temporarily replace the modules in Node's module cache
// Mock rationale: Intercepting the `require` calls for `fs/promises` and `crypto`
// to inject our mock implementations, ensuring `taskManager.js` uses these mocks.
const fsPromisesPath = require.resolve('fs/promises');
const cryptoPath = require.resolve('crypto');

const originalFsPromisesModule = require.cache[fsPromisesPath];
const originalCryptoModule = require.cache[cryptoPath];

require.cache[fsPromisesPath] = { exports: mockFsPromises };
require.cache[cryptoPath] = { exports: mockCrypto };

// Now load the module under test, which will use the mocked dependencies
const { addTask, listTasks, forgetTask } = require('../src/taskManager');

// --- Simple Test Runner ---
const tests = [];
const beforeEachCallbacks = [];

function describe(name, fn) {
    tests.push({ name, type: 'describe', fn, children: [] });
    const currentDescribe = tests[tests.length - 1];
    const originalTests = tests;
    tests = currentDescribe.children; // Scope tests to current describe block
    fn();
    tests = originalTests; // Restore scope
}

function it(name, fn) {
    tests.push({ name, type: 'it', fn });
}

function beforeEach(fn) {
    beforeEachCallbacks.push(fn);
}

async function runTests(testSuite, indent = 0) {
    const prefix = ' '.repeat(indent * 2);
    for (const testItem of testSuite) {
        if (testItem.type === 'describe') {
            console.log(`\n${prefix}${testItem.name}`);
            const originalBeforeEach = [...beforeEachCallbacks]; // Save current callbacks
            beforeEachCallbacks.length = 0; // Clear for this describe block
            testItem.fn(); // Execute describe to populate its children and beforeEach
            await runTests(testItem.children, indent + 1);
            beforeEachCallbacks.length = 0; // Clear after describe block
            beforeEachCallbacks.push(...originalBeforeEach); // Restore original callbacks
        } else if (testItem.type === 'it') {
            try {
                for (const cb of beforeEachCallbacks) {
                    await cb(); // Await beforeEach callbacks
                }
                await testItem.fn();
                process.stdout.write(`${prefix}  ✓ ${testItem.name}\n`);
            } catch (error) {
                process.stdout.write(`${prefix}  ✗ ${testItem.name}\n`);
                console.error(error);
                process.exit(1); // Exit on first failure
            }
        }
    }
}

// --- Test Cases ---
describe('TaskManager', () => {
    beforeEach(async () => {
        // Reset mock state before each test
        mockFileContent = '[]';
        mockCryptoRandomBytesReturn = 'testID';
    });

    it('should add a task and return its ID', async () => {
        const description = 'Test task 1';
        const id = await addTask(description);

        assert.strictEqual(id, 'testID', 'Task ID should be the mocked ID');
        const writtenTasks = JSON.parse(mockFileContent);
        assert.strictEqual(writtenTasks.length, 1, 'Should have one task');
        assert.strictEqual(writtenTasks[0].description, description, 'Task description should match');
        assert.strictEqual(writtenTasks[0].id, 'testID', 'Task ID should match');
        assert.ok(writtenTasks[0].timestamp, 'Task should have a timestamp');
    });

    it('should list tasks correctly', async () => {
        mockFileContent = JSON.stringify([{ id: 'task1', description: 'Existing task', timestamp: new Date().toISOString() }]);

        const tasks = await listTasks();

        assert.strictEqual(tasks.length, 1, 'Should list one task');
        assert.strictEqual(tasks[0].description, 'Existing task', 'Listed task description should match');
    });

    it('should return an empty array if tasks.json does not exist', async () => {
        mockFileContent = null; // Simulate ENOENT

        const tasks = await listTasks();
        assert.deepStrictEqual(tasks, [], 'Should return an empty array');
    });

    it('should forget an existing task', async () => {
        mockFileContent = JSON.stringify([
            { id: 'task1', description: 'Task to keep', timestamp: new Date().toISOString() },
            { id: 'task2', description: 'Task to forget', timestamp: new Date().toISOString() }
        ]);

        const forgotten = await forgetTask('task2');

        assert.strictEqual(forgotten, true, 'forgetTask should return true for success');
        const remainingTasks = JSON.parse(mockFileContent);
        assert.strictEqual(remainingTasks.length, 1, 'Should have one task remaining');
        assert.strictEqual(remainingTasks[0].id, 'task1', 'The correct task should remain');
    });

    it('should not forget a non-existent task', async () => {
        mockFileContent = JSON.stringify([
            { id: 'task1', description: 'Task to keep', timestamp: new Date().toISOString() }
        ]);

        const forgotten = await forgetTask('nonExistentTask');

        assert.strictEqual(forgotten, false, 'forgetTask should return false for failure');
        // Ensure content remains unchanged
        const remainingTasks = JSON.parse(mockFileContent);
        assert.strictEqual(remainingTasks.length, 1, 'Task list should remain unchanged');
    });

    it('should handle multiple add operations correctly', async () => {
        mockCryptoRandomBytesReturn = 'idA';
        await addTask('First task');
        mockCryptoRandomBytesReturn = 'idB'; // Change mock ID for next add
        await addTask('Second task');

        const tasks = await listTasks();
        assert.strictEqual(tasks.length, 2, 'Should have two tasks');
        assert.strictEqual(tasks[0].id, 'idA', 'First task ID should be correct');
        assert.strictEqual(tasks[1].id, 'idB', 'Second task ID should be correct');
    });
});

// --- Run all tests ---
(async () => {
    console.log('Running tests...');
    await runTests(tests);
    console.log('\nAll tests passed!');

    // Restore original modules after tests are done
    require.cache[fsPromisesPath] = originalFsPromisesModule;
    require.cache[cryptoPath] = originalCryptoModule;
})();
