const assert = require('assert');
const { selectEmoji } = require('../src/index');

function testSelectEmoji() {
  assert.strictEqual(selectEmoji('Fix bug in parser'), '+1');
  assert.strictEqual(selectEmoji('Add new feature for login'), 'rocket');
  assert.strictEqual(selectEmoji('Update docs for API'), 'book');
  assert.strictEqual(selectEmoji('Refactor code base'), 'eyes');
  assert.strictEqual(selectEmoji(''), 'eyes');
}

testSelectEmoji();
console.log('All emoji selector tests passed');
