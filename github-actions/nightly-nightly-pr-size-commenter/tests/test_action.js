// Mock rationale: we replace @actions/github and @actions/core with simple stubs to simulate the environment.

jest.mock('@actions/core', () => ({
  getInput: jest.fn(),
  setOutput: jest.fn(),
  setFailed: jest.fn(),
}));

jest.mock('@actions/github', () => ({
  context: {
    repo: { owner: 'test-owner', repo: 'test-repo' },
  },
  getOctokit: jest.fn(),
}));

const core = require('@actions/core');
const github = require('@actions/github');

// Load the action after mocks are set up
const action = require('../src/index');

// Helper to create a temporary event payload file
const fs = require('fs');
const path = require('path');

describe('PR Size Commenter Action', () => {
  const originalEnv = process.env;

  beforeEach(() => {
    jest.clearAllMocks();
    process.env = { ...originalEnv };
  });

  afterAll(() => {
    process.env = originalEnv;
  });

  test('comments Tiny size correctly', async () => {
    // Mock inputs
    core.getInput.mockReturnValue('fake-token');

    // Mock event payload
    const event = {
      pull_request: {
        number: 42,
        additions: 5,
        deletions: 2,
      },
    };
    const eventPath = path.join(__dirname, 'event.json');
    fs.writeFileSync(eventPath, JSON.stringify(event));
    process.env.GITHUB_EVENT_PATH = eventPath;

    // Mock octokit
    const createCommentMock = jest.fn();
    github.getOctokit.mockReturnValue({
      rest: {
        issues: {
          createComment: createCommentMock,
        },
      },
    });

    // Run action
    await require('../src/index');

    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      issue_number: 42,
      body: '🪶 This PR is **TINY** (7 line changes).',
    });
    expect(core.setOutput).toHaveBeenCalledWith('size-category', 'tiny');
  });

  test('handles missing GITHUB_EVENT_PATH gracefully', async () => {
    core.getInput.mockReturnValue('fake-token');
    delete process.env.GITHUB_EVENT_PATH;

    await require('../src/index');
    expect(core.setFailed).toHaveBeenCalledWith('GITHUB_EVENT_PATH is not defined');
  });
});
