const core = require('@actions/core');
const github = require('@actions/github');

// Mock the GitHub Actions toolkit
jest.mock('@actions/core');
jest.mock('@actions/github');

// Mock the Octokit instance and its methods
const mockCreateComment = jest.fn();
const mockCreateIssue = jest.fn();
const mockListBranches = jest.fn();
const mockGetCommit = jest.fn();
const mockListPulls = jest.fn();

const mockOctokit = {
  rest: {
    repos: {
      listBranches: mockListBranches,
      getCommit: mockGetCommit,
    },
    pulls: {
      list: mockListPulls,
    },
    issues: {
      createComment: mockCreateComment,
      create: mockCreateIssue,
    },
  },
};

github.getOctokit.mockReturnValue(mockOctokit);

// Mock github.context
github.context = {
  repo: {
    owner: 'test-owner',
    repo: 'test-repo',
  },
};

// Import the action to be tested
const run = require('../src/index');

describe('Nightly Branch Rot Monitor', () => {
  const originalDate = Date; // Store original Date object
  let mockDate;

  beforeAll(() => {
    // Mock Date to control current time for staleness calculation
    mockDate = new Date('2023-10-26T10:00:00Z'); // Mock current date
    global.Date = jest.fn(() => mockDate);
    global.Date.toISOString = originalDate.toISOString; // Keep original methods
    global.Date.now = originalDate.now;
    global.Date.parse = originalDate.parse;
    global.Date.UTC = originalDate.UTC;
    global.Date.prototype.setDate = originalDate.prototype.setDate; // Mock rationale: Control current date for deterministic staleness checks.
  });

  afterAll(() => {
    global.Date = originalDate; // Restore original Date object
  });

  beforeEach(() => {
    jest.clearAllMocks();
    core.getInput.mockImplementation((name) => {
      if (name === 'stale-days') return '30';
      if (name === 'repo-token') return 'mock-token';
      return '';
    });
    core.info.mockImplementation(() => {}); // Suppress info logs during tests
  });

  test('should find no stale branches and set output to 0', async () => {
    mockListBranches.mockResolvedValue({
      data: [
        { name: 'main' },
        { name: 'feature-active', commit: { sha: 'abc' } },
      ],
    });
    mockGetCommit.mockResolvedValue({
      data: {
        commit: { author: { date: '2023-10-01T10:00:00Z' } }, // Not stale (25 days old relative to mockDate)
        author: { login: 'test-user' },
      },
    });
    mockListPulls.mockResolvedValue({ data: [] }); // Mock rationale: Simulate no existing PRs.

    await run();

    expect(core.setOutput).toHaveBeenCalledWith('stale-branches-count', 0);
    expect(mockCreateComment).not.toHaveBeenCalled();
    expect(mockCreateIssue).not.toHaveBeenCalled();
  });

  test('should find a stale branch with an open PR and comment on it', async () => {
    mockListBranches.mockResolvedValue({
      data: [
        { name: 'main' },
        { name: 'stale-feature', commit: { sha: 'def' } },
      ],
    });
    mockGetCommit.mockResolvedValue({
      data: {
        commit: { author: { date: '2023-09-01T10:00:00Z' } }, // Stale (55 days old relative to mockDate)
        author: { login: 'stale-user' },
      },
    });
    mockListPulls.mockResolvedValue({
      data: [{ number: 123, head: { ref: 'stale-feature' } }], // Mock rationale: Simulate an existing PR for the stale branch.
    });

    await run();

    expect(mockCreateComment).toHaveBeenCalledTimes(1);
    expect(mockCreateComment).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      issue_number: 123,
      body: expect.stringContaining('Branch Rot Monitor Alert!'),
    });
    expect(mockCreateIssue).not.toHaveBeenCalled();
    expect(core.setOutput).toHaveBeenCalledWith('stale-branches-count', 1);
  });

  test('should find a stale branch without an open PR and open a new issue', async () => {
    mockListBranches.mockResolvedValue({
      data: [
        { name: 'main' },
        { name: 'another-stale', commit: { sha: 'ghi' } },
      ],
    });
    mockGetCommit.mockResolvedValue({
      data: {
        commit: { author: { date: '2023-08-15T10:00:00Z' } }, // Very stale relative to mockDate
        author: { login: 'another-stale-user' },
      },
    });
    mockListPulls.mockResolvedValue({ data: [] }); // Mock rationale: Simulate no existing PR for the stale branch.

    await run();

    expect(mockCreateIssue).toHaveBeenCalledTimes(1);
    expect(mockCreateIssue).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      title: '[Stale Branch Alert] another-stale needs attention!',
      body: expect.stringContaining('Branch Rot Monitor Alert!'),
      assignees: ['another-stale-user'],
    });
    expect(mockCreateComment).not.toHaveBeenCalled();
    expect(core.setOutput).toHaveBeenCalledWith('stale-branches-count', 1);
  });

  test('should handle multiple stale branches correctly', async () => {
    mockListBranches.mockResolvedValue({
      data: [
        { name: 'main' },
        { name: 'stale-pr', commit: { sha: 'jkl' } },
        { name: 'stale-issue', commit: { sha: 'mno' } },
      ],
    });

    // Mock getCommit for each branch
    mockGetCommit
      .mockResolvedValueOnce({ // stale-pr
        data: {
          commit: { author: { date: '2023-09-05T10:00:00Z' } }, // Stale
          author: { login: 'user-pr' },
        },
      })
      .mockResolvedValueOnce({ // stale-issue
        data: {
          commit: { author: { date: '2023-08-20T10:00:00Z' } }, // Stale
          author: { login: 'user-issue' },
        },
      });

    // Mock listPulls for each branch
    mockListPulls
      .mockResolvedValueOnce({ // stale-pr has a PR
        data: [{ number: 456, head: { ref: 'stale-pr' } }], // Mock rationale: Simulate an existing PR for 'stale-pr'.
      })
      .mockResolvedValueOnce({ // stale-issue has no PR
        data: [], // Mock rationale: Simulate no existing PR for 'stale-issue'.
      });

    await run();

    expect(mockCreateComment).toHaveBeenCalledTimes(1);
    expect(mockCreateComment).toHaveBeenCalledWith(expect.objectContaining({ issue_number: 456 }));
    expect(mockCreateIssue).toHaveBeenCalledTimes(1);
    expect(mockCreateIssue).toHaveBeenCalledWith(expect.objectContaining({ title: expect.stringContaining('stale-issue') }));
    expect(core.setOutput).toHaveBeenCalledWith('stale-branches-count', 2);
  });

  test('should set failed status on error', async () => {
    mockListBranches.mockRejectedValue(new Error('API Error')); // Mock rationale: Simulate a GitHub API error during branch listing.

    await run();

    expect(core.setFailed).toHaveBeenCalledWith('API Error');
    expect(core.setOutput).not.toHaveBeenCalled();
  });

  test('should skip protected branches', async () => {
    mockListBranches.mockResolvedValue({
      data: [
        { name: 'main' },
        { name: 'master' },
        { name: 'develop' },
        { name: 'feature-stale', commit: { sha: 'abc' } },
      ],
    });
    mockGetCommit.mockResolvedValue({
      data: {
        commit: { author: { date: '2023-09-01T10:00:00Z' } }, // Stale
        author: { login: 'test-user' },
      },
    });
    mockListPulls.mockResolvedValue({ data: [] }); // Mock rationale: Simulate no existing PRs.

    await run();

    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Skipping protected branch: main'));
    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Skipping protected branch: master'));
    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Skipping protected branch: develop'));
    expect(core.setOutput).toHaveBeenCalledWith('stale-branches-count', 1);
    expect(mockCreateIssue).toHaveBeenCalledTimes(1);
    expect(mockCreateIssue).toHaveBeenCalledWith(expect.objectContaining({ title: expect.stringContaining('feature-stale') }));
  });
});
