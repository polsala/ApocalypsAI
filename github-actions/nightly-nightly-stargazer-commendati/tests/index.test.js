const core = require('@actions/core');
const github = require('@actions/github');
const { comments } = require('../src/comments');

// Mock the GitHub Actions toolkit
jest.mock('@actions/core');
jest.mock('@actions/github');

describe('Nightly Stargazer Commendation', () => {
  let run;
  let mockListPullRequests;
  let mockCreateComment;
  let originalMathRandom;

  beforeEach(() => {
    jest.clearAllMocks();
    originalMathRandom = Math.random;
    Math.random = jest.fn(() => 0.5); // Mock Math.random for deterministic tests

    // Mock inputs
    core.getInput.mockImplementation((name) => {
      switch (name) {
        case 'github-token': return 'mock-token';
        case 'days-back': return '7';
        default: return '';
      }
    });

    // Mock github context
    github.context = {
      repo: {
        owner: 'test-owner',
        repo: 'test-repo',
      },
    };

    // Mock Octokit API calls
    mockListPullRequests = jest.fn();
    mockCreateComment = jest.fn();
    github.getOctokit.mockReturnValue({
      rest: {
        pulls: {
          list: mockListPullRequests,
        },
        issues: {
          createComment: mockCreateComment,
        },
      },
    });

    // Load the action's main file after mocks are set up
    run = require('../src/index');
  });

  afterEach(() => {
    Math.random = originalMathRandom; // Restore original Math.random
  });

  it('should commend a randomly selected PR if eligible PRs exist', async () => {
    // Mock rationale: Simulate GitHub API response for merged PRs.
    const mockMergedPRs = [
      { number: 1, title: 'PR 1', merged_at: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString() }, // 2 days ago
      { number: 2, title: 'PR 2', merged_at: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString() }, // 5 days ago
      { number: 3, title: 'PR 3', merged_at: new Date(Date.now() - 10 * 24 * 60 * 60 * 1000).toISOString() }, // 10 days ago (too old)
    ];
    mockListPullRequests.mockResolvedValueOnce({ data: mockMergedPRs });

    // Mock Math.random to select the second eligible PR (index 1, which is PR #2)
    Math.random.mockReturnValueOnce(0.5); // For PR selection
    Math.random.mockReturnValueOnce(0.5); // For comment selection

    await run();

    expect(mockListPullRequests).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      state: 'closed',
      sort: 'updated',
      direction: 'desc',
      per_page: 100,
    });

    // Expect the second eligible PR (index 1) to be selected
    const expectedComment = comments[Math.floor(0.5 * comments.length)]; // Deterministic comment selection
    expect(mockCreateComment).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      issue_number: 2,
      body: expectedComment,
    });
    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Selected PR #2: PR 2'));
    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Successfully commended PR #2.'));
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  it('should not commend if no eligible PRs are found', async () => {
    // Mock rationale: Simulate GitHub API response with no recently merged PRs.
    const mockMergedPRs = [
      { number: 1, title: 'PR 1', merged_at: new Date(Date.now() - 10 * 24 * 60 * 60 * 1000).toISOString() }, // 10 days ago (too old)
    ];
    mockListPullRequests.mockResolvedValueOnce({ data: mockMergedPRs });

    await run();

    expect(mockListPullRequests).toHaveBeenCalledTimes(1);
    expect(mockCreateComment).not.toHaveBeenCalled();
    expect(core.info).toHaveBeenCalledWith('No eligible merged Pull Requests found in the specified period.');
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  it('should handle API errors gracefully', async () => {
    // Mock rationale: Simulate a network or API error during PR listing.
    const errorMessage = 'GitHub API error';
    mockListPullRequests.mockRejectedValueOnce(new Error(errorMessage));

    await run();

    expect(mockListPullRequests).toHaveBeenCalledTimes(1);
    expect(mockCreateComment).not.toHaveBeenCalled();
    expect(core.setFailed).toHaveBeenCalledWith(errorMessage);
  });

  it('should use default days-back if not provided', async () => {
    core.getInput.mockImplementation((name) => {
      switch (name) {
        case 'github-token': return 'mock-token';
        case 'days-back': return ''; // No input for days-back
        default: return '';
      }
    });

    // Mock rationale: Simulate GitHub API response for merged PRs.
    const mockMergedPRs = [
      { number: 1, title: 'PR 1', merged_at: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString() }, // 2 days ago
    ];
    mockListPullRequests.mockResolvedValueOnce({ data: mockMergedPRs });

    await run();

    // The cutoff date calculation should use 7 days back
    // We can't directly assert the date object, but we can check if a PR within 7 days is processed
    expect(mockCreateComment).toHaveBeenCalledTimes(1);
    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Looking for merged PRs in test-owner/test-repo merged after'));
  });

  it('should filter out PRs merged before the cutoff date', async () => {
    // Mock rationale: Simulate GitHub API response with PRs both inside and outside the window.
    const mockMergedPRs = [
      { number: 1, title: 'Recent PR', merged_at: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString() }, // 1 day ago
      { number: 2, title: 'Old PR', merged_at: new Date(Date.now() - 8 * 24 * 60 * 60 * 1000).toISOString() }, // 8 days ago (outside 7-day window)
    ];
    mockListPullRequests.mockResolvedValueOnce({ data: mockMergedPRs });

    Math.random.mockReturnValueOnce(0.0); // Select the first eligible PR
    Math.random.mockReturnValueOnce(0.0); // Select the first comment

    await run();

    expect(mockCreateComment).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      issue_number: 1,
      body: comments[0],
    });
    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Selected PR #1: Recent PR'));
    expect(core.info).not.toHaveBeenCalledWith(expect.stringContaining('Selected PR #2: Old PR'));
  });
});
