import * as fs from 'fs';
import * as path from 'path';
import { execSync } from 'child_process';

// Mocking fs and path for deterministic tests
jest.mock('fs');
jest.mock('path');

// Mock fs functions
const mockFs = fs as jest.Mocked<typeof fs>;
const mockPath = path as jest.Mocked<typeof path>;

// Mock js-yaml for YAML parsing tests
jest.mock('js-yaml', () => ({
  load: jest.fn(),
}));
const mockYaml = require('js-yaml');

// Mock execSync for running the CLI tool
jest.mock('child_process', () => ({
  execSync: jest.fn(),
}));
const mockExecSync = execSync as jest.Mock;

// Helper to create mock files
const createMockFile = (filePath: string, content: string) => {
  mockFs.readFileSync.mockImplementation((file, encoding) => {
    if (file === filePath && encoding === 'utf-8') {
      return content;
    }
    throw new Error(`Mock readFileSync: Unexpected file ${file}`);
  });
};

describe('Nightly TypeScript Configuration Linter', () => {
  beforeEach(() => {
    // Reset mocks before each test
    mockFs.readFileSync.mockClear();
    mockPath.extname.mockClear();
    mockYaml.load.mockClear();
    mockExecSync.mockClear();
    // Mock path.extname to return default values if not specified in test
    mockPath.extname.mockReturnValue('.json');
  });

  it('should lint a valid JSON file successfully', () => {
    const validJsonContent = '{\n  "key": "value"\n}';
    const filePath = '/path/to/valid.json';
    createMockFile(filePath, validJsonContent);
    mockPath.extname.mockReturnValue('.json');

    // Mock JSON.parse to not throw an error for valid JSON
    const jsonParseSpy = jest.spyOn(JSON, 'parse').mockImplementation(() => ({}));

    // Simulate running the script directly
    process.argv = ['node', 'src/index.ts', filePath];
    const exitSpy = jest.spyOn(process, 'exit').mockImplementation(() => undefined as never);
    const logSpy = jest.spyOn(console, 'log').mockImplementation(() => {});

    require('../src/index'); // Re-require to run the main function

    expect(mockFs.readFileSync).toHaveBeenCalledWith(filePath, 'utf-8');
    expect(mockPath.extname).toHaveBeenCalledWith(filePath);
    expect(jsonParseSpy).toHaveBeenCalledWith(validJsonContent);
    expect(exitSpy).toHaveBeenCalledWith(0);
    expect(logSpy).toHaveBeenCalledWith(`Configuration file ${filePath} linted successfully.`);

    jsonParseSpy.mockRestore();
    exitSpy.mockRestore();
    logSpy.mockRestore();
  });

  it('should report an error for an invalid JSON file', () => {
    const invalidJsonContent = '{\n  "key": "value",\n}'; // Trailing comma
    const filePath = '/path/to/invalid.json';
    createMockFile(filePath, invalidJsonContent);
    mockPath.extname.mockReturnValue('.json');

    // Mock JSON.parse to throw an error
    const jsonParseSpy = jest.spyOn(JSON, 'parse').mockImplementation(() => {
      throw new Error('Unexpected token } in JSON at position 25');
    });

    process.argv = ['node', 'src/index.ts', filePath];
    const exitSpy = jest.spyOn(process, 'exit').mockImplementation(() => undefined as never);
    const errorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});

    require('../src/index');

    expect(mockFs.readFileSync).toHaveBeenCalledWith(filePath, 'utf-8');
    expect(mockPath.extname).toHaveBeenCalledWith(filePath);
    expect(jsonParseSpy).toHaveBeenCalledWith(invalidJsonContent);
    expect(exitSpy).toHaveBeenCalledWith(1);
    expect(errorSpy).toHaveBeenCalledWith(`Linting errors found in ${filePath}:`);
    expect(errorSpy).toHaveBeenCalledWith('- JSON parsing error: Unexpected token } in JSON at position 25');

    jsonParseSpy.mockRestore();
    exitSpy.mockRestore();
    errorSpy.mockRestore();
  });

  it('should lint a valid YAML file successfully', () => {
    const validYamlContent = 'key: value\nlist:\n  - item1\n  - item2';
    const filePath = '/path/to/valid.yaml';
    createMockFile(filePath, validYamlContent);
    mockPath.extname.mockReturnValue('.yaml');
    mockYaml.load.mockReturnValue({ key: 'value', list: ['item1', 'item2'] }); // Mock successful YAML load

    process.argv = ['node', 'src/index.ts', filePath];
    const exitSpy = jest.spyOn(process, 'exit').mockImplementation(() => undefined as never);
    const logSpy = jest.spyOn(console, 'log').mockImplementation(() => {});

    require('../src/index');

    expect(mockFs.readFileSync).toHaveBeenCalledWith(filePath, 'utf-8');
    expect(mockPath.extname).toHaveBeenCalledWith(filePath);
    expect(mockYaml.load).toHaveBeenCalledWith(validYamlContent);
    expect(exitSpy).toHaveBeenCalledWith(0);
    expect(logSpy).toHaveBeenCalledWith(`Configuration file ${filePath} linted successfully.`);

    exitSpy.mockRestore();
    logSpy.mockRestore();
  });

  it('should report an error for an invalid YAML file', () => {
    const invalidYamlContent = 'key: value\nlist:\n  - item1\n  - item2\n  -'; // Invalid YAML structure
    const filePath = '/path/to/invalid.yml';
    createMockFile(filePath, invalidYamlContent);
    mockPath.extname.mockReturnValue('.yml');

    // Mock js-yaml.load to throw an error
    mockYaml.load.mockImplementation(() => {
      throw new Error('Invalid YAML: Unexpected end of input');
    });

    process.argv = ['node', 'src/index.ts', filePath];
    const exitSpy = jest.spyOn(process, 'exit').mockImplementation(() => undefined as never);
    const errorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});

    require('../src/index');

    expect(mockFs.readFileSync).toHaveBeenCalledWith(filePath, 'utf-8');
    expect(mockPath.extname).toHaveBeenCalledWith(filePath);
    expect(mockYaml.load).toHaveBeenCalledWith(invalidYamlContent);
    expect(exitSpy).toHaveBeenCalledWith(1);
    expect(errorSpy).toHaveBeenCalledWith(`Linting errors found in ${filePath}:`);
    expect(errorSpy).toHaveBeenCalledWith('- YAML parsing error: Invalid YAML: Unexpected end of input');

    exitSpy.mockRestore();
    errorSpy.mockRestore();
  });

  it('should report an error for unsupported file extensions', () => {
    const filePath = '/path/to/unknown.txt';
    mockPath.extname.mockReturnValue('.txt');

    process.argv = ['node', 'src/index.ts', filePath];
    const exitSpy = jest.spyOn(process, 'exit').mockImplementation(() => undefined as never);
    const errorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});

    require('../src/index');

    expect(mockPath.extname).toHaveBeenCalledWith(filePath);
    expect(mockFs.readFileSync).not.toHaveBeenCalled(); // Should not read file for unsupported types
    expect(exitSpy).toHaveBeenCalledWith(1);
    expect(errorSpy).toHaveBeenCalledWith(`Linting errors found in ${filePath}:`);
    expect(errorSpy).toHaveBeenCalledWith('- Unsupported file extension: .txt');

    exitSpy.mockRestore();
    errorSpy.mockRestore();
  });

  it('should exit with error if no file path is provided', () => {
    process.argv = ['node', 'src/index.ts'];
    const exitSpy = jest.spyOn(process, 'exit').mockImplementation(() => undefined as never);
    const errorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});

    require('../src/index');

    expect(exitSpy).toHaveBeenCalledWith(1);
    expect(errorSpy).toHaveBeenCalledWith('Usage: nightly-ts-config-linter <path_to_config_file>');

    exitSpy.mockRestore();
    errorSpy.mockRestore();
  });
});
