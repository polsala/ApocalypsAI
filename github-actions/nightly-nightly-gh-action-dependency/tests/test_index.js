const process = require('process');
const cp = require('child_process');
const path = require('path');

// Mock the @actions/core module
jest.mock('@actions/core', () => ({
  getInput: jest.fn(),
  setOutput: jest.fn(),
  setFailed: jest.fn(),
}));

// Mock the fs module for file system operations
jest.mock('fs');

const core = require('@actions/core');
const fs = require('fs');

// Mock workflow content
const mockWorkflowContent = `
name: Test Workflow

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3 # This should be flagged as outdated
      - name: Setup Node
        uses: actions/setup-node@v2 # This should be flagged as outdated
      - name: Another Action
        uses: some-org/some-action@v1.2.3 # This is not mocked as outdated
      - name: Latest Checkout
        uses: actions/checkout@v4 # This should NOT be flagged as outdated
`;

describe('GitHub Actions Dependency Checker', () => {
  let index;

  beforeEach(() => {
    // Reset mocks before each test
    jest.clearAllMocks();

    // Mock fs.readdirSync and fs.readFileSync
    fs.readdirSync.mockReturnValue(['test.yml']);
    fs.readFileSync.mockReturnValue(mockWorkflowContent);

    // Dynamically import the action code to ensure mocks are applied
    index = require('../src/index');
  });

  test('should identify outdated dependencies', () => {
    core.getInput.mockReturnValue('.github/workflows/');

    index.run(); // Call the function directly

    // Mock rationale: We are mocking the output of core.getInput and fs.readFileSync
    // to simulate a specific workflow file content and ensure the action logic
    // correctly identifies the predefined outdated dependencies.

    expect(core.setOutput).toHaveBeenCalledWith('outdated_dependencies', JSON.stringify({
      'actions/checkout': 'v3',
      'actions/setup-node': 'v2'
    }));
  });

  test('should not report any outdated dependencies if none are found', () => {
    const mockWorkflowContentNoOutdated = `
name: Clean Workflow

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      - name: Setup Node
        uses: actions/setup-node@v3
`;
    fs.readFileSync.mockReturnValue(mockWorkflowContentNoOutdated);
    core.getInput.mockReturnValue('.github/workflows/');

    index.run();

    // Mock rationale: Similar to the previous test, we mock fs.readFileSync
    // with content that should not trigger any outdated dependency flags.
    // This verifies the action correctly handles cases with no outdated actions.

    expect(core.setOutput).toHaveBeenCalledWith('outdated_dependencies', JSON.stringify({}));
  });

  test('should handle multiple workflow files', () => {
    fs.readdirSync.mockReturnValue(['workflow1.yml', 'workflow2.yaml']);
    fs.readFileSync.mockImplementation((filePath) => {
      if (filePath.includes('workflow1.yml')) {
        return 'uses: actions/checkout@v3';
      } else if (filePath.includes('workflow2.yaml')) {
        return 'uses: actions/setup-node@v2';
      }
      return '';
    });
    core.getInput.mockReturnValue('.github/workflows/');

    index.run();

    // Mock rationale: This test ensures the action iterates through multiple files
    // and aggregates outdated dependencies correctly from each.

    expect(core.setOutput).toHaveBeenCalledWith('outdated_dependencies', JSON.stringify({
      'actions/checkout': 'v3',
      'actions/setup-node': 'v2'
    }));
  });

  test('should set failed if workflow path is invalid', () => {
    const invalidPathError = new Error('ENOENT: no such file or directory');
    fs.readdirSync.mockImplementation(() => {
      throw invalidPathError;
    });
    core.getInput.mockReturnValue('/invalid/path');

    index.run();

    // Mock rationale: This test verifies that the action gracefully handles
    // errors, such as an invalid workflow path, by calling core.setFailed.

    expect(core.setFailed).toHaveBeenCalledWith(invalidPathError.message);
  });
});
