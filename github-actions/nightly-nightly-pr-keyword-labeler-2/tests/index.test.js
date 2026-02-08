const core = require('@actions/core');
const github = require('@actions/github');
const { run } = require('../src/index');

jest.mock('@actions/core');
jest.mock('@actions/github');

describe('PR Keyword Labeler', () => {
  const mockAddLabels = jest.fn();
  const mockGetOctokit = jest.fn(() => ({
    rest: { issues: { addLabels: mockAddLabels } }
  }));

  beforeEach(() => {
    jest.clearAllMocks();
    core.getInput.mockImplementation((name) => {
      if (name === 'github-token') return 'fake-token';
      if (name === 'label-mapping') return '{"fix":"🛠️ bugfix","feature":"✨ feature"}';
      return '';
    });
    core.setFailed = jest.fn();
    core.info = jest.fn();
    github.context = {
      repo: { owner: 'owner', repo: 'repo' },
      payload: {
        pull_request: { number: 42, title: 'Fix: broken link' }
      }
    };
    github.getOctokit = mockGetOctokit;
  });

  test('adds correct label when keyword matches', async () => {
    await run();
    expect(mockAddLabels).toHaveBeenCalledWith({
      owner: 'owner',
      repo: 'repo',
      issue_number: 42,
      labels: ['🛠️ bugfix']
    });
    expect(core.info).toHaveBeenCalledWith('Added labels: 🛠️ bugfix');
  });

  test('does nothing when no keywords match', async () => {
    github.context.payload.pull_request.title = 'Update README';
    await run();
    expect(mockAddLabels).not.toHaveBeenCalled();
    expect(core.info).toHaveBeenCalledWith('No matching keywords found; no labels will be added.');
  });

  test('fails when label-mapping is invalid JSON', async () => {
    core.getInput.mockImplementation((name) => {
      if (name === 'github-token') return 'fake-token';
      if (name === 'label-mapping') return '{invalid json}';
      return '';
    });
    await run();
    expect(core.setFailed).toHaveBeenCalledWith('label-mapping must be valid JSON');
  });
});
