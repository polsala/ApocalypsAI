const assert = require('assert');
const { parseDuration, formatDuration } = require('../src/index.js');

// Mock rationale: deterministic tests without external dependencies

// parse tests
assert.strictEqual(parseDuration('2h30m'), 9000, '2h30m should be 9000 seconds');
assert.strictEqual(parseDuration('45m'), 2700, '45m should be 2700 seconds');
assert.strictEqual(parseDuration('10s'), 10, '10s should be 10 seconds');
assert.strictEqual(parseDuration('1h2m3s'), 3723, '1h2m3s should be 3723 seconds');
assert.strictEqual(parseDuration(''), 0, 'empty string should be 0 seconds');

// format tests
assert.strictEqual(formatDuration(9000), '2h 30m', '9000 seconds should format to 2h 30m');
assert.strictEqual(formatDuration(2700), '45m', '2700 seconds should format to 45m');
assert.strictEqual(formatDuration(10), '10s', '10 seconds should format to 10s');
assert.strictEqual(formatDuration(3723), '1h 2m 3s', '3723 seconds should format to 1h 2m 3s');
assert.strictEqual(formatDuration(0), '0s', '0 seconds should format to 0s');

console.log('All tests passed!');
