const core = require('@actions/core');
const github = require('@actions/github');
const { run } = require('../src/main');

// Mock the GitHub Actions toolkit
jest.mock('@actions/core');
jest.mock('@actions/github', () => ({
  getOctokit: jest.fn(() => ({
    rest: {
      issues: {
        createComment: jest.fn(() => ({ data: { id: 12345 } })),
      },
    },
  })),
  context: {
    repo: {
      owner: 'polsala',
      repo: 'ApocalypsAI',
    },
    payload: {
      pull_request: {
        number: 42,
      },
    },
  },
}));

describe('Whimsical PR Encourager', () => {
  let createCommentMock;

  beforeEach(() => {
    jest.clearAllMocks();
    createCommentMock = github.getOctokit().rest.issues.createComment;
    // Mock rationale: We mock Math.random to ensure deterministic message selection for testing.
    // This allows us to predict which message will be chosen from the list.
    jest.spyOn(global.Math, 'random').mockReturnValue(0.5); // Always pick the middle message (or close to it)
  });

  afterEach(() => {
    jest.restoreAllMocks(); // Restore Math.random to its original implementation
  });

  test('should post a default whimsical comment to a PR', async () => {
    // Mock rationale: We mock @actions/core to control inputs and capture outputs without actual GitHub API calls.
    // We mock @actions/github to simulate API responses and context, ensuring tests are deterministic and offline.
    core.getInput.mockImplementation((name) => {
      if (name === 'github-token') return 'mock-token';
      if (name === 'messages') return '[]'; // No custom messages
      return '';
    });

    await run();

    expect(core.getInput).toHaveBeenCalledWith('github-token', { required: true });
    expect(core.getInput).toHaveBeenCalledWith('messages');
    expect(github.getOctokit).toHaveBeenCalledWith('mock-token');
    expect(createCommentMock).toHaveBeenCalledTimes(1);
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'polsala',
      repo: 'ApocalypsAI',
      issue_number: 42,
      body: expect.any(String), // The specific message depends on Math.random mock
    });
    expect(core.setOutput).toHaveBeenCalledWith('comment-id', 12345);
    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Posted whimsical encouragement to PR #42: "'));
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('should post a custom whimsical comment if provided', async () => {
    const customMsgs = ['Custom message 1', 'Custom message 2', 'Custom message 3'];
    core.getInput.mockImplementation((name) => {
      if (name === 'github-token') return 'mock-token';
      if (name === 'messages') return JSON.stringify(customMsgs);
      return '';
    });
    // Mock rationale: Set Math.random to pick the first custom message for deterministic testing.
    jest.spyOn(global.Math, 'random').mockReturnValue(0.1); // Pick first custom message

    await run();

    expect(createCommentMock).toHaveBeenCalledTimes(1);
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'polsala',
      repo: 'ApocalypsAI',
      issue_number: 42,
      body: customMsgs[0],
    });
    expect(core.setOutput).toHaveBeenCalledWith('comment-id', 12345);
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('should handle invalid custom messages gracefully and use defaults', async () => {
    core.getInput.mockImplementation((name) => {
      if (name === 'github-token') return 'mock-token';
      if (name === 'messages') return '{"not": "an array"}'; // Invalid JSON array
      return '';
    });

    await run();

    expect(core.warning).toHaveBeenCalledWith(expect.stringContaining('Could not parse custom messages'));
    expect(createCommentMock).toHaveBeenCalledTimes(1);
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'polsala',
      repo: 'ApocalypsAI',
      issue_number: 42,
      body: expect.any(String), // Should use default messages
    });
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('should fail if github-token is not provided', async () => {
    core.getInput.mockImplementation((name) => {
      if (name === 'github-token') return ''; // Missing token
      if (name === 'messages') return '[]';
      return '';
    });

    await run();

    expect(core.setFailed).toHaveBeenCalledWith('Input required and not supplied: github-token');
    expect(createCommentMock).not.toHaveBeenCalled();
  });

  test('should fail if PR number is not available in context', async () => {
    // Mock rationale: Simulate a scenario where the GitHub context does not contain a pull_request number,
    // which might happen if the action is triggered by an event other than pull_request.opened,
    // or if the payload structure changes unexpectedly.
    github.context.payload.pull_request = undefined; // Simulate missing PR number
    core.getInput.mockImplementation((name) => {
      if (name === 'github-token') return 'mock-token';
      if (name === 'messages') return '[]';
      return '';
    });

    await run();

    expect(core.setFailed).toHaveBeenCalledWith('Could not get Pull Request number from context. This action should run on pull_request_target.');
    expect(createCommentMock).not.toHaveBeenCalled();
  });
});
