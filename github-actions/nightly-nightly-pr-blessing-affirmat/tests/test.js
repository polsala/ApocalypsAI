const core = require('@actions/core');
const github = require('@actions/github');
const { when } = require('jest-when');

// Mock the @actions/core and @actions/github modules
jest.mock('@actions/core');
jest.mock('@actions/github');

const run = require('../src/main'); // The actual action logic

describe('PR Blessing Affirmation Action', () => {
  let createCommentMock;
  let listForRefMock;

  beforeEach(() => {
    jest.clearAllMocks();

    // Mock core functions
    core.getInput.mockReturnValue('mock-token'); // Mock github-token input
    core.info.mockImplementation(console.log); // Log info messages for debugging
    core.warning.mockImplementation(console.warn); // Log warning messages
    core.setFailed.mockImplementation(console.error); // Log errors

    // Mock github.getOctokit().rest.issues.createComment
    createCommentMock = jest.fn();
    // Mock github.getOctokit().rest.checks.listForRef
    listForRefMock = jest.fn();

    github.getOctokit.mockReturnValue({
      rest: {
        issues: {
          createComment: createCommentMock,
        },
        checks: {
          listForRef: listForRefMock,
        },
      },
    });

    // Mock Math.random to ensure deterministic affirmation selection for tests
    // Mock rationale: Ensures that the random affirmation selection is predictable for testing purposes.
    jest.spyOn(Math, 'random').mockReturnValue(0.0); // Always pick the first affirmation
  });

  afterEach(() => {
    jest.restoreAllMocks(); // Restore Math.random
  });

  // Mock rationale: We need to simulate different GitHub event payloads and API responses
  // without making actual network requests. This ensures tests are fast, deterministic,
  // and isolated from external factors.

  test('should not post comment if PR is not merged', async () => {
    github.context.eventName = 'pull_request';
    github.context.payload = {
      pull_request: {
        number: 1,
        merged: false,
        head: { sha: 'abcdef' },
      },
    };

    await run();

    expect(core.info).toHaveBeenCalledWith('PR is not merged. No affirmation needed.');
    expect(createCommentMock).not.toHaveBeenCalled();
    expect(core.setOutput).not.toHaveBeenCalled();
  });

  test('should not post comment if no check runs are found and not merged', async () => {
    github.context.eventName = 'pull_request';
    github.context.payload = {
      pull_request: {
        number: 1,
        merged: false,
        head: { sha: 'abcdef' },
      },
    };
    // Mock rationale: Simulates an API response where no check runs exist for the given ref.
    listForRefMock.mockResolvedValue({ data: { check_runs: [] } });

    await run();

    expect(core.info).toHaveBeenCalledWith('PR is not merged. No affirmation needed.');
    expect(createCommentMock).not.toHaveBeenCalled();
    expect(core.setOutput).not.toHaveBeenCalled();
  });

  test('should post comment if PR is merged and all checks pass', async () => {
    github.context.eventName = 'pull_request';
    github.context.payload = {
      repo: { owner: 'polsala', repo: 'ApocalypsAI' },
      pull_request: {
        number: 123,
        merged: true,
        head: { sha: 'testsha123' },
      },
    };

    // Mock rationale: Simulates an API response where all check runs are completed successfully.
    listForRefMock.mockResolvedValue({
      data: {
        check_runs: [
          { name: 'build', status: 'completed', conclusion: 'success' },
          { name: 'test', status: 'completed', conclusion: 'success' },
        ],
      },
    });

    await run();

    expect(listForRefMock).toHaveBeenCalledWith({
      owner: 'polsala',
      repo: 'ApocalypsAI',
      ref: 'testsha123',
    });
    expect(createCommentMock).toHaveBeenCalledTimes(1);
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'polsala',
      repo: 'ApocalypsAI',
      issue_number: 123,
      body: "**ApocalypsAI Blessing:** The void acknowledges your diligence. Well merged, survivor!",
    });
    expect(core.setOutput).toHaveBeenCalledWith('affirmation-message', "The void acknowledges your diligence. Well merged, survivor!");
  });

  test('should not post comment if PR is merged but some checks fail', async () => {
    github.context.eventName = 'pull_request';
    github.context.payload = {
      repo: { owner: 'polsala', repo: 'ApocalypsAI' },
      pull_request: {
        number: 124,
        merged: true,
        head: { sha: 'testsha124' },
      },
    };

    // Mock rationale: Simulates an API response where one check run has failed.
    listForRefMock.mockResolvedValue({
      data: {
        check_runs: [
          { name: 'build', status: 'completed', conclusion: 'success' },
          { name: 'test', status: 'completed', conclusion: 'failure' },
        ],
      },
    });

    await run();

    expect(listForRefMock).toHaveBeenCalledTimes(1);
    expect(core.warning).toHaveBeenCalledWith(expect.stringContaining("Check 'test' failed or was not successful"));
    expect(core.info).toHaveBeenCalledWith('Not all checks passed successfully. No affirmation posted.');
    expect(createCommentMock).not.toHaveBeenCalled();
    expect(core.setOutput).not.toHaveBeenCalled();
  });

  test('should not post comment if PR is merged but checks are still in progress', async () => {
    github.context.eventName = 'pull_request';
    github.context.payload = {
      repo: { owner: 'polsala', repo: 'ApocalypsAI' },
      pull_request: {
        number: 125,
        merged: true,
        head: { sha: 'testsha125' },
      },
    };

    // Mock rationale: Simulates an API response where one check run is still in progress.
    listForRefMock.mockResolvedValue({
      data: {
        check_runs: [
          { name: 'build', status: 'completed', conclusion: 'success' },
          { name: 'deploy', status: 'in_progress', conclusion: null },
        ],
      },
    });

    await run();

    expect(listForRefMock).toHaveBeenCalledTimes(1);
    expect(core.warning).toHaveBeenCalledWith(expect.stringContaining("Check 'deploy' is still 'in_progress'"));
    expect(core.info).toHaveBeenCalledWith('Not all checks passed successfully. No affirmation posted.');
    expect(createCommentMock).not.toHaveBeenCalled();
    expect(core.setOutput).not.toHaveBeenCalled();
  });

  test('should handle API errors gracefully', async () => {
    github.context.eventName = 'pull_request';
    github.context.payload = {
      repo: { owner: 'polsala', repo: 'ApocalypsAI' },
      pull_request: {
        number: 126,
        merged: true,
        head: { sha: 'testsha126' },
      },
    };

    const errorMessage = 'GitHub API error';
    // Mock rationale: Simulates a network or API error during the check runs fetch.
    listForRefMock.mockRejectedValue(new Error(errorMessage));

    await run();

    expect(listForRefMock).toHaveBeenCalledTimes(1);
    expect(core.setFailed).toHaveBeenCalledWith(errorMessage);
    expect(createCommentMock).not.toHaveBeenCalled();
    expect(core.setOutput).not.toHaveBeenCalled();
  });

  test('should warn and bless if no check runs are found but PR is merged', async () => {
    github.context.eventName = 'pull_request';
    github.context.payload = {
      repo: { owner: 'polsala', repo: 'ApocalypsAI' },
      pull_request: {
        number: 127,
        merged: true,
        head: { sha: 'testsha127' },
      },
    };

    // Mock rationale: Simulates an API response where no check runs exist for the given ref.
    listForRefMock.mockResolvedValue({ data: { check_runs: [] } });

    await run();

    expect(listForRefMock).toHaveBeenCalledTimes(1);
    expect(core.warning).toHaveBeenCalledWith('No check runs found for this commit. Assuming success for blessing.');
    expect(createCommentMock).toHaveBeenCalledTimes(1);
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'polsala',
      repo: 'ApocalypsAI',
      issue_number: 127,
      body: "**ApocalypsAI Blessing:** The void acknowledges your diligence. Well merged, survivor!",
    });
    expect(core.setOutput).toHaveBeenCalledWith('affirmation-message', "The void acknowledges your diligence. Well merged, survivor!");
  });

  test('should not run if not a pull_request event', async () => {
    github.context.eventName = 'push';
    github.context.payload = {};

    await run();

    expect(core.warning).toHaveBeenCalledWith('This action only runs on pull_request events.');
    expect(createCommentMock).not.toHaveBeenCalled();
    expect(listForRefMock).not.toHaveBeenCalled();
    expect(core.setOutput).not.toHaveBeenCalled();
  });
});
