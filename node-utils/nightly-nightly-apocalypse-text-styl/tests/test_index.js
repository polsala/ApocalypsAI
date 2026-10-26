import assert from 'assert';
import { stylize } from '../src/index.js';

function testBasicLeet() {
  const input = 'Apocalypse';
  const expected = '4p0c4lyp53';
  assert.strictEqual(stylize(input, { noise: false }), expected);
}

function testNoiseAddsStatic() {
  const input = 'test case';
  const base = stylize(input, { noise: false });
  const noisy = stylize(input);
  assert.notStrictEqual(noisy, base, 'Noisy output should differ from base');
  const staticChars = ['~', '*', '^', '`'];
  const containsStatic = staticChars.some(c => noisy.includes(c));
  assert.ok(containsStatic, 'Noisy output should contain at least one static character');
}

testBasicLeet();
testNoiseAddsStatic();
console.log('All tests passed');
