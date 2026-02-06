const core = require('@actions/core');
const github = require('@actions/github');
const { when } = require('jest-when');

// Mock the GitHub Actions core library
jest.mock('@actions/core');
jest.mock('@actions/github');

const run = require('../src/main'); // The action's main script

describe('Stale Branch Whisperer', () => {
  let createIssueMock;
  let listBranchesMock;
  let getBranchMock;
  let listPullRequestsMock;

  beforeEach(() => {
    jest.clearAllMocks();

    // Mock github context
    github.context = {
      repo: {
        owner: 'test-owner',
        repo: 'test-repo',
      },
    };

    // Mock Octokit methods
    createIssueMock = jest.fn();
    listBranchesMock = jest.fn();
    getBranchMock = jest.fn();
    listPullRequestsMock = jest.fn();

    github.getOctokit.mockReturnValue({
      rest: {
        repos: {
          listBranches: listBranchesMock,
          getBranch: getBranchMock,
        },
        issues: {
          create: createIssueMock,
        },
        pulls: {
          list: listPullRequestsMock,
        }
      },
    });

    // Mock core.getInput
    when(core.getInput)
      .calledWith('github-token', expect.anything())
      .thenReturn('mock-token');
    when(core.getInput)
      .calledWith('stale-days')
      .thenReturn('30');
    when(core.getInput)
      .calledWith('default-branch')
      .thenReturn('main');
    when(core.getInput)
      .calledWith('issue-label')
      .thenReturn('stale-branch');
    when(core.getInput)
      .calledWith('dry-run')
      .thenReturn('false');
    when(core.getInput)
      .calledWith('exclude-branches')
      .thenReturn('');
  });

  // Mock rationale:
  // - core.getInput: Provides controlled test inputs to the action, ensuring deterministic behavior without relying on actual workflow inputs.
  // - core.info, core.debug, core.warning, core.setFailed, core.setOutput: Captures logging and output behavior for assertions, preventing actual console output or workflow failures during tests.
  // - github.context: Simulates the GitHub repository context (owner, repo) without needing a live GitHub environment.
  // - github.getOctokit: Returns a mock Octokit client, allowing us to control the responses of GitHub API calls (listBranches, getBranch, create, listPullRequests) and verify their invocation, making tests offline and deterministic.

  it('should find no stale branches and not create an issue', async () => {
    const recentDate = new Date();
    recentDate.setDate(recentDate.getDate() - 10); // 10 days ago, not stale

    listBranchesMock.mockResolvedValue({
      data: [
        { name: 'main', commit: { sha: 'sha1' } },
        { name: 'feature-a', commit: { sha: 'sha2' } },
      ],
    });

    when(getBranchMock)
      .calledWith(expect.objectContaining({ branch: 'feature-a' }))
      .mockResolvedValue({
        data: {
          commit: {
            commit: {
              author: { date: recentDate.toISOString() },
            },
          },
        },
      });

    listPullRequestsMock.mockResolvedValue({ data: [] }); // No merged PRs for feature-a

    await run();

    expect(listBranchesMock).toHaveBeenCalledTimes(1);
    expect(getBranchMock).toHaveBeenCalledWith(expect.objectContaining({ branch: 'feature-a' }));
    expect(listPullRequestsMock).toHaveBeenCalledWith(expect.objectContaining({ head: 'test-owner:feature-a' }));
    expect(createIssueMock).not.toHaveBeenCalled();
    expect(core.setOutput).toHaveBeenCalledWith('stale-branches-count', 0);
    expect(core.setOutput).toHaveBeenCalledWith('stale-branches-list', '[]');
    expect(core.info).toHaveBeenCalledWith('No stale branches found. The repository is spick and span!');
  });

  it('should find one stale branch and create an issue', async () => {
    const staleDate = new Date();
    staleDate.setDate(staleDate.getDate() - 40); // 40 days ago, stale

    listBranchesMock.mockResolvedValue({
      data: [
        { name: 'main', commit: { sha: 'sha1' } },
        { name: 'stale-feature', commit: { sha: 'sha2' } },
      ],
    });

    when(getBranchMock)
      .calledWith(expect.objectContaining({ branch: 'stale-feature' }))
      .mockResolvedValue({
        data: {
          commit: {
            commit: {
              author: { date: staleDate.toISOString() },
            },
          },
        },
      });

    listPullRequestsMock.mockResolvedValue({ data: [] }); // No merged PRs for stale-feature

    await run();

    expect(listBranchesMock).toHaveBeenCalledTimes(1);
    expect(getBranchMock).toHaveBeenCalledWith(expect.objectContaining({ branch: 'stale-feature' }));
    expect(listPullRequestsMock).toHaveBeenCalledWith(expect.objectContaining({ head: 'test-owner:stale-feature' }));
    expect(createIssueMock).toHaveBeenCalledTimes(1);
    expect(createIssueMock).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      title: 'A Gentle Whisper from the Repository Depths: Stale Branches Detected!',
      body: expect.stringContaining('- `stale-feature`'),
      labels: ['stale-branch'],
    });
    expect(core.setOutput).toHaveBeenCalledWith('stale-branches-count', 1);
    expect(core.setOutput).toHaveBeenCalledWith('stale-branches-list', '["stale-feature"]');
  });

  it('should not create an issue if dry-run is true', async () => {
    when(core.getInput)
      .calledWith('dry-run')
      .thenReturn('true');

    const staleDate = new Date();
    staleDate.setDate(staleDate.getDate() - 40);

    listBranchesMock.mockResolvedValue({
      data: [
        { name: 'main', commit: { sha: 'sha1' } },
        { name: 'dry-run-stale', commit: { sha: 'sha2' } },
      ],
    });

    when(getBranchMock)
      .calledWith(expect.objectContaining({ branch: 'dry-run-stale' }))
      .mockResolvedValue({
        data: {
          commit: {
            commit: {
              author: { date: staleDate.toISOString() },
            },
          },
        },
      });

    listPullRequestsMock.mockResolvedValue({ data: [] });

    await run();

    expect(createIssueMock).not.toHaveBeenCalled();
    expect(core.info).toHaveBeenCalledWith('Dry run enabled. No issue created.');
    expect(core.setOutput).toHaveBeenCalledWith('stale-branches-count', 1);
    expect(core.setOutput).toHaveBeenCalledWith('stale-branches-list', '["dry-run-stale"]');
  });

  it('should exclude specified branches', async () => {
    when(core.getInput)
      .calledWith('exclude-branches')
      .thenReturn('dev,release-.*');

    const staleDate = new Date();
    staleDate.setDate(staleDate.getDate() - 40);

    listBranchesMock.mockResolvedValue({
      data: [
        { name: 'main', commit: { sha: 'sha1' } },
        { name: 'dev', commit: { sha: 'sha2' } }, // Excluded
        { name: 'release-v1', commit: { sha: 'sha3' } }, // Excluded by regex
        { name: 'stale-but-not-excluded', commit: { sha: 'sha4' } },
      ],
    });

    when(getBranchMock)
      .calledWith(expect.objectContaining({ branch: 'dev' }))
      .mockResolvedValue({ data: { commit: { commit: { author: { date: staleDate.toISOString() } } } } });
    when(getBranchMock)
      .calledWith(expect.objectContaining({ branch: 'release-v1' }))
      .mockResolvedValue({ data: { commit: { commit: { author: { date: staleDate.toISOString() } } } } });
    when(getBranchMock)
      .calledWith(expect.objectContaining({ branch: 'stale-but-not-excluded' }))
      .mockResolvedValue({ data: { commit: { commit: { author: { date: staleDate.toISOString() } } } } });

    listPullRequestsMock.mockResolvedValue({ data: [] });

    await run();

    expect(core.info).toHaveBeenCalledWith(expect.stringContaining("excluding: dev, release-.*"));
    expect(core.debug).toHaveBeenCalledWith('Skipping excluded branch: dev');
    expect(core.debug).toHaveBeenCalledWith('Skipping excluded branch: release-v1');
    expect(createIssueMock).toHaveBeenCalledTimes(1);
    expect(createIssueMock).toHaveBeenCalledWith(expect.objectContaining({
      body: expect.stringContaining('- `stale-but-not-excluded`'),
    }));
    expect(core.setOutput).toHaveBeenCalledWith('stale-branches-count', 1);
    expect(core.setOutput).toHaveBeenCalledWith('stale-branches-list', '["stale-but-not-excluded"]');
  });

  it('should not report branches that have merged PRs', async () => {
    const staleDate = new Date();
    staleDate.setDate(staleDate.getDate() - 40);

    listBranchesMock.mockResolvedValue({
      data: [
        { name: 'main', commit: { sha: 'sha1' } },
        { name: 'merged-stale-branch', commit: { sha: 'sha2' } },
      ],
    });

    when(getBranchMock)
      .calledWith(expect.objectContaining({ branch: 'merged-stale-branch' }))
      .mockResolvedValue({
        data: {
          commit: {
            commit: {
              author: { date: staleDate.toISOString() },
            },
          },
        },
      });

    listPullRequestsMock.mockResolvedValue({
      data: [{ merged_at: new Date().toISOString() }] // Simulate a merged PR
    });

    await run();

    expect(core.info).toHaveBeenCalledWith("Branch 'merged-stale-branch' has a merged PR, skipping.");
    expect(createIssueMock).not.toHaveBeenCalled();
    expect(core.setOutput).toHaveBeenCalledWith('stale-branches-count', 0);
    expect(core.setOutput).toHaveBeenCalledWith('stale-branches-list', '[]');
  });

  it('should handle API errors gracefully', async () => {
    listBranchesMock.mockRejectedValue(new Error('API rate limit exceeded'));

    await run();

    expect(core.setFailed).toHaveBeenCalledWith('API rate limit exceeded');
    expect(core.setOutput).not.toHaveBeenCalledWith('stale-branches-count', expect.any(Number));
  });
});
