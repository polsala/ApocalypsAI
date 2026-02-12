// Mock rationale: simulate @actions/core and @actions/github without network calls
jest.mock('@actions/core', () => ({
  getInput: jest.fn(),
  setFailed: jest.fn(),
  setOutput: jest.fn()
}));

jest.mock('@actions/github', () => ({
  getOctokit: jest.fn(),
  context: {
    payload: {
      pull_request: { number: 42 }
    },
    repo: { owner: 'owner', repo: 'repo' }
  }
}));

const core = require('@actions/core');
const github = require('@actions/github');

describe('nightly-apocalypse-survival-tip action', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('posts a comment with a tip when PR context exists', async () => {
    const mockCreateComment = jest.fn().mockResolvedValue({});
    github.getOctokit.mockReturnValue({
      rest: { issues: { createComment: mockCreateComment } }
    });
    core.getInput.mockReturnValue('fake-token');

    // Require the action after mocks are set up
    await require('../src/index.js');

    expect(mockCreateComment).toHaveBeenCalledWith({
      owner: 'owner',
      repo: 'repo',
      issue_number: 42,
      body: expect.stringContaining('🛡️ **Apocalypse Survival Tip:**')
    });
    expect(core.setOutput).toHaveBeenCalledWith('tip', expect.any(String));
  });

  test('fails gracefully when no pull request in context', async () => {
    // Remove pull_request from payload
    github.context.payload.pull_request = undefined;
    core.getInput.mockReturnValue('fake-token');
    const mockCreateComment = jest.fn();
    github.getOctokit.mockReturnValue({
      rest: { issues: { createComment: mockCreateComment } }
    });

    await require('../src/index.js');

    expect(core.setFailed).toHaveBeenCalledWith('No pull request found in context.');
    expect(mockCreateComment).not.toHaveBeenCalled();
  });
});
