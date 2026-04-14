const core = require('@actions/core');
const github = require('@actions/github');
const { getRandomQuote, run } = require('../src/index');

jest.mock('@actions/core');
jest.mock('@actions/github');

describe('getRandomQuote', () => {
  test('returns a quote from the list', () => {
    // Mock Math.random to return 0 => first quote
    jest.spyOn(Math, 'random').mockReturnValue(0);
    const quote = getRandomQuote();
    expect(quote).toBe('The journey of a thousand miles begins with a single step.');
    Math.random.mockRestore();
  });
});

describe('run', () => {
  test('creates a comment with selected quote', async () => {
    const mockCreateComment = jest.fn().mockResolvedValue({});
    const mockGetOctokit = jest.fn(() => ({
      rest: {
        issues: {
          createComment: mockCreateComment
        }
      }
    }));
    github.getOctokit = mockGetOctokit;
    github.context = {
      payload: {
        issue: { number: 42 }
      },
      repo: { owner: 'owner', repo: 'repo' }
    };
    core.getInput.mockReturnValue('fake-token');
    // Mock Math.random to select second quote (index 1)
    jest.spyOn(Math, 'random').mockReturnValue(0.2);
    await run();
    expect(mockCreateComment).toHaveBeenCalledWith({
      owner: 'owner',
      repo: 'repo',
      issue_number: 42,
      body: 'When the mind is still, the universe surrenders.'
    });
    Math.random.mockRestore();
  });
});
