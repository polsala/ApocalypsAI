const core = require('@actions/core');
const { getRandomFact } = require('../src/index');

jest.mock('@actions/core');

describe('Fun Fact Action', () => {
  test('getRandomFact returns a fact from the list', () => {
    const fact = getRandomFact();
    const allowed = [
      "Honey never spoils.",
      "Bananas are berries, but strawberries hasn't.",
      "Octopuses have three hearts.",
      "A day on Venus is longer than its year.",
      "There are more stars in the universe than grains of sand on Earth."
    ];
    expect(allowed).toContain(fact);
  });

  test('run sets output to a fact', async () => {
    const mockSetOutput = jest.fn();
    core.getInput.mockReturnValue('fake-token');
    core.setOutput = mockSetOutput;
    core.info = jest.fn();
    core.setFailed = jest.fn();

    const github = require('@actions/github');
    github.context = {
      payload: {
        pull_request: { number: 1 }
      },
      repo: { owner: 'owner', repo: 'repo' }
    };
    const mockCreateComment = jest.fn().mockResolvedValue({});
    github.getOctokit = jest.fn(() => ({
      rest: {
        issues: {
          createComment: mockCreateComment
        }
      }
    }));

    const { run } = require('../src/index');
    await run();

    expect(mockSetOutput).toHaveBeenCalledWith('fun_fact', expect.any(String));
    expect(mockCreateComment).toHaveBeenCalledWith({
      owner: 'owner',
      repo: 'repo',
      issue_number: 1,
      body: expect.stringContaining('🤖 **Fun Fact:**')
    });
  });
});
