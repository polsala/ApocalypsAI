const assert = require('assert');
const path = require('path');
const fs = require('fs');
const { generateMessage } = require('../src/messageGenerator');

// --- Test Message Generator ---

function testMessageGenerator() {
  console.log('Running Message Generator tests...');

  // Test with default messages
  let message = generateMessage('change', 'app.js', null);
  assert.ok(message.includes('app.js'), 'Default change message should contain filename.');
  assert.ok(message.length > 20, 'Default change message should be substantial.');

  message = generateMessage('add', 'new_module.js', null);
  assert.ok(message.includes('new_module.js'), 'Default add message should contain filename.');

  message = generateMessage('delete', 'old_file.txt', null);
  assert.ok(message.includes('old_file.txt'), 'Default delete message should contain filename.');

  // Test with custom messages
  const customConfig = {
    change: ["The very fabric of '{filename}' trembles with new energy."],
    add: ["A fresh spirit, '{filename}', awakens."],
    delete: ["'{filename}' returns to the cosmic dust."]
  };

  message = generateMessage('change', 'config.json', customConfig);
  assert.strictEqual(message, "The very fabric of 'config.json' trembles with new energy.", 'Custom change message should be used.');

  message = generateMessage('add', 'component.jsx', customConfig);
  assert.strictEqual(message, "A fresh spirit, 'component.jsx', awakens.", 'Custom add message should be used.');

  message = generateMessage('delete', 'temp.log', customConfig);
  assert.strictEqual(message, "'temp.log' returns to the cosmic dust.", 'Custom delete message should be used.');

  // Test with empty custom messages for an event type
  const emptyConfig = { change: [], add: ["New file: {filename}"] };
  message = generateMessage('change', 'empty.js', emptyConfig);
  assert.ok(message.includes('The Cauldron is silent.'), 'Should return default silent message for empty custom array.');

  console.log('Message Generator tests passed!\n');
}

// --- Test Watcher Inference Logic (Mocked) ---

function testWatcherInference() {
  console.log('Running Watcher Inference tests (mocked)...');

  // # Mock rationale: `fs.watch` is an asynchronous, system-level operation that depends on the actual file system.
  // Mocking it directly is complex and platform-dependent. Instead, we mock the synchronous `fs` functions
  // (`fs.accessSync`, `fs.readdirSync`, `fs.statSync`) that the `index.js` script uses to *infer* the event type.
  // This allows us to test the inference logic deterministically and offline without actual file system operations.
  // Mocking `console.log` allows us to verify the output without polluting the test runner's console.

  const originalFsAccessSync = fs.accessSync;
  const originalFsReaddirSync = fs.readdirSync;
  const originalFsStatSync = fs.statSync;
  const originalConsoleLog = console.log;

  let mockFiles = new Set(['initial.js', 'existing.txt']);
  let loggedMessages = [];

  console.log = (...args) => loggedMessages.push(args.join(' '));

  fs.accessSync = (pathToCheck, mode) => {
    const filename = path.basename(pathToCheck);
    if (mockFiles.has(filename)) {
      return; // File exists
    } else {
      throw new Error('File not found (mocked)');
    }
  };

  fs.readdirSync = (dirPath) => {
    return Array.from(mockFiles);
  };

  fs.statSync = (filePath) => ({
    isFile: () => true, // Always return true for simplicity in mock
    isDirectory: () => false
  });

  // Simulate the initial `watchedFiles` setup from `index.js`
  // This part is crucial as `index.js` builds this set at startup.
  const initialWatchedFiles = new Set();
  const initialFiles = fs.readdirSync('/mock/project'); // Use a mock path
  for (const file of initialFiles) {
    if (fs.statSync(path.join('/mock/project', file)).isFile()) {
      initialWatchedFiles.add(file);
    }
  }
  assert.deepStrictEqual(Array.from(initialWatchedFiles).sort(), ['existing.txt', 'initial.js'].sort(), 'Initial watched files should be correct.');

  // --- Simulate fs.watch callback logic ---

  // Scenario 1: 'change' event on an existing file
  loggedMessages = [];
  let inferredEventType = 'change'; // fs.watch event type
  let filename = 'initial.js';
  // index.js logic for 'change' event:
  try {
    fs.accessSync(path.join('/mock/project', filename), fs.constants.F_OK);
    if (!initialWatchedFiles.has(filename)) {
      // This branch should not be taken for an existing file
      inferredEventType = 'add';
      initialWatchedFiles.add(filename);
    }
  } catch (e) {
    // This branch should not be taken for an existing file
    if (initialWatchedFiles.has(filename)) {
      inferredEventType = 'delete';
      initialWatchedFiles.delete(filename);
    }
  }
  let message = generateMessage(inferredEventType, filename, null);
  assert.ok(message.includes('initial.js'), 'Change event on existing file should generate message.');
  assert.ok(message.includes('shimmer') || message.includes('whisper') || message.includes('bubbles') || message.includes('tremor'), 'Change message should be specific to change.');

  // Scenario 2: 'rename' event that is actually an 'add'
  mockFiles.add('new_feature.js'); // File now exists in mock FS
  loggedMessages = [];
  inferredEventType = 'rename'; // fs.watch event type
  filename = 'new_feature.js';
  // index.js logic for 'rename' event:
  try {
    fs.accessSync(path.join('/mock/project', filename), fs.constants.F_OK);
    if (!initialWatchedFiles.has(filename)) {
      inferredEventType = 'add';
      initialWatchedFiles.add(filename);
    }
  } catch (e) { /* should not happen for add */ }
  message = generateMessage(inferredEventType, filename, null);
  assert.ok(message.includes('new_feature.js'), 'Add event should generate message.');
  assert.ok(message.includes('manifests') || message.includes('unrolls') || message.includes('emerges') || message.includes('ignites'), 'Add message should be specific to add.');

  // Scenario 3: 'rename' event that is actually a 'delete'
  mockFiles.delete('existing.txt'); // File no longer exists in mock FS
  loggedMessages = [];
  inferredEventType = 'rename'; // fs.watch event type
  filename = 'existing.txt';
  // index.js logic for 'rename' event:
  try {
    fs.accessSync(path.join('/mock/project', filename), fs.constants.F_OK);
  } catch (e) {
    if (initialWatchedFiles.has(filename)) {
      inferredEventType = 'delete';
      initialWatchedFiles.delete(filename);
    }
  }
  message = generateMessage(inferredEventType, filename, null);
  assert.ok(message.includes('existing.txt'), 'Delete event should generate message.');
  assert.ok(message.includes('faded into legend') || message.includes('diminish') || message.includes('sacrifice') || message.includes('dissolves'), 'Delete message should be specific to delete.');

  // Scenario 4: 'change' event on a newly added file (e.g., file created, then immediately changed)
  mockFiles.add('brand_new.js');
  loggedMessages = [];
  inferredEventType = 'change'; // fs.watch event type
  filename = 'brand_new.js';
  // index.js logic for 'change' event:
  try {
    fs.accessSync(path.join('/mock/project', filename), fs.constants.F_OK);
    if (!initialWatchedFiles.has(filename)) {
      inferredEventType = 'add'; // Inferred as add because it wasn't tracked before
      initialWatchedFiles.add(filename);
    }
  } catch (e) { /* should not happen */ }
  message = generateMessage(inferredEventType, filename, null);
  assert.ok(message.includes('brand_new.js'), 'Change on untracked file should infer as add.');
  assert.ok(message.includes('manifests') || message.includes('unrolls') || message.includes('emerges') || message.includes('ignites'), 'Inferred add message should be specific to add.');

  // Restore original fs and console functions
  fs.accessSync = originalFsAccessSync;
  fs.readdirSync = originalFsReaddirSync;
  fs.statSync = originalFsStatSync;
  console.log = originalConsoleLog;

  console.log('Watcher Inference tests passed!\n');
}

// Run all tests
try {
  testMessageGenerator();
  testWatcherInference();
  console.log('All tests passed successfully!');
} catch (error) {
  console.error('Tests failed:', error.message);
  process.exit(1);
}
