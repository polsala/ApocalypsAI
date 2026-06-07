const core = require('@actions/core');
const github = require('@actions/github');

jest.mock('@actions/core');
jest.mock('@actions/github');

const { run } = require('../src/index');

describe('PR labeler', () => {
  const mockAddLabels = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
    core.getInput.mockImplementation(name => {
      if (name === 'github_token') return 'fake-token';
      return '';
    });
    github.getOctokit.mockReturnValue({
      rest: {
        issues: {
          addLabels: mockAddLabels
        }
      }
    });
    github.context = {
      repo: { owner: 'owner', repo: 'repo' },
      payload: {
        pull_request: {
          number: 42,
          title: 'Bug: fix crash on startup'
        }
      }
    };
  });

  test('adds bug label', async () => {
    await run();
    expect(mockAddLabels).toHaveBeenCalledWith({
      owner: 'owner',
      repo: 'repo',
      issue_number: 42,
      labels: ['bug']
    });
    expect(core.setOutput).toHaveBeenCalledWith('added_labels', 'bug');
  });
});
