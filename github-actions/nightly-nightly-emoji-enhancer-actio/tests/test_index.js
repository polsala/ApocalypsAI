process.env['INPUT_TEXT'] = 'Hello World';
process.env['INPUT_SEED'] = '3';
require('../src/index.js');
const result = process.env['OUTPUT_ENHANCED_TEXT'];
if (result !== '🔥 Hello World') {
  console.error(`Test failed: expected "🔥 Hello World", got "${result}"`);
  process.exit(1);
}
console.log('All tests passed');
