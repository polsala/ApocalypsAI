const core = require('@actions/core');
const github = require('@actions/github');
const { when } = require('jest-when');

// Mock the action's main file
const run = require('../src/main');

// Mock @actions/core
jest.mock('@actions/core');
// Mock @actions/github
jest.mock('@actions/github');

describe('Nightly PR Cosmic Blesser', () => {
  let createCommentMock;
  let createCommitStatusMock;
  let contextPayload;
  let originalMathRandom;

  beforeEach(() => {
    jest.clearAllMocks();

    // Mock Octokit methods
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
    });

    // Mock github context payload for a PR event
    contextPayload = {
      pull_request: {
        number: 123,
        head: {
          sha: 'a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0',
        },
      },
      repo: {
        owner: 'polsala',
        repo: 'ApocalypsAI',
      },
    };
    github.context = contextPayload;

    // Mock core.getInput
    when(core.getInput)
      .calledWith('github-token', expect.any(Object))
      .mockReturnValue('mock-token');
    when(core.getInput)
      .calledWith('set-status-check')
      .mockReturnValue('true'); // Default to true for most tests

    // Store original Math.random and mock it for deterministic tests
    originalMathRandom = Math.random;
    Math.random = jest.fn(() => 0.5); // Mock to always return the middle blessing (index 5 of 10)

    // Mock core.info and core.setFailed to prevent console output during tests
    core.info.mockImplementation(() => {});
    core.setFailed.mockImplementation(() => {});
  });

  afterEach(() => {
    // Restore original Math.random
    Math.random = originalMathRandom;
  });

  test('should post a cosmic blessing comment to the PR', async () => {
    // Mock rationale: Math.random is mocked to ensure a deterministic blessing message is chosen.
    // @actions/github and @actions/core are mocked to prevent actual API calls and control inputs/outputs.
    // This allows testing the core logic of the action in isolation.
    await run();

    expect(createCommentMock).toHaveBeenCalledTimes(1);
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'polsala',
      repo: 'ApocalypsAI',
      issue_number: 123,
      body: expect.stringContaining('✨ **Cosmic Blessing Initiated!** ✨\n\nYour code resonates with the universal hum. It is blessed.\n\n_May your merges be swift and your deployments smooth._'),
    });
    expect(core.setOutput).toHaveBeenCalledWith('blessing-message', 'Your code resonates with the universal hum. It is blessed.');
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('should set a passing status check by default', async () => {
    // Mock rationale: Same as above. Ensures the status check API call is made with correct parameters.
    await run();

    expect(createCommitStatusMock).toHaveBeenCalledTimes(1);
    expect(createCommitStatusMock).toHaveBeenCalledWith({
      owner: 'polsala',
      repo: 'ApocalypsAI',
      sha: 'a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0',
      state: 'success',
      target_url: 'https://github.com/polsala/ApocalypsAI/pull/123/checks',
      description: 'Your code resonates with the universal hum. It is blessed.',
      context: 'Cosmic Blessing',
    });
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('should not set a status check if set-status-check is false', async () => {
    // Mock rationale: Tests conditional logic based on input.
    when(core.getInput)
      .calledWith('set-status-check')
      .mockReturnValue('false');

    await run();

    expect(createCommentMock).toHaveBeenCalledTimes(1); // Comment should still be posted
    expect(createCommitStatusMock).not.toHaveBeenCalled();
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('should fail if github-token is not provided', async () => {
    // Mock rationale: Tests error handling for missing required input.
    when(core.getInput)
      .calledWith('github-token', expect.any(Object))
      .mockReturnValue('');

    await run();

    expect(createCommentMock).not.toHaveBeenCalled();
    expect(createCommitStatusMock).not.toHaveBeenCalled();
    expect(core.setFailed).toHaveBeenCalledWith('Input required and not supplied: github-token');
  });

  test('should fail if not run on a pull_request event', async () => {
    // Mock rationale: Tests the guard clause for incorrect event types.
    github.context.payload.pull_request = undefined;

    await run();

    expect(createCommentMock).not.toHaveBeenCalled();
    expect(createCommitStatusMock).not.toHaveBeenCalled();
    expect(core.setFailed).toHaveBeenCalledWith('This action can only run on pull_request events.');
  });

  test('should handle API errors gracefully', async () => {
    // Mock rationale: Simulates a network or API error to ensure robust error handling.
    const errorMessage = 'GitHub API error: Something went wrong';
    createCommentMock.mockRejectedValue(new Error(errorMessage));

    await run();

    expect(createCommentMock).toHaveBeenCalledTimes(1);
    expect(core.setFailed).toHaveBeenCalledWith(errorMessage);
  });

  test('should output the chosen blessing message', async () => {
    // Mock rationale: Verifies that the action correctly sets its output.
    await run();

    expect(core.setOutput).toHaveBeenCalledWith('blessing-message', 'Your code resonates with the universal hum. It is blessed.');
  });

  test('should select a random blessing message', async () => {
    // Mock rationale: Tests that different random values lead to different blessings.
    // Reset Math.random mock for this specific test
    Math.random.mockRestore();
    const mockRandomValues = [0.1, 0.9]; // Two distinct random values
    let callCount = 0;
    Math.random = jest.fn(() => mockRandomValues[callCount++ % mockRandomValues.length]);

    await run(); // First run, Math.random returns 0.1
    const firstBlessing = core.setOutput.mock.calls[0][1];
    expect(firstBlessing).not.toBeUndefined();
    expect(firstBlessing).not.toBe('Your code resonates with the universal hum. It is blessed.'); // The 0.5 mock result

    jest.clearAllMocks(); // Clear mocks for the second run
    when(core.getInput)
      .calledWith('github-token', expect.any(Object))
      .mockReturnValue('mock-token');
    when(core.getInput)
      .calledWith('set-status-check')
      .mockReturnValue('true');
    github.context = contextPayload; // Re-set context after clearAllMocks

    await run(); // Second run, Math.random returns 0.9
    const secondBlessing = core.setOutput.mock.calls[0][1];
    expect(secondBlessing).not.toBeUndefined();
    expect(secondBlessing).not.toBe(firstBlessing); // Should be a different blessing
    expect(core.setFailed).not.toHaveBeenCalled();
  });
});
