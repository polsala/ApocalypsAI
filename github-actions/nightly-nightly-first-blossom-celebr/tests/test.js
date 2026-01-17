const core = require('@actions/core');
const github = require('@actions/github');
const { when } = require('jest-when');

// Mock the GitHub Actions core library
jest.mock('@actions/core');

// Mock the GitHub Actions github library
const mockGetOctokit = jest.fn();
const mockSearchIssuesAndPullRequests = jest.fn();
const mockCreateComment = jest.fn();

jest.mock('@actions/github', () => ({
  getOctokit: mockGetOctokit,
  context: {
    repo: {
      owner: 'test-owner',
      repo: 'test-repo',
    },
    payload: {
      pull_request: {
        number: 123,
        user: { login: 'test-user' },
        merged: true,
      },
    },
  },
}));

describe('First Blossom Celebrator', () => {
  let main;

  beforeEach(() => {
    jest.clearAllMocks();

    // Mock Octokit methods
    mockGetOctokit.mockReturnValue({
      rest: {
        search: {
          issuesAndPullRequests: mockSearchIssuesAndPullRequests,
        },
        issues: {
          createComment: mockCreateComment,
        },
      },
    });

    // Mock core.getInput
    when(core.getInput)
      .calledWith('github-token', expect.any(Object))
      .thenReturn('mock-token');

    // Re-require main to ensure mocks are applied correctly for each test
    main = require('../src/main');
  });

  // Mock rationale: Mocks the GitHub API client to prevent actual network calls during tests.
  // Mock rationale: Mocks the GitHub Actions event payload to simulate different PR scenarios.
  // Mock rationale: Mocks input parameters to the action.
  // Mock rationale: Mocks output setting to verify the action's results.
  // Mock rationale: Mocks the API response for searching PRs, allowing control over whether other merged PRs by the author are found.
  // Mock rationale: Mocks the API call to add a comment, verifying that the comment is correctly formed and would be posted.

  it('should celebrate a first contribution', async () => {
    // Simulate no other merged PRs by the author (only the current one)
    mockSearchIssuesAndPullRequests.mockResolvedValueOnce({
      data: {
        items: [
          { pull_request: {}, number: 123, user: { login: 'test-user' } } // Current PR
        ],
      },
    });

    await main.run();

    expect(mockSearchIssuesAndPullRequests).toHaveBeenCalledWith({
      q: 'is:pr author:test-user is:merged repo:test-owner/test-repo',
      per_page: 100,
    });
    expect(mockCreateComment).toHaveBeenCalledTimes(1);
    expect(mockCreateComment).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      issue_number: 123,
      body: expect.stringContaining('A new blossom has bloomed!'),
    });
    expect(core.setOutput).toHaveBeenCalledWith('is-first-contribution', 'true');
    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('first merged contribution! Celebrating!'));
  });

  it('should not celebrate if it is not the first contribution', async () => {
    // Simulate other merged PRs by the author
    mockSearchIssuesAndPullRequests.mockResolvedValueOnce({
      data: {
        items: [
          { pull_request: {}, number: 123, user: { login: 'test-user' } }, // Current PR
          { pull_request: {}, number: 100, user: { login: 'test-user' } }, // Another PR
        ],
      },
    });

    await main.run();

    expect(mockSearchIssuesAndPullRequests).toHaveBeenCalledTimes(1);
    expect(mockCreateComment).not.toHaveBeenCalled();
    expect(core.setOutput).toHaveBeenCalledWith('is-first-contribution', 'false');
    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Not their first contribution.'));
  });

  it('should not run if the PR is not merged', async () => {
    github.context.payload.pull_request.merged = false; // Simulate unmerged PR

    await main.run();

    expect(mockSearchIssuesAndPullRequests).not.toHaveBeenCalled();
    expect(mockCreateComment).not.toHaveBeenCalled();
    expect(core.setOutput).toHaveBeenCalledWith('is-first-contribution', 'false');
    expect(core.info).toHaveBeenCalledWith('PR is not merged. Skipping celebration.');
  });

  it('should handle API errors gracefully', async () => {
    mockSearchIssuesAndPullRequests.mockRejectedValueOnce(new Error('API rate limit exceeded'));

    await main.run();

    expect(core.setFailed).toHaveBeenCalledWith('API rate limit exceeded');
    expect(core.setOutput).not.toHaveBeenCalledWith('is-first-contribution', expect.any(String)); // Should not set output on failure
  });

  it('should handle missing pull_request payload gracefully', async () => {
    github.context.payload.pull_request = undefined; // Simulate missing PR payload

    await main.run();

    expect(mockSearchIssuesAndPullRequests).not.toHaveBeenCalled();
    expect(mockCreateComment).not.toHaveBeenCalled();
    expect(core.setOutput).toHaveBeenCalledWith('is-first-contribution', 'false');
    expect(core.info).toHaveBeenCalledWith('PR is not merged. Skipping celebration.');
  });
});
