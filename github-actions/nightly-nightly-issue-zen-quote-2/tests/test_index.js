jest.mock('@actions/core');
jest.mock('@actions/github');

const core = require('@actions/core');
const github = require('@actions/github');
const { run } = require('../src/index');

describe('Issue Zen Quote Action', () => {
  beforeEach(() => {
    jest.resetAllMocks();
    process.env.FIXED_RANDOM = '0'; // forces first quote
    core.getInput.mockReturnValue('fake-token');
    const createCommentMock = jest.fn().mockResolvedValue({});
    github.getOctokit.mockReturnValue({
      rest: {
        issues: {
          createComment: createCommentMock
        }
      }
    });
    github.context = {
      repo: { owner: 'owner', repo: 'repo' },
      payload: {
        issue: { number: 42 }
      }
    };
  });

  test('posts first quote as comment', async () => {
    await run();
    expect(github.getOctokit).toHaveBeenCalledWith('fake-token');
    const expectedBody = '> The journey of a thousand miles begins with a single step.\n\n*— ApocalypsAI*';
    expect(github.getOctokit().rest.issues.createComment).toHaveBeenCalledWith({
      owner: 'owner',
      repo: 'repo',
      issue_number: 42,
      body: expectedBody
    });
  });
});
