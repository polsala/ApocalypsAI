const core = require('@actions/core');
const github = require('@actions/github');
const { when } = require('jest-when'); // For more flexible mocking

// Mock the GitHub Actions toolkit
jest.mock('@actions/core');
jest.mock('@actions/github');

const run = require('../src/main'); // The action's main logic

describe('Nightly Branch Graveyard Keeper', () => {
  const mockToken = 'test-token';
  const mockOwner = 'test-owner';
  const mockRepo = 'test-repo';

  // Mock Date for deterministic tests
  const MOCK_CURRENT_DATE = new Date('2023-10-26T10:00:00Z');
  const RealDate = Date;

  beforeAll(() => {
    global.Date = jest.fn(() => MOCK_CURRENT_DATE);
    global.Date.toISOString = RealDate.toISOString; // Keep original for specific calls if needed
    global.Date.parse = RealDate.parse;
    global.Date.now = RealDate.now;
  });

  afterAll(() => {
    global.Date = RealDate; // Restore original Date
  });

  beforeEach(() => {
    jest.clearAllMocks();

    // Mock core inputs
    when(core.getInput)
      .calledWith('repo-token', expect.anything())
      .thenReturn(mockToken);
    when(core.getInput)
      .calledWith('stale-days', expect.anything())
      .thenReturn('90');
    when(core.getInput)
      .calledWith('ignore-branches', expect.anything())
      .thenReturn('main,master');

    // Mock github context
    github.context = {
      repo: {
        owner: mockOwner,
        repo: mockRepo,
      },
    };

    // Mock octokit
    github.getOctokit.mockReturnValue({
      rest: {
        repos: {
          listBranches: jest.fn(),
          getCommit: jest.fn(),
        },
      },
      paginate: jest.fn((fn, params) => fn(params)), // Mock rationale: Simulating GitHub API pagination by directly calling the function with params for simplicity in unit tests.
    });
  });

  it('should identify stale branches and output a report', async () => {
    // Mock rationale: Simulating GitHub API responses for branches and their last commits.
    // This allows deterministic testing without actual network calls.
    const mockBranches = [
      { name: 'main', commit: { sha: 'sha-main' } },
      { name: 'feature-new', commit: { sha: 'sha-new' } },
      { name: 'feature-stale-1', commit: { sha: 'sha-stale-1' } },
      { name: 'feature-stale-2', commit: { sha: 'sha-stale-2' } },
      { name: 'master', commit: { sha: 'sha-master' } }, // Should be ignored
    ];

    const mockCommits = {
      'sha-main': { commit: { author: { date: '2023-10-20T10:00:00Z' } } }, // 6 days old
      'sha-new': { commit: { author: { date: '2023-09-01T10:00:00Z' } } }, // ~55 days old
      'sha-stale-1': { commit: { author: { date: '2023-07-01T10:00:00Z' } } }, // ~117 days old (stale)
      'sha-stale-2': { commit: { author: { date: '2023-05-01T10:00:00Z' } } }, // ~178 days old (stale)
      'sha-master': { commit: { author: { date: '2023-08-01T10:00:00Z' } } }, // ~86 days old (ignored)
    };

    github.getOctokit().rest.repos.listBranches.mockResolvedValue(mockBranches);
    github.getOctokit().rest.repos.getCommit.mockImplementation(({ ref }) => {
      if (mockCommits[ref]) {
        return Promise.resolve({ data: mockCommits[ref] });
      }
      return Promise.reject(new Error(`Commit not found for ref: ${ref}`));
    });

    await run();

    expect(core.setOutput).toHaveBeenCalledWith('stale-branches-count', 2);
    const reportOutput = JSON.parse(core.setOutput.mock.calls[0][1]);
    expect(reportOutput).toHaveLength(2);
    expect(reportOutput[0].branchName).toBe('feature-stale-1');
    expect(reportOutput[0].lastCommitDate).toBe('2023-07-01');
    expect(reportOutput[0].ageDays).toBe(117); // 2023-10-26 - 2023-07-01 = 117 days
    expect(reportOutput[0].whimsicalSuggestion).toBeDefined();

    expect(reportOutput[1].branchName).toBe('feature-stale-2');
    expect(reportOutput[1].lastCommitDate).toBe('2023-05-01');
    expect(reportOutput[1].ageDays).toBe(178); // 2023-10-26 - 2023-05-01 = 178 days
    expect(reportOutput[1].whimsicalSuggestion).toBeDefined();
    expect(reportOutput[1].whimsicalSuggestion).not.toEqual(reportOutput[0].whimsicalSuggestion); // Ensure suggestions cycle

    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Stale branch found: feature-stale-1'));
    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Stale branch found: feature-stale-2'));
    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Branch Graveyard Report'));
    expect(core.info).not.toHaveBeenCalledWith(expect.stringContaining('No stale branches found!'));
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  it('should handle no stale branches gracefully', async () => {
    // Mock rationale: Simulating a repository with no stale branches.
    const mockBranches = [
      { name: 'main', commit: { sha: 'sha-main' } },
      { name: 'feature-fresh', commit: { sha: 'sha-fresh' } },
    ];

    const mockCommits = {
      'sha-main': { commit: { author: { date: '2023-10-20T10:00:00Z' } } }, // 6 days old
      'sha-fresh': { commit: { author: { date: '2023-09-15T10:00:00Z' } } }, // ~41 days old
    };

    github.getOctokit().rest.repos.listBranches.mockResolvedValue(mockBranches);
    github.getOctokit().rest.repos.getCommit.mockImplementation(({ ref }) => {
      if (mockCommits[ref]) {
        return Promise.resolve({ data: mockCommits[ref] });
      }
      return Promise.reject(new Error(`Commit not found for ref: ${ref}`));
    });

    await run();

    expect(core.setOutput).toHaveBeenCalledWith('stale-branches-count', 0);
    expect(core.setOutput).toHaveBeenCalledWith('stale-branches-report', '[]\n');
    expect(core.info).toHaveBeenCalledWith('🎉 No stale branches found! Your repository is spick and span!');
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  it('should respect stale-days input', async () => {
    // Mock rationale: Testing the `stale-days` input parameter.
    when(core.getInput)
      .calledWith('stale-days', expect.anything())
      .thenReturn('30'); // Set stale threshold to 30 days

    const mockBranches = [
      { name: 'feature-stale-30', commit: { sha: 'sha-stale-30' } },
    ];

    const mockCommits = {
      'sha-stale-30': { commit: { author: { date: '2023-09-01T10:00:00Z' } } }, // ~55 days old (should be stale with 30 days threshold)
    };

    github.getOctokit().rest.repos.listBranches.mockResolvedValue(mockBranches);
    github.getOctokit().rest.repos.getCommit.mockImplementation(({ ref }) => {
      if (mockCommits[ref]) {
        return Promise.resolve({ data: mockCommits[ref] });
      }
      return Promise.reject(new Error(`Commit not found for ref: ${ref}`));
    });

    await run();

    expect(core.setOutput).toHaveBeenCalledWith('stale-branches-count', 1);
    const reportOutput = JSON.parse(core.setOutput.mock.calls[0][1]);
    expect(reportOutput[0].branchName).toBe('feature-stale-30');
    expect(reportOutput[0].ageDays).toBe(55);
    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Scanning for branches older than 30 days'));
  });

  it('should respect ignore-branches input', async () => {
    // Mock rationale: Testing the `ignore-branches` input parameter.
    when(core.getInput)
      .calledWith('ignore-branches', expect.anything())
      .thenReturn('main,feature-ignored');

    const mockBranches = [
      { name: 'main', commit: { sha: 'sha-main' } },
      { name: 'feature-ignored', commit: { sha: 'sha-ignored' } },
      { name: 'feature-stale', commit: { sha: 'sha-stale' } },
    ];

    const mockCommits = {
      'sha-main': { commit: { author: { date: '2023-01-01T10:00:00Z' } } },
      'sha-ignored': { commit: { author: { date: '2023-01-01T10:00:00Z' } } },
      'sha-stale': { commit: { author: { date: '2023-07-01T10:00:00Z' } } }, // Stale
    };

    github.getOctokit().rest.repos.listBranches.mockResolvedValue(mockBranches);
    github.getOctokit().rest.repos.getCommit.mockImplementation(({ ref }) => {
      if (mockCommits[ref]) {
        return Promise.resolve({ data: mockCommits[ref] });
      }
      return Promise.reject(new Error(`Commit not found for ref: ${ref}`));
    });

    await run();

    expect(core.setOutput).toHaveBeenCalledWith('stale-branches-count', 1);
    const reportOutput = JSON.parse(core.setOutput.mock.calls[0][1]);
    expect(reportOutput).toHaveLength(1);
    expect(reportOutput[0].branchName).toBe('feature-stale');
    expect(core.debug).toHaveBeenCalledWith('Ignoring branch: main');
    expect(core.debug).toHaveBeenCalledWith('Ignoring branch: feature-ignored');
  });

  it('should call setFailed on API error', async () => {
    // Mock rationale: Simulating a GitHub API error during branch listing.
    github.getOctokit().rest.repos.listBranches.mockRejectedValue(new Error('API rate limit exceeded'));

    await run();

    expect(core.setFailed).toHaveBeenCalledWith(expect.stringContaining('API rate limit exceeded'));
    expect(core.setOutput).not.toHaveBeenCalled();
  });

  it('should warn and continue if commit details cannot be fetched for a branch', async () => {
    // Mock rationale: Simulating a scenario where commit details for a specific branch are unavailable,
    // but the action should continue processing other branches.
    const mockBranches = [
      { name: 'feature-good', commit: { sha: 'sha-good' } },
      { name: 'feature-bad', commit: { sha: 'sha-bad' } }, // This one will fail
      { name: 'feature-another-good', commit: { sha: 'sha-another-good' } },
    ];

    const mockCommits = {
      'sha-good': { commit: { author: { date: '2023-07-01T10:00:00Z' } } }, // Stale
      'sha-another-good': { commit: { author: { date: '2023-06-01T10:00:00Z' } } }, // Stale
    };

    github.getOctokit().rest.repos.listBranches.mockResolvedValue(mockBranches);
    github.getOctokit().rest.repos.getCommit.mockImplementation(({ ref }) => {
      if (mockCommits[ref]) {
        return Promise.resolve({ data: mockCommits[ref] });
      }
      return Promise.reject(new Error(`Commit not found for ref: ${ref}`));
    });

    await run();

    expect(core.warning).toHaveBeenCalledWith(expect.stringContaining('Could not get commit details for branch feature-bad'));
    expect(core.setOutput).toHaveBeenCalledWith('stale-branches-count', 2);
    const reportOutput = JSON.parse(core.setOutput.mock.calls[0][1]);
    expect(reportOutput).toHaveLength(2);
    expect(reportOutput[0].branchName).toBe('feature-good');
    expect(reportOutput[1].branchName).toBe('feature-another-good');
    expect(core.setFailed).not.toHaveBeenCalled();
  });
});
