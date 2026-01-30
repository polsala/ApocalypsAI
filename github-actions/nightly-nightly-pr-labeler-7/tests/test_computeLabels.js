const assert = require('assert');\nconst { computeLabels } = require('../src/index');\n\n// Mock rationale: deterministic inputs, no external calls.\n\nfunction testSimpleMatch() {\n  const files = ['docs/README.md', 'src/main.js', 'tests/main.test.js'];\n  const map = {\n    'docs/': 'documentation',\n    'src/': 'code',\n    'tests/': 'tests'\n  };\n  const result = computeLabels(files, map).sort();\n  assert.deepStrictEqual(result, ['code', 'documentation', 'tests']);\n}\n\nfunction testNoMatch() {\n  const files = ['assets/logo.png'];\n  const map = { 'src/': 'code' };
  const result = computeLabels(files, map);
  assert.deepStrictEqual(result, []);
}\n\nfunction testDuplicateLabels() {\n  const files = ['src/app.js', 'src/utils.js'];\n  const map = { 'src/': 'code' };
  const result = computeLabels(files, map);
  assert.deepStrictEqual(result, ['code']); // label appears only once\n}\n\nfunction runTests() {\n  testSimpleMatch();\n  testNoMatch();\n  testDuplicateLabels();\n  console.log('All tests passed');\n}\n\nrunTests();
