const core = require('@actions/core');
const github = require('@actions/github');
const { run } = require('../src/index');

// Mock the GitHub Actions toolkit
jest.mock('@actions/core');
jest.mock('@actions/github');

describe('Celestial PR Blesser', () => {
  let createCommentMock;

  beforeEach(() => {
    jest.clearAllMocks();

    // Mock rationale: We need to simulate the GitHub context and API calls without making actual network requests.
    // This allows for deterministic and offline testing of the action's logic.
    createCommentMock = jest.fn();
    github.getOctokit.mockReturnValue({
      rest: {
        issues: {
          createComment: createCommentMock,
        },
      },
    });

    // Mock rationale: Simulate the GitHub context payload for a pull request event.
    // This provides the necessary data (PR number, title, body, additions/deletions)
    // that the action would normally receive from the GitHub webhook event.
    github.context = {
      repo: {
        owner: 'polsala',
        repo: 'ApocalypsAI',
      },
      payload: {
        pull_request: {
          number: 123,
          title: 'feat: Add new celestial blessing feature',
          body: 'This PR introduces a new feature to bless PRs. It is very important.',
          additions: 100,
          deletions: 50,
        },
      },
      eventName: 'pull_request',
    };
  });

  test('should bless a PR that meets all criteria', async () => {
    // Mock rationale: Simulate inputs provided to the GitHub Action.
    // This allows testing different configurations of the action's behavior.
    core.getInput.mockImplementation((name) => {
      switch (name) {
        case 'github-token': return 'mock-token';
        case 'pr-title-keywords': return 'feat,fix';
        case 'pr-body-min-length': return '20';
        case 'max-lines-changed': return '500';
        case 'blessing-message': return '✨ Blessed!';
        case 'failure-message': return '🌌 Not blessed.';
        default: return '';
      }
    });

    await run();

    expect(core.setFailed).not.toHaveBeenCalled();
    expect(core.setOutput).toHaveBeenCalledWith('is-blessed', true);
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'polsala',
      repo: 'ApocalypsAI',
      issue_number: 123,
      body: '✨ Blessed!',
    });
  });

  test('should not bless a PR with a short body', async () => {
    github.context.payload.pull_request.body = 'Short.'; // Mock rationale: Change PR body to simulate a failure condition.
    core.getInput.mockImplementation((name) => {
      switch (name) {
        case 'github-token': return 'mock-token';
        case 'pr-title-keywords': return 'feat,fix';
        case 'pr-body-min-length': return '20';
        case 'max-lines-changed': return '500';
        case 'blessing-message': return '✨ Blessed!';
        case 'failure-message': return '🌌 Not blessed.';
        default: return '';
      }
    });

    await run();

    expect(core.setFailed).toHaveBeenCalledWith('PR did not achieve Celestial Alignment.');
    expect(core.setOutput).toHaveBeenCalledWith('is-blessed', false);
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'polsala',
      repo: 'ApocalypsAI',
      issue_number: 123,
      body: '🌌 Not blessed.\n\n**Reasons for non-alignment:**\n- PR body must be at least 20 characters long.',
    });
  });

  test('should not bless a PR with too many lines changed', async () => {
    github.context.payload.pull_request.additions = 400; // Mock rationale: Change lines added to simulate a failure condition.
    github.context.payload.pull_request.deletions = 200; // Total 600
    core.getInput.mockImplementation((name) => {
      switch (name) {
        case 'github-token': return 'mock-token';
        case 'pr-title-keywords': return 'feat,fix';
        case 'pr-body-min-length': return '20';
        case 'max-lines-changed': return '500';
        case 'blessing-message': return '✨ Blessed!';
        case 'failure-message': return '🌌 Not blessed.';
        default: return '';
      }
    });

    await run();

    expect(core.setFailed).toHaveBeenCalledWith('PR did not achieve Celestial Alignment.');
    expect(core.setOutput).toHaveBeenCalledWith('is-blessed', false);
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'polsala',
      repo: 'ApocalypsAI',
      issue_number: 123,
      body: '🌌 Not blessed.\n\n**Reasons for non-alignment:**\n- Total lines changed (600) exceeds maximum allowed (500).',
    });
  });

  test('should not bless a PR with missing title keyword', async () => {
    github.context.payload.pull_request.title = 'chore: Update dependencies'; // Mock rationale: Change PR title to simulate a failure condition.
    core.getInput.mockImplementation((name) => {
      switch (name) {
        case 'github-token': return 'mock-token';
        case 'pr-title-keywords': return 'feat,fix,docs'; // 'chore' is not in this list
        case 'pr-body-min-length': return '20';
        case 'max-lines-changed': return '500';
        case 'blessing-message': return '✨ Blessed!';
        case 'failure-message': return '🌌 Not blessed.';
        default: return '';
      }
    });

    await run();

    expect(core.setFailed).toHaveBeenCalledWith('PR did not achieve Celestial Alignment.');
    expect(core.setOutput).toHaveBeenCalledWith('is-blessed', false);
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'polsala',
      repo: 'ApocalypsAI',
      issue_number: 123,
      body: '🌌 Not blessed.\n\n**Reasons for non-alignment:**\n- PR title must contain one of: feat, fix, docs.',
    });
  });

  test('should handle multiple failure reasons', async () => {
    github.context.payload.pull_request.body = 'Short.';
    github.context.payload.pull_request.additions = 400;
    github.context.payload.pull_request.deletions = 200; // Total 600
    github.context.payload.pull_request.title = 'chore: Update dependencies';
    core.getInput.mockImplementation((name) => {
      switch (name) {
        case 'github-token': return 'mock-token';
        case 'pr-title-keywords': return 'feat,fix,docs';
        case 'pr-body-min-length': return '20';
        case 'max-lines-changed': return '500';
        case 'blessing-message': return '✨ Blessed!';
        case 'failure-message': return '🌌 Not blessed.';
        default: return '';
      }
    });

    await run();

    expect(core.setFailed).toHaveBeenCalledWith('PR did not achieve Celestial Alignment.');
    expect(core.setOutput).toHaveBeenCalledWith('is-blessed', false);
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'polsala',
      repo: 'ApocalypsAI',
      issue_number: 123,
      body: '🌌 Not blessed.\n\n**Reasons for non-alignment:**\n- PR title must contain one of: feat, fix, docs.\n- PR body must be at least 20 characters long.\n- Total lines changed (600) exceeds maximum allowed (500).',
    });
  });

  test('should not fail if PR number is missing (not a PR event)', async () => {
    github.context.payload.pull_request = null; // Mock rationale: Simulate a non-PR event.
    core.getInput.mockImplementation((name) => {
      switch (name) {
        case 'github-token': return 'mock-token';
        case 'pr-title-keywords': return 'feat,fix';
        case 'pr-body-min-length': return '20';
        case 'max-lines-changed': return '500';
        case 'blessing-message': return '✨ Blessed!';
        case 'failure-message': return '🌌 Not blessed.';
        default: return '';
      }
    });

    await run();

    expect(core.setFailed).toHaveBeenCalledWith('Could not get PR number from context. This action only runs on pull_request events.');
    expect(core.setOutput).not.toHaveBeenCalled();
    expect(createCommentMock).not.toHaveBeenCalled();
  });

  test('should handle empty title keywords gracefully', async () => {
    core.getInput.mockImplementation((name) => {
      switch (name) {
        case 'github-token': return 'mock-token';
        case 'pr-title-keywords': return ''; // No keywords
        case 'pr-body-min-length': return '20';
        case 'max-lines-changed': return '500';
        case 'blessing-message': return '✨ Blessed!';
        case 'failure-message': return '🌌 Not blessed.';
        default: return '';
      }
    });

    await run();

    expect(core.setFailed).not.toHaveBeenCalled();
    expect(core.setOutput).toHaveBeenCalledWith('is-blessed', true);
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'polsala',
      repo: 'ApocalypsAI',
      issue_number: 123,
      body: '✨ Blessed!',
    });
  });
});
