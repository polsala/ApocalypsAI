import { lintConfig } from '../src/index';
import * as fs from 'fs';
import * as path from 'path';

// Mock rationale: Using fs.writeFileSync and fs.unlinkSync to create temporary files for testing.
// This ensures tests are deterministic and offline, simulating file system interactions.

const TEST_DIR = path.join(__dirname, 'temp_configs');

function createTempFile(fileName: string, content: string): string {
  if (!fs.existsSync(TEST_DIR)) {
    fs.mkdirSync(TEST_DIR);
  }
  const filePath = path.join(TEST_DIR, fileName);
  fs.writeFileSync(filePath, content, 'utf8');
  return filePath;
}

function cleanupTempFile(filePath: string): void {
  if (fs.existsSync(filePath)) {
    fs.unlinkSync(filePath);
  }
}

function cleanupTempDir(): void {
  if (fs.existsSync(TEST_DIR)) {
    fs.rmdirSync(TEST_DIR, { recursive: true });
  }
}

describe('nightly-ts-config-linter', () => {
  afterAll(() => {
    cleanupTempDir();
  });

  describe('lintConfig', () => {
    it('should return no errors for a valid JSON file', () => {
      const validJsonContent = '{
        "appName": "ApocalypseApp",
        "version": "1.0.0"
      }';
      const filePath = createTempFile('valid.json', validJsonContent);
      const result = lintConfig(filePath);
      expect(result.errors).toEqual([]);
      cleanupTempFile(filePath);
    });

    it('should return errors for an invalid JSON file', () => {
      const invalidJsonContent = '{
        "appName": "ApocalypseApp",
        "version": "1.0.0",
      '; // Trailing comma
      const filePath = createTempFile('invalid.json', invalidJsonContent);
      const result = lintConfig(filePath);
      expect(result.errors.length).toBeGreaterThan(0);
      expect(result.errors[0]).toContain('Failed to parse config file: Unexpected token');
      cleanupTempFile(filePath);
    });

    it('should return no errors for an empty JSON file if no schema is provided', () => {
      const emptyJsonContent = '{}';
      const filePath = createTempFile('empty.json', emptyJsonContent);
      const result = lintConfig(filePath);
      expect(result.errors).toEqual([]);
      cleanupTempFile(filePath);
    });

    it('should return an error for an empty JSON file if no schema is provided and it is truly empty', () => {
      const trulyEmptyJsonContent = '';
      const filePath = createTempFile('truly_empty.json', trulyEmptyJsonContent);
      const result = lintConfig(filePath);
      expect(result.errors.length).toBeGreaterThan(0);
      expect(result.errors[0]).toContain('Failed to parse config file: Unexpected end of JSON input');
      cleanupTempFile(filePath);
    });

    it('should return no errors for a valid YAML file', () => {
      const validYamlContent = 'appName: ApocalypseApp
version: 1.0.0';
      const filePath = createTempFile('valid.yaml', validYamlContent);
      const result = lintConfig(filePath);
      expect(result.errors).toEqual([]);
      cleanupTempFile(filePath);
    });

    it('should return errors for an invalid YAML file', () => {
      const invalidYamlContent = 'appName: ApocalypseApp
version: 1.0.0
  invalid_indent: true';
      const filePath = createTempFile('invalid.yaml', invalidYamlContent);
      const result = lintConfig(filePath);
      expect(result.errors.length).toBeGreaterThan(0);
      expect(result.errors[0]).toContain('Failed to parse config file: invalid indentation');
      cleanupTempFile(filePath);
    });

    it('should return no errors for a valid JSON file with a matching schema', () => {
      const jsonContent = '{
        "name": "MyService",
        "port": 8080,
        "enabled": true
      }';
      const schemaContent = '{
        "type": "object",
        "properties": {
          "name": {"type": "string"},
          "port": {"type": "integer", "minimum": 1024},
          "enabled": {"type": "boolean"}
        },
        "required": ["name", "port"]
      }';
      const filePath = createTempFile('valid_with_schema.json', jsonContent);
      const schemaPath = createTempFile('valid_schema.json', schemaContent);
      const result = lintConfig(filePath, { schemaPath });
      expect(result.errors).toEqual([]);
      cleanupTempFile(filePath);
      cleanupTempFile(schemaPath);
    });

    it('should return schema validation errors for a JSON file with a non-matching schema', () => {
      const jsonContent = '{
        "name": "MyService",
        "port": 80,
        "enabled": "yes"
      }';
      const schemaContent = '{
        "type": "object",
        "properties": {
          "name": {"type": "string"},
          "port": {"type": "integer", "minimum": 1024},
          "enabled": {"type": "boolean"}
        },
        "required": ["name", "port"]
      }';
      const filePath = createTempFile('invalid_with_schema.json', jsonContent);
      const schemaPath = createTempFile('invalid_schema.json', schemaContent);
      const result = lintConfig(filePath, { schemaPath });
      expect(result.errors.length).toBeGreaterThan(0);
      expect(result.errors[0]).toContain('Schema validation error at /port: must be integer');
      expect(result.errors[1]).toContain('Schema validation error at /enabled: must be boolean');
      cleanupTempFile(filePath);
      cleanupTempFile(schemaPath);
    });

    it('should return an error if the schema file is not found', () => {
      const jsonContent = '{}';
      const filePath = createTempFile('no_schema_file.json', jsonContent);
      const result = lintConfig(filePath, { schemaPath: 'non_existent_schema.json' });
      expect(result.errors.length).toBeGreaterThan(0);
      expect(result.errors[0]).toContain('Schema file not found:');
      cleanupTempFile(filePath);
    });

    it('should return an error if the schema file is invalid JSON', () => {
      const jsonContent = '{}';
      const invalidSchemaContent = '{
        "type": "object",
        "properties": {
          "name": {"type": "string"}
        },
      '; // Missing closing brace
      const filePath = createTempFile('invalid_schema_file.json', jsonContent);
      const schemaPath = createTempFile('invalid_schema.json', invalidSchemaContent);
      const result = lintConfig(filePath, { schemaPath });
      expect(result.errors.length).toBeGreaterThan(0);
      expect(result.errors[0]).toContain('Invalid JSON schema:');
      cleanupTempFile(filePath);
      cleanupTempFile(schemaPath);
    });

    it('should throw an error for unsupported file extensions', () => {
      const txtContent = 'This is a text file.';
      const filePath = createTempFile('unsupported.txt', txtContent);
      expect(() => lintConfig(filePath)).toThrow('Unsupported file extension: .txt');
      cleanupTempFile(filePath);
    });
  });
});
