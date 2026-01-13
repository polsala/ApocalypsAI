const fs = require('fs');
const os = require('os');
const path = require('path');
const assert = require('assert');

// Helper to run tests with a temporary HOME directory
function withTempHome(callback) {
  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'emoji-mood-'));
  const originalHome = process.env.HOME;
  process.env.HOME = tmpDir;
  // Reload the module so LOG_PATH picks up the new HOME
  delete require.cache[require.resolve('../src/index')];
  const mod = require('../src/index');
  try {
    callback(mod, tmpDir);
  } finally {
    process.env.HOME = originalHome;
    // Cleanup temporary directory
    fs.rmSync(tmpDir, { recursive: true, force: true });
  }
}

// Mock rationale: using a temporary HOME ensures tests are deterministic and offline.
withTempHome((mod, tmpHome) => {
  // Ensure a clean state
  if (fs.existsSync(mod.LOG_PATH)) fs.unlinkSync(mod.LOG_PATH);

  mod.logMood('ð', 'Feeling great');
  mod.logMood('ð¢', 'Sad day');
  mod.logMood('ð', 'Another happy moment');

  const stats = mod.getStats();
  assert.strictEqual(stats['ð'], 2, 'ð count should be 2');
  assert.strictEqual(stats['ð¢'], 1, 'ð¢ count should be 1');

  // Verify file content structure
  const fileData = JSON.parse(fs.readFileSync(mod.LOG_PATH, 'utf8'));
  assert.strictEqual(fileData.length, 3, 'Log should have 3 entries');
});

console.log('All tests passed.');
