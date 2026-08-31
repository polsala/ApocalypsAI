const core = require('@actions/core');
const github = require('@actions/github');
const { run } = require('../src/main'); // Assuming main.js exports run function

// Mock the @actions/core and @actions/github modules
jest.mock('@actions/core');
jest.mock('@actions/github');

describe('Nightly Post-Merge Pep Talk Action', () => {
  let createCommentMock;
  let getInputMock;
  let setFailedMock;
  let infoMock;

  beforeEach(() => {
    jest.clearAllMocks();

    // Mock github.getOctokit and its methods
    createCommentMock = jest.fn().mockResolvedValue({});
    github.getOctokit.mockReturnValue({
      rest: {
        issues: {
          createComment: createCommentMock,
        },
      },
    });

    // Mock core functions
    getInputMock = core.getInput.mockReturnValue('mock-token'); // Default token
    setFailedMock = core.setFailed.mockImplementation(() => {});
    infoMock = core.info.mockImplementation(() => {});

    // Mock github.context for a merged PR
    github.context = {
      payload: {
        pull_request: {
          number: 123,
          merged: true,
        },
      },
      repo: {
        owner: 'test-owner',
        repo: 'test-repo',
      },
    };
  });

  // Mock rationale: We mock @actions/core and @actions/github to isolate the action's logic
  // from the actual GitHub API and environment. This ensures tests are fast, deterministic,
  // and do not require network access or actual GitHub credentials.

  test('should post a pep talk comment if PR is merged', async () => {
    await run();

    expect(getInputMock).toHaveBeenCalledWith('github-token', { required: true });
    expect(createCommentMock).toHaveBeenCalledTimes(1);
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      issue_number: 123,
      body: expect.stringContaining('ApocalypsAI Post-Merge Pep Talk:')
    });
    expect(infoMock).toHaveBeenCalledWith('Pep talk delivered to PR #123.');
    expect(setFailedMock).not.toHaveBeenCalled();
  });

  test('should not post a comment if PR is not merged', async () => {
    github.context.payload.pull_request.merged = false;

    await run();

    expect(createCommentMock).not.toHaveBeenCalled();
    expect(infoMock).toHaveBeenCalledWith('PR is not merged. Skipping pep talk.');
    expect(setFailedMock).not.toHaveBeenCalled();
  });

  test('should fail if not run on a pull_request_target event', async () => {
    github.context.payload.pull_request = undefined;

    await run();

    expect(createCommentMock).not.toHaveBeenCalled();
    expect(setFailedMock).toHaveBeenCalledWith('This action can only be run on pull_request_target events.');
  });

  test('should handle API errors gracefully', async () => {
    const errorMessage = 'Failed to create comment';
    createCommentMock.mockRejectedValue(new Error(errorMessage));

    await run();

    expect(createCommentMock).toHaveBeenCalledTimes(1);
    expect(setFailedMock).toHaveBeenCalledWith(errorMessage);
  });

  test('should use the provided github-token', async () => {
    getInputMock.mockReturnValue('custom-mock-token');
    await run();
    expect(github.getOctokit).toHaveBeenCalledWith('custom-mock-token');
  });
});
