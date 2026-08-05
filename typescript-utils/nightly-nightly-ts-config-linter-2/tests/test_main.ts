import * as fs from 'fs';
import * as path from 'path';
import { runLinter } from '../src/main'; // Assuming runLinter is exported for testing

// Mock the fs module to control file reading
jest.mock('fs');
const mockFs = fs as jest.Mocked<typeof fs>;

// Mock js-yaml for YAML parsing
jest.mock('js-yaml', () => ({
  load: jest.fn(),
}));
const mockYaml = require('js-yaml') as jest.Mocked<typeof import('js-yaml')>;

// Mock process.exit to prevent tests from exiting the process
let mockExit: jest.SpyInstance;

beforeAll(() => {
  mockExit = jest.spyOn(process, 'exit').mockImplementation(() => undefined as never);
});

afterAll(() => {
  mockExit.mockRestore();
});

// Helper to create mock files
const createMockFile = (filePath: string, content: string) => {
  mockFs.readFileSync.mockImplementation((file, encoding) => {
    if (path.resolve(file) === path.resolve(filePath) && encoding === 'utf-8') {
      return content;
    }
    throw new Error(`Unexpected file read: ${file}`);
  });
};

describe('nightly-ts-config-linter', () => {
  const testDir = path.join(__dirname, 'fixtures');

  beforeEach(() => {
    // Clear mocks before each test
    mockFs.readFileSync.mockClear();
    mockYaml.load.mockClear();
    mockExit.mockClear();

    // Ensure test directory exists (though not strictly needed for mocks)
    if (!fs.existsSync(testDir)) {
      fs.mkdirSync(testDir, { recursive: true });
    }
  });

  it('should lint a valid JSON config with no errors', () => {
    const validJsonConfig = {
      appName: "ApocalypseApp",
      version: "1.0.0",
      apiKey: "super-secret-key-123",
      settings: {
        timeout: 5000,
        retries: 3
      }
    };
    const jsonContent = JSON.stringify(validJsonConfig, null, 2);
    const filePath = path.join(testDir, 'valid.json');
    createMockFile(filePath, jsonContent);

    const errors = runLinter(filePath);

    expect(errors).toEqual([]);
    expect(mockFs.readFileSync).toHaveBeenCalledWith(filePath, 'utf-8');
  });

  it('should lint a valid YAML config with no errors', () => {
    const validYamlConfig = {
      appName: "ApocalypseApp",
      version: "1.0.0",
      apiKey: "super-secret-key-123",
      settings: {
        timeout: 5000,
        retries: 3
      }
    };
    const yamlContent = `---
appName: ApocalypseApp
version: 1.0.0
apiKey: super-secret-key-123
settings:
  timeout: 5000
  retries: 3
`;
    const filePath = path.join(testDir, 'valid.yaml');
    createMockFile(filePath, yamlContent);
    mockYaml.load.mockReturnValue(validYamlConfig);

    const errors = runLinter(filePath);

    expect(errors).toEqual([]);
    expect(mockFs.readFileSync).toHaveBeenCalledWith(filePath, 'utf-8');
    expect(mockYaml.load).toHaveBeenCalledWith(yamlContent);
  });

  it('should report empty string value error in JSON', () => {
    const invalidJsonConfig = {
      appName: "", // Empty value
      version: "1.0.0",
      apiKey: "valid-key"
    };
    const jsonContent = JSON.stringify(invalidJsonConfig, null, 2);
    const filePath = path.join(testDir, 'empty_value.json');
    createMockFile(filePath, jsonContent);

    const errors = runLinter(filePath);

    expect(errors).toHaveLength(1);
    expect(errors[0]).toEqual({
      ruleName: "no-empty-values",
      message: "Configuration key 'appName' has an empty string value.",
      filePath: filePath,
    });
  });

  it('should report missing apiKey error in JSON', () => {
    const invalidJsonConfig = {
      appName: "ApocalypseApp",
      version: "1.0.0"
      // apiKey is missing
    };
    const jsonContent = JSON.stringify(invalidJsonConfig, null, 2);
    const filePath = path.join(testDir, 'missing_api_key.json');
    createMockFile(filePath, jsonContent);

    const errors = runLinter(filePath);

    expect(errors).toHaveLength(1);
    expect(errors[0]).toEqual({
      ruleName: "require-api-key",
      message: "Configuration is missing an 'apiKey' field. This is crucial for many services!",
      filePath: filePath,
    });
  });

  it('should report sensitive data in comments error', () => {
    const configWithSensitiveComment = {
      appName: "ApocalypseApp",
      apiKey: "valid-key",
      comments: "This is a test comment with a password in it."
    };
    const jsonContent = JSON.stringify(configWithSensitiveComment, null, 2);
    const filePath = path.join(testDir, 'sensitive_comment.json');
    createMockFile(filePath, jsonContent);

    const errors = runLinter(filePath);

    expect(errors).toHaveLength(1);
    expect(errors[0]).toEqual({
      ruleName: "no-sensitive-data-in-comments",
      message: "Comment might contain sensitive information: 'password'. Please review.",
      filePath: filePath,
    });
  });

  it('should report multiple errors', () => {
    const multiErrorConfig = {
      appName: "", // Empty value
      version: "1.0.0"
      // apiKey is missing
    };
    const jsonContent = JSON.stringify(multiErrorConfig, null, 2);
    const filePath = path.join(testDir, 'multiple_errors.json');
    createMockFile(filePath, jsonContent);

    const errors = runLinter(filePath);

    expect(errors).toHaveLength(2);
    expect(errors).toContainEqual({
      ruleName: "no-empty-values",
      message: "Configuration key 'appName' has an empty string value.",
      filePath: filePath,
    });
    expect(errors).toContainEqual({
      ruleName: "require-api-key",
      message: "Configuration is missing an 'apiKey' field. This is crucial for many services!",
      filePath: filePath,
    });
  });

  it('should report JSON parsing error', () => {
    const malformedJson = "{\"appName\": \"Test\", \";
    const filePath = path.join(testDir, 'malformed.json');
    createMockFile(filePath, malformedJson);

    runLinter(filePath);

    // The runLinter function itself catches parsing errors and adds them
    // We expect the error to be of type 'parsing-error'
    const readErrors = mockFs.readFileSync.mock.results.filter(r => r.type === 'return').map(r => r.value);
    expect(readErrors.length).toBeGreaterThan(0);
    // We can't directly check runLinter's return value here without modifying it to export it.
    // Instead, we'll check if process.exit was called with 1, indicating an error.
    expect(mockExit).toHaveBeenCalledWith(1);
  });

  it('should report YAML parsing error', () => {
    const malformedYaml = "appName: Test\n  version: 1.0.0\n  invalid:
    - item1
    - item2: value"
    const filePath = path.join(testDir, 'malformed.yaml');
    createMockFile(filePath, malformedYaml);
    mockYaml.load.mockImplementation(() => {
      throw new Error('YAML parsing error: invalid syntax');
    });

    runLinter(filePath);
    expect(mockExit).toHaveBeenCalledWith(1);
  });

  it('should handle unsupported file extensions gracefully', () => {
    const filePath = path.join(testDir, 'unsupported.txt');
    createMockFile(filePath, 'some text content');

    // Expecting an error to be thrown and caught by the main execution flow
    // which would lead to process.exit(1)
    runLinter(filePath);
    expect(mockExit).toHaveBeenCalledWith(1);
  });
});
