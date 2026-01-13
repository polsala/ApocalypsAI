const core = require('@actions/core');
const github = require('@actions/github');

jest.mock('@actions/core');
jest.mock('@actions/github');

describe('Auto PR Labeler', () => {
  const mockAddLabels = jest.fn().mockResolvedValue({});
  const mockGetOctokit = jest.fn(() => ({
    rest: {
      issues: {
        addLabels: mockAddLabels
      }
    }
  }));

  beforeEach(() => {
    jest.clearAllMocks();
    github.getOctokit = mockGetOctokit;
    core.getInput.mockImplementation(name => {
      if (name === 'repo-token') return 'fake-token';
      return '';
    });
    github.context = {
      repo: { owner: 'owner', repo: 'repo' },
      payload: {
        pull_request: {
          number: 42,
          title: 'Fix: zombie apocalypse'
        }
      }
    };
  });

  test('adds correct label for fix keyword', async () => {
    // Require after mocks are set â the action runs on import
    require('../src/index.js');
    // Wait for the async run to complete
    await new Promise(process.nextTick);
    expect(mockAddLabels).toHaveBeenCalledWith({
      owner: 'owner',
      repo: 'repo',
      issue_number: 42,
      labels: ['ð§ zombie-fix']
    });
  });
});
