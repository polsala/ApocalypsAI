import { render } from '../src/main';
import * as assert from 'assert';

function stripAnsi(str: string): string {
  return str.replace(/\x1b\[[0-9;]*m/g, '');
}

// Test rendering of the letter A with a fixed seed
const outA = render('A', 0);
const strippedA = stripAnsi(outA);
const linesA = strippedA.split('
').map(l => l.trimEnd());
assert.deepStrictEqual(linesA, [
  '  #',
  ' # #',
  '#####',
  '#   #',
  '#   #',
]);

// Test that an unknown character renders as blanks
const outUnknown = render('?', 1);
const strippedU = stripAnsi(outUnknown);
const linesU = strippedU.split('
').map(l => l.trimEnd());
assert.deepStrictEqual(linesU, [
  '',
  '',
  '',
  '',
  '',
]);

console.log('All tests passed.');

