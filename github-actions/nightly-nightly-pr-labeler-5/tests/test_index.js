// Mock rationale: we replace GitHub SDK and core inputs with deterministic values.
jest.mock('@actions/core');
jest.mock('@actions/github');

const core = require('@actions/core');
const github = require('@actions/github');
const { run } = require('../src/index');

describe('Nightly PR Labeler', () => {
  beforeEach(() => {
    jest.resetAllMocks();
    // Mock core inputs
    core.getInput.mockImplementation(name => {
      if (name === 'github_token') return 'fake-token';
      if (name === 'emoji_labels') return '✨,🚀';
      return '';
    });
    core.setFailed = jest.fn();
    core.info = jest.fn();
    // Mock Octokit
    const addLabelsMock = jest.fn().mockResolvedValue({});
    github.getOctokit.mockReturnValue({
      rest: {
        issues: {
          addLabels: addLabelsMock,
        },
      },
    });
    // Mock context payload
    github.context = {
      repo: { owner: 'owner', repo: 'repo' },
      payload: {
        pull_request: {
          number: 42,
          title: 'feat: add new widget',
        },
      },
    };
  });

  test('adds feature label and a random emoji', async () => {
    await run();
    const octokit = github.getOctokit();
    expect(octokit.rest.issues.addLabels).toHaveBeenCalledWith({
      owner: 'owner',
      repo: 'repo',
      issue_number: 42,
      labels: expect.arrayContaining(['feature', expect.stringMatching(/✨|🚀/)]),
    });
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('fails gracefully when no PR in context', async () => {
    github.context.payload.pull_request = null;
    await run();
    expect(core.setFailed).toHaveBeenCalledWith('No pull request found in context');
  });
});
