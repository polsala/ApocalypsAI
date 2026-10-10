const core = require('@actions/core');
const github = require('@actions/github');
const { minimatch } = require('minimatch');

// Mock the main action file
const run = require('../src/main');

// Mock @actions/core
jest.mock('@actions/core', () => ({
  getInput: jest.fn(),
  setOutput: jest.fn(),
  setFailed: jest.fn(),
  info: jest.fn(),
  debug: jest.fn(),
}));

// Mock @actions/github
const mockGetOctokit = jest.fn();
const mockListBranches = jest.fn();
const mockGetCommit = jest.fn();

jest.mock('@actions/github', () => ({
  getOctokit: mockGetOctokit,
  context: {
    repo: {
      owner: 'test-owner',
      repo: 'test-repo',
    },
  },
}));

describe('Nightly Branch Archivist', () => {
  const OLD_DATE_91_DAYS_AGO = new Date(Date.now() - (91 * 24 * 60 * 60 * 1000)).toISOString();
  const OLD_DATE_180_DAYS_AGO = new Date(Date.now() - (180 * 24 * 60 * 60 * 1000)).toISOString();
  const RECENT_DATE = new Date(Date.now() - (10 * 24 * 60 * 60 * 1000)).toISOString(); // 10 days ago

  beforeEach(() => {
    jest.clearAllMocks();

    // Mock rationale: We need to simulate GitHub API responses for branches and commits
    // without making actual network calls. This ensures tests are fast, deterministic,
    // and can run offline. We control the exact state of the repository for testing
    // different scenarios (stale, fresh, protected branches).

    // Mock Octokit setup
    mockGetOctokit.mockReturnValue({
      rest: {
        repos: {
          listBranches: mockListBranches,
        },
        git: {
          getCommit: mockGetCommit,
        },
      },
    });

    // Mock core.getInput defaults
    core.getInput.mockImplementation((name) => {
      switch (name) {
        case 'stale-days': return '90';
        case 'protected-branches': return 'main,master,develop';
        case 'repo-token': return 'mock-token';
        default: return '';
      }
    });

    // Mock github.context.repo
    github.context.repo = {
      owner: 'test-owner',
      repo: 'test-repo',
    };
  });

  test('should identify stale branches correctly', async () => {
    mockListBranches.mockResolvedValueOnce({
      data: [
        { name: 'main', commit: { sha: 'sha1' } },
        { name: 'feature-new', commit: { sha: 'sha2' } },
        { name: 'old-feature', commit: { sha: 'sha3' } },
        { name: 'another-stale', commit: { sha: 'sha4' } },
      ],
    });

    mockGetCommit.mockImplementation(async ({ commit_sha }) => {
      if (commit_sha === 'sha1') return { data: { author: { date: RECENT_DATE } } }; // main, fresh
      if (commit_sha === 'sha2') return { data: { author: { date: RECENT_DATE } } }; // feature-new, fresh
      if (commit_sha === 'sha3') return { data: { author: { date: OLD_DATE_91_DAYS_AGO } } }; // old-feature, stale
      if (commit_sha === 'sha4') return { data: { author: { date: OLD_DATE_180_DAYS_AGO } } }; // another-stale, stale
      return { data: { author: { date: RECENT_DATE } } };
    });

    await run();

    expect(core.setOutput).toHaveBeenCalledWith('stale-branches-count', 2);
    expect(core.setOutput).toHaveBeenCalledWith('stale-branches-json', JSON.stringify(['old-feature', 'another-stale']));
    expect(core.setOutput).toHaveBeenCalledWith('stale-branches-message', expect.stringContaining('2 branches that seem to have overstayed their welcome'));
    expect(core.setOutput).toHaveBeenCalledWith('stale-branches-message', expect.stringContaining('- old-feature'));
    expect(core.setOutput).toHaveBeenCalledWith('stale-branches-message', expect.stringContaining('- another-stale'));
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('should ignore protected branches', async () => {
    core.getInput.mockImplementation((name) => {
      if (name === 'protected-branches') return 'main,develop';
      if (name === 'stale-days') return '90';
      if (name === 'repo-token') return 'mock-token';
      return '';
    });

    mockListBranches.mockResolvedValueOnce({
      data: [
        { name: 'main', commit: { sha: 'sha1' } }, // Protected, old
        { name: 'develop', commit: { sha: 'sha2' } }, // Protected, old
        { name: 'stale-branch', commit: { sha: 'sha3' } }, // Not protected, old
      ],
    });

    mockGetCommit.mockImplementation(async ({ commit_sha }) => {
      if (commit_sha === 'sha1') return { data: { author: { date: OLD_DATE_180_DAYS_AGO } } };
      if (commit_sha === 'sha2') return { data: { author: { date: OLD_DATE_180_DAYS_AGO } } };
      if (commit_sha === 'sha3') return { data: { author: { date: OLD_DATE_180_DAYS_AGO } } };
      return { data: { author: { date: RECENT_DATE } } };
    });

    await run();

    expect(core.setOutput).toHaveBeenCalledWith('stale-branches-count', 1);
    expect(core.setOutput).toHaveBeenCalledWith('stale-branches-json', JSON.stringify(['stale-branch']));
    expect(core.setOutput).toHaveBeenCalledWith('stale-branches-message', expect.stringContaining('1 branches that seem to have overstayed their welcome'));
    expect(core.setOutput).toHaveBeenCalledWith('stale-branches-message', expect.stringContaining('- stale-branch'));
    expect(core.setOutput).not.toHaveBeenCalledWith('stale-branches-message', expect.stringContaining('- main'));
    expect(core.setOutput).not.toHaveBeenCalledWith('stale-branches-message', expect.stringContaining('- develop'));
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('should handle no stale branches', async () => {
    mockListBranches.mockResolvedValueOnce({
      data: [
        { name: 'main', commit: { sha: 'sha1' } },
        { name: 'feature-x', commit: { sha: 'sha2' } },
      ],
    });

    mockGetCommit.mockImplementation(async ({ commit_sha }) => {
      if (commit_sha === 'sha1') return { data: { author: { date: RECENT_DATE } } };
      if (commit_sha === 'sha2') return { data: { author: { date: RECENT_DATE } } };
      return { data: { author: { date: RECENT_DATE } } };
    });

    await run();

    expect(core.setOutput).toHaveBeenCalledWith('stale-branches-count', 0);
    expect(core.setOutput).toHaveBeenCalledWith('stale-branches-json', JSON.stringify([]));
    expect(core.setOutput).toHaveBeenCalledWith('stale-branches-message', expect.stringContaining('All branches are sparkling clean and actively maintained'));
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('should handle API errors', async () => {
    mockListBranches.mockRejectedValueOnce(new Error('API rate limit exceeded'));

    await run();

    expect(core.setFailed).toHaveBeenCalledWith('API rate limit exceeded');
    expect(core.setOutput).not.toHaveBeenCalledWith('stale-branches-count', expect.any(Number));
  });

  test('should handle protected branches with glob patterns', async () => {
    core.getInput.mockImplementation((name) => {
      if (name === 'protected-branches') return 'main,feature/*';
      if (name === 'stale-days') return '90';
      if (name === 'repo-token') return 'mock-token';
      return '';
    });

    mockListBranches.mockResolvedValueOnce({
      data: [
        { name: 'main', commit: { sha: 'sha1' } }, // Protected by exact match
        { name: 'feature/login', commit: { sha: 'sha2' } }, // Protected by glob
        { name: 'feature/signup', commit: { sha: 'sha3' } }, // Protected by glob
        { name: 'bugfix/old-bug', commit: { sha: 'sha4' } }, // Not protected, stale
      ],
    });

    mockGetCommit.mockImplementation(async ({ commit_sha }) => {
      if (commit_sha === 'sha1') return { data: { author: { date: OLD_DATE_180_DAYS_AGO } } };
      if (commit_sha === 'sha2') return { data: { author: { date: OLD_DATE_180_DAYS_AGO } } };
      if (commit_sha === 'sha3') return { data: { author: { date: OLD_DATE_180_DAYS_AGO } } };
      if (commit_sha === 'sha4') return { data: { author: { date: OLD_DATE_180_DAYS_AGO } } };
      return { data: { author: { date: RECENT_DATE } } };
    });

    await run();

    expect(core.setOutput).toHaveBeenCalledWith('stale-branches-count', 1);
    expect(core.setOutput).toHaveBeenCalledWith('stale-branches-json', JSON.stringify(['bugfix/old-bug']));
    expect(core.setOutput).toHaveBeenCalledWith('stale-branches-message', expect.stringContaining('1 branches that seem to have overstayed their welcome'));
    expect(core.setOutput).toHaveBeenCalledWith('stale-branches-message', expect.stringContaining('- bugfix/old-bug'));
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('should use custom stale-days input', async () => {
    core.getInput.mockImplementation((name) => {
      if (name === 'stale-days') return '30'; // Custom stale days
      if (name === 'protected-branches') return '';
      if (name === 'repo-token') return 'mock-token';
      return '';
    });

    const OLD_DATE_31_DAYS_AGO = new Date(Date.now() - (31 * 24 * 60 * 60 * 1000)).toISOString();
    const RECENT_DATE_20_DAYS_AGO = new Date(Date.now() - (20 * 24 * 60 * 60 * 1000)).toISOString();

    mockListBranches.mockResolvedValueOnce({
      data: [
        { name: 'stale-31-days', commit: { sha: 'sha1' } },
        { name: 'fresh-20-days', commit: { sha: 'sha2' } },
      ],
    });

    mockGetCommit.mockImplementation(async ({ commit_sha }) => {
      if (commit_sha === 'sha1') return { data: { author: { date: OLD_DATE_31_DAYS_AGO } } };
      if (commit_sha === 'sha2') return { data: { author: { date: RECENT_DATE_20_DAYS_AGO } } };
      return { data: { author: { date: RECENT_DATE } } };
    });

    await run();

    expect(core.setOutput).toHaveBeenCalledWith('stale-branches-count', 1);
    expect(core.setOutput).toHaveBeenCalledWith('stale-branches-json', JSON.stringify(['stale-31-days']));
    expect(core.setOutput).toHaveBeenCalledWith('stale-branches-message', expect.stringContaining('1 branches that seem to have overstayed their welcome'));
    expect(core.setOutput).toHaveBeenCalledWith('stale-branches-message', expect.stringContaining('- stale-31-days'));
    expect(core.setFailed).not.toHaveBeenCalled();
  });
});
