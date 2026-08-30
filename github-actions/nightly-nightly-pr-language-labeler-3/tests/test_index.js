const assert = require('assert');
const {detectLabels} = require('../src/index');

function testDetect() {
  const files = [
    'app/main.py',
    'lib/util.js',
    'scripts/deploy.sh',
    'README.md',
    'src/component.ts',
    'Dockerfile' // no extension mapping, should be ignored
  ];
  const labels = detectLabels(files);
  const expected = [
    'language:python',
    'language:javascript',
    'language:shell',
    'language:markdown',
    'language:typescript'
  ];
  // Sort both arrays for order‑independent comparison
  assert.deepStrictEqual(labels.sort(), expected.sort());
}

testDetect();
console.log('All tests passed');
