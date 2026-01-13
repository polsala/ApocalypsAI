const assert = require('assert');
const { getForecast } = require('../src/forecast');

// Expected output computed from the deterministic hash algorithm
const expected = 'Silent snowfall of ash with a temperature of 3Â°C';
const actual = getForecast('Radiated Ruins');
assert.strictEqual(actual, expected);
console.log('All tests passed');
