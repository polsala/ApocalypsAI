// Tests for Nightly Apocalypse Color Namer
// Mock rationale: deterministic mapping based on fixed hue/lightness ranges.

const assert = require('assert');
const { nameColor } = require('../src/index.js');

const tests = [
  { hex: '#ff0000', expected: 'Scorched Ember' }, // pure red
  { hex: '#00ff00', expected: 'Radiant Ember' }, // pure green
  { hex: '#0000ff', expected: 'Frozen Ember' }, // pure blue
  { hex: '#ffff00', expected: 'Blazing Ember' }, // yellow
  { hex: '#808080', expected: 'Scorched Ash' }   // gray
];

tests.forEach(({ hex, expected }) => {
  const result = nameColor(hex);
  assert.strictEqual(result, expected, `For ${hex}, expected "${expected}" but got "${result}"`);
});

console.log('All tests passed.');
