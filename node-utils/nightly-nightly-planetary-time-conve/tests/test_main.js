// tests/test_main.js
const assert = require('assert');
const { convertEarthToPlanet } = require('../src/main');

// Helper to compare result objects
function expectEqual(actual, expected) {
  assert.strictEqual(actual.sol, expected.sol, 'sol mismatch');
  assert.strictEqual(actual.hour, expected.hour, 'hour mismatch');
  assert.strictEqual(actual.minute, expected.minute, 'minute mismatch');
  assert.strictEqual(actual.second, expected.second, 'second mismatch');
}

// Test case 1: Mars, 1 hour after epoch
const marsResult = convertEarthToPlanet('1970-01-01T01:00:00Z', 'mars');
// Expected calculation (see README):
// Earth seconds = 3600
// Mars factor = 88775.244 / 86400 ≈ 1.027491251
// Planet seconds ≈ 3698.968 → sol 0, 01:01:38.968 → rounded seconds = 39
expectEqual(marsResult, { sol: 0, hour: 1, minute: 1, second: 39 });

// Test case 2: Venus, same Earth time
const venusResult = convertEarthToPlanet('1970-01-01T01:00:00Z', 'venus');
// Venus factor = 20995200 / 86400 = 243
// Planet seconds = 3600 * 243 = 874800
// Sol 0, hour = floor(874800/3600) = 242, minute = 0, second = 0
expectEqual(venusResult, { sol: 0, hour: 242, minute: 0, second: 0 });

// Test case 3: Invalid planet should throw
let threw = false;
try {
  convertEarthToPlanet('1970-01-01T01:00:00Z', 'pluto');
} catch (e) {
  threw = true;
  assert.ok(e.message.includes('Unsupported planet'));
}
assert.ok(threw, 'Expected error for unsupported planet');

// Test case 4: Invalid timestamp should throw
threw = false;
try {
  convertEarthToPlanet('not-a-date', 'mars');
} catch (e) {
  threw = true;
  assert.ok(e.message.includes('Invalid ISO timestamp'));
}
assert.ok(threw, 'Expected error for invalid timestamp');

console.log('All tests passed.');
