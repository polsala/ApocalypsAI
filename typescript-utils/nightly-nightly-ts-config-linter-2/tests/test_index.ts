import { lintConfig, LintResult } from '../src/index';
import * as fs from 'fs';
import * as path from 'path';

// Mocking fs and path for deterministic tests
jest.mock('fs');
jest.mock('path');

// Mock fs module
const mockFs = fs as jest.Mocked<typeof fs>;
const mockPath = path as jest.Mocked<typeof path>;

describe('nightly-ts-config-linter', () => {
  const mockJsonContent = '{
  "appName": "ApocalypsAI",
  "version": "1.0.0"
}';
  const mockInvalidJsonContent = '{
  "appName": "ApocalypsAI",
  "version": "1.0.0",
  // This is a comment
}';
  const mockYamlContent = 'appName: ApocalypsAI
version: 1.0.0';
  const mockInvalidYamlContent = 'appName: ApocalypsAI
version: 1.0.0
  # This is a commented line';

  beforeEach(() => {
    // Reset mocks before each test
    mockFs.readFileSync.mockReset();
    mockPath.resolve.mockReset();
    mockPath.extname.mockReset();
  });

  it('should lint a valid JSON file successfully', () => {
    const mockFilePath = '/path/to/config.json';
    mockPath.resolve.mockReturnValue(mockFilePath);
    mockPath.extname.mockReturnValue('.json');
    mockFs.readFileSync.mockReturnValue(mockJsonContent);

    const result: LintResult = lintConfig(mockFilePath);

    expect(result.filePath).toBe(mockFilePath);
    expect(result.errors).toEqual([]);
  });

  it('should report an error for invalid JSON content', () => {
    const mockFilePath = '/path/to/invalid.json';
    mockPath.resolve.mockReturnValue(mockFilePath);
    mockPath.extname.mockReturnValue('.json');
    mockFs.readFileSync.mockReturnValue(mockInvalidJsonContent);

    const result: LintResult = lintConfig(mockFilePath);

    expect(result.filePath).toBe(mockFilePath);
    expect(result.errors).toContain('JSON files should not contain comments (//).');
    expect(result.errors.length).toBe(1);
  });

  it('should report a JSON parsing error for malformed JSON', () => {
    const mockFilePath = '/path/to/malformed.json';
    const malformedJson = '{ "key": "value"'; // Missing closing brace
    mockPath.resolve.mockReturnValue(mockFilePath);
    mockPath.extname.mockReturnValue('.json');
    mockFs.readFileSync.mockReturnValue(malformedJson);

    const result: LintResult = lintConfig(mockFilePath);

    expect(result.filePath).toBe(mockFilePath);
    expect(result.errors).toContain('JSON parsing error: Unexpected end of JSON input');
    expect(result.errors.length).toBe(1);
  });

  it('should lint a valid YAML file successfully', () => {
    const mockFilePath = '/path/to/config.yaml';
    mockPath.resolve.mockReturnValue(mockFilePath);
    mockPath.extname.mockReturnValue('.yaml');
    mockFs.readFileSync.mockReturnValue(mockYamlContent);

    const result: LintResult = lintConfig(mockFilePath);

    expect(result.filePath).toBe(mockFilePath);
    expect(result.errors).toEqual([]);
  });

  it('should report an error for invalid YAML content', () => {
    const mockFilePath = '/path/to/invalid.yaml';
    mockPath.resolve.mockReturnValue(mockFilePath);
    mockPath.extname.mockReturnValue('.yaml');
    mockFs.readFileSync.mockReturnValue(mockInvalidYamlContent);

    const result: LintResult = lintConfig(mockFilePath);

    expect(result.filePath).toBe(mockFilePath);
    expect(result.errors).toContain('YAML files should use `#` for comments, not `  #`.');
    expect(result.errors.length).toBe(1);
  });

  it('should report a YAML parsing error for malformed YAML', () => {
    const mockFilePath = '/path/to/malformed.yaml';
    const malformedYaml = 'key: value
  nested:
    - item1
    - item2'; // Intentional indentation issue for demonstration
    mockPath.resolve.mockReturnValue(mockFilePath);
    mockPath.extname.mockReturnValue('.yaml');
    mockFs.readFileSync.mockReturnValue(malformedYaml);

    const result: LintResult = lintConfig(mockFilePath);

    expect(result.filePath).toBe(mockFilePath);
    // The exact error message can vary slightly between js-yaml versions, so we check for a substring.
    expect(result.errors[0]).toMatch(/YAML parsing error:.*unexpected indentation/i);
    expect(result.errors.length).toBe(1);
  });

  it('should report an error for unsupported file extensions', () => {
    const mockFilePath = '/path/to/config.txt';
    mockPath.resolve.mockReturnValue(mockFilePath);
    mockPath.extname.mockReturnValue('.txt');
    mockFs.readFileSync.mockReturnValue('some text content');

    const result: LintResult = lintConfig(mockFilePath);

    expect(result.filePath).toBe(mockFilePath);
    expect(result.errors).toEqual(['Unsupported file extension: .txt']);
  });

  it('should handle file not found errors gracefully', () => {
    const mockFilePath = '/path/to/nonexistent.json';
    mockPath.resolve.mockReturnValue(mockFilePath);
    mockPath.extname.mockReturnValue('.json');
    // Mocking readFileSync to throw an error, simulating file not found
    mockFs.readFileSync.mockImplementation(() => {
      throw new Error('ENOENT: no such file or directory');
    });

    const result: LintResult = lintConfig(mockFilePath);

    expect(result.filePath).toBe(mockFilePath);
    expect(result.errors).toContain('JSON parsing error: ENOENT: no such file or directory');
    expect(result.errors.length).toBe(1);
  });
});
