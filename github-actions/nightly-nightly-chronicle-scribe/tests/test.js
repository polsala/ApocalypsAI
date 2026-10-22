const core = require('@actions/core');
const github = require('@actions/github');
const { run } = require('../src/main');

// Mock the GitHub Actions core library
jest.mock('@actions/core'); // Mock rationale: Simulates GitHub Actions core functions for input/output without actual interaction.
// Mock the GitHub Actions github library
jest.mock('@actions/github', () => ({
  getOctokit: jest.fn(),
  context: {
    repo: {
      owner: 'test-owner',
      repo: 'test-repo',
    },
    ref: 'refs/heads/main', // Branch the PR merged into
    payload: {
      pull_request: {
        number: 123,
        title: 'Feat: Add new chronicle scribe',
        user: { login: 'test-user' },
        merged: true,
        merged_at: '2023-10-27T10:00:00Z',
      },
    },
  },
})); // Mock rationale: Simulates GitHub Actions context for repository and pull request data without requiring a live GitHub environment.

describe('Chronicle Scribe Action', () => {
  let octokitMock;

  beforeEach(() => {
    jest.clearAllMocks();

    // Mock Octokit methods
    octokitMock = {
      rest: {
        repos: {
          getContent: jest.fn(),
          createOrUpdateFileContents: jest.fn(),
        },
      },
    };
    github.getOctokit.mockReturnValue(octokitMock); // Mock rationale: Simulates Octokit API calls for fetching and updating file content, preventing actual network requests and repository modifications during tests.

    // Mock core inputs
    core.getInput.mockImplementation((name) => {
      switch (name) {
        case 'github-token': return 'mock-token';
        case 'chronicle-file': return 'CHRONICLE.md';
        case 'entry-format': return '* {PR_TITLE} (#{PR_NUMBER}) by @{PR_AUTHOR} on {MERGE_DATE}';
        case 'commit-message': return 'docs: Chronicle update for PR #{PR_NUMBER}';
        default: return '';
      }
    });
  });

  // Test 1: Should skip if PR is not merged
  test('should skip if pull request is not merged', async () => {
    github.context.payload.pull_request.merged = false; // Override for this test
    await run();
    expect(core.info).toHaveBeenCalledWith('Skipping: Not a merged pull request event.');
    expect(octokitMock.rest.repos.getContent).not.toHaveBeenCalled();
    expect(octokitMock.rest.repos.createOrUpdateFileContents).not.toHaveBeenCalled();
  });

  // Test 2: Should create a new chronicle file if it doesn't exist
  test('should create a new chronicle file if it does not exist', async () => {
    octokitMock.rest.repos.getContent.mockRejectedValue({ status: 404 }); // File not found
    await run();

    const expectedEntry = '* Feat: Add new chronicle scribe (#123) by @test-user on October 27, 2023';
    expect(octokitMock.rest.repos.createOrUpdateFileContents).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      path: 'CHRONICLE.md',
      message: 'docs: Chronicle update for PR #123',
      content: Buffer.from(expectedEntry).toString('base64'),
      sha: null, // No SHA because file is new
      branch: 'refs/heads/main',
    });
    expect(core.setOutput).toHaveBeenCalledWith('chronicle-entry', expectedEntry);
    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Successfully updated chronicle file'));
  });

  // Test 3: Should append to an existing chronicle file
  test('should append to an existing chronicle file', async () => {
    const existingContent = 'Existing entry 1\nExisting entry 2';
    octokitMock.rest.repos.getContent.mockResolvedValue({
      data: {
        content: Buffer.from(existingContent).toString('base64'),
        sha: 'existing-sha',
      },
    });

    await run();

    const expectedEntry = '* Feat: Add new chronicle scribe (#123) by @test-user on October 27, 2023';
    const expectedUpdatedContent = `${existingContent}\n${expectedEntry}`;

    expect(octokitMock.rest.repos.createOrUpdateFileContents).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      path: 'CHRONICLE.md',
      message: 'docs: Chronicle update for PR #123',
      content: Buffer.from(expectedUpdatedContent).toString('base64'),
      sha: 'existing-sha', // SHA of the existing file
      branch: 'refs/heads/main',
    });
    expect(core.setOutput).toHaveBeenCalledWith('chronicle-entry', expectedEntry);
  });

  // Test 4: Should correctly format the entry with custom format and commit message
  test('should use custom entry-format and commit-message', async () => {
    core.getInput.mockImplementation((name) => {
      switch (name) {
        case 'github-token': return 'mock-token';
        case 'chronicle-file': return 'CHANGELOG.md';
        case 'entry-format': return '## {PR_TITLE} ({PR_NUMBER}) - {PR_AUTHOR}';
        case 'commit-message': return 'Changelog update for PR {PR_NUMBER}';
        default: return '';
      }
    });
    octokitMock.rest.repos.getContent.mockRejectedValue({ status: 404 }); // File not found

    await run();

    const expectedEntry = '## Feat: Add new chronicle scribe (123) - test-user';
    expect(octokitMock.rest.repos.createOrUpdateFileContents).toHaveBeenCalledWith(expect.objectContaining({
      path: 'CHANGELOG.md',
      message: 'Changelog update for PR 123',
      content: Buffer.from(expectedEntry).toString('base64'),
    }));
    expect(core.setOutput).toHaveBeenCalledWith('chronicle-entry', expectedEntry);
  });

  // Test 5: Error handling
  test('should set failed status on error', async () => {
    const errorMessage = 'API error';
    octokitMock.rest.repos.getContent.mockRejectedValue(new Error(errorMessage));

    await run();

    expect(core.setFailed).toHaveBeenCalledWith(errorMessage);
  });
});
