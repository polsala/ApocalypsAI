const core = require('@actions/core');
const github = require('@actions/github');
const { getSentiment, emojiForSentiment, run } = require('../src/index');

jest.mock('@actions/core');
jest.mock('@actions/github');

describe('sentiment analysis', () => {
  test('detects positive', () => {
    expect(getSentiment('Add new feature for login')).toBe('positive');
  });
  test('detects negative', () => {
    expect(getSentiment('Remove deprecated API causing bug')).toBe('negative');
  });
  test('defaults to neutral', () => {
    expect(getSentiment('Update documentation')).toBe('neutral');
  });
});

describe('emoji mapping', () => {
  test('positive maps to +1', () => {
    expect(emojiForSentiment('positive')).toBe('+1');
  });
  test('negative maps to -1', () => {
    expect(emojiForSentiment('negative')).toBe('-1');
  });
  test('neutral maps to confused', () => {
    expect(emojiForSentiment('neutral')).toBe('confused');
  });
});

describe('action run', () => {
  const mockCreateForCommit = jest.fn();
  const mockListCommits = jest.fn().mockResolvedValue({
    data: [
      { sha: 'abc123', commit: { message: 'Add feature' } },
      { sha: 'def456', commit: { message: 'Fix bug' } },
    ],
  });

  beforeAll(() => {
    core.getInput.mockImplementation(name => {
      if (name === 'github-token') return 'fake-token';
      if (name === 'pull-number') return '42';
      return '';
    });
    github.getOctokit.mockReturnValue({
      rest: {
        pulls: { listCommits: mockListCommits },
        reactions: { createForCommit: mockCreateForCommit },
      },
    });
    // Mock context repo information
    github.context = { repo: { owner: 'octocat', repo: 'hello-world' } };
  });

  test('adds correct reactions', async () => {
    await run();
    expect(mockListCommits).toHaveBeenCalledWith({
      owner: 'octocat',
      repo: 'hello-world',
      pull_number: 42,
    });
    expect(mockCreateForCommit).toHaveBeenCalledTimes(2);
    expect(mockCreateForCommit).toHaveBeenCalledWith({
      owner: 'octocat',
      repo: 'hello-world',
      commit_sha: 'abc123',
      content: '+1',
    });
    expect(mockCreateForCommit).toHaveBeenCalledWith({
      owner: 'octocat',
      repo: 'hello-world',
      commit_sha: 'def456',
      content: '+1',
    });
  });
});
