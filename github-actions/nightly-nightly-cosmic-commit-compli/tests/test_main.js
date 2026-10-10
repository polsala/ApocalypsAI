const core = require('@actions/core');
const github = require('@actions/github');
const { run } = require('../src/main'); // Import the exported run function

// Mock @actions/core
jest.mock('@actions/core', () => ({
  getInput: jest.fn(),
  setFailed: jest.fn(),
  setOutput: jest.fn(),
  info: jest.fn(),
  warning: jest.fn(),
}));

// Mock @actions/github
const mockCreateComment = jest.fn();
const mockCreateCommitComment = jest.fn();
jest.mock('@actions/github', () => ({
  getOctokit: jest.fn(() => ({
    rest: {
      issues: {
        createComment: mockCreateComment,
      },
      repos: {
        createCommitComment: mockCreateCommitComment,
      },
    },
  })),
  context: {
    repo: {
      owner: 'test-owner',
      repo: 'test-repo',
    },
    eventName: 'pull_request_target', // Default event for tests
    payload: {
      pull_request: {
        number: 123,
        merged: true,
      },
    },
    sha: 'test-sha-123',
  },
}));

describe('Cosmic Commit Complimenter', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    // Mock rationale: Resetting mocks before each test ensures isolation and deterministic behavior.
    // This prevents test pollution from previous runs.
    github.context.eventName = 'pull_request_target';
    github.context.payload = {
      pull_request: {
        number: 123,
        merged: true,
      },
    };
    core.getInput.mockImplementation((name) => {
      if (name === 'github-token') return 'mock-token';
      if (name === 'compliment-target') return 'pr-merge';
      return '';
    });
  });

  test('should post a compliment on a merged PR', async () => {
    await run();

    expect(core.getInput).toHaveBeenCalledWith('github-token', { required: true });
    expect(core.getInput).toHaveBeenCalledWith('compliment-target');
    expect(core.getInput).toHaveBeenCalledWith('compliment-message');
    expect(github.getOctokit).toHaveBeenCalledWith('mock-token');
    expect(mockCreateComment).toHaveBeenCalledTimes(1);
    expect(mockCreateComment).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      issue_number: 123,
      body: expect.stringContaining('✨ **Cosmic Compliment from ApocalypsAI:** ✨\n\n'),
    });
    expect(core.setOutput).toHaveBeenCalledWith('compliment', expect.any(String));
    expect(core.info).toHaveBeenCalledWith('PR #123 was merged. Posting cosmic compliment.');
    expect(core.info).toHaveBeenCalledWith('Compliment posted on PR #123.');
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('should not post a compliment if PR is closed but not merged', async () => {
    github.context.payload.pull_request.merged = false;

    await run();

    expect(mockCreateComment).not.toHaveBeenCalled();
    expect(core.info).toHaveBeenCalledWith('PR #123 was closed but not merged. No compliment.');
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('should post a compliment on a push event', async () => {
    github.context.eventName = 'push';
    core.getInput.mockImplementation((name) => {
      if (name === 'github-token') return 'mock-token';
      if (name === 'compliment-target') return 'push';
      return '';
    });

    await run();

    expect(mockCreateCommitComment).toHaveBeenCalledTimes(1);
    expect(mockCreateCommitComment).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      commit_sha: 'test-sha-123',
      body: expect.stringContaining('✨ **Cosmic Compliment from ApocalypsAI:** ✨\n\n'),
    });
    expect(core.setOutput).toHaveBeenCalledWith('compliment', expect.any(String));
    expect(core.info).toHaveBeenCalledWith('Push event detected for commit test-sha-123. Posting cosmic compliment.');
    expect(core.info).toHaveBeenCalledWith('Compliment posted on commit test-sha-123.');
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('should use custom compliment message if provided', async () => {
    const customMsg = "You're a star!";
    core.getInput.mockImplementation((name) => {
      if (name === 'github-token') return 'mock-token';
      if (name === 'compliment-target') return 'pr-merge';
      if (name === 'compliment-message') return customMsg;
      return '';
    });

    await run();

    expect(mockCreateComment).toHaveBeenCalledWith(expect.objectContaining({
      body: `✨ **Cosmic Compliment from ApocalypsAI:** ✨\n\n${customMsg}`,
    }));
    expect(core.setOutput).toHaveBeenCalledWith('compliment', customMsg);
  });

  test('should set action as failed if github-token is missing', async () => {
    core.getInput.mockImplementation((name) => {
      if (name === 'github-token') throw new Error('Input required and not supplied: github-token');
      return '';
    });

    await run();

    expect(core.setFailed).toHaveBeenCalledWith('Input required and not supplied: github-token');
    expect(mockCreateComment).not.toHaveBeenCalled();
  });

  test('should warn if event type and target mismatch', async () => {
    github.context.eventName = 'push'; // Event is push
    core.getInput.mockImplementation((name) => {
      if (name === 'github-token') return 'mock-token';
      if (name === 'compliment-target') return 'pr-merge'; // Target is pr-merge
      return '';
    });

    await run();

    expect(core.warning).toHaveBeenCalledWith('Action triggered by unsupported event type or target: push with target pr-merge. No compliment posted.');
    expect(mockCreateComment).not.toHaveBeenCalled();
    expect(mockCreateCommitComment).not.toHaveBeenCalled();
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('should handle errors gracefully', async () => {
    const errorMessage = 'API error';
    mockCreateComment.mockRejectedValue(new Error(errorMessage));

    await run();

    expect(core.setFailed).toHaveBeenCalledWith(errorMessage);
  });
});
