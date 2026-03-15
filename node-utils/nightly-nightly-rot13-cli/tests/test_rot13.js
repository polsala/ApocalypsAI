import { execFile } from 'node:child_process';
import { strict as assert } from 'node:assert';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const cliPath = path.resolve(__dirname, '..', 'src', 'index.js');

function run(args, input = '') {
  return new Promise((resolve, reject) => {
    const proc = execFile('node', [cliPath, ...args], (error, stdout, stderr) => {
      if (error) reject(error);
      else resolve(stdout.trim());
    });
    if (input) {
      proc.stdin.write(input);
      proc.stdin.end();
    }
  });
}

(async () => {
  const encoded = await run(['Hello']);
  assert.equal(encoded, 'Uryyb');

  const decoded = await run(['Uryyb']);
  assert.equal(decoded, 'Hello');

  const piped = await run([], 'Secret');
  assert.equal(piped, 'Frperg');

  console.log('All tests passed');
})();
