const { execSync } = require('child_process');
const path = require('path');

function run(args) {
  const cmd = `node ${path.join(__dirname, '..', 'src', 'main.js')} ${args}`;
  return execSync(cmd, { encoding: 'utf8' });
}

function runExpectError(args) {
  try {
    execSync(`node ${path.join(__dirname, '..', 'src', 'main.js')} ${args}`, { encoding: 'utf8', stdio: 'pipe' });
    return null; // should not reach here
  } catch (e) {
    // e.stdout may be empty; combine stdout and stderr for full message
    return (e.stdout || '') + (e.stderr || '');
  }
}

// Test 1: car 100 km => 21.0 kg
const out1 = run('100 car').trim();
if (out1 !== 'Estimated CO2 emission: 21.0 kg') {
  console.error('Test 1 failed');
  process.exit(1);
}

// Test 2: bus 50 km => 5.3 kg (50 * 0.105 = 5.25 -> 5.3)
const out2 = run('50 bus').trim();
if (out2 !== 'Estimated CO2 emission: 5.3 kg') {
  console.error('Test 2 failed');
  process.exit(2);
}

// Test 3: unknown mode should produce an error message
const err3 = runExpectError('10 spaceship');
if (!err3.includes("Error: unknown mode 'spaceship'.")) {
  console.error('Test 3 failed');
  process.exit(3);
}

// Test 4: missing arguments should show usage
const err4 = runExpectError('');
if (!err4.includes('Usage:')) {
  console.error('Test 4 failed');
  process.exit(4);
}

console.log('All tests passed');
process.exit(0);
