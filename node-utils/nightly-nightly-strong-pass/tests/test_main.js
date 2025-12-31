const assert = require('assert');
const { evaluate } = require('../src/main');

function testScore(pwd, expectedScore) {
  const { score } = evaluate(pwd);
  assert.strictEqual(score, expectedScore, `Score for "${pwd}" should be ${expectedScore}`);
}

function testSuggestions(pwd, expectedSuggestions) {
  const { suggestions } = evaluate(pwd);
  assert.deepStrictEqual(suggestions.sort(), expectedSuggestions.sort(), `Suggestions for "${pwd}"`);
}

// Test cases
testScore('abc', 0); // too short, no variety
testScore('abcdefgh', 20); // length 8, only lower
testScore('Abcdefgh', 30); // length 8, lower+upper
testScore('Abcdefgh1', 40); // add digit
testScore('Abcdefgh1!', 50); // add symbol
testScore('Abcdefgh1!Abcdefgh1!', 100); // long and varied

testSuggestions('abc', ['Add uppercase letters', 'Add digits', 'Add symbols', 'Increase length']);
testSuggestions('Abcdefgh', ['Add digits', 'Add symbols', 'Increase length']);
testSuggestions('Abcdefgh1', ['Add symbols', 'Increase length']);
testSuggestions('Abcdefgh1!', []);

console.log('All tests passed.');
