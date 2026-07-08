const { run, lintWorkflowFile, isValidYaml, setMockFs, setMockGlob, getFs, getGlob } = require('../src/index');
const core = require('@actions/core');

// Mocking @actions/core functions
jest.mock('@actions/core', () => ({
  info: jest.fn(),
  warning: jest.fn(),
  error: jest.fn(),
  setFailed: jest.fn(),
  setOutput: jest.fn(),
}));

// Mocking fs and glob for deterministic tests
let mockFilesystem = {};
let mockGlobFiles = [];

const mockFsModule = {
  readFileSync: jest.fn((filePath, encoding) => {
    if (mockFilesystem[filePath]) {
      return mockFilesystem[filePath];
    }
    throw new Error(`File not found: ${filePath}`);
  }),
  writeFileSync: jest.fn((filePath, content) => {
    mockFilesystem[filePath] = content;
  }),
  existsSync: jest.fn((filePath) => filePath in mockFilesystem),
};

const mockGlobModule = {
  sync: jest.fn((pattern, options) => {
    if (mockGlobFiles.length === 0) return [];
    // Simple mock globbing: return files that match the pattern (if any)
    // In a real scenario, this would be more sophisticated.
    // For this mock, we'll assume the pattern is simple and mockGlobFiles are absolute paths.
    return mockGlobFiles.filter(file => file.includes(pattern.split('*')[0]));
  }),
};

// Mocking js-yaml for isValidYaml
jest.mock('js-yaml', () => ({
  load: jest.fn((content) => {
    if (content.includes('invalid yaml')) {
      throw new Error('Mock YAML parsing error');
    }
    // Simulate successful parsing for valid YAML
    return { mockParsed: true };
  }),
}));

describe('GitHub Action Lint Runner', () => {

  beforeEach(() => {
    // Reset mocks before each test
    jest.clearAllMocks();
    mockFilesystem = {};
    mockGlobFiles = [];
    setMockFs(mockFsModule);
    setMockGlob(mockGlobModule);

    // Set default mock implementations for fs and glob
    jest.spyOn(fs, 'readFileSync').mockImplementation(mockFsModule.readFileSync);
    jest.spyOn(fs, 'writeFileSync').mockImplementation(mockFsModule.writeFileSync);
    jest.spyOn(fs, 'existsSync').mockImplementation(mockFsModule.existsSync);
    jest.spyOn(glob, 'sync').mockImplementation(mockGlobModule.sync);
  });

  describe('lintWorkflowFile', () => {
    it('should return no issues for a valid workflow', () => {
      const validWorkflowContent = `
name: My Awesome Workflow

on: push

jobs:
  build: # This job sounds fun!
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
`;
      mockFilesystem['/path/to/workflow.yml'] = validWorkflowContent;
      const result = lintWorkflowFile('/path/to/workflow.yml');
      expect(result.isValid).toBe(true);
      expect(result.issues).toEqual([]);
    });

    it('should return issues for missing on trigger', () => {
      const invalidWorkflowContent = `
name: No Trigger Workflow

jobs:
  build:
    runs-on: ubuntu-latest
`;
      mockFilesystem['/path/to/workflow.yml'] = invalidWorkflowContent;
      const result = lintWorkflowFile('/path/to/workflow.yml');
      expect(result.isValid).toBe(false);
      expect(result.issues).toContain('Workflow must have an `on:` trigger defined.');
    });

    it('should return issues for missing jobs section', () => {
      const invalidWorkflowContent = `
name: No Jobs Workflow

on: push
`;
      mockFilesystem['/path/to/workflow.yml'] = invalidWorkflowContent;
      const result = lintWorkflowFile('/path/to/workflow.yml');
      expect(result.isValid).toBe(false);
      expect(result.issues).toContain('Workflow must have a `jobs:` section defined.');
    });

    it('should return issues for missing runs-on', () => {
      const invalidWorkflowContent = `
name: No Runner Workflow

on: push

jobs:
  build:
    steps:
      - uses: actions/checkout@v4
`;
      mockFilesystem['/path/to/workflow.yml'] = invalidWorkflowContent;
      const result = lintWorkflowFile('/path/to/workflow.yml');
      expect(result.isValid).toBe(false);
      expect(result.issues).toContain('Each job must define a `runs-on:` runner.');
    });

    it('should return issues for deprecated checkout version', () => {
      const invalidWorkflowContent = `
name: Deprecated Checkout Workflow

on: push

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v1
`;
      mockFilesystem['/path/to/workflow.yml'] = invalidWorkflowContent;
      const result = lintWorkflowFile('/path/to/workflow.yml');
      expect(result.isValid).toBe(false);
      expect(result.issues).toContain('`actions/checkout@v1` is deprecated. Please use a newer version like `@v3` or `@v4`.');
    });

    it('should suggest adventurous job names', () => {
      const workflowContent = `
name: Adventure Time Workflow

on: push

jobs:
  quest_for_code:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
`;
      mockFilesystem['/path/to/workflow.yml'] = workflowContent;
      const result = lintWorkflowFile('/path/to/workflow.yml');
      expect(result.isValid).toBe(true);
      expect(result.issues).toEqual([]); // No *errors*, just a suggestion
    });

    it('should warn about direct secrets usage', () => {
      const workflowContent = `
name: Secret Workflow

on: push

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Use secret
        run: echo ${{ secrets.MY_API_KEY }}
`;
      mockFilesystem['/path/to/workflow.yml'] = workflowContent;
      const result = lintWorkflowFile('/path/to/workflow.yml');
      expect(result.isValid).toBe(false);
      expect(result.issues).toContain('Be cautious when using `secrets.` directly. Consider using `secrets.MASKED` or specific secret names.');
    });
  });

  describe('isValidYaml', () => {
    it('should return true for valid YAML', () => {
      const validYamlContent = `
name: Valid YAML
on: push
jobs:
  test:
    runs-on: ubuntu-latest
`;
      mockFilesystem['/path/to/valid.yml'] = validYamlContent;
      expect(isValidYaml('/path/to/valid.yml')).toBe(true);
    });

    it('should return false for invalid YAML', () => {
      const invalidYamlContent = `
name: Invalid YAML
on: push
jobs:
  test:
    runs-on: ubuntu-latest
    invalid yaml
`;
      mockFilesystem['/path/to/invalid.yml'] = invalidYamlContent;
      expect(isValidYaml('/path/to/invalid.yml')).toBe(false);
      expect(core.warning).toHaveBeenCalled();
    });
  });

  describe('run', () => {
    it('should successfully lint multiple valid workflows', async () => {
      mockFilesystem['/path/to/workflow1.yml'] = `
name: Workflow One
on: push
jobs:
  build: # Fun build!
    runs-on: ubuntu-latest
`;
      mockFilesystem['/path/to/workflow2.yml'] = `
name: Workflow Two
on: pull_request
jobs:
  test: # Adventure test!
    runs-on: ubuntu-latest
`;
      mockGlobFiles = ['/path/to/workflow1.yml', '/path/to/workflow2.yml'];
      await run();
      expect(core.setOutput).toHaveBeenCalledWith('lint_status', 'success');
      expect(core.setOutput).toHaveBeenCalledWith('lint_summary', expect.stringContaining('2 files passed, 0 files failed.'));
      expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Linting passed for'));
    });

    it('should fail if any workflow has linting errors', async () => {
      mockFilesystem['/path/to/workflow1.yml'] = `
name: Workflow One
on: push
jobs:
  build: # Fun build!
    runs-on: ubuntu-latest
`;
      mockFilesystem['/path/to/workflow2.yml'] = `
name: Workflow Two (Bad)
jobs:
  test:
    runs-on: ubuntu-latest
`; // Missing 'on:' trigger
      mockGlobFiles = ['/path/to/workflow1.yml', '/path/to/workflow2.yml'];
      await run();
      expect(core.setFailed).toHaveBeenCalledWith(expect.stringContaining('Some GitHub Actions workflows failed linting.'));
      expect(core.setOutput).toHaveBeenCalledWith('lint_status', 'failure');
      expect(core.setOutput).toHaveBeenCalledWith('lint_summary', expect.stringContaining('1 files passed, 1 files failed.'));
      expect(core.error).toHaveBeenCalledWith(expect.stringContaining('Linting failed for /path/to/workflow2.yml'));
    });

    it('should handle no workflow files found', async () => {
      mockGlobFiles = []; // No files found
      await run();
      expect(core.warning).toHaveBeenCalledWith('No workflow files found matching the pattern. No linting performed.');
      expect(core.setOutput).toHaveBeenCalledWith('lint_status', 'success');
      expect(core.setOutput).toHaveBeenCalledWith('lint_summary', 'No workflow files found to lint.');
    });

    it('should handle custom workflow path', async () => {
      mockFilesystem['/custom/path/my-workflow.yml'] = `
name: Custom Workflow
on: push
jobs:
  build: # Fun build!
    runs-on: ubuntu-latest
`;
      mockGlobFiles = ['/custom/path/my-workflow.yml'];
      // Mocking core.getInput to return a custom path
      core.getInput = jest.fn((name) => {
        if (name === 'workflow_path') return '/custom/path/*.yml';
        return '';
      });
      await run();
      expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Looking for workflows matching pattern: /custom/path/*.yml'));
      expect(core.setOutput).toHaveBeenCalledWith('lint_status', 'success');
    });

    it('should fail if a workflow has YAML parsing errors', async () => {
      mockFilesystem['/path/to/workflow1.yml'] = `
name: Workflow One
on: push
jobs:
  build: # Fun build!
    runs-on: ubuntu-latest
`;
      mockFilesystem['/path/to/workflow2.yml'] = `
name: Workflow Two (Invalid YAML)
on: push
jobs:
  test:
    runs-on: ubuntu-latest
    invalid yaml
`;
      mockGlobFiles = ['/path/to/workflow1.yml', '/path/to/workflow2.yml'];
      await run();
      expect(core.setFailed).toHaveBeenCalledWith(expect.stringContaining('Some GitHub Actions workflows failed linting.'));
      expect(core.setOutput).toHaveBeenCalledWith('lint_status', 'failure');
      expect(core.setOutput).toHaveBeenCalledWith('lint_summary', expect.stringContaining('1 files passed, 1 files failed.'));
      expect(core.error).toHaveBeenCalledWith(expect.stringContaining('Skipping linting for /path/to/workflow2.yml due to YAML parsing errors.'));
    });
  });
});
