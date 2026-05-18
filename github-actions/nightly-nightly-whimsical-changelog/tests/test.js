const core = require('@actions/core');
const github = require('@actions/github');
const fs = require('fs');

// Mock the GitHub Actions toolkit
jest.mock('@actions/core');
jest.mock('@actions/github');
jest.mock('fs'); // Mock fs to prevent actual file writes

const run = require('../src/main'); // The action's main script

describe('Whimsical Changelog Action', () => {
  let mockGetInput;
  let mockSetOutput;
  let mockSetFailed;
  let mockListCommits;
  let mockWriteFileSync;

  beforeEach(() => {
    // Reset mocks before each test
    mockGetInput = jest.spyOn(core, 'getInput').mockImplementation((name) => {
      switch (name) {
        case 'commit-prefix': return '[whimsy]';
        case 'output-file': return 'TEST_CHANGELOG.md';
        case 'max-commits': return '50';
        case 'github-token': return 'mock-token';
        default: return '';
      }
    });
    mockSetOutput = jest.spyOn(core, 'setOutput');
    mockSetFailed = jest.spyOn(core, 'setFailed');
    jest.spyOn(core, 'info'); // Mock info to prevent console output during tests

    mockListCommits = jest.fn();
    github.getOctokit.mockReturnValue({
      rest: {
        repos: {
          listCommits: mockListCommits,
        },
      },
    });
    github.context = {
      repo: {
        owner: 'test-owner',
        repo: 'test-repo',
      },
    };

    mockWriteFileSync = jest.spyOn(fs, 'writeFileSync');
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  it('should generate a changelog with whimsical commits', async () => {
    // Mock rationale: Simulate GitHub API response with relevant commit messages.
    mockListCommits.mockResolvedValue({
      data: [
        { sha: 'abcdef1234567890', commit: { message: '[whimsy] Added a sparkle effect to buttons' } },
        { sha: '1234567890abcdef', commit: { message: 'feat: Implemented user login' } },
        { sha: 'fedcba0987654321', commit: { message: '[whimsy] Fixed a bug where cats would bark' } },
        { sha: '0987654321fedcba', commit: { message: 'docs: Updated README' } },
      ],
    });

    await run();

    expect(mockGetInput).toHaveBeenCalledWith('commit-prefix', { required: true });
    expect(mockGetInput).toHaveBeenCalledWith('output-file', { required: true });
    expect(mockGetInput).toHaveBeenCalledWith('max-commits', { required: true });
    expect(mockGetInput).toHaveBeenCalledWith('github-token', { required: true });

    expect(mockListCommits).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      per_page: 50,
    });

    const expectedChangelog = '## Whimsical Changelog\n\n- Added a sparkle effect to buttons (abcdef1)\n- Fixed a bug where cats would bark (fedcba0)\n';
    expect(mockWriteFileSync).toHaveBeenCalledWith('TEST_CHANGELOG.md', expectedChangelog);
    expect(mockSetOutput).toHaveBeenCalledWith('changelog-content', expectedChangelog);
    expect(mockSetOutput).toHaveBeenCalledWith('changelog-path', 'TEST_CHANGELOG.md');
    expect(mockSetFailed).not.toHaveBeenCalled();
  });

  it('should handle no whimsical commits found', async () => {
    // Mock rationale: Simulate GitHub API response with no commits matching the prefix.
    mockListCommits.mockResolvedValue({
      data: [
        { sha: 'abcdef1234567890', commit: { message: 'feat: Implemented user login' } },
        { sha: '1234567890abcdef', commit: { message: 'docs: Updated README' } },
      ],
    });

    await run();

    const expectedChangelog = '## Whimsical Changelog\n\nNo whimsical changes found in recent commits.\n';
    expect(mockWriteFileSync).toHaveBeenCalledWith('TEST_CHANGELOG.md', expectedChangelog);
    expect(mockSetOutput).toHaveBeenCalledWith('changelog-content', expectedChangelog);
    expect(mockSetOutput).toHaveBeenCalledWith('changelog-path', 'TEST_CHANGELOG.md');
    expect(mockSetFailed).not.toHaveBeenCalled();
  });

  it('should handle API errors gracefully', async () => {
    // Mock rationale: Simulate an error during the GitHub API call.
    const errorMessage = 'GitHub API rate limit exceeded';
    mockListCommits.mockRejectedValue(new Error(errorMessage));

    await run();

    expect(mockSetFailed).toHaveBeenCalledWith(errorMessage);
    expect(mockWriteFileSync).not.toHaveBeenCalled();
    expect(mockSetOutput).not.toHaveBeenCalledWith('changelog-content', expect.any(String));
  });

  it('should use custom commit prefix and output file', async () => {
    mockGetInput.mockImplementation((name) => {
      switch (name) {
        case 'commit-prefix': return '[joyful]';
        case 'output-file': return 'JOYFUL_NOTES.md';
        case 'max-commits': return '10';
        case 'github-token': return 'mock-token';
        default: return '';
      }
    });

    // Mock rationale: Simulate GitHub API response with custom prefix.
    mockListCommits.mockResolvedValue({
      data: [
        { sha: 'abcdef1234567890', commit: { message: '[joyful] Added a happy little cloud' } },
        { sha: '1234567890abcdef', commit: { message: 'feat: Regular commit' } },
      ],
    });

    await run();

    expect(mockListCommits).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      per_page: 10,
    });
    const expectedChangelog = '## Whimsical Changelog\n\n- Added a happy little cloud (abcdef1)\n';
    expect(mockWriteFileSync).toHaveBeenCalledWith('JOYFUL_NOTES.md', expectedChangelog);
    expect(mockSetOutput).toHaveBeenCalledWith('changelog-content', expectedChangelog);
    expect(mockSetOutput).toHaveBeenCalledWith('changelog-path', 'JOYFUL_NOTES.md');
  });
});
