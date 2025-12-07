// Tests for Nightly GitHub Actions Branch Cleaner
// Mock rationale: We mock the GitHub API and glob functionality to test logic without making real API calls

const { describe, it, expect, beforeEach, afterEach } = require('@jest/globals');
const core = require('@actions/core');
const { github } = require('@actions/github');

// Mock the glob module
const mockGlob = {
  makeRegex: jest.fn((pattern) => {
    // Simple glob to regex conversion for testing
    const regexPattern = pattern
      .replace(/\*/g, '.*')
      .replace(/\?/g, '.');
    return new RegExp(`^${regexPattern}$`);
  })
};

// Mock @actions/toolkit
jest.mock('@actions/toolkit', () => ({
  glob: mockGlob
}));

// Mock @actions/core
jest.mock('@actions/core', () => ({
  getInput: jest.fn(),
  getBooleanInput: jest.fn(),
  setOutput: jest.fn(),
  setFailed: jest.fn()
}));

// Mock @actions/github
jest.mock('@actions/github', () => ({
  getOctokit: jest.fn(),
  context: {
    repo: {
      owner: 'test-owner',
      repo: 'test-repo'
    }
  }
}));

const { run } = require('../src/main');

describe('Branch Cleaner', () => {
  let mockOctokit;
  let consoleSpy;

  beforeEach(() => {
    // Mock console.log for testing
    consoleSpy = jest.spyOn(console, 'log').mockImplementation(() => {});

    // Mock GitHub API responses
    mockOctokit = {
      rest: {
        repos: {
          listBranches: jest.fn().mockResolvedValue({
            data: [
              { name: 'main', commit: { sha: 'abc123' } },
              { name: 'master', commit: { sha: 'def456' } },
              { name: 'feature-1', commit: { sha: 'ghi789' } },
              { name: 'feature-2', commit: { sha: 'jkl012' } },
              { name: 'release/v1.0', commit: { sha: 'mno345' } },
              { name: 'hotfix/critical', commit: { sha: 'pqr678' } }
            ]
          }),
          deleteRef: jest.fn().mockResolvedValue({})
        }
      }
    };

    github.getOctokit.mockReturnValue(mockOctokit);

    // Mock inputs
    core.getInput.mockImplementation((name) => {
      const inputs = {
        'github-token': 'test-token',
        'protected-branches': 'main,master',
        'retention-days': '7',
        'max-branches-to-delete': '10',
        'verbose': 'true'
      };
      return inputs[name] || '';
    });

    core.getBooleanInput.mockImplementation((name) => {
      const inputs = {
        'dry-run': true
      };
      return inputs[name] || false;
    });
  });

  afterEach(() => {
    jest.clearAllMocks();
    consoleSpy.mockRestore();
  });

  describe('Protected Branch Detection', () => {
    it('should protect main and master branches', async () => {
      await run();

      expect(core.setOutput).toHaveBeenCalledWith('protected-branches', JSON.stringify(['main', 'master']));
      expect(core.setOutput).toHaveBeenCalledWith('total-deleted', '0');
    });

    it('should protect branches with glob patterns', async () => {
      core.getInput.mockImplementation((name) => {
        const inputs = {
          'github-token': 'test-token',
          'protected-branches': 'main,master,release/**,hotfix/**',
          'retention-days': '7',
          'max-branches-to-delete': '10',
          'verbose': 'true'
        };
        return inputs[name] || '';
      });

      await run();

      expect(core.setOutput).toHaveBeenCalledWith('protected-branches', JSON.stringify(['main', 'master', 'release/v1.0', 'hotfix/critical']));
    });
  });

  describe('Branch Deletion', () => {
    it('should perform dry run without deleting branches', async () => {
      core.getBooleanInput.mockImplementation((name) => {
        const inputs = {
          'dry-run': true
        };
        return inputs[name] || false;
      });

      await run();

      expect(mockOctokit.rest.git.deleteRef).not.toHaveBeenCalled();
      expect(core.setOutput).toHaveBeenCalledWith('total-deleted', '0');
    });

    it('should delete branches when dry run is false', async () => {
      core.getBooleanInput.mockImplementation((name) => {
        const inputs = {
          'dry-run': false
        };
        return inputs[name] || false;
      });

      await run();

      expect(mockOctokit.rest.git.deleteRef).toHaveBeenCalledTimes(2);
      expect(mockOctokit.rest.git.deleteRef).toHaveBeenCalledWith({
        owner: 'test-owner',
        repo: 'test-repo',
        ref: 'heads/feature-1'
      });
      expect(mockOctokit.rest.git.deleteRef).toHaveBeenCalledWith({
        owner: 'test-owner',
        repo: 'test-repo',
        ref: 'heads/feature-2'
      });
    });
  });

  describe('Retention Policy', () => {
    it('should respect max branches to delete limit', async () => {
      core.getInput.mockImplementation((name) => {
        const inputs = {
          'github-token': 'test-token',
          'protected-branches': 'main,master',
          'retention-days': '7',
          'max-branches-to-delete': '1',
          'verbose': 'true'
        };
        return inputs[name] || '';
      });

      await run();

      expect(mockOctokit.rest.git.deleteRef).toHaveBeenCalledTimes(1);
      expect(core.setOutput).toHaveBeenCalledWith('total-deleted', '1');
    });
  });

  describe('Error Handling', () => {
    it('should handle API errors gracefully', async () => {
      mockOctokit.rest.git.deleteRef.mockRejectedValueOnce(new Error('API Error'));

      core.getBooleanInput.mockImplementation((name) => {
        const inputs = {
          'dry-run': false
        };
        return inputs[name] || false;
      });

      await run();

      expect(core.setFailed).toHaveBeenCalledWith('Action failed: API Error');
    });
  });

  describe('Output Formatting', () => {
    it('should output correct JSON format for deleted branches', async () => {
      await run();

      expect(core.setOutput).toHaveBeenCalledWith('deleted-branches', JSON.stringify([]));
      expect(core.setOutput).toHaveBeenCalledWith('protected-branches', JSON.stringify(['main', 'master']));
      expect(core.setOutput).toHaveBeenCalledWith('total-deleted', '0');
    });
  });
});
