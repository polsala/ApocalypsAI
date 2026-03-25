const core = require('@actions/core');
const github = require('@actions/github');
const { when } = require('jest-when');

// Mock the GitHub Actions toolkit
jest.mock('@actions/core');
jest.mock('@actions/github');

const mockCreateComment = jest.fn();
const mockGetOctokit = jest.fn(() => ({
  rest: {
    issues: {
      createComment: mockCreateComment,
    },
  },
}));

// Mock rationale: We need to control the GitHub context (e.g., event payload)
// and the Octokit client's behavior (e.g., createComment API call)
// to ensure deterministic and offline testing.
github.getOctokit.mockImplementation(mockGetOctokit);

describe('Nightly Whimsical Morale Boost Action', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    // Reset inputs for each test
    when(core.getInput)
      .calledWith('github-token', expect.any(Object))
      .mockReturnValue('mock-token');
    when(core.getInput)
      .calledWith('message-type')
      .mockReturnValue('whimsical');

    // Mock the createComment response
    mockCreateComment.mockResolvedValue({ data: { id: 12345 } });
  });

  test('posts a comment on a new pull request', async () => {
    // Mock rationale: Simulate a pull_request.opened event
    github.context = {
      eventName: 'pull_request',
      payload: {
        pull_request: {
          number: 101,
        },
      },
      repo: {
        owner: 'polsala',
        repo: 'ApocalypsAI',
      },
    };

    // Import and run the action
    require('../src/main');
    await new Promise(process.nextTick); // Allow promises to resolve

    expect(core.getInput).toHaveBeenCalledWith('github-token', { required: true });
    expect(github.getOctokit).toHaveBeenCalledWith('mock-token');
    expect(mockCreateComment).toHaveBeenCalledTimes(1);
    expect(mockCreateComment).toHaveBeenCalledWith(expect.objectContaining({
      owner: 'polsala',
      repo: 'ApocalypsAI',
      issue_number: 101,
      body: expect.any(String), // Message content is random, so check type
    }));
    expect(core.setOutput).toHaveBeenCalledWith('comment-id', 12345);
    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Detected Pull Request #101. Posting morale boost.'));
    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Morale boost posted successfully! Comment ID: 12345'));
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('posts a comment on a new issue', async () => {
    // Mock rationale: Simulate an issues.opened event
    github.context = {
      eventName: 'issues',
      payload: {
        issue: {
          number: 202,
        },
      },
      repo: {
        owner: 'polsala',
        repo: 'ApocalypsAI',
      },
    };

    require('../src/main');
    await new Promise(process.nextTick);

    expect(mockCreateComment).toHaveBeenCalledTimes(1);
    expect(mockCreateComment).toHaveBeenCalledWith(expect.objectContaining({
      owner: 'polsala',
      repo: 'ApocalypsAI',
      issue_number: 202,
      body: expect.any(String),
    }));
    expect(core.setOutput).toHaveBeenCalledWith('comment-id', 12345);
    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Detected Issue #202. Posting morale boost.'));
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('does not post a comment if event is not pull_request or issues', async () => {
    // Mock rationale: Simulate an unsupported event type
    github.context = {
      eventName: 'push',
      payload: {},
      repo: {
        owner: 'polsala',
        repo: 'ApocalypsAI',
      },
    };

    require('../src/main');
    await new Promise(process.nextTick);

    expect(mockCreateComment).not.toHaveBeenCalled();
    expect(core.warning).toHaveBeenCalledWith('This action is intended to run on pull_request or issues events. No comment will be posted.');
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('handles API errors gracefully', async () => {
    // Mock rationale: Simulate an error during the API call
    mockCreateComment.mockRejectedValue(new Error('API rate limit exceeded'));

    github.context = {
      eventName: 'pull_request',
      payload: {
        pull_request: {
          number: 303,
        },
      },
      repo: {
        owner: 'polsala',
        repo: 'ApocalypsAI',
      },
    };

    require('../src/main');
    await new Promise(process.nextTick);

    expect(mockCreateComment).toHaveBeenCalledTimes(1);
    expect(core.setFailed).toHaveBeenCalledWith('API rate limit exceeded');
    expect(core.setOutput).not.toHaveBeenCalled();
  });

  test('fails if github-token is missing', async () => {
    // Mock rationale: Simulate missing required input
    when(core.getInput)
      .calledWith('github-token', expect.any(Object))
      .mockReturnValue(''); // Empty token

    github.context = {
      eventName: 'pull_request',
      payload: {
        pull_request: {
          number: 404,
        },
      },
      repo: {
        owner: 'polsala',
        repo: 'ApocalypsAI',
      },
    };

    require('../src/main');
    await new Promise(process.nextTick);

    expect(core.setFailed).toHaveBeenCalledWith('Input required and not supplied: github-token');
    expect(mockCreateComment).not.toHaveBeenCalled();
  });
});
