// Mock rationale: All network interactions are replaced with in‑memory objects so the test runs offline.
const { run } = require('../src/main');
const core = require('@actions/core');

// Mock core input retrieval
jest.mock('@actions/core', () => ({
  getInput: jest.fn(),
  info: jest.fn(),
  setFailed: jest.fn(),
}));

describe('Branch Cleaner Logic', () => {
  const mockOctokit = {
    rest: {
      repos: {
        listBranches: jest.fn(),
        compareCommits: jest.fn(),
      },
      git: {
        deleteRef: jest.fn(),
      },
    },
  };

  const mockContext = {
    repo: { owner: 'test-owner', repo: 'test-repo' },
    payload: { repository: { default_branch: 'main' } },
  };

  beforeEach(() => {
    jest.clearAllMocks();
    core.getInput.mockImplementation((name) => {
      if (name === 'github_token') return 'fake-token';
      if (name === 'days_to_keep') return '10';
      return '';
    });
  });

  test('deletes merged branches older than threshold', async () => {
    // Branch list: feature-old (merged, old), feature-recent (merged, recent), feature-unmerged (not merged)
    mockOctokit.rest.repos.listBranches.mockResolvedValue({
      data: [
        { name: 'feature-old', commit: { commit: { author: { date: '2020-01-01T00:00:00Z' } } } },
        { name: 'feature-recent', commit: { commit: { author: { date: new Date().toISOString() } } } },
        { name: 'feature-unmerged', commit: { commit: { author: { date: '2020-01-01T00:00:00Z' } } } },
      ],
    });

    // compareCommits mock: merged for first two, not merged for third
    mockOctokit.rest.repos.compareCommits
      .mockResolvedValueOnce({ data: { merged: true } }) // feature-old
      .mockResolvedValueOnce({ data: { merged: true } }) // feature-recent
      .mockResolvedValueOnce({ data: { merged: false } }); // feature-unmerged

    await run(mockOctokit, mockContext);

    // Expect deleteRef called only for feature-old
    expect(mockOctokit.rest.git.deleteRef).toHaveBeenCalledTimes(1);
    expect(mockOctokit.rest.git.deleteRef).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      ref: 'heads/feature-old',
    });
    // Info logs for kept branches
    expect(core.info).toHaveBeenCalledWith('Keeping branch feature-recent (age within threshold)');
  });
});
