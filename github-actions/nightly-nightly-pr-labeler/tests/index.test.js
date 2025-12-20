const core = require('@actions/core');
const github = require('@actions/github');

jest.mock('@actions/core');
jest.mock('@actions/github');

const run = require('../src/index.js');

describe('PR Labeler', () => {
  const mockAddLabels = jest.fn();
  beforeEach(() => {
    jest.resetAllMocks();
    core.getInput.mockImplementation((name) => {
      if (name === 'github-token') return 'fake-token';
      return '';
    });
    github.getOctokit.mockReturnValue({
      rest: {
        issues: {
          addLabels: mockAddLabels,
        },
      },
    });
    github.context = {
      payload: {
        pull_request: {
          number: 42,
          title: 'Urgent: fix critical bug',
        },
      },
      repo: {
        owner: 'owner',
        repo: 'repo',
      },
    };
  });

  test('adds high priority label for urgent PR', async () => {
    await run();
    expect(mockAddLabels).toHaveBeenCalledWith({
      owner: 'owner',
      repo: 'repo',
      issue_number: 42,
      labels: ['high priority'],
    });
  });

  test('skips labeling when no keyword matches', async () => {
    github.context.payload.pull_request.title = 'Just a normal PR';
    await run();
    expect(mockAddLabels).not.toHaveBeenCalled();
  });
});
