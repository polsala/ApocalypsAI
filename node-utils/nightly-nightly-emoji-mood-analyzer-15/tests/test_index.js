const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const assert = require('assert');
const os = require('os');

function withTempFile(content, fn) {
  const tmpPath = path.join(os.tmpdir(), `temp-${Date.now()}.txt`);
  fs.writeFileSync(tmpPath, content);
  try {
    fn(tmpPath);
  } finally {
    fs.unlinkSync(tmpPath);
  }
}

// Happy text should yield 😊
withTempFile('I am very happy and love this wonderful day', (file) => {
  const out = execSync(`node src/index.js ${file}`).toString().trim();
  assert.strictEqual(out, '😊');
});

// Sad text should yield 😢
withTempFile('It is a terrible, sad, and depressing situation', (file) => {
  const out = execSync(`node src/index.js ${file}`).toString().trim();
  assert.strictEqual(out, '😢');
});

// Neutral text should yield 😐
withTempFile('The sky is blue and the grass is green', (file) => {
  const out = execSync(`node src/index.js ${file}`).toString().trim();
  assert.strictEqual(out, '😐');
});

console.log('All tests passed');
