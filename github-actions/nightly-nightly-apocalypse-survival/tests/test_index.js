const { execSync } = require('child_process');
const assert = require('assert');

// Expected tip when FORCE_RANDOM is 0 (first element)
const expectedTip = "Always keep a spare can‑of‑beans in your bunker.";

const env = { ...process.env, FORCE_RANDOM: '0' };
const output = execSync('node src/index.js', { env, encoding: 'utf8' }).trim();
assert.strictEqual(output, `::set-output name=tip::${expectedTip}`);

console.log('Test passed: deterministic tip selection works.');
