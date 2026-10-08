import * as fs from 'fs';
import * as path from 'path';
import { Linter, Rule } from '../src/index'; // Assuming Linter and Rule are exported from index.ts

// Mock the file system module
jest.mock('fs');
jest.mock('path');

// Mock fs and path functions
const mockFs = fs as jest.Mocked<typeof fs>;
const mockPath = path as jest.Mocked<typeof path>;

// Mock js-yaml
jest.mock('js-yaml', () => ({
  load: jest.fn(),
}));
const mockYaml = require('js-yaml') as jest.Mocked<typeof import('js-yaml')>;

// Helper to create a dummy config file
const createDummyConfigFile = (content: string, extension: string = '.json'): string => {
  const filePath = `dummy_config${extension}`;
  mockFs.readFileSync.mockReturnValue(content);
  mockPath.extname.mockReturnValue(extension);
  return filePath;
};

describe('Nightly TypeScript Configuration Linter', () => {
  let linter: Linter;

  beforeEach(() => {
    // Reset mocks before each test
    jest.clearAllMocks();

    // Mock default rules to ensure they are present
    const mockDefaultRules: Rule[] = [
      {
        name: "require-app-name",
        description: "Configuration must have an 'appName' field.",
        check: (config) => {
          if (!config.appName) {
            return ["'appName' field is missing."];
          }
          return [];
        }
      },
      {
        name: "valid-log-level",
        description: "'logLevel' must be one of INFO, WARN, ERROR, DEBUG.",
        check: (config) => {
          const validLevels = ["INFO", "WARN", "ERROR", "DEBUG"];
          if (config.logLevel && !validLevels.includes(config.logLevel.toUpperCase())) {
            return [`Invalid logLevel: ${config.logLevel}. Must be one of ${validLevels.join(', ')}.`];
          }
          return [];
        }
      },
      {
        name: "features-object",
        description: "The 'features' field should be an object.",
        check: (config) => {
          if (config.features && typeof config.features !== 'object') {
            return ["'features' field must be an object."];
          }
          return [];
        }
      }
    ];
    linter = new Linter(mockDefaultRules);
  });

  it('should pass linting for a valid JSON configuration', () => {
    const validConfig = {
      appName: "TestApp",
      version: "1.0.0",
      logLevel: "INFO",
      features: {
        newUI: true
      }
    };
    const configPath = createDummyConfigFile(JSON.stringify(validConfig), '.json');
    mockYaml.load.mockReturnValue(validConfig); // Ensure yaml mock doesn't interfere

    const errors = linter.lint(configPath);
    expect(errors).toEqual([]);
  });

  it('should fail linting for missing appName in JSON', () => {
    const invalidConfig = {
      version: "1.0.0",
      logLevel: "INFO"
    };
    const configPath = createDummyConfigFile(JSON.stringify(invalidConfig), '.json');

    const errors = linter.lint(configPath);
    expect(errors.length).toBeGreaterThan(0);
    expect(errors[0]).toContain("Rule 'require-app-name'");
    expect(errors[0]).toContain("'appName' field is missing.");
  });

  it('should fail linting for invalid logLevel in JSON', () => {
    const invalidConfig = {
      appName: "TestApp",
      logLevel: "VERBOSE"
    };
    const configPath = createDummyConfigFile(JSON.stringify(invalidConfig), '.json');

    const errors = linter.lint(configPath);
    expect(errors.length).toBeGreaterThan(0);
    expect(errors[0]).toContain("Rule 'valid-log-level'");
    expect(errors[0]).toContain("Invalid logLevel: VERBOSE.");
  });

  it('should fail linting for non-object features in JSON', () => {
    const invalidConfig = {
      appName: "TestApp",
      features: "enabled"
    };
    const configPath = createDummyConfigFile(JSON.stringify(invalidConfig), '.json');

    const errors = linter.lint(configPath);
    expect(errors.length).toBeGreaterThan(0);
    expect(errors[0]).toContain("Rule 'features-object'");
    expect(errors[0]).toContain("'features' field must be an object.");
  });

  it('should pass linting for a valid YAML configuration', () => {
    const validConfig = {
      appName: "TestAppYAML",
      version: "1.0.0",
      logLevel: "WARN",
      features: {
        betaFeature: true
      }
    };
    const configPath = createDummyConfigFile(JSON.stringify(validConfig), '.yaml'); // Content is JSON string, but extname is .yaml
    mockYaml.load.mockReturnValue(validConfig);

    const errors = linter.lint(configPath);
    expect(errors).toEqual([]);
  });

  it('should fail linting for missing appName in YAML', () => {
    const invalidConfig = {
      version: "1.0.0",
      logLevel: "ERROR"
    };
    const configPath = createDummyConfigFile(JSON.stringify(invalidConfig), '.yaml');
    mockYaml.load.mockReturnValue(invalidConfig);

    const errors = linter.lint(configPath);
    expect(errors.length).toBeGreaterThan(0);
    expect(errors[0]).toContain("Rule 'require-app-name'");
    expect(errors[0]).toContain("'appName' field is missing.");
  });

  it('should return an error for unsupported file types', () => {
    const configPath = createDummyConfigFile("some text content", '.txt');
    mockPath.extname.mockReturnValue('.txt');

    const errors = linter.lint(configPath);
    expect(errors.length).toBeGreaterThan(0);
    expect(errors[0]).toContain("Unsupported file extension: .txt");
  });

  it('should return an error if file reading fails', () => {
    const configPath = 'non_existent_file.json';
    mockFs.readFileSync.mockImplementation(() => {
      throw new Error('File not found');
    });

    const errors = linter.lint(configPath);
    expect(errors.length).toBeGreaterThan(0);
    expect(errors[0]).toContain("Error reading or parsing file");
    expect(errors[0]).toContain("File not found");
  });

  it('should return an error if JSON parsing fails', () => {
    const invalidJsonContent = '{ "appName": "TestApp", "version": "1.0.0", }'; // Trailing comma
    const configPath = createDummyConfigFile(invalidJsonContent, '.json');

    const errors = linter.lint(configPath);
    expect(errors.length).toBeGreaterThan(0);
    expect(errors[0]).toContain("Error reading or parsing file");
    expect(errors[0]).toContain("Unexpected token"); // Or similar JSON parse error message
  });

  it('should return an error if YAML parsing fails', () => {
    const invalidYamlContent = 'appName: TestApp
version: 1.0.0
logLevel: INFO
features:
  newUI: true
  betaFeature:'; // Incomplete value
    const configPath = createDummyConfigFile(invalidYamlContent, '.yaml');
    mockYaml.load.mockImplementation(() => {
      throw new Error('YAML parse error');
    });

    const errors = linter.lint(configPath);
    expect(errors.length).toBeGreaterThan(0);
    expect(errors[0]).toContain("Error reading or parsing file");
    expect(errors[0]).toContain("YAML parse error");
  });

  it('should handle custom rules', () => {
    const customRule: Rule = {
      name: "custom-rule-example",
      description: "A custom rule that checks for a specific key.",
      check: (config) => {
        if (!config.customSetting) {
          return ["'customSetting' is required."];
        }
        return [];
      }
    };
    linter.addRule(customRule);

    const configWithCustomSetting = {
      appName: "TestApp",
      customSetting: "enabled"
    };
    const configPath = createDummyConfigFile(JSON.stringify(configWithCustomSetting), '.json');

    const errors = linter.lint(configPath);
    expect(errors).toEqual([]);

    const configWithoutCustomSetting = {
      appName: "TestApp"
    };
    const configPath2 = createDummyConfigFile(JSON.stringify(configWithoutCustomSetting), '.json');
    const errors2 = linter.lint(configPath2);
    expect(errors2.length).toBeGreaterThan(0);
    expect(errors2[0]).toContain("Rule 'custom-rule-example'");
    expect(errors2[0]).toContain("'customSetting' is required.");
  });
});
