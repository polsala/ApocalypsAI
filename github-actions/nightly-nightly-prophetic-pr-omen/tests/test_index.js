const { run } = require('../src/index');
const core = require('@actions/core');
const github = require('@actions/github');

// Mock rationale: We need to mock @actions/core and @actions/github to prevent actual API calls and
// to control inputs/outputs for deterministic testing. This allows us to test the logic in isolation.
jest.mock('@actions/core');
jest.mock('@actions/github', () => ({
  getOctokit: jest.fn(() => ({
    rest: {
      issues: {
        createComment: jest.fn(),
      },
    },
  })),
  context: {
    repo: {
      owner: 'test-owner',
      repo: 'test-repo',
    },
    payload: {
      pull_request: {
        number: 123,
      },
    },
  },
}));

describe('Prophetic PR Omen Action', () => {
  let createCommentMock;

  beforeEach(() => {
    jest.clearAllMocks();
    createCommentMock = github.getOctokit().rest.issues.createComment;
  });

  it('should generate a deterministic omen based on PR title length', async () => {
    core.getInput.mockImplementation((name) => {
      if (name === 'pr-title') return 'Short title'; // length 11
      if (name === 'pr-body') return '';
      if (name === 'github-token') return 'mock-token';
      return '';
    });

    await run();

    // The omens array has 10 elements. (11 % 10) = 1.
    // The omen at index 1: "A whisper from the void: your changes ripple through the cosmos. Expect either enlightenment or a cosmic rollback."
    expect(core.setOutput).toHaveBeenCalledWith('omen-message', expect.stringContaining('A whisper from the void'));
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      issue_number: 123,
      body: expect.stringContaining('✨ ApocalypsAI Prophetic Omen ✨\n\nA whisper from the void'),
    });
  });

  it('should generate a deterministic omen based on PR title and body length', async () => {
    core.getInput.mockImplementation((name) => {
      if (name === 'pr-title') return 'A longer title for testing'; // length 26
      if (name === 'pr-body') return 'And a body that adds more length.'; // length 33
      if (name === 'github-token') return 'mock-token';
      return '';
    });

    await run();

    // Total length = 26 + 33 = 59. (59 % 10) = 9.
    // The omen at index 9: "The great debugger foresees: a single line change, a universe of impact. Choose wisely, young padawan."
    expect(core.setOutput).toHaveBeenCalledWith('omen-message', expect.stringContaining('The great debugger foresees'));
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      issue_number: 123,
      body: expect.stringContaining('✨ ApocalypsAI Prophetic Omen ✨\n\nThe great debugger foresees'),
    });
  });

  it('should handle empty PR body gracefully', async () => {
    core.getInput.mockImplementation((name) => {
      if (name === 'pr-title') return 'Title only'; // length 10
      if (name === 'pr-body') return '';
      if (name === 'github-token') return 'mock-token';
      return '';
    });

    await run();

    // Total length = 10. (10 % 10) = 0.
    // The omen at index 0: "The ancient scrolls foretell: this code shall compile on the first try, or summon a thousand tiny bugs."
    expect(core.setOutput).toHaveBeenCalledWith('omen-message', expect.stringContaining('The ancient scrolls foretell'));
  });

  it('should call setFailed if an error occurs', async () => {
    core.getInput.mockImplementation((name) => {
      if (name === 'pr-title') throw new Error('Failed to get title');
      if (name === 'github-token') return 'mock-token';
      return '';
    });

    await run();

    expect(core.setFailed).toHaveBeenCalledWith('Failed to get title');
  });

  it('should not comment if not a pull request event', async () => {
    // Mock rationale: Simulate a non-PR event by setting pull_request to undefined.
    github.context.payload.pull_request = undefined;
    core.getInput.mockImplementation((name) => {
      if (name === 'pr-title') return 'Title';
      if (name === 'pr-body') return '';
      if (name === 'github-token') return 'mock-token';
      return '';
    });

    await run();

    expect(core.setOutput).toHaveBeenCalledWith('omen-message', expect.any(String));
    expect(createCommentMock).not.toHaveBeenCalled();
    expect(core.warning).toHaveBeenCalledWith('Not a pull request event. Omen will only be set as output, not commented.');

    // Restore for other tests to ensure isolation
    github.context.payload.pull_request = { number: 123 };
  });
});
