const core = require('@actions/core');
const github = require('@actions/github');
const { when } = require('jest-when');

// Mock the action's main file
const run = require('../src/main');

// Mock @actions/core
jest.mock('@actions/core');
// Mock @actions/github
jest.mock('@actions/github');

describe('Nightly Whimsy Enforcer Action', () => {
  beforeEach(() => {
    jest.clearAllMocks();

    // Mock rationale: We need to control the inputs to the action for testing different scenarios.
    when(core.getInput)
      .calledWith('whimsy-keywords', expect.anything())
      .mockReturnValue('void, temporal, anomaly, whisper, wasteland, cosmic, glitch, echo, paradox, shimmer');
    when(core.getInput)
      .calledWith('target-type', expect.anything())
      .mockReturnValue('pr_title'); // Default for most tests
    when(core.getInput)
      .calledWith('github-token', expect.anything())
      .mockReturnValue('mock-github-token'); // Mock rationale: Provide a token for Octokit calls

    // Mock rationale: We need to control the GitHub context for testing different event types and payloads.
    github.context = {
      eventName: 'pull_request',
      payload: {
        pull_request: {
          title: 'Default PR Title',
          head: {
            sha: 'mock_sha_pr'
          }
        },
        head_commit: {
          message: 'Default Commit Message'
        }
      },
      repo: {
        owner: 'polsala',
        repo: 'ApocalypsAI'
      }
    };

    // Mock rationale: Octokit is used to fetch commit messages for PRs when target-type is 'commit_message'.
    // We need to mock its behavior to avoid actual API calls.
    github.getOctokit.mockReturnValue({
      rest: {
        git: {
          getCommit: jest.fn().mockResolvedValue({
            data: {
              message: 'Mocked commit message for PR head'
            }
          })
        }
      }
    });
  });

  test('sets success if PR title contains a whimsical keyword', async () => {
    github.context.payload.pull_request.title = 'Fix: Resolve a temporal anomaly in the build process';
    await run();
    expect(core.setFailed).not.toHaveBeenCalled();
    expect(core.setOutput).toHaveBeenCalledWith('whimsy-detected', true);
    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Whimsy detected!'));
  });

  test('sets success if PR title contains a whimsical keyword (case-insensitive)', async () => {
    github.context.payload.pull_request.title = 'feat: Add new VOID functionality';
    await run();
    expect(core.setFailed).not.toHaveBeenCalled();
    expect(core.setOutput).toHaveBeenCalledWith('whimsy-detected', true);
  });

  test('sets failure if PR title does not contain a whimsical keyword', async () => {
    github.context.payload.pull_request.title = 'Fix: Update dependencies';
    await run();
    expect(core.setFailed).toHaveBeenCalledWith(expect.stringContaining('No whimsy detected.'));
    expect(core.setOutput).toHaveBeenCalledWith('whimsy-detected', false);
  });

  test('sets success if commit message contains a whimsical keyword (push event)', async () => {
    when(core.getInput).calledWith('target-type', expect.anything()).mockReturnValue('commit_message');
    github.context.eventName = 'push';
    github.context.payload.head_commit.message = 'feat: Implement new wasteland scavenger logic';
    await run();
    expect(core.setFailed).not.toHaveBeenCalled();
    expect(core.setOutput).toHaveBeenCalledWith('whimsy-detected', true);
  });

  test('sets failure if commit message does not contain a whimsical keyword (push event)', async () => {
    when(core.getInput).calledWith('target-type', expect.anything()).mockReturnValue('commit_message');
    github.context.eventName = 'push';
    github.context.payload.head_commit.message = 'chore: Update documentation';
    await run();
    expect(core.setFailed).toHaveBeenCalledWith(expect.stringContaining('No whimsy detected.'));
    expect(core.setOutput).toHaveBeenCalledWith('whimsy-detected', false);
  });

  test('handles empty whimsy-keywords gracefully', async () => {
    when(core.getInput).calledWith('whimsy-keywords', expect.anything()).mockReturnValue('');
    github.context.payload.pull_request.title = 'Any title';
    await run();
    expect(core.warning).toHaveBeenCalledWith('No whimsy keywords provided. This action will always pass.');
    expect(core.setFailed).not.toHaveBeenCalled();
    expect(core.setOutput).toHaveBeenCalledWith('whimsy-detected', true);
  });

  test('fails on invalid target-type', async () => {
    when(core.getInput).calledWith('target-type', expect.anything()).mockReturnValue('invalid_type');
    await run();
    expect(core.setFailed).toHaveBeenCalledWith('Invalid target-type: invalid_type. Must be "pr_title" or "commit_message".');
    expect(core.setOutput).not.toHaveBeenCalledWith('whimsy-detected', expect.any(Boolean));
  });

  test('passes if target-type is pr_title but not a PR event', async () => {
    github.context.eventName = 'push'; // Not a pull_request event
    when(core.getInput).calledWith('target-type', expect.anything()).mockReturnValue('pr_title');
    await run();
    expect(core.warning).toHaveBeenCalledWith(expect.stringContaining('Action triggered outside of a pull_request event'));
    expect(core.setFailed).not.toHaveBeenCalled();
    expect(core.setOutput).toHaveBeenCalledWith('whimsy-detected', true);
  });

  test('passes if target-type is commit_message but not a push/PR event or no head_commit', async () => {
    github.context.eventName = 'schedule'; // Not a push event
    github.context.payload = {}; // No head_commit
    when(core.getInput).calledWith('target-type', expect.anything()).mockReturnValue('commit_message');
    await run();
    expect(core.warning).toHaveBeenCalledWith(expect.stringContaining('Action triggered outside of a push or pull_request event'));
    expect(core.setFailed).not.toHaveBeenCalled();
    expect(core.setOutput).toHaveBeenCalledWith('whimsy-detected', true);
  });

  test('fetches commit message for PR event when target-type is commit_message and finds whimsy', async () => {
    when(core.getInput).calledWith('target-type', expect.anything()).mockReturnValue('commit_message');
    github.context.eventName = 'pull_request';
    github.context.payload.pull_request.head.sha = 'mock_sha_pr_with_whimsy';
    github.getOctokit().rest.git.getCommit.mockResolvedValueOnce({
      data: {
        message: 'feat: Add a new cosmic ray deflector'
      }
    });
    await run();
    expect(github.getOctokit().rest.git.getCommit).toHaveBeenCalledWith({
      owner: 'polsala',
      repo: 'ApocalypsAI',
      commit_sha: 'mock_sha_pr_with_whimsy'
    });
    expect(core.setFailed).not.toHaveBeenCalled();
    expect(core.setOutput).toHaveBeenCalledWith('whimsy-detected', true);
  });

  test('fails if fetched commit message for PR event has no whimsy', async () => {
    when(core.getInput).calledWith('target-type', expect.anything()).mockReturnValue('commit_message');
    github.context.eventName = 'pull_request';
    github.context.payload.pull_request.head.sha = 'mock_sha_pr_no_whimsy';
    github.getOctokit().rest.git.getCommit.mockResolvedValueOnce({
      data: {
        message: 'chore: Update build script'
      }
    });
    await run();
    expect(github.getOctokit().rest.git.getCommit).toHaveBeenCalledWith({
      owner: 'polsala',
      repo: 'ApocalypsAI',
      commit_sha: 'mock_sha_pr_no_whimsy'
    });
    expect(core.setFailed).toHaveBeenCalledWith(expect.stringContaining('No whimsy detected.'));
    expect(core.setOutput).toHaveBeenCalledWith('whimsy-detected', false);
  });

  test('fails if github-token is missing when fetching commit message for PR', async () => {
    when(core.getInput).calledWith('target-type', expect.anything()).mockReturnValue('commit_message');
    when(core.getInput).calledWith('github-token', expect.anything()).mockReturnValue(''); // Mock rationale: Simulate missing token
    github.context.eventName = 'pull_request';
    github.context.payload.pull_request.head.sha = 'mock_sha_pr_no_token';
    await run();
    expect(core.setFailed).toHaveBeenCalledWith(expect.stringContaining('GITHUB_TOKEN is required to fetch commit messages for PRs'));
    expect(core.setOutput).not.toHaveBeenCalledWith('whimsy-detected', expect.any(Boolean));
  });
});
