// Mock rationale: Use jest to mock @actions/core and @actions/github, simulate context and verify reaction call.

jest.mock('@actions/core');
jest.mock('@actions/github');

const core = require('@actions/core');
const github = require('@actions/github');

describe('Issue Emoji Reaction Action', () => {
  beforeEach(() => {
    jest.resetAllMocks();
    // Mock environment and context
    process.env['GITHUB_REPOSITORY'] = 'owner/repo';
    github.context = {
      payload: {
        issue: { number: 42 }
      },
      repo: { owner: 'owner', repo: 'repo' }
    };
    core.getInput = jest.fn(name => {
      if (name === 'token') return 'fake-token';
      if (name === 'emojis') return undefined; // use default
      return '';
    });
    core.setOutput = jest.fn();
    core.setFailed = jest.fn();
  });

  test('adds reaction with default emojis', async () => {
    const createMock = jest.fn().mockResolvedValue({});
    github.getOctokit.mockReturnValue({
      rest: { reactions: { createForIssue: createMock } }
    });

    const action = require('../src/index.js');
    await action.run();

    expect(core.getInput).toHaveBeenCalledWith('token', { required: true });
    expect(core.getInput).toHaveBeenCalledWith('emojis');
    expect(createMock).toHaveBeenCalledWith(expect.objectContaining({
      owner: 'owner',
      repo: 'repo',
      issue_number: 42,
      content: expect.any(String)
    }));
    expect(core.setOutput).toHaveBeenCalledWith('emoji', expect.any(String));
    expect(core.setFailed).not.toHaveBeenCalled();
  });
});
