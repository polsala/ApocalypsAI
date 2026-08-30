// Mock rationale: Use jest to mock @actions/core and @actions/github, ensuring deterministic behavior.

const core = require('@actions/core');
const github = require('@actions/github');

jest.mock('@actions/core');
jest.mock('@actions/github');

describe('nightly-apocalypse-quote-commenter', () => {
  beforeEach(() => {
    jest.resetAllMocks();
  });

  test('posts a comment with a quote', async () => {
    const mockToken = 'fake-token';
    core.getInput.mockReturnValue(mockToken);
    const mockCreateComment = jest.fn().mockResolvedValue({});
    github.getOctokit.mockReturnValue({
      rest: {
        issues: {
          createComment: mockCreateComment
        }
      }
    });
    // Mock context
    github.context = {
      repo: { owner: 'owner', repo: 'repo' },
      payload: { pull_request: { number: 42 } }
    };
    // Mock random to be deterministic
    jest.spyOn(Math, 'random').mockReturnValue(0.1); // selects first quote

    // Require the action after mocks are set (the action runs on import)
    require('../src/index.js');
    // Wait a tick for the async run() to finish
    await new Promise(process.nextTick);

    expect(mockCreateComment).toHaveBeenCalledWith({
      owner: 'owner',
      repo: 'repo',
      issue_number: 42,
      body: 'The sky is falling, but the code still compiles.'
    });
    expect(core.setOutput).toHaveBeenCalledWith('comment', 'The sky is falling, but the code still compiles.');
  });

  test('fails when no PR in context', async () => {
    core.getInput.mockReturnValue('token');
    github.context = {
      repo: { owner: 'owner', repo: 'repo' },
      payload: {}
    };
    require('../src/index.js');
    await new Promise(process.nextTick);
    expect(core.setFailed).toHaveBeenCalledWith('No pull request found in context.');
  });
});
