const fs = require('fs');
const { execSync } = require('child_process');
const path = require('path');

// Mock rationale: Avoid real GitHub API calls and file system side effects by mocking core functions.
jest.mock('@actions/core', () => ({
  getInput: jest.fn(),
  setOutput: jest.fn(),
  setFailed: jest.fn(),
  warning: jest.fn()
}));

const core = require('@actions/core');

const run = require('../src/index.js');

beforeEach(() => {
  jest.clearAllMocks();
});

afterEach(() => {
  if (fs.existsSync('test-output.md')) fs.unlinkSync('test-output.md');
  if (fs.existsSync('test-reports')) {
    fs.rmSync('test-reports', { recursive: true });
  }
});

it('should aggregate reports correctly', async () => {
  fs.mkdirSync('test-reports');
  fs.writeFileSync('test-reports/run1.json', JSON.stringify({ success: true, run_id: 'run1' }));
  fs.writeFileSync('test-reports/run2.json', JSON.stringify({ success: false, run_id: 'run2', reason: 'timeout' }));

  core.getInput.mockImplementation(name => {
    if (name === 'input-dir') return 'test-reports';
    if (name === 'output-file') return 'test-output.md';
    return '';
  });

  await run();

  const output = fs.readFileSync('test-output.md', 'utf-8');
  expect(output).toContain('Total Runs: 2');
  expect(output).toContain('Failed Runs: 1');
  expect(output).toContain('Run ID: `run2` - Reason: timeout');
});

it('should handle missing input directory', async () => {
  core.getInput.mockImplementation(name => {
    if (name === 'input-dir') return 'missing-dir';
    if (name === 'output-file') return 'test-output.md';
    return '';
  });

  await run();

  expect(core.setFailed).toHaveBeenCalledWith('Input directory does not exist: missing-dir');
});

it('should skip invalid JSON files', async () => {
  fs.mkdirSync('test-reports');
  fs.writeFileSync('test-reports/invalid.json', '{ invalid json }');
  fs.writeFileSync('test-reports/valid.json', JSON.stringify({ success: true, run_id: 'valid' }));

  core.getInput.mockImplementation(name => {
    if (name === 'input-dir') return 'test-reports';
    if (name === 'output-file') return 'test-output.md';
    return '';
  });

  await run();

  expect(core.warning).toHaveBeenCalledWith('Skipping invalid JSON file: invalid.json');
  const output = fs.readFileSync('test-output.md', 'utf-8');
  expect(output).toContain('Total Runs: 1');
  expect(output).toContain('Failed Runs: 0');
});
