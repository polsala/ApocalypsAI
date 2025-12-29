const assert = require('assert');
const { generateBoard } = require('../src/utils.js');

const board = generateBoard();
assert(Array.isArray(board), 'Board should be an array');
assert.strictEqual(board.length, 5, 'Board should have 5 rows');
board.forEach((row, i) => {
  assert(Array.isArray(row), `Row ${i} should be an array`);
  assert.strictEqual(row.length, 5, `Row ${i} should have 5 columns`);
  row.forEach((cell, j) => {
    assert(typeof cell === 'string', `Cell [${i}][${j}] should be a string`);
  });
});
console.log('All tests passed.');
