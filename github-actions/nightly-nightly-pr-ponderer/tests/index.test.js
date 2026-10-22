const core = require('@actions/core');
const github = require('@actions/github');
const { when } = require('jest-when');

// Mock the action's main function
const run = require('../src/index');

// Mock @actions/core
jest.mock('@actions/core');

// Mock @actions/github
const mockCreateComment = jest.fn();
jest.mock('@actions/github', () => ({
  getOctokit: jest.fn(() => ({
    rest: {
      issues: {
        createComment: mockCreateComment,
      },
    },
  })),
  context: {
    eventName: 'pull_request',
    payload: {
      pull_request: {
        number: 123,
      },
    },
    repo: {
      owner: 'polsala',
      repo: 'ApocalypsAI',
    },
  },
}));

describe('Nightly PR Ponderer', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    // Mock rationale: Math.random is mocked to ensure deterministic quote selection for testing.
    jest.spyOn(Math, 'random').mockReturnValue(0.5); // Always pick the middle quote for deterministic tests
    when(core.getInput)
      .calledWith('github-token', expect.anything())
      .thenReturn('mock-token');
  });

  afterAll(() => {
    jest.restoreAllMocks();
  });

  it('should add a philosophical quote to a pull request comment', async () => {
    await run();

    expect(core.getInput).toHaveBeenCalledWith('github-token', { required: true });
    expect(github.getOctokit).toHaveBeenCalledWith('mock-token');
    expect(mockCreateComment).toHaveBeenCalledTimes(1);
    expect(mockCreateComment).toHaveBeenCalledWith({
      owner: 'polsala',
      repo: 'ApocalypsAI',
      issue_number: 123,
      body: expect.stringContaining('✨ A moment of contemplation for your Pull Request, fellow traveler:\n\n> _\"To be yourself in a world that is constantly trying to make you something else is the greatest accomplishment. - Ralph Waldo Emerson\"_'),
    });
    expect(core.setOutput).toHaveBeenCalledWith('quote', 'To be yourself in a world that is constantly trying to make you something else is the greatest accomplishment. - Ralph Waldo Emerson');
    expect(core.info).toHaveBeenCalledWith('Pondered PR #123 with: \"To be yourself in a world that is constantly trying to make you something else is the greatest accomplishment. - Ralph Waldo Emerson\"');
  });

  it('should handle non-pull_request events gracefully', async () => {
    github.context.eventName = 'push'; // Mock rationale: Simulating a non-PR event to test graceful handling.
    github.context.payload.pull_request = undefined; // Mock rationale: Simulating a non-PR event to test graceful handling.

    await run();

    expect(core.warning).toHaveBeenCalledWith('This action is intended to run on pull_request events.');
    expect(mockCreateComment).not.toHaveBeenCalled();
    expect(core.setOutput).toHaveBeenCalledWith('quote', 'No PR context available for pondering.');
  });

  it('should set failed status if an error occurs', async () => {
    when(core.getInput)
      .calledWith('github-token', expect.anything())
      .thenThrow(new Error('Test error')); // Mock rationale: Simulating an error during input retrieval.

    await run();

    expect(core.setFailed).toHaveBeenCalledWith('Test error');
  });
});
