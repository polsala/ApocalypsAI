import { encodeToAsciiArt } from '../src/index';
import assert from 'assert';

function captureConsoleLog(fn: () => void): string {
  const originalLog = console.log;
  let output = '';
  console.log = (msg?: any, ...optionalParams: any[]) => {
    output += msg + (optionalParams.length ? ' ' + optionalParams.join(' ') : '');
  };
  try {
    fn();
  } finally {
    console.log = originalLog;
  }
  return output;
}

// Test the core function
const result = encodeToAsciiArt('A');
assert.strictEqual(result, '░█░░░░░█');

// Test CLI execution simulation
const output = captureConsoleLog(() => {
  const originalArgv = process.argv;
  process.argv = ['node', 'src/index.ts', 'B'];
  delete require.cache[require.resolve('../src/index')];
  require('../src/index');
  process.argv = originalArgv;
});
assert.ok(output.includes('█░░░░░█'));
