import assert from 'assert';
import { generateRiddle } from '../src/riddle';

const originalRandom = Math.random;
Math.random = () => 0.1; // deterministic
const riddle = generateRiddle();
assert.strictEqual(riddle.question, 'What has keys but can’t open locks?');
assert.strictEqual(riddle.answer, 'A piano.');
Math.random = originalRandom;
console.log('All tests passed.');
