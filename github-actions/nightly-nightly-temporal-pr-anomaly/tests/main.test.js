const core = require('@actions/core');
const github = require('@actions/github');
const { when } = require('jest-when'); // For more flexible mocking

// Mock the GitHub Actions toolkit
jest.mock('@actions/core');
jest.mock('@actions/github');

// Import the main action file's run function
const run = require('../src/main');

describe('Nightly Temporal PR Anomaly Check', () => {
  let createCommentMock;
  let listCommitsMock;

  beforeEach(() => {
    jest.clearAllMocks();

    // Mock rationale:
    // - core.getInput: Simulates action inputs without requiring actual environment variables.
    // - github.getOctokit: Prevents actual API calls to GitHub by returning a mock Octokit client.
    // - github.context: Provides a consistent PR context for tests, avoiding reliance on a live GitHub event.
    // - createCommentMock: Allows verification that a comment was attempted and with what content.
    // - listCommitsMock: Simulates the response from the GitHub API for commit messages, ensuring deterministic commit content.
    // - console.log/debug/info: Suppresses console output during tests for cleaner results.

    // Mock core.getInput
    when(core.getInput)
      .calledWith('github-token', expect.anything())
      .thenReturn('mock-token');

    // Mock github.getOctokit().rest.issues.createComment and pulls.listCommits
    createCommentMock = jest.fn();
    listCommitsMock = jest.fn();

    github.getOctokit.mockReturnValue({
      rest: {
        issues: {
          createComment: createCommentMock,
        },
        pulls: {
          listCommits: listCommitsMock,
        },
      },
    });

    // Mock github.context for a pull_request event
    github.context = {
      repo: {
        owner: 'polsala',
        repo: 'ApocalypsAI',
      },
      payload: {
        pull_request: {
          number: 123,
          title: 'feat: Add new feature',
          head: {
            sha: 'mocksha123'
          }
        },
      },
      eventName: 'pull_request',
    };

    // Mock console.log for debug/info messages
    jest.spyOn(console, 'log').mockImplementation(() => {});
    jest.spyOn(console, 'debug').mockImplementation(() => {});
    jest.spyOn(console, 'info').mockImplementation(() => {});
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  test('should post a comment if PR title contains a temporal keyword', async () => {
    github.context.payload.pull_request.title = 'feat: Implement time travel functionality';
    listCommitsMock.mockResolvedValue({ data: [] }); // No commits for this test

    await run();

    expect(createCommentMock).toHaveBeenCalledTimes(1);
    expect(createCommentMock).toHaveBeenCalledWith(expect.objectContaining({
      owner: 'polsala',
      repo: 'ApocalypsAI',
      issue_number: 123,
      body: expect.stringContaining('Temporal Anomaly Alert!')
    }));
    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Temporal anomaly keyword detected: "time travel"'));
    expect(core.info).toHaveBeenCalledWith('Whimsical temporal anomaly warning posted to PR.');
  });

  test('should post a comment if a commit message contains a temporal keyword', async () => {
    github.context.payload.pull_request.title = 'feat: Regular feature update';
    listCommitsMock.mockResolvedValue({
      data: [
        { commit: { message: 'Initial commit' } },
        { commit: { message: 'Fix: Resolve a paradox in the codebase' } },
      ],
    });

    await run();

    expect(createCommentMock).toHaveBeenCalledTimes(1);
    expect(createCommentMock).toHaveBeenCalledWith(expect.objectContaining({
      owner: 'polsala',
      repo: 'ApocalypsAI',
      issue_number: 123,
      body: expect.stringContaining('Temporal Anomaly Alert!')
    }));
    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Temporal anomaly keyword detected: "paradox"'));
    expect(core.info).toHaveBeenCalledWith('Whimsical temporal anomaly warning posted to PR.');
  });

  test('should not post a comment if no temporal keywords are found', async () => {
    github.context.payload.pull_request.title = 'feat: Implement new UI component';
    listCommitsMock.mockResolvedValue({
      data: [
        { commit: { message: 'Initial UI setup' } },
        { commit: { message: 'Add styling' } },
      ],
    });

    await run();

    expect(createCommentMock).not.toHaveBeenCalled();
    expect(core.info).toHaveBeenCalledWith('No temporal anomaly keywords detected. All clear for now.');
  });

  test('should handle multiple keywords gracefully (post only one comment)', async () => {
    github.context.payload.pull_request.title = 'feat: Time travel and paradox resolution';
    listCommitsMock.mockResolvedValue({ data: [] });

    await run();

    expect(createCommentMock).toHaveBeenCalledTimes(1); // Only one comment should be posted
    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Temporal anomaly keyword detected: "time travel"'));
    // The action stops after the first detection, so 'paradox' might not be logged, but the comment is still posted.
  });

  test('should not run if not a pull_request event', async () => {
    github.context.payload.pull_request = undefined; // Simulate non-PR event
    github.context.eventName = 'push';

    await run();

    expect(createCommentMock).not.toHaveBeenCalled();
    expect(core.info).toHaveBeenCalledWith('This action only runs on pull_request events. Skipping.');
  });

  test('should call setFailed on error', async () => {
    listCommitsMock.mockRejectedValue(new Error('API Error')); // Simulate API error

    await run();

    expect(core.setFailed).toHaveBeenCalledTimes(1);
    expect(core.setFailed).toHaveBeenCalledWith('API Error');
  });
});
