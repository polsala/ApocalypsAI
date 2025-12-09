const assert = require('assert');
const { getJoke } = require('../src/index.js');

// Mock Math.random to return 0.5
const originalRandom = Math.random;
Math.random = () => 0.5;

const joke = getJoke();
assert.strictEqual(joke, "I told my computer I needed a break, and it said 'No problem, I'll go to sleep.' 😴");

Math.random = originalRandom;
console.log('All tests passed.');
