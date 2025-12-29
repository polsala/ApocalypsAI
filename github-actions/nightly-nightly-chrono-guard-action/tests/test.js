const core = require('@actions/core');
const github = require('@actions/github');
const { run } = require('../src/main');

// Mock the GitHub Actions toolkit
jest.mock('@actions/core');
jest.mock('@actions/github');

describe('Nightly Chrono-Guard Action', () => {
  let createCommentMock;

  beforeEach(() => {
    jest.clearAllMocks();

    // Mock rationale: Simulate core functions for input/output/logging without actual side effects.
    core.getInput.mockImplementation((name, options) => {
      if (name === 'github-token') return 'mock-token';
      if (name === 'keywords') return 'time travel,paradox,anachronism';
      return '';
    });
    core.info.mockImplementation(jest.fn());
    core.warning.mockImplementation(jest.fn());
    core.setFailed.mockImplementation(jest.fn());
    core.setOutput.mockImplementation(jest.fn());

    // Mock rationale: Simulate GitHub API calls and context for deterministic testing.
    createCommentMock = jest.fn();
    github.getOctokit.mockReturnValue({
      rest: {
        pulls: {
          get: jest.fn().mockResolvedValue({
            data: { title: 'Feature: Implement new login flow' }
          }),
          listCommits: jest.fn().mockResolvedValue({
            data: [
              { commit: { message: 'feat: initial commit' } },
              { commit: { message: 'fix: address review comments' } },
            ]
          }),
        },
        issues: {
          createComment: createCommentMock,
        },
      },
    });

    github.context = {
      repo: {
        owner: 'polsala',
        repo: 'ApocalypsAI',
      },
      payload: {
        pull_request: {
          number: 123,
        },
      },
    };
  });

  test('should not detect anomaly if no keywords are present', async () => {
    await run();

    expect(core.setOutput).toHaveBeenCalledWith('temporal-anomaly-detected', false);
    expect(core.warning).not.toHaveBeenCalled();
    expect(createCommentMock).not.toHaveBeenCalled();
  });

  test('should detect anomaly in PR title and add a comment', async () => {
    github.getOctokit.mockReturnValue({
      rest: {
        pulls: {
          get: jest.fn().mockResolvedValue({
            data: { title: 'Feature: Implement time travel login' } // Keyword in title
          }),
          listCommits: jest.fn().mockResolvedValue({
            data: [
              { commit: { message: 'feat: initial commit' } },
            ]
          }),
        },
        issues: {
          createComment: createCommentMock,
        },
      },
    });

    await run();

    expect(core.setOutput).toHaveBeenCalledWith('temporal-anomaly-detected', true);
    expect(core.warning).toHaveBeenCalledWith(expect.stringContaining('Temporal anomaly detected in PR #123. Keywords: time travel'));
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'polsala',
      repo: 'ApocalypsAI',
      issue_number: 123,
      body: expect.stringContaining('🕰️ **Temporal Anomaly Detected!** 🕰️\n\n') && expect.stringContaining('Detected keywords: `time travel`'),
    });
  });

  test('should detect anomaly in commit message and add a comment', async () => {
    github.getOctokit.mockReturnValue({
      rest: {
        pulls: {
          get: jest.fn().mockResolvedValue({
            data: { title: 'Feature: Implement new login flow' }
          }),
          listCommits: jest.fn().mockResolvedValue({
            data: [
              { commit: { message: 'feat: initial commit' } },
              { commit: { message: 'fix: address paradox in login logic' } }, // Keyword in commit
            ]
          }),
        },
        issues: {
          createComment: createCommentMock,
        },
      },
    });

    await run();

    expect(core.setOutput).toHaveBeenCalledWith('temporal-anomaly-detected', true);
    expect(core.warning).toHaveBeenCalledWith(expect.stringContaining('Temporal anomaly detected in PR #123. Keywords: paradox'));
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'polsala',
      repo: 'ApocalypsAI',
      issue_number: 123,
      body: expect.stringContaining('🕰️ **Temporal Anomaly Detected!** 🕰️\n\n') && expect.stringContaining('Detected keywords: `paradox`'),
    });
  });

  test('should handle case-insensitivity', async () => {
    github.getOctokit.mockReturnValue({
      rest: {
        pulls: {
          get: jest.fn().mockResolvedValue({
            data: { title: 'Feature: Implement Time Travel login' } // Mixed case
          }),
          listCommits: jest.fn().mockResolvedValue({
            data: [
              { commit: { message: 'feat: initial commit' } },
            ]
          }),
        },
        issues: {
          createComment: createCommentMock,
        },
      },
    });

    await run();

    expect(core.setOutput).toHaveBeenCalledWith('temporal-anomaly-detected', true);
    expect(core.warning).toHaveBeenCalledWith(expect.stringContaining('Temporal anomaly detected in PR #123. Keywords: time travel'));
  });

  test('should use custom keywords if provided', async () => {
    core.getInput.mockImplementation((name, options) => {
      if (name === 'github-token') return 'mock-token';
      if (name === 'keywords') return 'flux capacitor,delorean'; // Custom keywords
      return '';
    });

    github.getOctokit.mockReturnValue({
      rest: {
        pulls: {
          get: jest.fn().mockResolvedValue({
            data: { title: 'Feature: Install flux capacitor' }
          }),
          listCommits: jest.fn().mockResolvedValue({
            data: [
              { commit: { message: 'feat: initial commit' } },
            ]
          }),
        },
        issues: {
          createComment: createCommentMock,
        },
      },
    });

    await run();

    expect(core.setOutput).toHaveBeenCalledWith('temporal-anomaly-detected', true);
    expect(core.warning).toHaveBeenCalledWith(expect.stringContaining('Temporal anomaly detected in PR #123. Keywords: flux capacitor'));
  });

  test('should not run if not a pull request event', async () => {
    github.context.payload.pull_request = undefined; // Not a PR event

    await run();

    expect(core.info).toHaveBeenCalledWith('Not a pull request event. Skipping chrono-guard scan.');
    expect(core.setOutput).toHaveBeenCalledWith('temporal-anomaly-detected', false);
    expect(createCommentMock).not.toHaveBeenCalled();
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('should handle API errors gracefully', async () => {
    github.getOctokit.mockReturnValue({
      rest: {
        pulls: {
          get: jest.fn().mockRejectedValue(new Error('API error')), // Simulate API error
          listCommits: jest.fn().mockResolvedValue({ data: [] }),
        },
        issues: {
          createComment: createCommentMock,
        },
      },
    });

    await run();

    expect(core.setFailed).toHaveBeenCalledWith('API error');
    expect(core.setOutput).toHaveBeenCalledWith('temporal-anomaly-detected', false);
    expect(createCommentMock).not.toHaveBeenCalled();
  });
});
