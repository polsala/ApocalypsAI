// Mock rationale: We mock @actions/core and @actions/github to prevent
// actual API calls and to control input/output for deterministic testing.
const core = require('@actions/core');
const github = require('@actions/github');

// Mock the GitHub Actions toolkit
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

const run = require('../src/index'); // Import the action's main function

describe('Nightly Whisper of Encouragement Action', () => {
  let createCommentMock;

  beforeEach(() => {
    jest.clearAllMocks();
    createCommentMock = github.getOctokit().rest.issues.createComment;
    // Reset context for each test
    github.context.payload = {
      pull_request: {
        number: 123,
      },
    };
  });

  test('should post a default whisper to a pull request', async () => {
    core.getInput.mockImplementation((name) => {
      if (name === 'github-token') return 'mock-token';
      if (name === 'whispers') return ''; // Use default whispers
      return '';
    });

    await run();

    expect(core.getInput).toHaveBeenCalledWith('github-token', { required: true });
    expect(core.getInput).toHaveBeenCalledWith('whispers');
    expect(createCommentMock).toHaveBeenCalledTimes(1);
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      issue_number: 123,
      body: expect.stringContaining('A Whisper from the ApocalypsAI:'),
    });
    expect(core.setOutput).toHaveBeenCalledWith('whisper-chosen', expect.any(String));
  });

  test('should post a custom whisper to a pull request', async () => {
    const customWhisper = 'Your code is a beacon in the digital darkness!';
    core.getInput.mockImplementation((name) => {
      if (name === 'github-token') return 'mock-token';
      if (name === 'whispers') return customWhisper;
      return '';
    });

    await run();

    expect(createCommentMock).toHaveBeenCalledTimes(1);
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      issue_number: 123,
      body: `**A Whisper from the ApocalypsAI:**\n\n> _"${customWhisper}"_`,
    });
    expect(core.setOutput).toHaveBeenCalledWith('whisper-chosen', customWhisper);
  });

  test('should handle multiple custom whispers and pick one', async () => {
    const customWhispers = 'Whisper A,Whisper B,Whisper C';
    core.getInput.mockImplementation((name) => {
      if (name === 'github-token') return 'mock-token';
      if (name === 'whispers') return customWhispers;
      return '';
    });

    // Mock Math.random to ensure a specific whisper is chosen for deterministic test
    const mockMath = Object.create(global.Math);
    mockMath.random = () => 0.5; // This will pick the middle element (index 1)
    global.Math = mockMath;

    await run();

    expect(createCommentMock).toHaveBeenCalledTimes(1);
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      issue_number: 123,
      body: `**A Whisper from the ApocalypsAI:**\n\n> _"Whisper B"_`,
    });
    expect(core.setOutput).toHaveBeenCalledWith('whisper-chosen', 'Whisper B');

    global.Math = Math; // Restore original Math
  });

  test('should post to an issue if no pull request is present', async () => {
    github.context.payload = {
      issue: {
        number: 456,
      },
    };
    core.getInput.mockImplementation((name) => {
      if (name === 'github-token') return 'mock-token';
      if (name === 'whispers') return 'Issue whisper!';
      return '';
    });

    await run();

    expect(createCommentMock).toHaveBeenCalledTimes(1);
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      issue_number: 456,
      body: `**A Whisper from the ApocalypsAI:**\n\n> _"Issue whisper!"_`,
    });
    expect(core.setOutput).toHaveBeenCalledWith('whisper-chosen', 'Issue whisper!');
  });

  test('should post to an issue from an issue_comment event', async () => {
    github.context.payload = {
      comment: {
        body: '/encourage',
      },
      issue: {
        number: 789,
      },
    };
    core.getInput.mockImplementation((name) => {
      if (name === 'github-token') return 'mock-token';
      if (name === 'whispers') return 'Comment whisper!';
      return '';
    });

    await run();

    expect(createCommentMock).toHaveBeenCalledTimes(1);
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      issue_number: 789,
      body: `**A Whisper from the ApocalypsAI:**\n\n> _"Comment whisper!"_`,
    });
    expect(core.setOutput).toHaveBeenCalledWith('whisper-chosen', 'Comment whisper!');
  });

  test('should warn and not post if no issue or PR number is found', async () => {
    github.context.payload = {}; // No PR or issue in context
    core.getInput.mockImplementation((name) => {
      if (name === 'github-token') return 'mock-token';
      if (name === 'whispers') return 'Test whisper';
      return '';
    });

    await run();

    expect(core.warning).toHaveBeenCalledWith('Could not determine a pull request or issue number from the context. Skipping comment.');
    expect(createCommentMock).not.toHaveBeenCalled();
    expect(core.setOutput).not.toHaveBeenCalledWith('whisper-chosen', expect.any(String)); // Output should not be set
  });

  test('should warn and not post if whispers list is empty', async () => {
    core.getInput.mockImplementation((name) => {
      if (name === 'github-token') return 'mock-token';
      if (name === 'whispers') return ' , '; // Empty custom whispers
      return '';
    });

    await run();

    expect(core.warning).toHaveBeenCalledWith('No whispers provided, and default list is empty. Skipping comment.');
    expect(createCommentMock).not.toHaveBeenCalled();
    expect(core.setOutput).toHaveBeenCalledWith('whisper-chosen', 'No whisper posted (empty list).');
  });

  test('should call setFailed on error', async () => {
    core.getInput.mockImplementation((name) => {
      if (name === 'github-token') throw new Error('Failed to get token');
      return '';
    });

    await run();

    expect(core.setFailed).toHaveBeenCalledWith('Failed to get token');
    expect(createCommentMock).not.toHaveBeenCalled();
  });
});
