import { validateConfig, parseArgs, readJsonFile } from '../src/index';
import * as fs from 'fs';
import * as path from 'path';

// Mock rationale: Mocking file system operations to ensure deterministic and offline tests.
jest.mock('fs');
jest.mock('path');

const mockFs = fs as jest.Mocked<typeof fs>;
const mockPath = path as jest.Mocked<typeof path>;

describe('ts-config-linter', () => {

  beforeEach(() => {
    // Reset mocks before each test
    mockFs.readFileSync.mockClear();
    mockPath.resolve.mockClear();
  });

  describe('parseArgs', () => {
    it('should parse valid arguments', () => {
      const args = parseArgs(['--config', 'my-config.json', '--schema', 'my-schema.json']);
      expect(args).toEqual({
        config: 'my-config.json',
        schema: 'my-schema.json',
      });
    });

    it('should throw an error if --config is missing', () => {
      expect(() => parseArgs(['--schema', 'my-schema.json'])).toThrow();
    });

    it('should throw an error if --schema is missing', () => {
      expect(() => parseArgs(['--config', 'my-config.json'])).toThrow();
    });
  });

  describe('readJsonFile', () => {
    it('should read and parse a JSON file', () => {
      const mockContent = '{"key": "value"}';
      mockFs.readFileSync.mockReturnValue(mockContent);
      const result = readJsonFile('test.json');
      expect(mockFs.readFileSync).toHaveBeenCalledWith('test.json', 'utf-8');
      expect(result).toEqual({ key: 'value' });
    });

    it('should throw an error if file cannot be read', () => {
      mockFs.readFileSync.mockImplementation(() => {
        throw new Error('File not found');
      });
      expect(() => readJsonFile('nonexistent.json')).toThrow('Error reading or parsing file nonexistent.json: File not found');
    });

    it('should throw an error if JSON is invalid', () => {
      const invalidJson = '{key: "value"}'; // Missing quotes around key
      mockFs.readFileSync.mockReturnValue(invalidJson);
      expect(() => readJsonFile('invalid.json')).toThrow('Error reading or parsing file invalid.json: Unexpected token k in JSON at position 1');
    });
  });

  describe('validateConfig', () => {
    const validSchema = {
      type: 'object',
      properties: {
        name: { type: 'string' },
        age: { type: 'integer' },
      },
      required: ['name', 'age'],
    };

    it('should return an empty array for valid configuration', () => {
      const validConfig = { name: 'Alice', age: 30 };
      const errors = validateConfig(validConfig, validSchema);
      expect(errors).toEqual([]);
    });

    it('should return errors for missing required properties', () => {
      const invalidConfig = { name: 'Bob' }; // Missing age
      const errors = validateConfig(invalidConfig, validSchema);
      expect(errors.length).toBeGreaterThan(0);
      expect(errors.some(err => err.includes('age') && err.includes('is a required property'))).toBe(true);
    });

    it('should return errors for incorrect property types', () => {
      const invalidConfig = { name: 'Charlie', age: 'twenty' }; // Age is string
      const errors = validateConfig(invalidConfig, validSchema);
      expect(errors.length).toBeGreaterThan(0);
      expect(errors.some(err => err.includes('age') && err.includes('must be integer'))).toBe(true);
    });

    it('should handle nested schemas and properties', () => {
      const nestedSchema = {
        type: 'object',
        properties: {
          user: {
            type: 'object',
            properties: {
              id: { type: 'number' },
              username: { type: 'string' },
            },
            required: ['id', 'username'],
          }
        },
        required: ['user'],
      };
      const invalidConfig = { user: { id: 123 } }; // Missing username
      const errors = validateConfig(invalidConfig, nestedSchema);
      expect(errors.length).toBeGreaterThan(0);
      expect(errors.some(err => err.includes('/user/username') && err.includes('is a required property'))).toBe(true);
    });
  });

  // Mocking the main function's exit behavior for tests
  let processExitSpy: jest.SpyInstance;
  beforeAll(() => {
    processExitSpy = jest.spyOn(process, 'exit').mockImplementation((code?: number) => {
      throw new Error(`process.exit called with code: ${code}`);
    });
  });

  afterAll(() => {
    processExitSpy.mockRestore();
  });

  // Test for the main execution flow (integration-like)
  describe('main execution', () => {
    const mockConfigContent = '{"appName": "TestApp", "version": "1.0.0", "port": 8080, "features": {"darkMode": true, "betaFeatures": false}}';
    const mockSchemaContent = '{
      "type": "object",
      "properties": {
        "appName": {"type": "string"},
        "version": {"type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$"},
        "port": {"type": "integer", "minimum": 1024, "maximum": 65535},
        "features": {
          "type": "object",
          "properties": {
            "darkMode": {"type": "boolean"},
            "betaFeatures": {"type": "boolean"}
          },
          "required": ["darkMode", "betaFeatures"]
        }
      },
      "required": ["appName", "version", "port", "features"]
    }';

    it('should exit with code 0 for valid configuration', () => {
      mockFs.readFileSync.mockReturnValueOnce(mockConfigContent).mockReturnValueOnce(mockSchemaContent);
      mockPath.resolve.mockImplementation((p) => p);
      const consoleLogSpy = jest.spyOn(console, 'log').mockImplementation(() => {});

      expect(() => require('../src/index')).toThrow('process.exit called with code: 0');
      expect(consoleLogSpy).toHaveBeenCalledWith('Configuration is valid.');

      consoleLogSpy.mockRestore();
    });

    it('should exit with code 1 and print errors for invalid configuration', () => {
      const invalidConfigContent = '{"appName": "TestApp", "version": "1.0.0", "port": 80, "features": {"darkMode": true, "betaFeatures": false}}'; // Port is invalid
      mockFs.readFileSync.mockReturnValueOnce(invalidConfigContent).mockReturnValueOnce(mockSchemaContent);
      mockPath.resolve.mockImplementation((p) => p);
      const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});

      expect(() => require('../src/index')).toThrow('process.exit called with code: 1');
      expect(consoleErrorSpy).toHaveBeenCalledWith('Configuration validation failed:');
      expect(consoleErrorSpy).toHaveBeenCalledWith('- /port must be >= 1024 and <= 65535');

      consoleErrorSpy.mockRestore();
    });
  });
});
