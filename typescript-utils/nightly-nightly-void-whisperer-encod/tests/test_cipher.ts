import { encode, decode } from '../src/cipher';

// Mock rationale: Testing symmetric cipher behavior with known inputs and outputs.

console.assert(encode('hello') === 'svool', 'Encoding failed for "hello"');
console.assert(decode('svool') === 'hello', 'Decoding failed for "svool"');
console.assert(encode('world') === 'dliow', 'Encoding failed for "world"');
console.assert(decode('dliow') === 'world', 'Decoding failed for "dliow"');
console.assert(encode('typescript') === 'gbkvhxirkg', 'Encoding failed for "typescript"');
console.assert(decode('gbkvhxirkg') === 'typescript', 'Decoding failed for "gbkvhxirkg"');

console.log('All tests passed!');
