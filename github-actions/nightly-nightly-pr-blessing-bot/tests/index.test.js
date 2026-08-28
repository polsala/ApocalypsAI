const core = require('@actions/core');
const github = require('@actions/github');
const { run } = require('../src/index');

// Mock the GitHub Actions toolkit
jest.mock('@actions/core');
jest.mock('@actions/github');

describe('Nightly PR Blessing Bot', () => {
  let createCommentMock;

  beforeEach(() => {
    jest.clearAllMocks();

    // Mock core functions
    core.getInput.mockImplementation((name) => {
      if (name === 'github-token') return 'mock-token';
      if (name === 'blessing-type') return 'affirmation'; // Default for tests
      return '';
    });
    core.setFailed.mockImplementation(jest.fn());
    core.info.mockImplementation(jest.fn());
    core.setOutput.mockImplementation(jest.fn());

    // Mock github context
    github.context = {
      eventName: 'pull_request',
      payload: {
        action: 'closed',
        pull_request: {
          number: 123,
          merged: true,
        },
      },
      repo: {
        owner: 'polsala',
        repo: 'ApocalypsAI',
      },
    };

    // Mock Octokit
    createCommentMock = jest.fn();
    github.getOctokit.mockReturnValue({
      rest: {
        issues: {
          createComment: createCommentMock,
        },
      },
    });
  });

  // Mock rationale:
  // @actions/core: Mocks input/output/logging functions to control test inputs and observe outputs without actual side effects.
  // @actions/github: Mocks the GitHub context (event, payload, repo) and the Octokit client to simulate GitHub events and API calls without making real network requests. This ensures tests are deterministic and offline.

  test('should post an affirmation blessing on a merged PR', async () => {
    await run();

    expect(core.getInput).toHaveBeenCalledWith('github-token', { required: true });
    expect(core.getInput).toHaveBeenCalledWith('blessing-type');
    expect(github.getOctokit).toHaveBeenCalledWith('mock-token');
    expect(createCommentMock).toHaveBeenCalledTimes(1);
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'polsala',
      repo: 'ApocalypsAI',
      issue_number: 123,
      body: expect.stringContaining('✨ ApocalypsAI Blessing ✨\n\n'),
    });
    expect(core.setOutput).toHaveBeenCalledWith('blessing-message', expect.any(String));
    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Posted blessing to PR #123: "'));
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('should post an emoji blessing when blessing-type is "emoji"', async () => {
    core.getInput.mockImplementation((name) => {
      if (name === 'github-token') return 'mock-token';
      if (name === 'blessing-type') return 'emoji';
      return '';
    });

    await run();

    expect(createCommentMock).toHaveBeenCalledTimes(1);
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'polsala',
      repo: 'ApocalypsAI',
      issue_number: 123,
      body: expect.stringMatching(/^✨ ApocalypsAI Blessing ✨\n\n[✨🌌🚀🌟💖🔮🌠💫🎉✅]$/), // Check for one of the emojis
    });
    expect(core.setOutput).toHaveBeenCalledWith('blessing-message', expect.any(String));
  });

  test('should post a quote blessing when blessing-type is "quote"', async () => {
    core.getInput.mockImplementation((name) => {
      if (name === 'github-token') return 'mock-token';
      if (name === 'blessing-type') return 'quote';
      return '';
    });

    await run();

    expect(createCommentMock).toHaveBeenCalledTimes(1);
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'polsala',
      repo: 'ApocalypsAI',
      issue_number: 123,
      body: expect.stringContaining('✨ ApocalypsAI Blessing ✨\n\n'),
    });
    expect(core.setOutput).toHaveBeenCalledWith('blessing-message', expect.any(String));
  });

  test('should do nothing if PR is not merged', async () => {
    github.context.payload.pull_request.merged = false;

    await run();

    expect(core.info).toHaveBeenCalledWith('This action only runs on merged pull requests. Skipping.');
    expect(createCommentMock).not.toHaveBeenCalled();
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('should do nothing if event is not pull_request', async () => {
    github.context.eventName = 'push';

    await run();

    expect(core.info).toHaveBeenCalledWith('This action only runs on merged pull requests. Skipping.');
    expect(createCommentMock).not.toHaveBeenCalled();
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('should handle errors gracefully', async () => {
    const errorMessage = 'API error';
    createCommentMock.mockRejectedValue(new Error(errorMessage));

    await run();

    expect(createCommentMock).toHaveBeenCalledTimes(1);
    expect(core.setFailed).toHaveBeenCalledWith(errorMessage);
  });
});
