import { lintConfigFile } from '../src/index';
import * as fs from 'fs';
import * as path from 'path';

// Mocking fs and path for deterministic tests
jest.mock('fs');
jest.mock('path');

// Mock implementations
const mockFs = fs as jest.Mocked<typeof fs>;
const mockPath = path as jest.Mocked<typeof path>;

// Helper to create mock files
const createMockFile = (filePath: string, content: string) => {
  mockFs.readFileSync.mockImplementation((file, encoding) => {
    if (path.resolve(file) === path.resolve(filePath) && encoding === 'utf-8') {
      return content;
    }
    throw new Error(`Mock file not found: ${file}`);
  });
  mockFs.existsSync.mockImplementation((file) => {
    return path.resolve(file) === path.resolve(filePath);
  });
};

// Helper to clear mocks between tests
const resetMocks = () => {
  mockFs.readFileSync.mockClear();
  mockFs.existsSync.mockClear();
  mockPath.extname.mockClear();
};

describe('nightly-ts-config-linter', () => {
  beforeEach(() => {
    resetMocks();
    // Default mock for path.extname
    mockPath.extname.mockImplementation((filePath) => path.extname(filePath));
  });

  it('should return no errors for a valid JSON file', () => {
    const validJsonContent = '{
      "name": "my-app",
      "version": "1.0.0",
      "description": "A sample app"
    }';
    const filePath = '/path/to/valid.json';
    createMockFile(filePath, validJsonContent);

    const errors = lintConfigFile(filePath);
    expect(errors).toEqual([]);
  });

  it('should report syntax error for invalid JSON', () => {
    const invalidJsonContent = '{
      "name": "my-app",
      "version": "1.0.0",
      "description": "A sample app",
    }'; // Trailing comma
    const filePath = '/path/to/invalid.json';
    createMockFile(filePath, invalidJsonContent);

    const errors = lintConfigFile(filePath);
    expect(errors.length).toBe(1);
    expect(errors[0].rule).toBe('syntax-error');
    expect(errors[0].message).toContain('Unexpected token');
    expect(errors[0].filePath).toBe(filePath);
  });

  it('should report missing required key in JSON', () => {
    const missingKeyJsonContent = '{
      "name": "my-app",
      "description": "A sample app"
    }';
    const filePath = '/path/to/missing_key.json';
    createMockFile(filePath, missingKeyJsonContent);

    const errors = lintConfigFile(filePath);
    expect(errors.length).toBe(1);
    expect(errors[0].rule).toBe('json-required-key');
    expect(errors[0].message).toContain('missing the required "version" key');
    expect(errors[0].filePath).toBe(filePath);
  });

  it('should return no errors for a valid YAML file', () => {
    const validYamlContent = 'name: my-app
version: 1.0.0
description: A sample app
settings:
  timeout: 30
  retries: 3';
    const filePath = '/path/to/valid.yaml';
    createMockFile(filePath, validYamlContent);

    const errors = lintConfigFile(filePath);
    expect(errors).toEqual([]);
  });

  it('should report syntax error for invalid YAML', () => {
    const invalidYamlContent = 'name: my-app
version: 1.0.0
  settings:
  timeout: 30
  retries: 3'; // Incorrect indentation for version
    const filePath = '/path/to/invalid.yaml';
    createMockFile(filePath, invalidYamlContent);

    const errors = lintConfigFile(filePath);
    expect(errors.length).toBe(1);
    expect(errors[0].rule).toBe('syntax-error');
    expect(errors[0].message).toContain('mapping values are not allowed here');
    expect(errors[0].filePath).toBe(filePath);
  });

  it('should report indentation issue in YAML', () => {
    const indentationYamlContent = 'parent:
  child1: value1
 child2: value2'; // child2 is less indented than child1
    const filePath = '/path/to/indentation.yaml';
    createMockFile(filePath, indentationYamlContent);

    const errors = lintConfigFile(filePath);
    expect(errors.length).toBe(1);
    expect(errors[0].rule).toBe('yaml-indentation');
    expect(errors[0].message).toContain('Potential indentation issue');
    expect(errors[0].filePath).toBe(filePath);
    expect(errors[0].line).toBe(3);
  });

  it('should report empty file error', () => {
    const emptyContent = '';
    const filePath = '/path/to/empty.json';
    createMockFile(filePath, emptyContent);

    const errors = lintConfigFile(filePath);
    expect(errors.length).toBe(1);
    expect(errors[0].rule).toBe('empty-file');
    expect(errors[0].message).toBe('Configuration file is empty.');
    expect(errors[0].filePath).toBe(filePath);
  });

  it('should report empty object error for JSON', () => {
    const emptyObjectContent = '{}';
    const filePath = '/path/to/empty_obj.json';
    createMockFile(filePath, emptyObjectContent);

    const errors = lintConfigFile(filePath);
    expect(errors.length).toBe(1);
    expect(errors[0].rule).toBe('empty-file');
    expect(errors[0].message).toBe('Configuration file is empty.');
    expect(errors[0].filePath).toBe(filePath);
  });

  it('should throw an error if file does not exist', () => {
    const filePath = '/path/to/nonexistent.json';
    mockFs.existsSync.mockReturnValue(false);

    expect(() => lintConfigFile(filePath)).toThrow('File not found: /path/to/nonexistent.json');
  });

  it('should handle TOML files correctly', () => {
    const validTomlContent = '[owner]
name = "Tom"

[database]
server = "192.168.1.1"
ports = [ 8001, 8001, 8002 ]
connection_max = 5000
enabled = true';
    const filePath = '/path/to/valid.toml';
    createMockFile(filePath, validTomlContent);

    const errors = lintConfigFile(filePath);
    expect(errors).toEqual([]);
  });

  it('should report syntax error for invalid TOML', () => {
    const invalidTomlContent = '[owner]
name = "Tom"

[database
server = "192.168.1.1"'; // Missing closing bracket for database section
    const filePath = '/path/to/invalid.toml';
    createMockFile(filePath, invalidTomlContent);

    const errors = lintConfigFile(filePath);
    expect(errors.length).toBe(1);
    expect(errors[0].rule).toBe('syntax-error');
    expect(errors[0].message).toContain('Expected "|" or "."');
    expect(errors[0].filePath).toBe(filePath);
  });

});
