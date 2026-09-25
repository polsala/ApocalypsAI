const core = require('@actions/core');
const github = require('@actions/github');
const { when } = require('jest-when'); // For more flexible mocking

// Mock the GitHub Actions toolkit
jest.mock('@actions/core');
jest.mock('@actions/github');

const run = require('../src/main'); // The action's main script

describe('Nightly Whimsical Commit Curator', () => {
  let listCommitsMock;

  beforeEach(() => {
    jest.clearAllMocks();

    // Mock rationale: Simulate GitHub API calls without making actual network requests.
    // This ensures tests are deterministic and offline.
    listCommitsMock = jest.fn();
    github.getOctokit.mockReturnValue({
      rest: {
        repos: {
          listCommits: listCommitsMock,
        },
      },
    });

    // Mock rationale: Simulate the GitHub context (owner, repo) for the action.
    github.context = {
      repo: {
        owner: 'test-owner',
        repo: 'test-repo',
      },
    };

    // Mock rationale: Simulate action inputs.
    when(core.getInput)
      .calledWith('github-token', expect.anything())
      .mockReturnValue('mock-token');
    when(core.getInput)
      .calledWith('days-ago')
      .mockReturnValue('7');
    when(core.getInput)
      .calledWith('keywords')
      .mockReturnValue('');
    when(core.getInput)
      .calledWith('emoji-patterns')
      .mockReturnValue('');
  });

  test('should find no whimsical commits if none match criteria', async () => {
    // Mock rationale: Provide a set of non-whimsical commit messages.
    listCommitsMock.mockResolvedValue({
      data: [
        { commit: { message: 'feat: Add new feature' } },
        { commit: { message: 'fix: Resolve bug in login' } },
        { commit: { message: 'docs: Update README' } },
        { commit: { message: 'chore: Clean up dependencies' } },
      ],
    });

    await run();

    expect(core.setOutput).toHaveBeenCalledWith('whimsical-commits', '[]');
    expect(core.setOutput).toHaveBeenCalledWith('whimsical-summary', 'No particularly whimsical commits found recently. Keep up the good work!\n');
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('should find whimsical commits based on keywords', async () => {
    // Mock rationale: Provide commit messages, some matching the 'sparkle' keyword.
    when(core.getInput)
      .calledWith('keywords')
      .mockReturnValue('sparkle, magic');

    listCommitsMock.mockResolvedValue({
      data: [
        { commit: { message: 'feat: Add new feature ✨' } },
        { commit: { message: 'fix: Resolve bug with a sprinkle of magic' } },
        { commit: { message: 'docs: Update README' } },
        { commit: { message: 'chore: Clean up dependencies' } },
        { commit: { message: 'refactor: Make it sparkle and shine!' } },
      ],
    });

    await run();

    expect(core.setOutput).toHaveBeenCalledWith('whimsical-commits', JSON.stringify([
      'fix: Resolve bug with a sprinkle of magic',
      'refactor: Make it sparkle and shine!'
    ]));
    expect(core.setOutput).toHaveBeenCalledWith('whimsical-summary', expect.stringContaining('✨ Recent Whimsical Commits (2):\n- fix: Resolve bug with a sprinkle of magic\n- refactor: Make it sparkle and shine!\n'));
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('should find whimsical commits based on emoji patterns', async () => {
    // Mock rationale: Provide commit messages, some matching the emoji patterns.
    when(core.getInput)
      .calledWith('emoji-patterns')
      .mockReturnValue(':sparkles:,:tada:');

    listCommitsMock.mockResolvedValue({
      data: [
        { commit: { message: 'feat: Add new feature 🎉' } },
        { commit: { message: 'fix: Resolve bug' } },
        { commit: { message: 'docs: Update README ✨' } },
        { commit: { message: 'chore: Clean up dependencies' } },
      ],
    });

    await run();

    expect(core.setOutput).toHaveBeenCalledWith('whimsical-commits', JSON.stringify([
      'feat: Add new feature 🎉',
      'docs: Update README ✨'
    ]));
    expect(core.setOutput).toHaveBeenCalledWith('whimsical-summary', expect.stringContaining('✨ Recent Whimsical Commits (2):\n- feat: Add new feature 🎉\n- docs: Update README ✨\n'));
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('should find whimsical commits based on positive words heuristic', async () => {
    // Mock rationale: Provide commit messages, some matching the positive words heuristic.
    listCommitsMock.mockResolvedValue({
      data: [
        { commit: { message: 'feat: Add new feature' } },
        { commit: { message: 'fix: Resolve bug' } },
        { commit: { message: 'docs: Update README' } },
        { commit: { message: 'chore: Clean up dependencies' } },
        { commit: { message: 'Make it a joy to use!' } },
        { commit: { message: 'This change brings pure delight.' } },
        { commit: { message: 'A little bit of magic for everyone.' } },
      ],
    });

    await run();

    expect(core.setOutput).toHaveBeenCalledWith('whimsical-commits', JSON.stringify([
      'Make it a joy to use!',
      'This change brings pure delight.',
      'A little bit of magic for everyone.'
    ]));
    expect(core.setOutput).toHaveBeenCalledWith('whimsical-summary', expect.stringContaining('✨ Recent Whimsical Commits (3):\n- Make it a joy to use!\n- This change brings pure delight.\n- A little bit of magic for everyone.\n'));
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('should handle API errors gracefully', async () => {
    // Mock rationale: Simulate an API error.
    listCommitsMock.mockRejectedValue(new Error('GitHub API error'));

    await run();

    expect(core.setFailed).toHaveBeenCalledWith('GitHub API error');
    expect(core.setOutput).not.toHaveBeenCalledWith('whimsical-commits', expect.any(String));
    expect(core.setOutput).not.toHaveBeenCalledWith('whimsical-summary', expect.any(String));
  });

  test('should use default days-ago if not provided', async () => {
    when(core.getInput)
      .calledWith('days-ago')
      .mockReturnValue(''); // Simulate no input

    listCommitsMock.mockResolvedValue({ data: [] }); // No commits for simplicity

    await run();

    // Check that listCommits was called with a 'since' date roughly 7 days ago
    const callArgs = listCommitsMock.mock.calls[0][0];
    const sinceDate = new Date(callArgs.since);
    const sevenDaysAgo = new Date();
    sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);

    // Allow for slight time differences in test execution
    expect(sinceDate.getTime()).toBeGreaterThanOrEqual(sevenDaysAgo.getTime() - 1000);
    expect(sinceDate.getTime()).toBeLessThanOrEqual(sevenDaysAgo.getTime() + 1000);
  });
});
