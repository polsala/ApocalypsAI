const { encode, decode } = require('../src/index');

// Mock rationale: Testing deterministic transformations without external dependencies.

console.assert(encode('hello') === 'svool', 'Encoding failed for "hello"');
console.assert(encode('world') === 'dliow', 'Encoding failed for "world"');
console.assert(decode('svool') === 'hello', 'Decoding failed for "svool"');
console.assert(decode('dliow') === 'world', 'Decoding failed for "dliow"');
console.assert(encode('Apocalypse') === 'Zkxlkzsv', 'Encoding failed for "Apocalypse"');
console.assert(decode('Zkxlkzsv') === 'Apocalypse', 'Decoding failed for "Zkxlkzsv"');
console.log('All tests passed!');
