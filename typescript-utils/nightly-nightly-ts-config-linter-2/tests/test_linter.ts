import * as fs from 'fs';
import * as path from 'path';
import { lintConfig } from '../src/index'; // Assuming index.ts exports lintConfig

// Mocking fs and path for deterministic tests
jest.mock('fs');
jest.mock('path');

const mockFs = fs as jest.Mocked<typeof fs>;
const mockPath = path as jest.Mocked<typeof path>;

// Mock console.error and console.log to capture output
let consoleErrorSpy: jest.SpyInstance;
let consoleLogSpy: jest.SpyInstance;

beforeEach(() => {
  consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
  consoleLogSpy = jest.spyOn(console, 'log').mockImplementation(() => {});
  mockFs.existsSync.mockReturnValue(true);
  mockPath.extname.mockReturnValue('.json'); // Default to JSON for most tests
});

afterEach(() => {
  jest.restoreAllMocks();
});

describe('Nightly TypeScript Configuration Linter', () => {

  it('should report success for a valid JSON file with default config', () => {
    const mockContent = JSON.stringify({
      name: 'test-package',
      version: '1.0.0'
    });
    mockFs.readFileSync.mockReturnValue(mockContent);
    mockPath.extname.mockReturnValue('.json');

    // Mocking process.exit to prevent actual exit during tests
    const processExitSpy = jest.spyOn(process, 'exit').mockImplementation((code?: number) => {
      throw new Error(`process.exit called with code: ${code}`);
    });

    try {
      lintConfig('/path/to/valid.json');
    } catch (e: any) {
      // We expect it to throw if process.exit is called, but we want to check logs first
      expect(e.message).toContain('process.exit called with code: 1');
    }

    expect(consoleLogSpy).toHaveBeenCalledWith("Linting successful for '/path/to/valid.json'");
    expect(consoleErrorSpy).not.toHaveBeenCalled();
    expect(processExitSpy).not.toHaveBeenCalled(); // Should not exit with error code
  });

  it('should report error for invalid JSON syntax', () => {
    const mockContent = '{
      name: "invalid-json",
      version: "1.0.0"
    }'; // Missing quotes around name key
    mockFs.readFileSync.mockReturnValue(mockContent);
    mockPath.extname.mockReturnValue('.json');

    const processExitSpy = jest.spyOn(process, 'exit').mockImplementation((code?: number) => {
      throw new Error(`process.exit called with code: ${code}`);
    });

    try {
      lintConfig('/path/to/invalid.json');
    } catch (e: any) {
      expect(e.message).toContain('process.exit called with code: 1');
    }

    expect(consoleErrorSpy).toHaveBeenCalledWith("Linting failed for '/path/to/invalid.json':");
    expect(consoleErrorSpy).toHaveBeenCalledWith("  - Invalid JSON syntax: Unexpected token n in JSON at position 10"); // Example error message
    expect(consoleLogSpy).not.toHaveBeenCalled();
  });

  it('should report error for missing required field in JSON', () => {
    const mockContent = JSON.stringify({
      version: '1.0.0'
    }); // Missing 'name'
    mockFs.readFileSync.mockReturnValue(mockContent);
    mockPath.extname.mockReturnValue('.json');

    const processExitSpy = jest.spyOn(process, 'exit').mockImplementation((code?: number) => {
      throw new Error(`process.exit called with code: ${code}`);
    });

    try {
      lintConfig('/path/to/missing_field.json');
    } catch (e: any) {
      expect(e.message).toContain('process.exit called with code: 1');
    }

    expect(consoleErrorSpy).toHaveBeenCalledWith("Linting failed for '/path/to/missing_field.json':");
    expect(consoleErrorSpy).toHaveBeenCalledWith("  - Missing required field: 'name'");
    expect(consoleLogSpy).not.toHaveBeenCalled();
  });

  it('should report error for type mismatch in JSON', () => {
    const mockContent = JSON.stringify({
      name: 'test-package',
      version: 1.0,
      private: 'true'
    }); // version should be string, private should be boolean
    mockFs.readFileSync.mockReturnValue(mockContent);
    mockPath.extname.mockReturnValue('.json');

    const processExitSpy = jest.spyOn(process, 'exit').mockImplementation((code?: number) => {
      throw new Error(`process.exit called with code: ${code}`);
    });

    try {
      lintConfig('/path/to/type_mismatch.json');
    } catch (e: any) {
      expect(e.message).toContain('process.exit called with code: 1');
    }

    expect(consoleErrorSpy).toHaveBeenCalledWith("Linting failed for '/path/to/type_mismatch.json':");
    expect(consoleErrorSpy).toHaveBeenCalledWith("  - Type mismatch for field 'version': expected 'string' but got 'number'");
    expect(consoleErrorSpy).toHaveBeenCalledWith("  - Type mismatch for field 'private': expected 'boolean' but got 'string'");
    expect(consoleLogSpy).not.toHaveBeenCalled();
  });

  it('should report success for a valid YAML file with default config', () => {
    const mockContent = "name: test-package\nversion: 1.0.0";
    mockFs.readFileSync.mockReturnValue(mockContent);
    mockPath.extname.mockReturnValue('.yaml');

    const processExitSpy = jest.spyOn(process, 'exit').mockImplementation((code?: number) => {
      throw new Error(`process.exit called with code: ${code}`);
    });

    try {
      lintConfig('/path/to/valid.yaml');
    } catch (e: any) {
      expect(e.message).toContain('process.exit called with code: 1');
    }

    expect(consoleLogSpy).toHaveBeenCalledWith("Linting successful for '/path/to/valid.yaml'");
    expect(consoleErrorSpy).not.toHaveBeenCalled();
    expect(processExitSpy).not.toHaveBeenCalled();
  });

  it('should report error for invalid YAML syntax', () => {
    const mockContent = "name: invalid-yaml\n  version: 1.0.0"; // Incorrect indentation
    mockFs.readFileSync.mockReturnValue(mockContent);
    mockPath.extname.mockReturnValue('.yaml');

    const processExitSpy = jest.spyOn(process, 'exit').mockImplementation((code?: number) => {
      throw new Error(`process.exit called with code: ${code}`);
    });

    try {
      lintConfig('/path/to/invalid.yaml');
    } catch (e: any) {
      expect(e.message).toContain('process.exit called with code: 1');
    }

    expect(consoleErrorSpy).toHaveBeenCalledWith("Linting failed for '/path/to/invalid.yaml':");
    expect(consoleErrorSpy).toHaveBeenCalledWith(expect.stringContaining('Invalid YAML syntax')); // Check for general YAML error
    expect(consoleLogSpy).not.toHaveBeenCalled();
  });

  it('should report error for missing required field in YAML', () => {
    const mockContent = "version: 1.0.0"; // Missing 'name'
    mockFs.readFileSync.mockReturnValue(mockContent);
    mockPath.extname.mockReturnValue('.yaml');

    const processExitSpy = jest.spyOn(process, 'exit').mockImplementation((code?: number) => {
      throw new Error(`process.exit called with code: ${code}`);
    });

    try {
      lintConfig('/path/to/missing_field.yaml');
    } catch (e: any) {
      expect(e.message).toContain('process.exit called with code: 1');
    }

    expect(consoleErrorSpy).toHaveBeenCalledWith("Linting failed for '/path/to/missing_field.yaml':");
    expect(consoleErrorSpy).toHaveBeenCalledWith("  - Missing required field: 'name'");
    expect(consoleLogSpy).not.toHaveBeenCalled();
  });

  it('should report error for type mismatch in YAML', () => {
    const mockContent = "name: test-package\nversion: 1.0\nprivate: 'true'"; // version should be string, private should be boolean
    mockFs.readFileSync.mockReturnValue(mockContent);
    mockPath.extname.mockReturnValue('.yaml');

    const processExitSpy = jest.spyOn(process, 'exit').mockImplementation((code?: number) => {
      throw new Error(`process.exit called with code: ${code}`);
    });

    try {
      lintConfig('/path/to/type_mismatch.yaml');
    } catch (e: any) {
      expect(e.message).toContain('process.exit called with code: 1');
    }

    expect(consoleErrorSpy).toHaveBeenCalledWith("Linting failed for '/path/to/type_mismatch.yaml':");
    expect(consoleErrorSpy).toHaveBeenCalledWith("  - Type mismatch for field 'version': expected 'string' but got 'number'");
    expect(consoleErrorSpy).toHaveBeenCalledWith("  - Type mismatch for field 'private': expected 'boolean' but got 'string'");
    expect(consoleLogSpy).not.toHaveBeenCalled();
  });

  it('should report error if file not found', () => {
    mockFs.existsSync.mockReturnValue(false);

    const processExitSpy = jest.spyOn(process, 'exit').mockImplementation((code?: number) => {
      throw new Error(`process.exit called with code: ${code}`);
    });

    try {
      lintConfig('/path/to/nonexistent.json');
    } catch (e: any) {
      expect(e.message).toContain('process.exit called with code: 1');
    }

    expect(consoleErrorSpy).toHaveBeenCalledWith("Error: File not found at '/path/to/nonexistent.json'");
    expect(consoleLogSpy).not.toHaveBeenCalled();
  });

  it('should warn for unsupported file extension', () => {
    const mockContent = "some content";
    mockFs.readFileSync.mockReturnValue(mockContent);
    mockPath.extname.mockReturnValue('.txt');

    lintConfig('/path/to/unsupported.txt');

    expect(console.warn).toHaveBeenCalledWith("Warning: Unsupported file extension '.txt'. Only JSON and YAML are supported.");
    expect(consoleErrorSpy).not.toHaveBeenCalled();
    expect(consoleLogSpy).not.toHaveBeenCalled();
  });

});
