const core = require('@actions/core');
const github = require('@actions/github');
const { run } = require('../src/main');

// Mock the GitHub Actions toolkit
jest.mock('@actions/core');
jest.mock('@actions/github');

describe('Nightly Branch Bard', () => {
  let listBranchesMock;
  let getCommitMock;
  let createCommentMock;
  let addRawSummaryMock;

  beforeEach(() => {
    jest.clearAllMocks();

    // Mock github.context
    github.context = {
      repo: {
        owner: 'test-owner',
        repo: 'test-repo',
      },
    };

    // Mock octokit.paginate
    listBranchesMock = jest.fn();
    github.getOctokit.mockReturnValue({
      paginate: jest.fn((apiCall, params) => {
        if (apiCall === github.getOctokit().rest.repos.listBranches) {
          return listBranchesMock(params);
        }
        return [];
      }),
      rest: {
        repos: {
          listBranches: jest.fn(), // This is just for the paginate mock to reference
          getCommit: jest.fn(),
        },
        issues: {
          createComment: jest.fn(),
        },
      },
    });

    getCommitMock = github.getOctokit().rest.repos.getCommit;
    createCommentMock = github.getOctokit().rest.issues.createComment;
    addRawSummaryMock = jest.fn();
    core.summary = { addRaw: addRawSummaryMock }; // Mock core.summary.addRaw

    // Mock core inputs
    core.getInput.mockImplementation((name) => {
      switch (name) {
        case 'repo-token': return 'mock-token';
        case 'stale-days': return '60';
        case 'ignore-branches': return 'main,master,develop';
        case 'output-type': return 'summary';
        case 'issue-number': return '';
        default: return '';
      }
    });
  });

  // Mock rationale: We need to control the GitHub API responses to simulate different repository states
  // (e.g., branches with various last commit dates, ignored branches) without making actual network calls.
  // This ensures tests are deterministic, fast, and don't require a live GitHub repository.

  test('should identify stale branches and output to summary', async () => {
    const now = new Date();
    const sixtyDaysAgo = new Date(now.setDate(now.getDate() - 60));
    const seventyDaysAgo = new Date(now.setDate(now.getDate() - 10)); // 70 days ago from original 'now'
    const thirtyDaysAgo = new Date(now.setDate(now.getDate() + 40)); // 30 days ago from original 'now'

    listBranchesMock.mockResolvedValueOnce([
      { name: 'main', commit: { sha: 'sha1' } },
      { name: 'feature/stale-old', commit: { sha: 'sha2' } },
      { name: 'bugfix/recent-fix', commit: { sha: 'sha3' } },
      { name: 'develop', commit: { sha: 'sha4' } }, // Should be ignored
    ]);

    getCommitMock.mockImplementation(async ({ ref }) => {
      if (ref === 'sha1') return { data: { commit: { author: { date: thirtyDaysAgo.toISOString() } } } };
      if (ref === 'sha2') return { data: { commit: { author: { date: seventyDaysAgo.toISOString() } } } };
      if (ref === 'sha3') return { data: { commit: { author: { date: thirtyDaysAgo.toISOString() } } } };
      if (ref === 'sha4') return { data: { commit: { author: { date: seventyDaysAgo.toISOString() } } } }; // Ignored anyway
      return { data: { commit: { author: { date: now.toISOString() } } } };
    });

    await run();

    expect(core.getInput).toHaveBeenCalledWith('repo-token', { required: true });
    expect(core.getInput).toHaveBeenCalledWith('stale-days');
    expect(core.getInput).toHaveBeenCalledWith('ignore-branches');
    expect(core.getInput).toHaveBeenCalledWith('output-type');
    expect(core.getInput).toHaveBeenCalledWith('issue-number');

    expect(listBranchesMock).toHaveBeenCalledWith({ owner: 'test-owner', repo: 'test-repo', per_page: 100 });
    expect(getCommitMock).toHaveBeenCalledTimes(3); // main, feature/stale-old, bugfix/recent-fix (develop is ignored before commit check)

    expect(core.setOutput).toHaveBeenCalledWith(
      'stale-branches-json',
      expect.stringContaining('feature/stale-old')
    );
    expect(core.setOutput).toHaveBeenCalledWith(
      'summary-output',
      expect.stringContaining('### 📜 Nightly Branch Bard\'s Archival Suggestions 📜')
    );
    expect(core.setOutput).toHaveBeenCalledWith(
      'summary-output',
      expect.stringContaining('feature/stale-old')
    );
    expect(addRawSummaryMock).toHaveBeenCalledWith(expect.stringContaining('feature/stale-old'));
    expect(createCommentMock).not.toHaveBeenCalled();
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('should not identify any stale branches if all are recent', async () => {
    const now = new Date();
    const thirtyDaysAgo = new Date(now.setDate(now.getDate() - 30));

    listBranchesMock.mockResolvedValueOnce([
      { name: 'main', commit: { sha: 'sha1' } },
      { name: 'feature/new-feature', commit: { sha: 'sha2' } },
    ]);

    getCommitMock.mockImplementation(async ({ ref }) => {
      if (ref === 'sha1') return { data: { commit: { author: { date: thirtyDaysAgo.toISOString() } } } };
      if (ref === 'sha2') return { data: { commit: { author: { date: thirtyDaysAgo.toISOString() } } } };
      return { data: { commit: { author: { date: now.toISOString() } } } };
    });

    await run();

    expect(core.setOutput).toHaveBeenCalledWith('stale-branches-json', '[]');
    expect(core.setOutput).toHaveBeenCalledWith(
      'summary-output',
      expect.stringContaining('### ✨ Repository Tidy! ✨')
    );
    expect(addRawSummaryMock).toHaveBeenCalledWith(expect.stringContaining('No stale branches found.'));
    expect(createCommentMock).not.toHaveBeenCalled();
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('should output to issue comment if output-type is "issue-comment"', async () => {
    core.getInput.mockImplementation((name) => {
      switch (name) {
        case 'repo-token': return 'mock-token';
        case 'stale-days': return '30';
        case 'ignore-branches': return 'main';
        case 'output-type': return 'issue-comment';
        case 'issue-number': return '123';
        default: return '';
      }
    });

    const now = new Date();
    const fortyDaysAgo = new Date(now.setDate(now.getDate() - 40));

    listBranchesMock.mockResolvedValueOnce([
      { name: 'feature/very-old', commit: { sha: 'sha1' } },
    ]);

    getCommitMock.mockResolvedValueOnce({ data: { commit: { author: { date: fortyDaysAgo.toISOString() } } } });

    await run();

    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      issue_number: '123',
      body: expect.stringContaining('feature/very-old'),
    });
    expect(addRawSummaryMock).not.toHaveBeenCalled();
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('should fail if output-type is "issue-comment" but no issue-number is provided', async () => {
    core.getInput.mockImplementation((name) => {
      switch (name) {
        case 'repo-token': return 'mock-token';
        case 'output-type': return 'issue-comment';
        case 'issue-number': return ''; // Missing issue number
        default: return '';
      }
    });

    await run();

    expect(core.setFailed).toHaveBeenCalledWith('issue-number is required when output-type is "issue-comment".');
    expect(createCommentMock).not.toHaveBeenCalled();
    expect(addRawSummaryMock).not.toHaveBeenCalled();
  });

  test('should correctly ignore branches using glob patterns', async () => {
    core.getInput.mockImplementation((name) => {
      switch (name) {
        case 'repo-token': return 'mock-token';
        case 'stale-days': return '1'; // Make everything stale
        case 'ignore-branches': return 'main,feature/*';
        case 'output-type': return 'summary';
        default: return '';
      }
    });

    const now = new Date();
    const twoDaysAgo = new Date(now.setDate(now.getDate() - 2));

    listBranchesMock.mockResolvedValueOnce([
      { name: 'main', commit: { sha: 'sha1' } }, // Ignored
      { name: 'feature/ignored-feature', commit: { sha: 'sha2' } }, // Ignored by glob
      { name: 'bugfix/needs-attention', commit: { sha: 'sha3' } }, // Should be stale
    ]);

    getCommitMock.mockImplementation(async ({ ref }) => {
      // All commits are old enough to be stale
      return { data: { commit: { author: { date: twoDaysAgo.toISOString() } } } };
    });

    await run();

    expect(core.setOutput).toHaveBeenCalledWith(
      'stale-branches-json',
      expect.stringContaining('bugfix/needs-attention')
    );
    expect(core.setOutput).not.toHaveBeenCalledWith(
      'stale-branches-json',
      expect.stringContaining('main')
    );
    expect(core.setOutput).not.toHaveBeenCalledWith(
      'stale-branches-json',
      expect.stringContaining('feature/ignored-feature')
    );
    expect(addRawSummaryMock).toHaveBeenCalledWith(expect.stringContaining('bugfix/needs-attention'));
    expect(addRawSummaryMock).not.toHaveBeenCalledWith(expect.stringContaining('main'));
    expect(addRawSummaryMock).not.toHaveBeenCalledWith(expect.stringContaining('feature/ignored-feature'));
    expect(core.setFailed).not.toHaveBeenCalled();
  });
});
