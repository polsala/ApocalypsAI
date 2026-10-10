const { test, mock } = require('node:test');
const assert = require('node:assert');
const fs = require('node:fs');
const path = require('node:path');
const { loadTasks, getRandomTask, main } = require('../src/index');

// Mock rationale: fs.readFileSync is mocked to provide deterministic file contents
// for task loading, preventing reliance on actual file system state.
mock.method(fs, 'readFileSync', (filePath, encoding) => {
  if (filePath.includes('src/tasks.json')) { // Matches default tasks path
    return JSON.stringify(["Task A", "Task B", "Task C"]);
  }
  if (filePath.includes('custom-tasks.json')) { // Matches custom tasks path
    return JSON.stringify(["Custom Task 1", "Custom Task 2"]);
  }
  if (filePath.includes('empty-tasks.json')) {
    return JSON.stringify([]);
  }
  if (filePath.includes('invalid-tasks.json')) {
    return '{"not": "an array"}';
  }
  if (filePath.includes('malformed.json')) {
    return '{invalid json';
  }
  // For non-mocked paths, simulate file not found
  const error = new Error(`ENOENT: no such file or directory, open '${filePath}'`);
  error.code = 'ENOENT';
  throw error;
});

// Mock rationale: Math.random is mocked to provide deterministic random numbers
// for task selection, ensuring predictable test outcomes.
mock.method(Math, 'random', () => 0.5); // Always return 0.5 for predictable index

test('loadTasks should load tasks from a valid JSON file', () => {
  const tasks = loadTasks(path.join(__dirname, '../src/tasks.json')); // Use actual path for default
  assert.deepStrictEqual(tasks, ["Task A", "Task B", "Task C"]);
});

test('loadTasks should return an empty array for a non-existent file', () => {
  const tasks = loadTasks(path.join(__dirname, 'non-existent.json'));
  assert.deepStrictEqual(tasks, []);
});

test('loadTasks should return an empty array for an invalid JSON file', () => {
  const tasks = loadTasks(path.join(__dirname, 'malformed.json'));
  assert.deepStrictEqual(tasks, []);
});

test('loadTasks should return an empty array for a non-array JSON file', () => {
  const tasks = loadTasks(path.join(__dirname, 'invalid-tasks.json'));
  assert.deepStrictEqual(tasks, []);
});

test('getRandomTask should return a random task from the list', () => {
  const tasks = ["Task 1", "Task 2", "Task 3"];
  // With Math.random() mocked to 0.5, and tasks.length = 3,
  // Math.floor(0.5 * 3) = Math.floor(1.5) = 1.
  // So it should pick tasks[1].
  const task = getRandomTask(tasks);
  assert.strictEqual(task, "Task 2");
});

test('getRandomTask should return a default message if task list is empty', () => {
  const tasks = [];
  const task = getRandomTask(tasks);
  assert.strictEqual(task, "No tasks available. Perhaps it's time for a coffee break?");
});

test('main should print a default task if no custom file is provided', () => {
  // Mock console.log to capture output
  const consoleLog = mock.method(console, 'log', () => {});
  const consoleWarn = mock.method(console, 'warn', () => {});
  const consoleError = mock.method(console, 'error', () => {});

  // Mock rationale: process.argv is mocked to simulate CLI arguments
  // for deterministic testing of argument parsing.
  mock.method(process, 'argv', ['node', 'src/index.js']);

  main();

  // Check that 'Task B' (index 1 from mocked Math.random) from default tasks is logged
  assert.ok(consoleLog.mock.calls[2].arguments[0].includes('Task B'));
  assert.strictEqual(consoleWarn.mock.calls.length, 0);
  assert.strictEqual(consoleError.mock.calls.length, 0);

  consoleLog.mock.restore();
  consoleWarn.mock.restore();
  consoleError.mock.restore();
});

test('main should print a task from a custom file if provided', () => {
  const consoleLog = mock.method(console, 'log', () => {});
  const consoleWarn = mock.method(console, 'warn', () => {});
  const consoleError = mock.method(console, 'error', () => {});

  mock.method(process, 'argv', ['node', 'src/index.js', '--file', path.join(__dirname, 'custom-tasks.json')]);

  main();

  // Check that 'Custom Task 2' (index 1 from mocked Math.random) is logged
  assert.ok(consoleLog.mock.calls[2].arguments[0].includes('Custom Task 2'));
  assert.strictEqual(consoleWarn.mock.calls.length, 0);
  assert.strictEqual(consoleError.mock.calls.length, 0);

  consoleLog.mock.restore();
  consoleWarn.mock.restore();
  consoleError.mock.restore();
});

test('main should warn and use default tasks if custom file is empty', () => {
  const consoleLog = mock.method(console, 'log', () => {});
  const consoleWarn = mock.method(console, 'warn', () => {});
  const consoleError = mock.method(console, 'error', () => {});

  mock.method(process, 'argv', ['node', 'src/index.js', '--file', path.join(__dirname, 'empty-tasks.json')]);

  main();

  assert.ok(consoleWarn.mock.calls[0].arguments[0].includes('Custom task file was empty or invalid. Using default tasks.'));
  // Should fall back to default tasks, so 'Task B' should be logged
  assert.ok(consoleLog.mock.calls[2].arguments[0].includes('Task B'));
  assert.strictEqual(consoleError.mock.calls.length, 0);

  consoleLog.mock.restore();
  consoleWarn.mock.restore();
  consoleError.mock.restore();
});

test('main should warn and use default tasks if custom file is non-existent', () => {
  const consoleLog = mock.method(console, 'log', () => {});
  const consoleWarn = mock.method(console, 'warn', () => {});
  const consoleError = mock.method(console, 'error', () => {});

  mock.method(process, 'argv', ['node', 'src/index.js', '--file', path.join(__dirname, 'non-existent-custom.json')]);

  main();

  assert.ok(consoleError.mock.calls[0].arguments[0].includes('Error: Task file not found'));
  assert.ok(consoleWarn.mock.calls[0].arguments[0].includes('Custom task file was empty or invalid. Using default tasks.'));
  // Should fall back to default tasks, so 'Task B' should be logged
  assert.ok(consoleLog.mock.calls[2].arguments[0].includes('Task B'));

  consoleLog.mock.restore();
  consoleWarn.mock.restore();
  consoleError.mock.restore();
});

// Restore all mocks after all tests
test.after(() => {
  mock.restoreAll();
});
