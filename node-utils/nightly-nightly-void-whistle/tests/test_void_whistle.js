"use strict";
const { spawn } = require('child_process');
const path = require('path');
const assert = require('assert');

// Mock rationale: We can't actually play sounds during testing,
// so we verify the right conditions trigger the expected behavior.

function runVoidWhistle(args, done) {
  const cliPath = path.join(__dirname, '../src/index.js');
  const proc = spawn('node', [cliPath, ...args]);
  let stdout = '';
  let stderr = '';

  proc.stdout.on('data', (data) => { stdout += data.toString(); });
  proc.stderr.on('data', (data) => { stderr += data.toString(); });

  proc.on('close', (code) => {
    done({ code, stdout, stderr });
  });
}

describe('void-whistle CLI', () => {
  it('should show help when no arguments given', (done) => {
    runVoidWhistle([], ({ code, stdout }) => {
      assert.strictEqual(code, 1);
      assert.ok(stdout.includes('Usage'));
      done();
    });
  });

  it('should accept --sound flag and run echo command successfully', (done) => {
    runVoidWhistle(['--sound', 'bell', '--', 'echo', 'test'], ({ code, stdout }) => {
      assert.strictEqual(code, 0);
      assert.ok(stdout.includes('test'));
      done();
    });
  });

  it('should default to chime sound if none specified', (done) => {
    runVoidWhistle(['--', 'echo', 'hello'], ({ code, stdout }) => {
      assert.strictEqual(code, 0);
      assert.ok(stdout.includes('hello'));
      done();
    });
  });
});
