const { execSync } = require('child_process');
const path = require('path');

function run(input) {
  const script = path.resolve(__dirname, '..', 'src', 'main.js');
  // Execute the script with the provided stdin input
  return execSync(`node ${script}`, { input, encoding: 'utf8' }).trim();
}

function assertEqual(actual, expected, message) {
  if (actual !== expected) {
    throw new Error(`${message}\nExpected: ${expected}\nActual:   ${actual}`);
  }
}

// Test positive sentiment → happy emoji
(function testPositive() {
  const out = run('I am feeling great and wonderful!');
  assertEqual(out, '😊', 'Positive sentiment should yield 😊');
})();

// Test negative sentiment → sad emoji
(function testNegative() {
  const out = run('This is terrible and I am sad.');
  assertEqual(out, '☹️', 'Negative sentiment should yield ☹️');
})();

// Test neutral sentiment → neutral emoji
(function testNeutral() {
  const out = run('The sky is blue.');
  assertEqual(out, '😐', 'Neutral sentiment should yield 😐');
})();

console.log('All tests passed.');
