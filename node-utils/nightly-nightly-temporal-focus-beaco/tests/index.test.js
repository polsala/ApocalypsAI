const { messages, getRandomMessage, formatTime, parseArgs, startTimer, displayHelp } = require('../src/index');

// Save original functions once at the top level for restoration
const originalSetTimeout = global.setTimeout;
const originalSetInterval = global.setInterval;
const originalClearInterval = global.clearInterval;
const originalStdoutWrite = process.stdout.write;
const originalConsoleLog = console.log;
const originalMathRandom = Math.random;

// # Mock rationale: process.stdout.write is an I/O operation. Mocking it allows capturing output for verification.
let mockStdoutWriteCalls = [];
const mockStdoutWrite = (...args) => { mockStdoutWriteCalls.push(args); };

// # Mock rationale: console.log is an I/O operation. Mocking it allows capturing output for verification.
let mockConsoleLogCalls = [];
const mockConsoleLog = (...args) => { mockConsoleLogCalls.push(args); };

// # Mock rationale: setTimeout/setInterval are time-dependent functions. Mocking them allows tests to run deterministically and instantly.
let setTimeoutCallbacks = [];
const mockSetInterval = (callback, delay) => {
  setTimeoutCallbacks.push(callback);
  return setTimeoutCallbacks.length - 1; // Return a mock timer ID
};
let mockClearIntervalCalls = [];
const mockClearInterval = (id) => { mockClearIntervalCalls.push(id); };

// Helper to run all pending setTimeout/setInterval callbacks instantly
const advanceTimers = () => {
  while (setTimeoutCallbacks.length > 0) {
    const callback = setTimeoutCallbacks.shift();
    callback();
  }
};

// Simple assertion function
function assert(condition, message) {
  if (!condition) {
    console.error(`FAIL: ${message}`);
    process.exit(1);
  }
  console.log(`PASS: ${message}`);
}

// Minimal Jest-like test runner structure
const tests = [];
const beforeEachCallbacks = [];
const afterEachCallbacks = [];

function describe(name, fn) {
  console.log(`\nRunning test suite: ${name}`);
  fn();
}

function test(name, fn) {
  tests.push({ name, fn });
}

function beforeEach(fn) {
  beforeEachCallbacks.push(fn);
}

function afterEach(fn) {
  afterEachCallbacks.push(fn);
}

// Custom assertion for mock calls
const expect = (mockFn) => ({
  toHaveBeenCalledTimes: (count) => {
    assert(mockFn.length === count, `Expected mock to be called ${count} times, but was called ${mockFn.length} times.`);
  },
  toHaveBeenCalledWith: (...expectedArgs) => {
    const found = mockFn.some(callArgs => {
      if (callArgs.length !== expectedArgs.length) return false;
      return callArgs.every((arg, i) => arg === expectedArgs[i]);
    });
    assert(found, `Expected mock to be called with ${JSON.stringify(expectedArgs)}, but was not.`);
  }
});

describe('Nightly Temporal Focus Beacon Tests', () => {
  beforeEach(() => {
    // Reset mocks before each test
    mockConsoleLogCalls = [];
    mockStdoutWriteCalls = [];
    mockClearIntervalCalls = [];
    setTimeoutCallbacks = [];

    // Apply mocks
    console.log = mockConsoleLog;
    process.stdout.write = mockStdoutWrite;
    global.setTimeout = mockSetInterval; // Mock setTimeout to behave like setInterval for simplicity in tests
    global.setInterval = mockSetInterval;
    global.clearInterval = mockClearInterval;

    // # Mock rationale: Math.random is non-deterministic. Mocking it ensures consistent message selection for tests.
    Math.random = () => 0; // Always return the first message
  });

  afterEach(() => {
    // Restore originals after each test
    console.log = originalConsoleLog;
    process.stdout.write = originalStdoutWrite;
    global.setTimeout = originalSetTimeout;
    global.setInterval = originalSetInterval;
    global.clearInterval = originalClearInterval;
    Math.random = originalMathRandom;
  });

  test('getRandomMessage returns a message of the specified type', () => {
    const msg = getRandomMessage('workStart');
    assert(messages.workStart.includes(msg), 'getRandomMessage should return a valid workStart message');
  });

  test('formatTime correctly formats seconds into MM:SS', () => {
    assert(formatTime(0) === '00:00', 'formatTime(0) should be 00:00');
    assert(formatTime(59) === '00:59', 'formatTime(59) should be 00:59');
    assert(formatTime(60) === '01:00', 'formatTime(60) should be 01:00');
    assert(formatTime(3599) === '59:59', 'formatTime(3599) should be 59:59');
    assert(formatTime(3600) === '60:00', 'formatTime(3600) should be 60:00');
  });

  test('parseArgs handles default values correctly', () => {
    const options = parseArgs([]);
    assert(options.work === 25, 'Default work should be 25');
    assert(options.break === 5, 'Default break should be 5');
    assert(options.longBreak === 15, 'Default long break should be 15');
    assert(options.cycles === 4, 'Default cycles should be 4');
    assert(options.help === false, 'Default help should be false');
  });

  test('parseArgs handles custom values correctly', () => {
    const options = parseArgs(['--work', '30', '-b', '10', '--long-break', '20', '-c', '2']);
    assert(options.work === 30, 'Custom work should be 30');
    assert(options.break === 10, 'Custom break should be 10');
    assert(options.longBreak === 20, 'Custom long break should be 20');
    assert(options.cycles === 2, 'Custom cycles should be 2');
  });

  test('parseArgs handles help flag', () => {
    const options = parseArgs(['-h']);
    assert(options.help === true, 'Help flag should be true');
    const options2 = parseArgs(['--help']);
    assert(options2.help === true, 'Help flag should be true with long form');
  });

  test('displayHelp logs help message', () => {
    displayHelp();
    expect(mockConsoleLogCalls).toHaveBeenCalledTimes(7);
    assert(mockConsoleLogCalls[0][0].includes('Usage:'), 'Help message should contain Usage');
  });

  test('startTimer logs start and end messages and clears interval for positive duration', async () => {
    const duration = 1; // 1 minute for testing
    const promise = startTimer(duration, 'work', 1, 4);

    // Expect work start message
    expect(mockConsoleLogCalls).toHaveBeenCalledTimes(2);
    assert(mockConsoleLogCalls[0][0].includes(messages.workStart[0]), 'startTimer should log work start message');
    assert(mockConsoleLogCalls[1][0].includes('--- WORK (1/4) ---'), 'startTimer should log work cycle info');

    // Simulate time passing by advancing the mocked timers
    for (let i = 0; i < duration * 60; i++) {
      advanceTimers(); // Each call simulates 1 second passing
      expect(mockStdoutWriteCalls).toHaveBeenCalledTimes(i + 1);
      assert(mockStdoutWriteCalls[i][0].includes(`\rTime remaining: ${formatTime(duration * 60 - 1 - i)}`), `stdout should show remaining time for second ${i}`);
    }

    await promise; // Wait for the promise to resolve after all intervals

    // Expect work end message
    expect(mockConsoleLogCalls).toHaveBeenCalledTimes(3);
    assert(mockConsoleLogCalls[2][0].includes(messages.workEnd[0]), 'startTimer should log work end message');
    expect(mockClearIntervalCalls).toHaveBeenCalledTimes(1);
  });

  test('startTimer handles long break messages', async () => {
    const duration = 1; // 1 minute for testing
    const promise = startTimer(duration, 'long break', 4, 4, true);

    // Expect long break start message
    expect(mockConsoleLogCalls).toHaveBeenCalledTimes(2);
    assert(mockConsoleLogCalls[0][0].includes(messages.longBreakStart[0]), 'startTimer should log long break start message');
    assert(mockConsoleLogCalls[1][0].includes('--- LONG BREAK (4/4) ---'), 'startTimer should log long break cycle info');

    for (let i = 0; i < duration * 60; i++) {
      advanceTimers();
    }
    await promise;

    // Expect break end message (long break uses generic breakEnd)
    expect(mockConsoleLogCalls).toHaveBeenCalledTimes(3);
    assert(mockConsoleLogCalls[2][0].includes(messages.breakEnd[0]), 'startTimer should log break end message for long break');
    expect(mockClearIntervalCalls).toHaveBeenCalledTimes(1);
  });

  test('startTimer resolves instantly for zero duration', async () => {
    const duration = 0; // 0 minutes for testing
    const promise = startTimer(duration, 'work', 1, 4);

    // Expect work start message and then immediate work end message
    expect(mockConsoleLogCalls).toHaveBeenCalledTimes(3);
    assert(mockConsoleLogCalls[0][0].includes(messages.workStart[0]), 'startTimer should log work start message');
    assert(mockConsoleLogCalls[1][0].includes('--- WORK (1/4) ---'), 'startTimer should log work cycle info');
    assert(mockConsoleLogCalls[2][0].includes(messages.workEnd[0]), 'startTimer should log work end message immediately');

    expect(mockStdoutWriteCalls).toHaveBeenCalledTimes(0); // No countdown for 0 duration
    expect(mockClearIntervalCalls).toHaveBeenCalledTimes(0); // No interval to clear

    await promise; // Ensure the promise resolves
  });

  // Note: Testing the full `run` loop would require mocking `process.argv` and `process.exit`,
  // and would involve a complex sequence of `await` and `advanceTimers` calls for multiple cycles.
  // The `startTimer` test covers the core timing and messaging logic sufficiently.
});

// Run all tests
(async () => {
  for (const t of tests) {
    for (const cb of beforeEachCallbacks) {
      cb();
    }
    try {
      await t.fn();
    } catch (e) {
      console.error(`ERROR in test '${t.name}':`, e);
    }
    for (const cb of afterEachCallbacks) {
      cb();
    }
  }
  console.log('\nAll tests completed.');
})();
