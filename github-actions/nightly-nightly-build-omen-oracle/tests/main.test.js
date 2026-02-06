const core = require('@actions/core');
const github = require('@actions/github');
const fs = require('fs');
const path = require('path');

// Mock the GitHub Actions toolkit
jest.mock('@actions/core');
jest.mock('@actions/github');
jest.mock('fs'); // Mock fs to control omens.json content
jest.mock('path'); // Mock path to control file resolution

const run = require('../src/main'); // The action's entry point

describe('Nightly Build Omen Oracle', () => {
  let createCommentMock;
  let createCommitStatusMock;
  let setOutputMock;
  let setFailedMock;
  let warningMock;
  let infoMock;

  const mockOmens = [
    "Test Omen 1: The code sings!",
    "Test Omen 2: A future without bugs!",
    "Test Omen 3: Destiny awaits!"
  ];

  beforeEach(() => {
    jest.clearAllMocks();

    // Mock fs.readFileSync to return our deterministic omens
    fs.readFileSync.mockReturnValue(JSON.stringify(mockOmens));
    // Mock path.join to ensure it resolves correctly for the test environment
    path.join.mockImplementation((...args) => args.join('/')); // Mock rationale: Ensures fs.readFileSync gets a predictable path in tests.

    // Mock @actions/core functions
    setOutputMock = jest.spyOn(core, 'setOutput');
    setFailedMock = jest.spyOn(core, 'setFailed');
    warningMock = jest.spyOn(core, 'warning');
    infoMock = jest.spyOn(core, 'info');

    // Mock @actions/github.getOctokit
    createCommentMock = jest.fn();
    createCommitStatusMock = jest.fn();
    github.getOctokit.mockReturnValue({
      rest: {
        issues: {
          createComment: createCommentMock,
        },
        repos: {
          createCommitStatus: createCommitStatusMock,
        },
      },
    }); // Mock rationale: Simulates GitHub API interactions without making actual network requests.

    // Mock github.context
    github.context = {
      repo: {
        owner: 'polsala',
        repo: 'ApocalypsAI',
      },
      sha: 'a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0',
      payload: {
        pull_request: {
          number: 123,
        },
      },
    }; // Mock rationale: Provides a consistent GitHub context for testing PR and commit status scenarios.
  });

  test('should select a random omen and set it as output', async () => {
    // Mock Math.random to always return a specific index
    jest.spyOn(Math, 'random').mockReturnValue(0.5); // Mock rationale: Ensures deterministic omen selection for testing.

    core.getInput.mockImplementation((name) => {
      if (name === 'github-token') return 'mock-token';
      if (name === 'target-type') return 'pr-comment';
      return '';
    }); // Mock rationale: Provides controlled input values for the action.

    await run();

    expect(setOutputMock).toHaveBeenCalledWith('omen', mockOmens[1]); // 0.5 * 3 = 1.5, floor is 1
    expect(setFailedMock).not.toHaveBeenCalled();
  });

  test('should post omen as a PR comment when target-type is pr-comment', async () => {
    jest.spyOn(Math, 'random').mockReturnValue(0); // Mock rationale: Ensures deterministic omen selection for testing.

    core.getInput.mockImplementation((name) => {
      if (name === 'github-token') return 'mock-token';
      if (name === 'target-type') return 'pr-comment';
      return '';
    }); // Mock rationale: Provides controlled input values for the action.

    await run();

    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'polsala',
      repo: 'ApocalypsAI',
      issue_number: 123,
      body: `🔮 Build Omen Oracle says: ${mockOmens[0]} `
    });
    expect(createCommitStatusMock).not.toHaveBeenCalled();
    expect(setOutputMock).toHaveBeenCalledWith('omen', mockOmens[0]);
    expect(setFailedMock).not.toHaveBeenCalled();
  });

  test('should post omen as a commit status when target-type is commit-status', async () => {
    jest.spyOn(Math, 'random').mockReturnValue(0.99); // Mock rationale: Ensures deterministic omen selection for testing.

    core.getInput.mockImplementation((name) => {
      if (name === 'github-token') return 'mock-token';
      if (name === 'target-type') return 'commit-status';
      if (name === 'status-context') return 'Custom Omen';
      return '';
    }); // Mock rationale: Provides controlled input values for the action.

    await run();

    expect(createCommitStatusMock).toHaveBeenCalledWith({
      owner: 'polsala',
      repo: 'ApocalypsAI',
      sha: 'a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0',
      state: 'success',
      description: mockOmens[2],
      context: 'Custom Omen',
    });
    expect(createCommentMock).not.toHaveBeenCalled();
    expect(setOutputMock).toHaveBeenCalledWith('omen', mockOmens[2]);
    expect(setFailedMock).not.toHaveBeenCalled();
  });

  test('should handle missing PR number gracefully for pr-comment target-type', async () => {
    github.context.payload.pull_request = undefined; // Mock rationale: Simulates a workflow run not associated with a PR.

    core.getInput.mockImplementation((name) => {
      if (name === 'github-token') return 'mock-token';
      if (name === 'target-type') return 'pr-comment';
      return '';
    }); // Mock rationale: Provides controlled input values for the action.

    await run();

    expect(warningMock).toHaveBeenCalledWith('No pull request found in context. Skipping PR comment.');
    expect(createCommentMock).not.toHaveBeenCalled();
    expect(createCommitStatusMock).not.toHaveBeenCalled();
    expect(setFailedMock).not.toHaveBeenCalled();
  });

  test('should call setFailed for invalid target-type', async () => {
    core.getInput.mockImplementation((name) => {
      if (name === 'github-token') return 'mock-token';
      if (name === 'target-type') return 'invalid-type';
      return '';
    }); // Mock rationale: Provides controlled input values for the action.

    await run();

    expect(setFailedMock).toHaveBeenCalledWith("Invalid target-type: invalid-type. Must be 'pr-comment' or 'commit-status'.");
    expect(createCommentMock).not.toHaveBeenCalled();
    expect(createCommitStatusMock).not.toHaveBeenCalled();
  });

  test('should call setFailed if github-token is missing', async () => {
    core.getInput.mockImplementation((name) => {
      if (name === 'github-token') return ''; // Missing token
      if (name === 'target-type') return 'pr-comment';
      return '';
    }); // Mock rationale: Simulates a missing required input.

    await run();

    expect(setFailedMock).toHaveBeenCalledWith('Input required and not supplied: github-token');
    expect(createCommentMock).not.toHaveBeenCalled();
    expect(createCommitStatusMock).not.toHaveBeenCalled();
  });

  test('should handle errors during API calls', async () => {
    createCommentMock.mockRejectedValue(new Error('API Error')); // Mock rationale: Simulates a failure during GitHub API interaction.

    core.getInput.mockImplementation((name) => {
      if (name === 'github-token') return 'mock-token';
      if (name === 'target-type') return 'pr-comment';
      return '';
    }); // Mock rationale: Provides controlled input values for the action.

    await run();

    expect(setFailedMock).toHaveBeenCalledWith('API Error');
  });
});
