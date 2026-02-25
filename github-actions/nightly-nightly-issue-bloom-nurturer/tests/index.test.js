const core = require('@actions/core');
const github = require('@actions/github');
const { when } = require('jest-when'); // For more precise mocking

// Mock the GitHub Actions toolkit
jest.mock('@actions/core');
jest.mock('@actions/github');

// Import the main action file's run function
const run = require('../src/index');

describe('Issue Bloom Nurturer', () => {
  let createCommentMock;
  let listForRepoMock;

  beforeEach(() => {
    jest.clearAllMocks();

    // Mock core.getInput
    when(core.getInput)
      .calledWith('repo-token', expect.any(Object))
      .mockReturnValue('mock-token');
    when(core.getInput)
      .calledWith('stale-days')
      .mockReturnValue('30');
    when(core.getInput)
      .calledWith('overgrown-comment-threshold')
      .mockReturnValue('50');

    // Mock core output and logging functions
    core.setOutput = jest.fn();
    core.setFailed = jest.fn();
    core.info = jest.fn();

    // Mock github.context.repo
    github.context = {
      repo: {
        owner: 'test-owner',
        repo: 'test-repo',
      },
    };

    // Mock octokit.rest.issues
    createCommentMock = jest.fn();
    listForRepoMock = jest.fn();

    github.getOctokit.mockReturnValue({
      rest: {
        issues: {
          listForRepo: listForRepoMock,
          createComment: createCommentMock,
        },
      },
    });
  });

  // Mock rationale: We mock the GitHub API calls (listForRepo, createComment) to ensure tests are deterministic and do not make actual network requests.
  // We also mock @actions/core functions (getInput, setOutput, setFailed, info) to control inputs and observe outputs/errors without side effects.

  test('should not comment on fresh issues', async () => {
    const now = new Date();
    const freshDate = new Date(now.setDate(now.getDate() - 5)).toISOString(); // 5 days ago

    listForRepoMock.mockResolvedValueOnce({
      data: [
        { number: 1, updated_at: freshDate, comments: 5, pull_request: {} }, // PR
        { number: 2, updated_at: freshDate, comments: 10 }, // Issue
      ],
    }).mockResolvedValueOnce({ data: [] }); // End pagination

    await run();

    expect(createCommentMock).not.toHaveBeenCalled();
    expect(core.setOutput).toHaveBeenCalledWith('nurtured-items-count', 0);
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('should comment on stale issues (parched)', async () => {
    const now = new Date();
    const staleDate = new Date(now.setDate(now.getDate() - 35)).toISOString(); // 35 days ago, > 30 stale-days

    listForRepoMock.mockResolvedValueOnce({
      data: [
        { number: 3, updated_at: staleDate, comments: 5 }, // Issue
      ],
    }).mockResolvedValueOnce({ data: [] }); // End pagination

    await run();

    expect(createCommentMock).toHaveBeenCalledTimes(1);
    expect(createCommentMock).toHaveBeenCalledWith(
      expect.objectContaining({
        issue_number: 3,
        body: expect.stringMatching(/parched|nurturing|dry|nap|revive/),
      })
    );
    expect(core.setOutput).toHaveBeenCalledWith('nurtured-items-count', 1);
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('should comment on overgrown issues', async () => {
    const now = new Date();
    const freshDate = new Date(now.setDate(now.getDate() - 5)).toISOString(); // 5 days ago, not stale

    listForRepoMock.mockResolvedValueOnce({
      data: [
        { number: 4, updated_at: freshDate, comments: 55 }, // 55 comments, > 50 threshold
      ],
    }).mockResolvedValueOnce({ data: [] }); // End pagination

    await run();

    expect(createCommentMock).toHaveBeenCalledTimes(1);
    expect(createCommentMock).toHaveBeenCalledWith(
      expect.objectContaining({
        issue_number: 4,
        body: expect.stringMatching(/blooming wildly|prune|forest|bountiful harvest|thriving ecosystem/),
      })
    );
    expect(core.setOutput).toHaveBeenCalledWith('nurtured-items-count', 1);
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('should handle both stale and overgrown issues', async () => {
    const now = new Date();
    const staleDate = new Date(now.setDate(now.getDate() - 35)).toISOString();
    const freshButOvergrownDate = new Date(now.setDate(now.getDate() - 5)).toISOString();

    listForRepoMock.mockResolvedValueOnce({
      data: [
        { number: 5, updated_at: staleDate, comments: 10 }, // Stale
        { number: 6, updated_at: freshButOvergrownDate, comments: 60 }, // Overgrown
      ],
    }).mockResolvedValueOnce({ data: [] }); // End pagination

    await run();

    expect(createCommentMock).toHaveBeenCalledTimes(2);
    expect(createCommentMock).toHaveBeenCalledWith(
      expect.objectContaining({
        issue_number: 5,
        body: expect.stringMatching(/parched|nurturing|dry|nap|revive/),
      })
    );
    expect(createCommentMock).toHaveBeenCalledWith(
      expect.objectContaining({
        issue_number: 6,
        body: expect.stringMatching(/blooming wildly|prune|forest|bountiful harvest|thriving ecosystem/),
      })
    );
    expect(core.setOutput).toHaveBeenCalledWith('nurtured-items-count', 2);
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('should set failed if API call fails', async () => {
    listForRepoMock.mockRejectedValue(new Error('API Error'));

    await run();

    expect(createCommentMock).not.toHaveBeenCalled();
    expect(core.setFailed).toHaveBeenCalledWith('API Error');
    expect(core.setOutput).not.toHaveBeenCalled(); // Output should not be set on failure
  });

  test('should use custom stale-days and overgrown-comment-threshold', async () => {
    when(core.getInput)
      .calledWith('stale-days')
      .mockReturnValue('10');
    when(core.getInput)
      .calledWith('overgrown-comment-threshold')
      .mockReturnValue('5');

    const now = new Date();
    const customStaleDate = new Date(now.setDate(now.getDate() - 12)).toISOString(); // 12 days ago, > 10 stale-days
    const customOvergrownDate = new Date(now.setDate(now.getDate() - 2)).toISOString(); // 2 days ago

    listForRepoMock.mockResolvedValueOnce({
      data: [
        { number: 7, updated_at: customStaleDate, comments: 2 }, // Stale with custom threshold
        { number: 8, updated_at: customOvergrownDate, comments: 7 }, // Overgrown with custom threshold
      ],
    }).mockResolvedValueOnce({ data: [] }); // End pagination

    await run();

    expect(createCommentMock).toHaveBeenCalledTimes(2);
    expect(createCommentMock).toHaveBeenCalledWith(
      expect.objectContaining({
        issue_number: 7,
        body: expect.stringMatching(/parched|nurturing|dry|nap|revive/),
      })
    );
    expect(createCommentMock).toHaveBeenCalledWith(
      expect.objectContaining({
        issue_number: 8,
        body: expect.stringMatching(/blooming wildly|prune|forest|bountiful harvest|thriving ecosystem/),
      })
    );
    expect(core.setOutput).toHaveBeenCalledWith('nurtured-items-count', 2);
    expect(core.setFailed).not.toHaveBeenCalled();
  });
});
