const core = require('@actions/core');
const github = require('@actions/github');
const { run } = require('../src/index');

// Mock the GitHub Actions toolkit
jest.mock('@actions/core');
jest.mock('@actions/github', () => ({
  getOctokit: jest.fn(),
  context: {
    repo: {
      owner: 'test-owner',
      repo: 'test-repo',
    },
  },
}));

describe('nightly-stale-branch-echo-cleaner', () => {
  let listBranchesMock;
  let getCommitMock;
  let deleteRefMock;
  let createIssueMock;

  beforeEach(() => {
    jest.clearAllMocks();

    // Mock rationale: We are testing the action's logic, not the GitHub API itself.
    // Mocking @actions/core and @actions/github allows us to control inputs,
    // simulate API responses, and verify outputs and side effects (like logging or API calls)
    // without making actual network requests or requiring a real GitHub environment.

    // Mock core inputs
    core.getInput.mockImplementation((name) => {
      switch (name) {
        case 'stale_days': return '30';
        case 'dry_run': return 'true';
        case 'exclude_branches': return 'main,develop';
        case 'action_type': return 'log';
        case 'issue_labels': return 'stale,cleanup';
        case 'github_token': return 'mock-token';
        default: return '';
      }
    });
    core.getBooleanInput.mockImplementation((name) => {
      if (name === 'dry_run') return true;
      return false;
    });
    core.info.mockImplementation(jest.fn());
    core.debug.mockImplementation(jest.fn());
    core.setFailed.mockImplementation(jest.fn());
    core.setOutput.mockImplementation(jest.fn());

    // Mock Octokit API calls
    listBranchesMock = jest.fn();
    getCommitMock = jest.fn();
    deleteRefMock = jest.fn();
    createIssueMock = jest.fn();

    github.getOctokit.mockReturnValue({
      rest: {
        repos: {
          listBranches: listBranchesMock,
          getCommit: getCommitMock,
        },
        git: {
          deleteRef: deleteRefMock,
        },
        issues: {
          create: createIssueMock,
        },
      },
    });
  });

  test('should identify stale branches in dry run mode (log action)', async () => {
    const now = new Date();
    const thirtyOneDaysAgo = new Date(now.getTime() - (31 * 24 * 60 * 60 * 1000)).toISOString();
    const twentyDaysAgo = new Date(now.getTime() - (20 * 24 * 60 * 60 * 1000)).toISOString();

    listBranchesMock.mockResolvedValue({
      data: [
        { name: 'main', commit: { sha: 'sha1' } },
        { name: 'feature-stale', commit: { sha: 'sha2' } },
        { name: 'feature-fresh', commit: { sha: 'sha3' } },
        { name: 'develop', commit: { sha: 'sha4' } },
      ],
    });

    getCommitMock.mockImplementation((params) => {
      if (params.ref === 'sha1') return Promise.resolve({ data: { commit: { author: { date: twentyDaysAgo } } } });
      if (params.ref === 'sha2') return Promise.resolve({ data: { commit: { author: { date: thirtyOneDaysAgo } } } });
      if (params.ref === 'sha3') return Promise.resolve({ data: { commit: { author: { date: twentyDaysAgo } } } });
      if (params.ref === 'sha4') return Promise.resolve({ data: { commit: { author: { date: twentyDaysAgo } } } });
      return Promise.resolve({ data: { commit: { author: { date: twentyDaysAgo } } } });
    });

    await run();

    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Found stale branch: feature-stale (last commit 31 days ago)'));
    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Dry run enabled. Would have performed action \'log\' for branch feature-stale.'));
    expect(core.setOutput).toHaveBeenCalledWith('stale_branches_found', JSON.stringify(['feature-stale']));
    expect(core.setOutput).toHaveBeenCalledWith('branches_processed', 4);
    expect(deleteRefMock).not.toHaveBeenCalled();
    expect(createIssueMock).not.toHaveBeenCalled();
  });

  test('should delete stale branches when dry_run is false and action_type is delete', async () => {
    core.getInput.mockImplementation((name) => {
      switch (name) {
        case 'stale_days': return '10';
        case 'dry_run': return 'false'; // Important for this test
        case 'exclude_branches': return 'main';
        case 'action_type': return 'delete'; // Important for this test
        case 'github_token': return 'mock-token';
        default: return '';
      }
    });
    core.getBooleanInput.mockReturnValue(false); // dry_run is false

    const now = new Date();
    const elevenDaysAgo = new Date(now.getTime() - (11 * 24 * 60 * 60 * 1000)).toISOString();
    const fiveDaysAgo = new Date(now.getTime() - (5 * 24 * 60 * 60 * 1000)).toISOString();

    listBranchesMock.mockResolvedValue({
      data: [
        { name: 'main', commit: { sha: 'sha1' } },
        { name: 'stale-branch-to-delete', commit: { sha: 'sha2' } },
        { name: 'fresh-branch', commit: { sha: 'sha3' } },
      ],
    });

    getCommitMock.mockImplementation((params) => {
      if (params.ref === 'sha1') return Promise.resolve({ data: { commit: { author: { date: fiveDaysAgo } } } });
      if (params.ref === 'sha2') return Promise.resolve({ data: { commit: { author: { date: elevenDaysAgo } } } });
      if (params.ref === 'sha3') return Promise.resolve({ data: { commit: { author: { date: fiveDaysAgo } } } });
      return Promise.resolve({ data: { commit: { author: { date: fiveDaysAgo } } } });
    });

    await run();

    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Found stale branch: stale-branch-to-delete (last commit 11 days ago)'));
    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Deleting branch: stale-branch-to-delete'));
    expect(deleteRefMock).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      ref: 'heads/stale-branch-to-delete',
    });
    expect(core.setOutput).toHaveBeenCalledWith('stale_branches_found', JSON.stringify(['stale-branch-to-delete']));
    expect(core.setOutput).toHaveBeenCalledWith('branches_processed', 3);
    expect(createIssueMock).not.toHaveBeenCalled();
  });

  test('should create an issue for stale branches when dry_run is false and action_type is issue', async () => {
    core.getInput.mockImplementation((name) => {
      switch (name) {
        case 'stale_days': return '5';
        case 'dry_run': return 'false';
        case 'exclude_branches': return '';
        case 'action_type': return 'issue';
        case 'issue_labels': return 'cleanup,stale-echo';
        case 'github_token': return 'mock-token';
        default: return '';
      }
    });
    core.getBooleanInput.mockReturnValue(false);

    const now = new Date();
    const sixDaysAgo = new Date(now.getTime() - (6 * 24 * 60 * 60 * 1000)).toISOString();

    listBranchesMock.mockResolvedValue({
      data: [
        { name: 'stale-branch-for-issue', commit: { sha: 'sha1' } },
      ],
    });

    getCommitMock.mockResolvedValue({ data: { commit: { author: { date: sixDaysAgo } } } });

    await run();

    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Found stale branch: stale-branch-for-issue (last commit 6 days ago)'));
    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Creating issue for branch: stale-branch-for-issue'));
    expect(createIssueMock).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      title: 'Stale Branch Detected: stale-branch-for-issue',
      body: 'The branch `stale-branch-for-issue` has not been updated in 6 days. Consider reviewing or deleting it.',
      labels: ['cleanup', 'stale-echo'],
    });
    expect(core.setOutput).toHaveBeenCalledWith('stale_branches_found', JSON.stringify(['stale-branch-for-issue']));
    expect(core.setOutput).toHaveBeenCalledWith('branches_processed', 1);
    expect(deleteRefMock).not.toHaveBeenCalled();
  });

  test('should handle API errors gracefully', async () => {
    listBranchesMock.mockRejectedValue(new Error('API rate limit exceeded'));

    await run();

    expect(core.setFailed).toHaveBeenCalledWith('API rate limit exceeded');
    expect(core.setOutput).not.toHaveBeenCalledWith('stale_branches_found', expect.any(String));
    expect(core.setOutput).not.toHaveBeenCalledWith('branches_processed', expect.any(Number));
  });

  test('should exclude specified branches and wildcard patterns', async () => {
    core.getInput.mockImplementation((name) => {
      switch (name) {
        case 'stale_days': return '1';
        case 'dry_run': return 'true';
        case 'exclude_branches': return 'main,feature-x,release/*';
        case 'action_type': return 'log';
        case 'github_token': return 'mock-token';
        default: return '';
      }
    });

    const now = new Date();
    const twoDaysAgo = new Date(now.getTime() - (2 * 24 * 60 * 60 * 1000)).toISOString();

    listBranchesMock.mockResolvedValue({
      data: [
        { name: 'main', commit: { sha: 'sha1' } },
        { name: 'feature-x', commit: { sha: 'sha2' } },
        { name: 'release/v1.0', commit: { sha: 'sha3' } },
        { name: 'stale-feature', commit: { sha: 'sha4' } },
      ],
    });

    getCommitMock.mockResolvedValue({ data: { commit: { author: { date: twoDaysAgo } } } });

    await run();

    expect(core.info).toHaveBeenCalledWith('Skipping excluded branch: main');
    expect(core.info).toHaveBeenCalledWith('Skipping excluded branch: feature-x');
    expect(core.info).toHaveBeenCalledWith('Skipping excluded branch: release/v1.0');
    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Found stale branch: stale-feature (last commit 2 days ago)'));
    expect(core.setOutput).toHaveBeenCalledWith('stale_branches_found', JSON.stringify(['stale-feature']));
    expect(core.setOutput).toHaveBeenCalledWith('branches_processed', 4);
  });
});
