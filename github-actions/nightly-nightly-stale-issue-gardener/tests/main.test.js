const core = require('@actions/core');
const github = require('@actions/github');
const { run } = require('../src/main');

// Mock the GitHub Actions toolkit
jest.mock('@actions/core');
jest.mock('@actions/github');

describe('Stale Issue Gardener', () => {
  let listForRepoMock;
  let addLabelsMock;
  let createCommentMock;
  let updateIssueMock;

  beforeEach(() => {
    jest.clearAllMocks();

    // Mock rationale:
    // - @actions/core.getInput: Mocks the action's inputs to provide deterministic values for testing different scenarios without relying on actual GitHub workflow inputs.
    // - @actions/github.context: Mocks the repository context to provide consistent owner/repo information.
    // - @actions/github.getOctokit: Mocks the GitHub API client to prevent actual network requests during tests. This ensures tests are fast, deterministic, and offline.
    // - octokit.rest.issues.* methods (listForRepo, addLabels, createComment, update): Mocks specific API calls to control their return values and verify they are called with the correct arguments.

    core.getInput.mockImplementation((name) => {
      switch (name) {
        case 'repo-token': return 'mock-token';
        case 'stale-issue-label': return 'stale';
        case 'days-before-stale': return '30';
        case 'days-before-close': return '7';
        case 'stale-issue-message': return 'This issue is stale.';
        case 'close-issue-message': return 'This issue was closed.';
        case 'exempt-labels': return 'bug,enhancement';
        case 'only-labels': return '';
        default: return '';
      }
    });

    github.context = {
      repo: {
        owner: 'test-owner',
        repo: 'test-repo',
      },
    };

    listForRepoMock = jest.fn();
    addLabelsMock = jest.fn();
    createCommentMock = jest.fn();
    updateIssueMock = jest.fn();

    github.getOctokit.mockReturnValue({
      rest: {
        issues: {
          listForRepo: listForRepoMock,
          addLabels: addLabelsMock,
          createComment: createCommentMock,
          update: updateIssueMock,
        },
      },
    });
  });

  test('should mark an issue as stale and comment', async () => {
    const thirtyOneDaysAgo = new Date();
    thirtyOneDaysAgo.setDate(thirtyOneDaysAgo.getDate() - 31);

    listForRepoMock.mockResolvedValue({
      data: [
        {
          number: 1,
          updated_at: thirtyOneDaysAgo.toISOString(),
          labels: [],
          pull_request: undefined,
        },
      ],
    });

    await run();

    expect(listForRepoMock).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      state: 'open',
      per_page: 100,
    });
    expect(addLabelsMock).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      issue_number: 1,
      labels: ['stale'],
    });
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      issue_number: 1,
      body: 'This issue is stale.',
    });
    expect(updateIssueMock).not.toHaveBeenCalled();
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('should close a stale issue after total inactivity threshold', async () => {
    const thirtyEightDaysAgo = new Date(); // Updated 38 days ago (30 days stale + 8 days close)
    thirtyEightDaysAgo.setDate(thirtyEightDaysAgo.getDate() - (30 + 8));

    listForRepoMock.mockResolvedValue({
      data: [
        {
          number: 2,
          updated_at: thirtyEightDaysAgo.toISOString(),
          labels: [{ name: 'stale' }], // Already has stale label
          pull_request: undefined,
        },
      ],
    });

    await run();

    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      issue_number: 2,
      body: 'This issue was closed.',
    });
    expect(updateIssueMock).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      issue_number: 2,
      state: 'closed',
    });
    expect(addLabelsMock).not.toHaveBeenCalled(); // No new labels added
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('should not mark or close issues with exempt labels', async () => {
    const thirtyOneDaysAgo = new Date();
    thirtyOneDaysAgo.setDate(thirtyOneDaysAgo.getDate() - 31);

    listForRepoMock.mockResolvedValue({
      data: [
        {
          number: 3,
          updated_at: thirtyOneDaysAgo.toISOString(),
          labels: [{ name: 'bug' }],
          pull_request: undefined,
        },
      ],
    });

    await run();

    expect(addLabelsMock).not.toHaveBeenCalled();
    expect(createCommentMock).not.toHaveBeenCalled();
    expect(updateIssueMock).not.toHaveBeenCalled();
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('should not process pull requests', async () => {
    const thirtyOneDaysAgo = new Date();
    thirtyOneDaysAgo.setDate(thirtyOneDaysAgo.getDate() - 31);

    listForRepoMock.mockResolvedValue({
      data: [
        {
          number: 4,
          updated_at: thirtyOneDaysAgo.toISOString(),
          labels: [],
          pull_request: {}, // Presence of pull_request object indicates it's a PR
        },
      ],
    });

    await run();

    expect(addLabelsMock).not.toHaveBeenCalled();
    expect(createCommentMock).not.toHaveBeenCalled();
    expect(updateIssueMock).not.toHaveBeenCalled();
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('should handle only-labels correctly', async () => {
    core.getInput.mockImplementation((name) => {
      if (name === 'only-labels') return 'feature';
      if (name === 'repo-token') return 'mock-token';
      if (name === 'stale-issue-label') return 'stale';
      if (name === 'days-before-stale') return '30';
      if (name === 'days-before-close') return '7';
      if (name === 'stale-issue-message') return 'This issue is stale.';
      if (name === 'close-issue-message') return 'This issue was closed.';
      if (name === 'exempt-labels') return '';
      return '';
    });

    const thirtyOneDaysAgo = new Date();
    thirtyOneDaysAgo.setDate(thirtyOneDaysAgo.getDate() - 31);

    listForRepoMock.mockResolvedValue({
      data: [
        {
          number: 5,
          updated_at: thirtyOneDaysAgo.toISOString(),
          labels: [{ name: 'feature' }], // Should be processed
          pull_request: undefined,
        },
        {
          number: 6,
          updated_at: thirtyOneDaysAgo.toISOString(),
          labels: [{ name: 'documentation' }], // Should be skipped
          pull_request: undefined,
        },
      ],
    });

    await run();

    expect(addLabelsMock).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      issue_number: 5,
      labels: ['stale'],
    });
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      issue_number: 5,
      body: 'This issue is stale.',
    });
    expect(addLabelsMock).not.toHaveBeenCalledWith(expect.objectContaining({ issue_number: 6 }));
    expect(createCommentMock).not.toHaveBeenCalledWith(expect.objectContaining({ issue_number: 6 }));
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('should not mark active issues as stale', async () => {
    const twentyDaysAgo = new Date();
    twentyDaysAgo.setDate(twentyDaysAgo.getDate() - 20);

    listForRepoMock.mockResolvedValue({
      data: [
        {
          number: 7,
          updated_at: twentyDaysAgo.toISOString(),
          labels: [],
          pull_request: undefined,
        },
      ],
    });

    await run();

    expect(addLabelsMock).not.toHaveBeenCalled();
    expect(createCommentMock).not.toHaveBeenCalled();
    expect(updateIssueMock).not.toHaveBeenCalled();
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('should not close a stale issue if total inactivity threshold not met', async () => {
    const thirtyFiveDaysAgo = new Date(); // Updated 35 days ago (30 days stale + 5 days close)
    thirtyFiveDaysAgo.setDate(thirtyFiveDaysAgo.getDate() - (30 + 5));

    listForRepoMock.mockResolvedValue({
      data: [
        {
          number: 8,
          updated_at: thirtyFiveDaysAgo.toISOString(),
          labels: [{ name: 'stale' }],
          pull_request: undefined,
        },
      ],
    });

    await run();

    expect(createCommentMock).not.toHaveBeenCalledWith(expect.objectContaining({ issue_number: 8, body: 'This issue was closed.' }));
    expect(updateIssueMock).not.toHaveBeenCalledWith(expect.objectContaining({ issue_number: 8, state: 'closed' }));
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('should call setFailed on error', async () => {
    listForRepoMock.mockRejectedValue(new Error('API Error'));

    await run();

    expect(core.setFailed).toHaveBeenCalledWith('API Error');
  });
});
