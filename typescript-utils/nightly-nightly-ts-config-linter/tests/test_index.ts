import * as fs from 'fs';
import * as path from 'path';
import { execSync } from 'child_process';

// Mocking fs and path for deterministic tests
jest.mock('fs');
jest.mock('path');

// Mock implementations
const mockFs = fs as jest.Mocked<typeof fs>;
const mockPath = path as jest.Mocked<typeof path>;

// Mock data for test files
const mockJsonContent = '{
  "name": "test-app",
  "version": "1.0.0",
  "dependencies": {
    "react": "^18.0.0"
  }
}';

const mockYamlContent = '---
name: test-app-yaml
version: 1.0.0
services:
  web:
    image: nginx
';

const mockEmptyJsonContent = '{}';
const mockYamlWithTrailingComma = '---
key: value,
';

// Helper to mock file system operations
const mockFile = (filePath: string, content: string) => {
  mockFs.readFileSync.mockImplementation((readPath: string | Buffer, options?: { encoding?: string; flag?: string; }): string => {
    if (readPath.toString() === filePath) {
      return content;
    }
    throw new Error(`Mock FS: File not found - ${readPath}`);
  });
  mockFs.existsSync.mockReturnValue(true);
};

// Helper to mock path operations
const mockPathResolve = (resolvedPath: string) => {
  mockPath.resolve.mockReturnValue(resolvedPath);
};

// Mock the main function to capture output and exit code
jest.mock('../src/index', () => {
  const originalModule = jest.requireActual('../src/index');
  return {
    ...originalModule,
    main: jest.fn(),
  };
});

import { main as mockMain } from '../src/index';

// Mock process.argv and process.exit
let mockArgv: string[];
let mockExitCode: number | null = null;

beforeEach(() => {
  mockArgv = ['node', 'dist/index.js']; // Default mock argv
  mockExitCode = null;
  jest.clearAllMocks();

  // Reset mocks for fs and path before each test
  mockFs.readFileSync.mockReset();
  mockFs.existsSync.mockReset();
  mockPath.resolve.mockReset();

  // Mock path.resolve to return the input path for simplicity in tests
  mockPath.resolve.mockImplementation((p) => p);

  // Mock process.exit
  Object.defineProperty(process, 'exit', {
    value: jest.fn((code?: number) => {
      mockExitCode = code;
      throw new Error(`process.exit called with code ${code}`); // Throw to stop execution
    }),
    writable: true,
  });

  // Mock console.log and console.error
  jest.spyOn(console, 'log').mockImplementation(() => {});
  jest.spyOn(console, 'error').mockImplementation(() => {});
});

afterEach(() => {
  (console.log as jest.Mock).mockRestore();
  (console.error as jest.Mock).mockRestore();
  (process.exit as jest.Mock).mockRestore();
});

describe('nightly-ts-config-linter', () => {

  it('should exit with error code 0 for a valid JSON file', () => {
    const testFilePath = '/path/to/valid.json';
    mockFile(testFilePath, mockJsonContent);
    mockArgv.push(testFilePath);
    process.argv = mockArgv;

    try {
      require('../src/index'); // Execute the main function
    } catch (e: any) {
      // Expecting process.exit to be called with 0
      expect(e.message).toBe('process.exit called with code 0');
      expect(mockExitCode).toBe(0);
      expect(console.error).not.toHaveBeenCalled();
    }
  });

  it('should exit with error code 0 for a valid YAML file', () => {
    const testFilePath = '/path/to/valid.yaml';
    mockFile(testFilePath, mockYamlContent);
    mockArgv.push(testFilePath);
    process.argv = mockArgv;

    try {
      require('../src/index');
    } catch (e: any) {
      expect(e.message).toBe('process.exit called with code 0');
      expect(mockExitCode).toBe(0);
      expect(console.error).not.toHaveBeenCalled();
    }
  });

  it('should exit with error code 1 for an empty JSON file', () => {
    const testFilePath = '/path/to/empty.json';
    mockFile(testFilePath, mockEmptyJsonContent);
    mockArgv.push(testFilePath);
    process.argv = mockArgv;

    try {
      require('../src/index');
    } catch (e: any) {
      expect(e.message).toBe('process.exit called with code 1');
      expect(mockExitCode).toBe(1);
      expect(console.error).toHaveBeenCalledWith(expect.stringContaining('Linting results for:'));
      expect(console.error).toHaveBeenCalledWith(expect.stringContaining('[ERROR] NO-EMPTY-CONFIG: Configuration file is empty.'));
    }
  });

  it('should exit with error code 1 for a YAML file with trailing comma', () => {
    const testFilePath = '/path/to/trailing_comma.yaml';
    mockFile(testFilePath, mockYamlWithTrailingComma);
    mockArgv.push(testFilePath);
    process.argv = mockArgv;

    try {
      require('../src/index');
    } catch (e: any) {
      expect(e.message).toBe('process.exit called with code 1');
      expect(mockExitCode).toBe(1);
      expect(console.error).toHaveBeenCalledWith(expect.stringContaining('Linting results for:'));
      expect(console.error).toHaveBeenCalledWith(expect.stringContaining('[WARNING] NO-TRAILING-COMMAS: Potential trailing comma found on line 2.'));
    }
  });

  it('should exit with error code 1 if file not found', () => {
    const testFilePath = '/path/to/nonexistent.json';
    mockFs.existsSync.mockReturnValue(false);
    mockArgv.push(testFilePath);
    process.argv = mockArgv;

    try {
      require('../src/index');
    } catch (e: any) {
      expect(e.message).toBe('process.exit called with code 1');
      expect(mockExitCode).toBe(1);
      expect(console.error).toHaveBeenCalledWith(`Error: File not found at ${testFilePath}`);
    }
  });

  it('should exit with error code 1 for an unsupported file type', () => {
    const testFilePath = '/path/to/unsupported.txt';
    mockFile(testFilePath, 'some text content');
    mockArgv.push(testFilePath);
    process.argv = mockArgv;

    try {
      require('../src/index');
    } catch (e: any) {
      expect(e.message).toBe('process.exit called with code 1');
      expect(mockExitCode).toBe(1);
      expect(console.error).toHaveBeenCalledWith('Unsupported file extension: .txt');
    }
  });

  it('should exit with error code 1 for invalid JSON syntax', () => {
    const testFilePath = '/path/to/invalid.json';
    const invalidJson = '{
      "key": "value",
      "malformed": true
    '; // Missing closing brace
    mockFile(testFilePath, invalidJson);
    mockArgv.push(testFilePath);
    process.argv = mockArgv;

    try {
      require('../src/index');
    } catch (e: any) {
      expect(e.message).toBe('process.exit called with code 1');
      expect(mockExitCode).toBe(1);
      expect(console.error).toHaveBeenCalledWith(expect.stringContaining('Error parsing file'));
      expect(console.error).toHaveBeenCalledWith(expect.stringContaining('Unexpected end of JSON input'));
    }
  });

  it('should exit with error code 1 for invalid YAML syntax', () => {
    const testFilePath = '/path/to/invalid.yaml';
    const invalidYaml = 'key: value
  invalid indentation';
    mockFile(testFilePath, invalidYaml);
    mockArgv.push(testFilePath);
    process.argv = mockArgv;

    try {
      require('../src/index');
    } catch (e: any) {
      expect(e.message).toBe('process.exit called with code 1');
      expect(mockExitCode).toBe(1);
      expect(console.error).toHaveBeenCalledWith(expect.stringContaining('Error parsing file'));
      expect(console.error).toHaveBeenCalledWith(expect.stringContaining('mapping values are not allowed here'));
    }
  });

});
