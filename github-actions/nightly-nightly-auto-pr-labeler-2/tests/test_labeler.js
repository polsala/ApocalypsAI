const { getLabelFromTitle } = require('../src/labeler');
const assert = require('assert');

function runTests() {
  // Mock titles and expected labels
  assert.strictEqual(getLabelFromTitle('feat: add new API'), 'feature');
  assert.strictEqual(getLabelFromTitle('Fix bug in parser'), 'bug');
  assert.strictEqual(getLabelFromTitle('docs: update README'), 'documentation');
  assert.strictEqual(getLabelFromTitle('chore: clean up workspace'), 'chore');
  assert.strictEqual(getLabelFromTitle('refactor: improve logic flow'), 'refactor');
  assert.strictEqual(getLabelFromTitle('random title with no prefix'), null);
  console.log('All labeler tests passed');
}

runTests();
