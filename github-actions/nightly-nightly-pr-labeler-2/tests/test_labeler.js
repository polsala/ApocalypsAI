// Mock rationale: we test the pure function `determineLabels` without contacting GitHub.
const assert = require('assert')
const { determineLabels } = require('../src/index')

function testCase(name, files, expected) {
  const result = determineLabels(files).sort()
  const expSorted = expected.sort()
  try {
    assert.deepStrictEqual(result, expSorted)
    console.log(`â ${name}`)
  } catch (e) {
    console.error(`â ${name}`)
    console.error(e.message)
    process.exit(1)
  }
}

// 1. Documentation files
testCase('Docs detection', ['README.md', 'docs/guide/introduction.md'], ['documentation'])

// 2. Test files
testCase('Test detection', ['tests/unit/example_test.py', 'src/foo.test.js'], ['tests'])

// 3. CI configuration files
testCase('CI detection', ['.github/workflows/build.yml', 'ci/config.yaml'], ['ci'])

// 4. Source code files
testCase('Code detection', ['src/main.py', 'lib/util.js', 'src/main.rs'], ['code'])

// 5. Mixed files â should combine labels without duplicates
testCase('Mixed detection', [
  'README.md',
  'docs/usage.md',
  'tests/unit/foo_test.py',
  '.github/workflows/ci.yml',
  'src/app.js'
], ['documentation', 'tests', 'ci', 'code'])

// 6. No matching files â expect empty array
testCase('No match', ['assets/logo.png', 'LICENSE'], [])
