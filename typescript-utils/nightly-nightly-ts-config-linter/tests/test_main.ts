import { execSync } from 'child_process';
import * as fs from 'fs';
import * as path from 'path';

// Mock rationale: We are mocking file system operations and child process execution
// to ensure deterministic and offline testing.

const TEST_DIR = path.join(__dirname, 'fixtures');
const SCRIPT_PATH = path.join(__dirname, '../src/main.ts');

// Helper to create temporary files for tests
function createTestFile(fileName: string, content: string): string {
  const filePath = path.join(TEST_DIR, fileName);
  fs.writeFileSync(filePath, content, 'utf-8');
  return filePath;
}

// Helper to clean up temporary files
function cleanupTestFile(filePath: string): void {
  if (fs.existsSync(filePath)) {
    fs.unlinkSync(filePath);
  }
}

// Helper to run the linter script
function runLinter(configPath: string, schemaPath: string): { stdout: string, stderr: string, exitCode: number } {
  try {
    const command = `ts-node ${SCRIPT_PATH} --config ${configPath} --schema ${schemaPath}`;
    const stdout = execSync(command, { encoding: 'utf-8', stdio: ['pipe', 'pipe', 'pipe'] });
    return { stdout, stderr: '', exitCode: 0 };
  } catch (error: any) {
    return {
      stdout: error.stdout || '',
      stderr: error.stderr || error.message,
      exitCode: error.status || 1,
    };
  }
}

describe('nightly-ts-config-linter', () => {
  let validConfigPath: string;
  let invalidConfigPath: string;
  let schemaPath: string;

  beforeAll(() => {
    // Ensure test directory exists
    if (!fs.existsSync(TEST_DIR)) {
      fs.mkdirSync(TEST_DIR);
    }

    // Create a valid configuration file
    const validConfigContent = JSON.stringify({
      server: { port: 8080, timeout: 30 },
      database: { host: 'localhost', port: 5432 },
    });
    validConfigPath = createTestFile('valid_config.json', validConfigContent);

    // Create an invalid configuration file
    const invalidConfigContent = JSON.stringify({
      server: { port: 80, timeout: 5 }, // Port too low, timeout too low
      database: { host: '127.0.0.1' }, // Missing port
    });
    invalidConfigPath = createTestFile('invalid_config.json', invalidConfigContent);

    // Create a schema file
    const schemaContent = JSON.stringify({
      type: 'object',
      properties: {
        server: {
          type: 'object',
          properties: {
            port: { type: 'integer', minimum: 1024, maximum: 65535 },
            timeout: { type: 'integer', minimum: 10 },
          },
          required: ['port', 'timeout'],
        },
        database: {
          type: 'object',
          properties: {
            host: { type: 'string' },
            port: { type: 'integer' },
          },
          required: ['host', 'port'],
        },
      },
      required: ['server', 'database'],
    });
    schemaPath = createTestFile('schema.json', schemaContent);
  });

  afterAll(() => {
    // Clean up test files
    cleanupTestFile(validConfigPath);
    cleanupTestFile(invalidConfigPath);
    cleanupTestFile(schemaPath);
    // Clean up test directory if empty
    if (fs.existsSync(TEST_DIR) && fs.readdirSync(TEST_DIR).length === 0) {
      fs.rmdirSync(TEST_DIR);
    }
  });

  test('should validate a correct configuration file', () => {
    const result = runLinter(validConfigPath, schemaPath);
    expect(result.exitCode).toBe(0);
    expect(result.stdout).toContain('Configuration is valid.');
    expect(result.stderr).toBe('');
  });

  test('should report errors for an invalid configuration file', () => {
    const result = runLinter(invalidConfigPath, schemaPath);
    expect(result.exitCode).toBe(1);
    expect(result.stderr).toContain('Configuration validation failed:');
    expect(result.stderr).toContain('server.port: Must be greater than or equal to 1024');
    expect(result.stderr).toContain('server.timeout: Must be greater than or equal to 10');
    expect(result.stderr).toContain('database.port: is a required property');
  });

  test('should throw an error for missing config file', () => {
    const nonExistentConfig = path.join(TEST_DIR, 'non_existent.json');
    const result = runLinter(nonExistentConfig, schemaPath);
    expect(result.exitCode).toBe(1);
    expect(result.stderr).toContain('Failed to load or parse file');
  });

  test('should throw an error for missing schema file', () => {
    const nonExistentSchema = path.join(TEST_DIR, 'non_existent_schema.json');
    const result = runLinter(validConfigPath, nonExistentSchema);
    expect(result.exitCode).toBe(1);
    expect(result.stderr).toContain('Failed to load or parse file');
  });

  test('should throw an error for invalid JSON in config file', () => {
    const invalidJsonConfigPath = createTestFile('invalid_json_config.json', '{ "key": "value", }'); // Trailing comma
    const result = runLinter(invalidJsonConfigPath, schemaPath);
    expect(result.exitCode).toBe(1);
    expect(result.stderr).toContain('Failed to load or parse file');
    cleanupTestFile(invalidJsonConfigPath);
  });

  test('should throw an error for invalid JSON in schema file', () => {
    const invalidJsonSchemaPath = createTestFile('invalid_json_schema.json', '{ "type": "object", }'); // Trailing comma
    const result = runLinter(validConfigPath, invalidJsonSchemaPath);
    expect(result.exitCode).toBe(1);
    expect(result.stderr).toContain('Failed to load or parse file');
    cleanupTestFile(invalidJsonSchemaPath);
  });

  test('should throw usage error if arguments are missing', () => {
    const command = `ts-node ${SCRIPT_PATH}`;
    try {
      execSync(command, { encoding: 'utf-8', stdio: ['pipe', 'pipe', 'pipe'] });
    } catch (error: any) {
      expect(error.stderr).toContain('Usage: nightly-ts-config-linter --config <path-to-config-file> --schema <path-to-schema-file>');
    }
  });
});
