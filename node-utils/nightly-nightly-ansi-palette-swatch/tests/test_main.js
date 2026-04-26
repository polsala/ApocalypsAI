// Tests for nightly-ansi-palette-swatch
// These tests run offline and use child_process to capture output.

const { execSync } = require('child_process');
const assert = require('assert');
const path = require('path');

function run(args = '') {
  // Execute the utility and return stdout as a string.
  const cmd = `node ${path.join(__dirname, '..', 'src', 'main.js')} ${args}`;
  // Mock rationale: we run the script synchronously; no external resources are needed.
  return execSync(cmd, { encoding: 'utf8' });
}

// Helper to check for an ANSI escape sequence for a given index.
function containsColor(output, idx) {
  const esc = `\x1b[38;5;${idx}m█\x1b[0m`;
  return output.includes(esc);
}

// Test that the basic palette includes the first and last colors.
(function testBasicPalette() {
  const out = run();
  assert(containsColor(out, 0), 'output should contain color index 0');
  assert(containsColor(out, 255), 'output should contain color index 255');
  console.log('✅ testBasicPalette passed');
})();

// Test that the --format=hex flag adds hex codes.
(function testHexFormat() {
  const out = run('--format=hex');
  assert(out.includes('#000000'), 'hex output should contain #000000 for index 0');
  assert(out.includes('#ffffff'), 'hex output should contain #ffffff for index 15');
  console.log('✅ testHexFormat passed');
})();

// Test that the --format=rgb flag adds rgb strings.
(function testRgbFormat() {
  const out = run('--format=rgb');
  assert(out.includes('rgb(0,0,0)'), 'rgb output should contain rgb(0,0,0) for index 0');
  assert(out.includes('rgb(255,255,255)'), 'rgb output should contain rgb(255,255,255) for index 15');
  console.log('✅ testRgbFormat passed');
})();
