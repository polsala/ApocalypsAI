const core = require('@actions/core');
const github = require('@actions/github');
const { when } = require('jest-when');

// Mock the main entry point
const run = require('../src/main');

// Mock @actions/core
jest.mock('@actions/core');
// Mock @actions/github
jest.mock('@actions/github', () => ({
  getOctokit: jest.fn(),
  context: {
    repo: {
      owner: 'test-owner',
      repo: 'test-repo',
    },
  },
}));

describe('Ghost Branch Buster', () => {
  let octokitMock;
  let listBranchesMock;
  let getCommitMock;
  let deleteRefMock;
  let createIssueMock;

  beforeEach(() => {
    jest.clearAllMocks();

    // Mock Octokit methods
    listBranchesMock = jest.fn();
    getCommitMock = jest.fn();
    deleteRefMock = jest.fn();
    createIssueMock = jest.fn();

    octokitMock = {
      paginate: jest.fn((method, params) => method(params).then(res => res.data)), // Simulate paginate
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
    };
    github.getOctokit.mockReturnValue(octokitMock);

    // Mock core inputs
    when(core.getInput)
      .calledWith('repo-token', expect.anything())
      .mockReturnValue('mock-token');
    when(core.getInput)
      .calledWith('stale-days', expect.anything())
      .mockReturnValue('90');
    when(core.getInput)
      .calledWith('exempt-branches', expect.anything())
      .mockReturnValue('main,master');
    when(core.getInput)
      .calledWith('issue-title', expect.anything())
      .mockReturnValue('Stale Branches Detected');
    when(core.getInput)
      .calledWith('issue-label', expect.anything())
      .mockReturnValue('');

    when(core.getBooleanInput)
      .calledWith('dry-run', expect.anything())
      .mockReturnValue(true);
    when(core.getBooleanInput)
      .calledWith('delete-stale', expect.anything())
      .mockReturnValue(false);
  });

  // Mock rationale:
  // - @actions/core functions (getInput, setOutput, info, error, setFailed) are mocked to control test inputs and observe outputs/logs without actual side effects.
  // - @actions/github.getOctokit is mocked to return a controlled Octokit instance.
  // - Octokit API methods (listBranches, getCommit, deleteRef, create) are mocked to simulate GitHub API responses and actions without making real network calls.
  // - github.context.repo is mocked to provide a consistent repository context.

  test('should find no stale branches', async () => {
    const freshDate = new Date();
    freshDate.setDate(freshDate.getDate() - 10); // 10 days ago, not stale

    listBranchesMock.mockResolvedValueOnce({
      data: [
        { name: 'main', commit: { sha: 'sha1' } },
        { name: 'feature-a', commit: { sha: 'sha2' } },
      ],
    });
    getCommitMock
      .mockResolvedValueOnce({ data: { commit: { author: { date: freshDate.toISOString() } } } }) // main branch
      .mockResolvedValueOnce({ data: { commit: { author: { date: freshDate.toISOString() } } } }); // feature-a

    await run();

    expect(core.setOutput).toHaveBeenCalledWith('stale-branches-count', 0);
    expect(core.setOutput).toHaveBeenCalledWith('deleted-branches-count', 0);
    expect(core.setOutput).toHaveBeenCalledWith('stale-branches-list', '[]');
    expect(core.info).toHaveBeenCalledWith('No stale branches found. Repository is clean!');
    expect(deleteRefMock).not.toHaveBeenCalled();
    expect(createIssueMock).not.toHaveBeenCalled();
  });

  test('should find stale branches in dry run mode', async () => {
    const staleDate = new Date();
    staleDate.setDate(staleDate.getDate() - 100); // 100 days ago, stale

    listBranchesMock.mockResolvedValueOnce({
      data: [
        { name: 'main', commit: { sha: 'sha1' } },
        { name: 'stale-feature', commit: { sha: 'sha2' } },
        { name: 'another-stale', commit: { sha: 'sha3' } },
      ],
    });
    getCommitMock
      .mockResolvedValueOnce({ data: { commit: { author: { date: new Date().toISOString() } } } }) // main branch
      .mockResolvedValueOnce({ data: { commit: { author: { date: staleDate.toISOString() } } } }) // stale-feature
      .mockResolvedValueOnce({ data: { commit: { author: { date: staleDate.toISOString() } } } }); // another-stale

    when(core.getInput)
      .calledWith('exempt-branches', expect.anything())
      .mockReturnValue('main'); // Only main is exempt

    await run();

    expect(core.setOutput).toHaveBeenCalledWith('stale-branches-count', 2);
    expect(core.setOutput).toHaveBeenCalledWith('deleted-branches-count', 0);
    expect(core.setOutput).toHaveBeenCalledWith('stale-branches-list', JSON.stringify(['stale-feature', 'another-stale']));
    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Found stale branch: stale-feature'));
    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('This was a dry run. No branches were deleted.'));
    expect(deleteRefMock).not.toHaveBeenCalled();
    expect(createIssueMock).toHaveBeenCalledTimes(1);
    expect(createIssueMock).toHaveBeenCalledWith(expect.objectContaining({
      title: 'Stale Branches Detected',
      body: expect.stringContaining('- `stale-feature`\n- `another-stale`'),
      labels: [],
    }));
  });

  test('should delete stale branches when dry-run is false and delete-stale is true', async () => {
    const staleDate = new Date();
    staleDate.setDate(staleDate.getDate() - 100); // 100 days ago, stale

    listBranchesMock.mockResolvedValueOnce({
      data: [
        { name: 'main', commit: { sha: 'sha1' } },
        { name: 'stale-feature', commit: { sha: 'sha2' } },
      ],
    });
    getCommitMock
      .mockResolvedValueOnce({ data: { commit: { author: { date: new Date().toISOString() } } } }) // main branch
      .mockResolvedValueOnce({ data: { commit: { author: { date: staleDate.toISOString() } } } }); // stale-feature

    when(core.getInput)
      .calledWith('exempt-branches', expect.anything())
      .mockReturnValue('main');
    when(core.getBooleanInput)
      .calledWith('dry-run', expect.anything())
      .mockReturnValue(false);
    when(core.getBooleanInput)
      .calledWith('delete-stale', expect.anything())
      .mockReturnValue(true);

    await run();

    expect(core.setOutput).toHaveBeenCalledWith('stale-branches-count', 1);
    expect(core.setOutput).toHaveBeenCalledWith('deleted-branches-count', 1);
    expect(core.setOutput).toHaveBeenCalledWith('stale-branches-list', JSON.stringify(['stale-feature']));
    expect(deleteRefMock).toHaveBeenCalledTimes(1);
    expect(deleteRefMock).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      ref: 'heads/stale-feature',
    });
    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Successfully deleted stale branch: stale-feature'));
    expect(createIssueMock).toHaveBeenCalledTimes(1);
    expect(createIssueMock).toHaveBeenCalledWith(expect.objectContaining({
      title: 'Stale Branches Detected',
      body: expect.stringContaining('Stale branches were deleted.'),
    }));
  });

  test('should handle API errors gracefully', async () => {
    listBranchesMock.mockRejectedValueOnce(new Error('API error'));

    await run();

    expect(core.setFailed).toHaveBeenCalledWith('API error');
    expect(core.setOutput).not.toHaveBeenCalled();
  });

  test('should create issue with custom title and label', async () => {
    const staleDate = new Date();
    staleDate.setDate(staleDate.getDate() - 100); // 100 days ago, stale

    listBranchesMock.mockResolvedValueOnce({
      data: [
        { name: 'feature-x', commit: { sha: 'sha1' } },
      ],
    });
    getCommitMock
      .mockResolvedValueOnce({ data: { commit: { author: { date: staleDate.toISOString() } } } });

    when(core.getInput)
      .calledWith('exempt-branches', expect.anything())
      .mockReturnValue('');
    when(core.getInput)
      .calledWith('issue-title', expect.anything())
      .mockReturnValue('Forgotten Branches Report');
    when(core.getInput)
      .calledWith('issue-label', expect.anything())
      .mockReturnValue('branch-cleanup');

    await run();

    expect(core.setOutput).toHaveBeenCalledWith('stale-branches-count', 1);
    expect(createIssueMock).toHaveBeenCalledTimes(1);
    expect(createIssueMock).toHaveBeenCalledWith(expect.objectContaining({
      title: 'Forgotten Branches Report',
      labels: ['branch-cleanup'],
    }));
  });

  test('should not delete if delete-stale is false even if dry-run is false', async () => {
    const staleDate = new Date();
    staleDate.setDate(staleDate.getDate() - 100); // 100 days ago, stale

    listBranchesMock.mockResolvedValueOnce({
      data: [
        { name: 'stale-feature', commit: { sha: 'sha2' } },
      ],
    });
    getCommitMock
      .mockResolvedValueOnce({ data: { commit: { author: { date: staleDate.toISOString() } } } });

    when(core.getBooleanInput)
      .calledWith('dry-run', expect.anything())
      .mockReturnValue(false);
    when(core.getBooleanInput)
      .calledWith('delete-stale', expect.anything())
      .mockReturnValue(false); // Explicitly false

    await run();

    expect(core.setOutput).toHaveBeenCalledWith('stale-branches-count', 1);
    expect(core.setOutput).toHaveBeenCalledWith('deleted-branches-count', 0);
    expect(deleteRefMock).not.toHaveBeenCalled();
    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('No branches were deleted (delete-stale was false).'));
  });
});
