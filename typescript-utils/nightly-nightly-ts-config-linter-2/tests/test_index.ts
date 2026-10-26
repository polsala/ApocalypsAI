import { lintConfig, lintFile } from '../src/index';

// Mock fs and js-yaml for offline testing
jest.mock('fs/promises', () => ({
  readFile: jest.fn(),
}));
jest.mock('js-yaml', () => ({
  load: jest.fn(),
}));

const mockFs = require('fs/promises');
const mockYaml = require('js-yaml');

describe('nightly-ts-config-linter', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    // Mock default behavior for fs.readFile
    mockFs.readFile.mockResolvedValue('{}');
    // Mock default behavior for yaml.load
    mockYaml.load.mockReturnValue({});
  });

  describe('lintConfig', () => {
    it('should return no errors for a valid JSON config', async () => {
      const validJson = '{"port": 8080, "database": {"host": "localhost"}}';
      const errors = await lintConfig(validJson, 'config.json');
      expect(errors).toEqual([]);
    });

    it('should return no errors for a valid YAML config', async () => {
      const validYaml = 'port: 8080
database:
  host: localhost';
      mockYaml.load.mockReturnValue({ port: 8080, database: { host: 'localhost' } });
      const errors = await lintConfig(validYaml, 'config.yaml');
      expect(errors).toEqual([]);
    });

    it('should report missing port in JSON', async () => {
      const missingPortJson = '{"database": {"host": "localhost"}}';
      const errors = await lintConfig(missingPortJson, 'config.json');
      expect(errors).toEqual([
        { message: 'Configuration must include a "port" property.' }
      ]);
    });

    it('should report missing port in YAML', async () => {
      const missingPortYaml = 'database:
  host: localhost';
      mockYaml.load.mockReturnValue({ database: { host: 'localhost' } });
      const errors = await lintConfig(missingPortYaml, 'config.yaml');
      expect(errors).toEqual([
        { message: 'Configuration must include a "port" property.' }
      ]);
    });

    it('should report non-local database host in JSON', async () => {
      const invalidHostJson = '{"port": 8080, "database": {"host": "remote.server.com"}}';
      const errors = await lintConfig(invalidHostJson, 'config.json');
      expect(errors).toEqual([
        { message: 'Database host "remote.server.com" is not a local address.', location: 'database.host' }
      ]);
    });

    it('should report non-local database host in YAML', async () => {
      const invalidHostYaml = 'port: 8080
database:
  host: remote.server.com';
      mockYaml.load.mockReturnValue({ port: 8080, database: { host: 'remote.server.com' } });
      const errors = await lintConfig(invalidHostYaml, 'config.yaml');
      expect(errors).toEqual([
        { message: 'Database host "remote.server.com" is not a local address.', location: 'database.host' }
      ]);
    });

    it('should handle unsupported file types', async () => {
      const content = 'some text';
      const errors = await lintConfig(content, 'config.txt');
      expect(errors).toEqual([{ message: 'Failed to parse configuration: Unsupported file type: config.txt' }]);
    });

    it('should handle JSON parsing errors', async () => {
      const invalidJson = '{ "port": 8080, "database": { "host": "localhost" }'; // Missing closing brace
      const errors = await lintConfig(invalidJson, 'config.json');
      expect(errors[0].message).toContain('Failed to parse configuration:');
    });

    it('should handle YAML parsing errors', async () => {
      const invalidYaml = 'port: 8080
database:
  host: localhost
  invalid:'; // Invalid YAML syntax
      mockYaml.load.mockImplementation(() => {
        throw new Error('YAML parsing error');
      });
      const errors = await lintConfig(invalidYaml, 'config.yaml');
      expect(errors).toEqual([{ message: 'Failed to parse configuration: YAML parsing error' }]);
    });

    it('should use user-defined rules from .ts-config-linterrc.json', async () => {
      // Mock reading the user config file
      mockFs.readFile.mockResolvedValueOnce('{"rules": {"require-port": "warn"}}');
      const missingPortJson = '{"database": {"host": "localhost"}}';
      const errors = await lintConfig(missingPortJson, 'config.json');
      // Expect a warning, not an error, for missing port
      expect(errors).toEqual([]);
      // Check if console.warn was called for the missing port
      expect(console.warn).toHaveBeenCalledWith('[WARN] Configuration must include a "port" property. in config.json');
    });
  });

  describe('lintFile', () => {
    it('should read and lint a JSON file', async () => {
      const validJson = '{"port": 8080}';
      mockFs.readFile.mockResolvedValue(validJson);
      const errors = await lintConfig(validJson, 'config.json'); // lintConfig is called internally by lintFile
      expect(errors).toEqual([]);
    });

    it('should report file read errors', async () => {
      mockFs.readFile.mockRejectedValue(new Error('File not found'));
      const errors = await lintFile('nonexistent.json');
      expect(errors).toEqual([{ message: 'Failed to read file: File not found' }]);
    });
  });
});
