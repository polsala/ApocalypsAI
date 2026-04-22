import { lintConfig, LintError } from '../src/main';
import * as fs from 'fs';
import * as path from 'path';

// Mock the file system to avoid actual file operations during tests
jest.mock('fs');
jest.mock('path');

const mockFs = fs as jest.Mocked<typeof fs>;
const mockPath = path as jest.Mocked<typeof path>;

// Mock rationale: These mocks are essential for deterministic and offline testing.
// They allow us to control the input (file content) and simulate file system interactions
// without relying on the actual file system, ensuring tests are fast, reliable, and runnable anywhere.

describe('nightly-ts-config-linter', () => {
  beforeEach(() => {
    // Reset mocks before each test
    mockFs.readFileSync.mockClear();
    mockPath.extname.mockClear();
    mockPath.resolve.mockClear();
    mockFs.existsSync.mockClear();
  });

  it('should return no errors for a valid JSON config', () => {
    const validJsonConfig = {
      version: '1.0.0',
      settings: {
        timeout: 5000,
        retries: 3
      }
    };
    mockFs.readFileSync.mockReturnValue(JSON.stringify(validJsonConfig));
    mockPath.extname.mockReturnValue('.json');
    mockFs.existsSync.mockReturnValue(true);

    const errors = lintConfig('/fake/path/to/config.json');
    expect(errors).toEqual([]);
  });

  it('should return no errors for a valid YAML config', () => {
    const validYamlConfig = `
version: "1.0.0"
settings:
  timeout: 5000
  retries: 3
`;
    mockFs.readFileSync.mockReturnValue(validYamlConfig);
    mockPath.extname.mockReturnValue('.yaml');
    mockFs.existsSync.mockReturnValue(true);

    const errors = lintConfig('/fake/path/to/config.yaml');
    expect(errors).toEqual([]);
  });

  it('should report missing required keys', () => {
    const invalidJsonConfig = {
      settings: {
        timeout: 5000
      }
    };
    mockFs.readFileSync.mockReturnValue(JSON.stringify(invalidJsonConfig));
    mockPath.extname.mockReturnValue('.json');
    mockFs.existsSync.mockReturnValue(true);

    const errors = lintConfig('/fake/path/to/config.json');
    expect(errors).toContainEqual({
      rule: 'required-keys',
      message: "Required key 'version' is missing.",
      path: ''
    });
    expect(errors.length).toBe(1);
  });

  it('should report empty objects', () => {
    const invalidJsonConfig = {
      version: '1.0.0',
      settings: {},
      features: {
        experimental: {}
      }
    };
    mockFs.readFileSync.mockReturnValue(JSON.stringify(invalidJsonConfig));
    mockPath.extname.mockReturnValue('.json');
    mockFs.existsSync.mockReturnValue(true);

    const errors = lintConfig('/fake/path/to/config.json');
    expect(errors).toContainEqual({
      rule: 'no-empty-objects',
      message: "Object at path 'settings' is empty.",
      path: 'settings'
    });
    expect(errors).toContainEqual({
      rule: 'no-empty-objects',
      message: "Object at path 'features.experimental' is empty.",
      path: 'features.experimental'
    });
    expect(errors.length).toBe(2);
  });

  it('should report parsing errors for invalid JSON', () => {
    const invalidJsonContent = '{ "version": "1.0.0", "settings": { }'; // Missing closing brace
    mockFs.readFileSync.mockReturnValue(invalidJsonContent);
    mockPath.extname.mockReturnValue('.json');
    mockFs.existsSync.mockReturnValue(true);

    const errors = lintConfig('/fake/path/to/invalid.json');
    expect(errors).toContainEqual({
      rule: 'parsing-error',
      message: expect.stringContaining('Unexpected end of JSON input')
    });
    expect(errors.length).toBe(1);
  });

  it('should report parsing errors for invalid YAML', () => {
    const invalidYamlContent = 'version: 1.0.0
settings:
  timeout: 5000
  retries: 3
  invalid: {'; // Malformed YAML
    mockFs.readFileSync.mockReturnValue(invalidYamlContent);
    mockPath.extname.mockReturnValue('.yaml');
    mockFs.existsSync.mockReturnValue(true);

    const errors = lintConfig('/fake/path/to/invalid.yaml');
    expect(errors).toContainEqual({
      rule: 'parsing-error',
      message: expect.stringContaining('mapping values are not allowed here')
    });
    expect(errors.length).toBe(1);
  });

  it('should throw an error for unsupported file extensions', () => {
    mockFs.readFileSync.mockReturnValue('some content');
    mockPath.extname.mockReturnValue('.txt');
    mockFs.existsSync.mockReturnValue(true);

    expect(() => lintConfig('/fake/path/to/config.txt')).toThrow('Unsupported file extension: .txt. Only JSON and YAML are supported.');
  });

  it('should handle nested structures correctly for empty object rule', () => {
    const nestedConfig = {
      version: '1.0.0',
      settings: {
        network: {
          protocol: 'http',
          options: {}
        },
        database: {
          host: 'localhost'
        }
      }
    };
    mockFs.readFileSync.mockReturnValue(JSON.stringify(nestedConfig));
    mockPath.extname.mockReturnValue('.json');
    mockFs.existsSync.mockReturnValue(true);

    const errors = lintConfig('/fake/path/to/nested.json');
    expect(errors).toContainEqual({
      rule: 'no-empty-objects',
      message: "Object at path 'settings.network.options' is empty.",
      path: 'settings.network.options'
    });
    expect(errors.length).toBe(1);
  });
});
