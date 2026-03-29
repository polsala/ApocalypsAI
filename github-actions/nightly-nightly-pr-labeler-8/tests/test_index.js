const assert = require('assert');
const { computeLabels } = require('../src/index');

function testComputeLabels() {
  const mapping = { bug: 'bug', feat: 'feature', docs: 'documentation' };

  const title1 = 'Fix critical bug in parser';
  const res1 = computeLabels(title1, mapping);
  assert.deepStrictEqual(res1, ['bug']);

  const title2 = 'Add new feat for user login';
  const res2 = computeLabels(title2, mapping);
  assert.deepStrictEqual(res2, ['feature']);

  const title3 = 'Docs: update README and changelog';
  const res3 = computeLabels(title3, mapping);
  assert.deepStrictEqual(res3, ['documentation']);

  const title4 = 'Refactor code without keywords';
  const res4 = computeLabels(title4, mapping);
  assert.deepStrictEqual(res4, []);

  console.log('All computeLabels tests passed');
}

testComputeLabels();
