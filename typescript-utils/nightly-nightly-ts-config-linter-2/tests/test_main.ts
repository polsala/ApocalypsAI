import { lintConfig, LintRule, LintError } from '../src/main';
import * as fs from 'fs';
import * as path from 'path';

// Mocking fs and path for deterministic tests
jest.mock('fs');
jest.mock('path');

const mockFs = fs as jest.Mocked<typeof fs>;
const mockPath = path as jest.Mocked<typeof path>;

// Mock data for test configuration files
const mockJsonConfig = {
  name: 'my-app',
  version: '1.0.0',
  description: 'A sample app',
  main: 'index.js',
  scripts: {
    start: 'node index.js'
  },
  dependencies: {
    react: '^18.0.0'
  }
};

const mockYamlConfig = `
name: my-yaml-app
version: 0.5.0
description: Another sample config
settings:
  timeout: 5000
  retries: 3
`;

const mockJsonConfigMissingVersion = {
  name: 'app-without-version',
  description: 'This config is missing version',
  main: 'index.js'
};

const mockJsonConfigEmptyString = {
  name: '',
  version: '1.0.0',
  description: 'App with empty name',
  main: 'index.js'
};

describe('Nightly TypeScript Config Linter', () => {

  beforeEach(() => {
    // Reset mocks before each test
    jest.clearAllMocks();

    // Mock path.extname to return consistent extensions
    mockPath.extname.mockImplementation((filePath) => path.extname(filePath));
    mockPath.resolve.mockImplementation((filePath) => filePath); // Simple resolve for tests
  });

  describe('parseConfigFile', () => {
    it('should parse JSON files correctly', () => {
      // Mock fs.readFileSync for JSON
      mockFs.readFileSync.mockReturnValue(JSON.stringify(mockJsonConfig));
      const parsed = lintConfig('test.json');
      // The lintConfig function itself calls parseConfigFile internally, so we test its output
      // We expect no errors for a valid config
      expect(parsed).toEqual([]);
    });

    it('should parse YAML files correctly', () => {
      // Mock fs.readFileSync for YAML
      mockFs.readFileSync.mockReturnValue(mockYamlConfig);
      // Need to mock js-yaml's load function if it's not directly imported in main.ts
      // For simplicity, assuming js-yaml is correctly imported and used.
      // If js-yaml is a direct import, we'd mock it here.
      // For this test, we'll assume the parsing logic within lintConfig works.
      // A more thorough test would mock js-yaml directly.
      const parsed = lintConfig('test.yaml');
      expect(parsed).toEqual([]);
    });

    it('should throw an error for unsupported file types', () => {
      mockFs.readFileSync.mockReturnValue('some content');
      const errors = lintConfig('test.txt');
      expect(errors.length).toBe(1);
      expect(errors[0].rule).toBe('parsing');
      expect(errors[0].message).toContain('Unsupported file extension: .txt');
    });
  });

  describe('lintConfig', () => {
    it('should return no errors for a valid JSON configuration', () => {
      mockFs.readFileSync.mockReturnValue(JSON.stringify(mockJsonConfig));
      const errors = lintConfig('valid.json');
      expect(errors).toEqual([]);
    });

    it('should return no errors for a valid YAML configuration', () => {
      mockFs.readFileSync.mockReturnValue(mockYamlConfig);
      const errors = lintConfig('valid.yaml');
      expect(errors).toEqual([]);
    });

    it('should report missing required fields', () => {
      mockFs.readFileSync.mockReturnValue(JSON.stringify(mockJsonConfigMissingVersion));
      const errors = lintConfig('missing_version.json');
      expect(errors.length).toBe(1);
      expect(errors[0].rule).toBe('required-fields');
      expect(errors[0].message).toContain("Required field 'version' is missing.");
    });

    it('should report empty string values', () => {
      mockFs.readFileSync.mockReturnValue(JSON.stringify(mockJsonConfigEmptyString));
      const errors = lintConfig('empty_string.json');
      expect(errors.length).toBe(1);
      expect(errors[0].rule).toBe('no-empty-strings');
      expect(errors[0].message).toContain("Field 'name' has an empty string value.");
    });

    it('should handle multiple errors from different rules', () => {
      const configWithMultipleIssues = {
        name: '',
        description: 'This config has multiple issues'
        // Missing version
      };
      mockFs.readFileSync.mockReturnValue(JSON.stringify(configWithMultipleIssues));
      const errors = lintConfig('multiple_issues.json');
      expect(errors.length).toBe(2);
      expect(errors).toContainEqual({
        rule: 'required-fields',
        message: "Required field 'version' is missing.",
        filePath: 'multiple_issues.json'
      });
      expect(errors).toContainEqual({
        rule: 'no-empty-strings',
        message: "Field 'name' has an empty string value.",
        filePath: 'multiple_issues.json'
      });
    });

    it('should handle nested empty strings', () => {
      const nestedEmptyConfig = {
        name: 'parent',
        version: '1.0.0',
        settings: {
          host: '',
          port: 8080
        }
      };
      mockFs.readFileSync.mockReturnValue(JSON.stringify(nestedEmptyConfig));
      const errors = lintConfig('nested_empty.json');
      expect(errors.length).toBe(1);
      expect(errors[0].rule).toBe('no-empty-strings');
      expect(errors[0].message).toContain("Field 'settings.host' has an empty string value.");
    });
  });

  // Mock rationale: js-yaml is a dependency for YAML parsing. We mock its load method
  // to ensure our tests are deterministic and don't rely on the actual js-yaml library
  // being installed or its behavior changing. This allows us to control the output
  // of YAML parsing for testing purposes.
  describe('YAML Parsing Mock', () => {
    let jsyaml: any;

    beforeAll(() => {
      // Dynamically import js-yaml to mock it
      jsyaml = require('js-yaml');
      jest.spyOn(jsyaml, 'load').mockImplementation((content: string) => {
        // Simple mock implementation for YAML parsing
        if (content.includes('name: mock-yaml')) {
          return { name: 'mock-yaml', version: '1.0.0' };
        } else if (content.includes('invalid-yaml')) {
          throw new Error('Mocked YAML parsing error');
        }
        return {}; // Default empty object for other cases
      });
    });

    afterAll(() => {
      jest.restoreAllMocks(); // Restore original js-yaml functions
    });

    it('should correctly parse mocked YAML content', () => {
      mockFs.readFileSync.mockReturnValue('name: mock-yaml\nversion: 1.0.0');
      const errors = lintConfig('mocked.yaml');
      expect(errors).toEqual([]);
    });

    it('should report errors for mocked invalid YAML', () => {
      mockFs.readFileSync.mockReturnValue('invalid-yaml');
      const errors = lintConfig('invalid.yaml');
      expect(errors.length).toBe(1);
      expect(errors[0].rule).toBe('parsing');
      expect(errors[0].message).toContain('Mocked YAML parsing error');
    });
  });
});
