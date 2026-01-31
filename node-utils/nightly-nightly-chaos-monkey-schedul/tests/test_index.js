"use strict";

const { spawn } = require('child_process');

// Mock rationale: Avoid actual system disruption in tests
jest.mock('child_process');

const mockSpawn = {
  stdout: { on: jest.fn() },
  stderr: { on: jest.fn() },
  on: jest.fn()
};

spawn.mockReturnValue(mockSpawn);

beforeEach(() => {
  jest.clearAllMocks();
  jest.useFakeTimers();
});

afterEach(() => {
  jest.useRealTimers();
});

function runCLI(args) {
  const { execFileSync } = require('child_process');
  try {
    return execFileSync('node', ['./src/index.js', ...args], { encoding: 'utf-8' });
  } catch (e) {
    return e.stdout || e.stderr;
  }
}

it('should show help when no args', () => {
  const output = runCLI([]);
  expect(output).toContain('Usage');
});

it('should accept valid chaos type and interval', () => {
  const output = runCLI(['--chaos', 'banana-peel', '--interval', '1s']);
  expect(output).toContain('🌀 Chaos Monkey activated: banana-peel');
});

it('should reject invalid interval', () => {
  const output = runCLI(['--chaos', 'banana-peel', '--interval', 'bad']);
  expect(output).toContain('Invalid interval format');
});

it('should trigger banana-peel chaos in dry-run', () => {
  const output = runCLI(['--chaos', 'banana-peel', '--interval', '1s', '--dry-run']);
  expect(output).toContain('[DRY RUN] Triggering: banana-peel');
});

it('should trigger sneaky-cat chaos', () => {
  const output = runCLI(['--chaos', 'sneaky-cat', '--interval', '1s']);
  expect(output).toContain('🐱 Sneaky cat unplugged the server!');
});
