const core = require('@actions/core');
const github = require('@actions/github');
const { Octokit } = require('@octokit/rest');

// Mock the GitHub Actions toolkit
jest.mock('@actions/core');
jest.mock('@actions/github');

describe('Branch Bloom Pruner', () => {
  let mockOctokit;
  let mockListBranches;
  let mockGetCommit;
  let mockCompareCommits;
  let mockDeleteRef;

  beforeEach(() => {
    jest.clearAllMocks();

    // Mock Octokit methods
    mockListBranches = jest.fn();
    mockGetCommit = jest.fn();
    mockCompareCommits = jest.fn();
    mockDeleteRef = jest.fn();

    mockOctokit = {
      rest: {
        repos: {
          listBranches: mockListBranches,
          getCommit: mockGetCommit,
          compareCommits: mockCompareCommits,
        },
        git: {
          deleteRef: mockDeleteRef,
        },
      },
      paginate: jest.fn((fn, params) => fn(params).then(res => res.data)), // Mock paginate to just return data from the first call
    };

    github.getOctokit.mockReturnValue(mockOctokit);
    github.context = {
      repo: {
        owner: 'test-owner',
        repo: 'test-repo',
      },
    };

    // Mock core inputs
    core.getInput.mockImplementation((name) => {
      switch (name) {
        case 'github-token': return 'mock-token';
        case 'stale-days': return '90';
        case 'default-branch': return 'main';
        case 'dry-run': return 'true';
        default: return '';
      }
    });
    core.info.mockImplementation(console.log);
    core.warning.mockImplementation(console.warn);
    core.error.mockImplementation(console.error);
  });

  // Mock rationale: We need to simulate GitHub API responses without making actual network calls.
  // @actions/github.getOctokit is mocked to return a custom Octokit instance.
  // The Octokit instance's methods (listBranches, getCommit, compareCommits, deleteRef) are
  // mocked to return predefined data based on test scenarios, ensuring deterministic and offline tests.
  // @actions/core methods (getInput, setOutput, setFailed, info) are mocked to capture interactions
  // and prevent side effects, allowing assertions on inputs, outputs, and logs.

  it('should identify and report stale, unmerged branches in dry-run mode', async () => {
    const mainBranchSha = 'main-sha';
    const staleBranchSha = 'stale-sha';
    const freshBranchSha = 'fresh-sha';
    const mergedBranchSha = 'merged-sha';

    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - 90); // 90 days ago

    mockListBranches.mockResolvedValueOnce({
      data: [
        { name: 'main', commit: { sha: mainBranchSha }, protected: true },
        { name: 'stale-unmerged', commit: { sha: staleBranchSha }, protected: false },
        { name: 'fresh-feature', commit: { sha: freshBranchSha }, protected: false },
        { name: 'merged-feature', commit: { sha: mergedBranchSha }, protected: false },
      ],
    });

    mockGetCommit
      .mockResolvedValueOnce({ data: { commit: { author: { date: new Date(cutoffDate.getTime() - 1000 * 60 * 60 * 24 * 10).toISOString() } } } }) // stale-unmerged (10 days before cutoff)
      .mockResolvedValueOnce({ data: { commit: { author: { date: new Date().toISOString() } } } }) // fresh-feature (today)
      .mockResolvedValueOnce({ data: { commit: { author: { date: new Date(cutoffDate.getTime() - 1000 * 60 * 60 * 24 * 5).toISOString() } } } }); // merged-feature (5 days before cutoff)

    mockCompareCommits
      .mockResolvedValueOnce({ data: { status: 'ahead' } }) // stale-unmerged is ahead/diverged
      .mockResolvedValueOnce({ data: { status: 'identical' } }) // fresh-feature is identical (shouldn't matter, not stale)
      .mockResolvedValueOnce({ data: { status: 'behind' } }); // merged-feature is behind (merged)

    // Set dry-run to true explicitly for this test
    core.getInput.mockImplementation((name) => {
      if (name === 'dry-run') return 'true';
      return jest.requireActual('@actions/core').getInput(name); // Use actual for others or mock all
    });

    // Dynamically import the action to ensure mocks are applied
    const action = require('../src/main');
    await action.run();

    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Branch \'stale-unmerged\' is stale'));
    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('[DRY RUN] Would prune branch: stale-unmerged'));
    expect(core.info).not.toHaveBeenCalledWith(expect.stringContaining('Pruning branch: stale-unmerged'));
    expect(mockDeleteRef).not.toHaveBeenCalled();
    expect(core.setOutput).toHaveBeenCalledWith('pruned-branches', JSON.stringify([{ name: 'stale-unmerged', status: 'would be pruned (dry-run)' }]));
  });

  it('should prune stale, unmerged branches when dry-run is false', async () => {
    const mainBranchSha = 'main-sha';
    const staleBranchSha = 'stale-sha';

    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - 90);

    mockListBranches.mockResolvedValueOnce({
      data: [
        { name: 'main', commit: { sha: mainBranchSha }, protected: true },
        { name: 'stale-unmerged', commit: { sha: staleBranchSha }, protected: false },
      ],
    });

    mockGetCommit.mockResolvedValueOnce({ data: { commit: { author: { date: new Date(cutoffDate.getTime() - 1000 * 60 * 60 * 24 * 10).toISOString() } } } }); // stale-unmerged

    mockCompareCommits.mockResolvedValueOnce({ data: { status: 'ahead' } }); // stale-unmerged is ahead/diverged

    // Set dry-run to false
    core.getInput.mockImplementation((name) => {
      if (name === 'dry-run') return 'false';
      return jest.requireActual('@actions/core').getInput(name);
    });

    const action = require('../src/main');
    await action.run();

    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Branch \'stale-unmerged\' is stale'));
    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Pruning branch: stale-unmerged'));
    expect(mockDeleteRef).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      ref: 'heads/stale-unmerged',
    });
    expect(core.setOutput).toHaveBeenCalledWith('pruned-branches', JSON.stringify([{ name: 'stale-unmerged', status: 'pruned' }]));
  });

  it('should skip protected branches', async () => {
    const mainBranchSha = 'main-sha';
    const protectedStaleBranchSha = 'protected-stale-sha';

    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - 90);

    mockListBranches.mockResolvedValueOnce({
      data: [
        { name: 'main', commit: { sha: mainBranchSha }, protected: true },
        { name: 'protected-stale', commit: { sha: protectedStaleBranchSha }, protected: true },
      ],
    });

    mockGetCommit.mockResolvedValueOnce({ data: { commit: { author: { date: new Date(cutoffDate.getTime() - 1000 * 60 * 60 * 24 * 10).toISOString() } } } }); // protected-stale

    // No compareCommits needed as it should be skipped earlier

    const action = require('../src/main');
    await action.run();

    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Skipping protected branch: protected-stale'));
    expect(mockDeleteRef).not.toHaveBeenCalled();
    expect(core.setOutput).toHaveBeenCalledWith('pruned-branches', '[]');
  });

  it('should skip branches that are not stale', async () => {
    const mainBranchSha = 'main-sha';
    const freshBranchSha = 'fresh-sha';

    mockListBranches.mockResolvedValueOnce({
      data: [
        { name: 'main', commit: { sha: mainBranchSha }, protected: true },
        { name: 'fresh-feature', commit: { sha: freshBranchSha }, protected: false },
      ],
    });

    mockGetCommit.mockResolvedValueOnce({ data: { commit: { author: { date: new Date().toISOString() } } } }); // fresh-feature (today)

    // No compareCommits needed as it should be skipped earlier

    const action = require('../src/main');
    await action.run();

    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Branch \'fresh-feature\' is not stale'));
    expect(mockDeleteRef).not.toHaveBeenCalled();
    expect(core.setOutput).toHaveBeenCalledWith('pruned-branches', '[]');
  });

  it('should skip branches that are stale but merged', async () => {
    const mainBranchSha = 'main-sha';
    const mergedBranchSha = 'merged-sha';

    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - 90);

    mockListBranches.mockResolvedValueOnce({
      data: [
        { name: 'main', commit: { sha: mainBranchSha }, protected: true },
        { name: 'merged-feature', commit: { sha: mergedBranchSha }, protected: false },
      ],
    });

    mockGetCommit.mockResolvedValueOnce({ data: { commit: { author: { date: new Date(cutoffDate.getTime() - 1000 * 60 * 60 * 24 * 5).toISOString() } } } }); // merged-feature

    mockCompareCommits.mockResolvedValueOnce({ data: { status: 'behind' } }); // merged-feature is behind (merged)

    const action = require('../src/main');
    await action.run();

    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Branch \'merged-feature\' is stale but already merged'));
    expect(mockDeleteRef).not.toHaveBeenCalled();
    expect(core.setOutput).toHaveBeenCalledWith('pruned-branches', '[]');
  });

  it('should handle API errors gracefully', async () => {
    const mainBranchSha = 'main-sha';
    const staleBranchSha = 'stale-sha';

    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - 90);

    mockListBranches.mockResolvedValueOnce({
      data: [
        { name: 'main', commit: { sha: mainBranchSha }, protected: true },
        { name: 'stale-unmerged-fail', commit: { sha: staleBranchSha }, protected: false },
      ],
    });

    mockGetCommit.mockResolvedValueOnce({ data: { commit: { author: { date: new Date(cutoffDate.getTime() - 1000 * 60 * 60 * 24 * 10).toISOString() } } } });

    mockCompareCommits.mockResolvedValueOnce({ data: { status: 'ahead' } });

    mockDeleteRef.mockRejectedValueOnce(new Error('API delete failed'));

    core.getInput.mockImplementation((name) => {
      if (name === 'dry-run') return 'false';
      return jest.requireActual('@actions/core').getInput(name);
    });

    const action = require('../src/main');
    await action.run();

    expect(core.error).toHaveBeenCalledWith(expect.stringContaining('Failed to prune branch \'stale-unmerged-fail\': API delete failed'));
    expect(core.setOutput).toHaveBeenCalledWith('pruned-branches', JSON.stringify([{ name: 'stale-unmerged-fail', status: 'failed to prune: API delete failed' }]));
  });

  it('should set failed if default branch not found', async () => {
    mockListBranches.mockResolvedValueOnce({
      data: [
        { name: 'feature-branch', commit: { sha: 'feature-sha' }, protected: false },
      ],
    });

    core.getInput.mockImplementation((name) => {
      if (name === 'default-branch') return 'non-existent-main';
      return jest.requireActual('@actions/core').getInput(name);
    });

    const action = require('../src/main');
    await action.run();

    expect(core.setFailed).toHaveBeenCalledWith(expect.stringContaining('Default branch \'non-existent-main\' not found.'));
  });
});
