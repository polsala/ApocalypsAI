import { strict as assert } from 'assert';
import { getAnsiEscape, paintSample } from '../src/index';

// Mock rationale: deterministic checks of ANSI codes
assert.equal(getAnsiEscape('red'), '\x1b[31m');
assert.equal(getAnsiEscape('#00ff00'), '\x1b[38;2;0;255;0m');

// paintSample should contain the escape code and reset sequence
const sample = paintSample('blue');
assert.ok(sample.includes('\x1b[34m'), 'contains blue code');
assert.ok(sample.includes('\x1b[0m'), 'contains reset code');

console.log('All tests passed.');
