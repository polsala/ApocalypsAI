import { main } from '../src/index';
import * as fs from 'fs';
import * as path from 'path';

// Mock rationale: We need to simulate file system operations without actually touching the disk
// to ensure tests are deterministic, fast, and isolated from the environment.
jest.mock('fs', () => ({
  readFileSync: jest.fn(),
}));

// Mock rationale: We need to capture console output to verify the CLI's behavior
// without interfering with the actual console during test runs.
const mockConsoleLog = jest.spyOn(console, 'log').mockImplementation(() => {});
const mockConsoleError = jest.spyOn(console, 'error').mockImplementation(() => {});
const mockProcessExit = jest.spyOn(process, 'exit').mockImplementation((code?: number) => {
  throw new Error(`process.exit called with code: ${code}`); // Throw to stop execution
});

describe('CLI functionality', () => {
  const mockReadFileSync = fs.readFileSync as jest.Mock;

  beforeEach(() => {
    mockConsoleLog.mockClear();
    mockConsoleError.mockClear();
    mockProcessExit.mockClear();
    mockReadFileSync.mockClear();
  });

  it('should display usage if not enough arguments are provided', async () => {
    process.argv = ['node', 'index.js']; // Simulate no arguments
    await expect(main()).rejects.toThrow('process.exit called with code: 1');
    expect(mockConsoleLog).toHaveBeenCalledWith('Usage: ncd-detect <file1.json> <file2.json>');
    expect(mockProcessExit).toHaveBeenCalledWith(1);
  });

  it('should report no drift for identical files', async () => {
    process.argv = ['node', 'index.js', 'config1.json', 'config2.json'];
    mockReadFileSync
      .mockReturnValueOnce(JSON.stringify({ a: 1, b: 'hello' })) // config1.json
      .mockReturnValueOnce(JSON.stringify({ a: 1, b: 'hello' })); // config2.json

    await main();
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Temporal Harmony Achieved!'));
    expect(mockProcessExit).not.toHaveBeenCalled();
  });

  it('should report drift for different files', async () => {
    process.argv = ['node', 'index.js', 'config1.json', 'config2.json'];
    mockReadFileSync
      .mockReturnValueOnce(JSON.stringify({ a: 1, b: 'hello' })) // config1.json
      .mockReturnValueOnce(JSON.stringify({ a: 1, b: 'world', c: true })); // config2.json

    await main();
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Configuration Drift Detected!'));
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('➕ Added Keys:\n  - c'));
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('✏️ Modified Values:\n  - b:\n    Old: "hello"\n    New: "world"'));
    expect(mockProcessExit).not.toHaveBeenCalled();
  });

  it('should exit with error if file cannot be read', async () => {
    process.argv = ['node', 'index.js', 'nonexistent.json', 'config2.json'];
    mockReadFileSync.mockImplementationOnce(() => {
      throw new Error('File not found');
    });

    await expect(main()).rejects.toThrow('process.exit called with code: 1');
    expect(mockConsoleError).toHaveBeenCalledWith(expect.stringContaining('Error reading or parsing file nonexistent.json: File not found'));
    expect(mockProcessExit).toHaveBeenCalledWith(1);
  });

  it('should exit with error if file is invalid JSON', async () => {
    process.argv = ['node', 'index.js', 'invalid.json', 'config2.json'];
    mockReadFileSync
      .mockReturnValueOnce('{ "a": 1, "b": }') // invalid JSON
      .mockReturnValueOnce(JSON.stringify({ a: 1 }));

    await expect(main()).rejects.toThrow('process.exit called with code: 1');
    expect(mockConsoleError).toHaveBeenCalledWith(expect.stringContaining('Error reading or parsing file invalid.json: Unexpected token } in JSON at position 15'));
    expect(mockProcessExit).toHaveBeenCalledWith(1);
  });
});
