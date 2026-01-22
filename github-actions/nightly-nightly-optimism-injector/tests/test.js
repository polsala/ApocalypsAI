const core = require('@actions/core');
const github = require('@actions/github');
const { when } = require('jest-when');

// Mock the GitHub Actions toolkit
jest.mock('@actions/core');
jest.mock('@actions/github');

const run = require('../src/main'); // Assuming main.js is in src/

describe('Nightly Optimism Injector', () => {
  let createCommentMock;

  beforeEach(() => {
    jest.clearAllMocks();

    // Mock core.getInput
    when(core.getInput)
      .calledWith('github-token')
      .mockReturnValue('mock-token');
    when(core.getInput)
      .calledWith('optimism-messages')
      .mockReturnValue('Hope is a good thing!\nKeep pushing!\nEvery byte counts!');
    when(core.getInput)
      .calledWith('negative-keywords')
      .mockReturnValue('fail,broken,despair');
    when(core.getInput)
      .calledWith('threshold')
      .mockReturnValue('1');

    // Mock github.getOctokit
    createCommentMock = jest.fn();
    github.getOctokit.mockReturnValue({
      rest: {
        issues: {
          createComment: createCommentMock,
        },
      },
    });

    // Mock Math.random to make tests deterministic
    jest.spyOn(Math, 'random').mockReturnValue(0.5); // Will always pick the middle message
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  // Mock rationale: We need to simulate different GitHub event payloads (PRs, Issues)
  // and the GitHub API calls (createComment) without making actual network requests.
  // This ensures tests are fast, deterministic, and isolated.

  test('should inject optimism for a PR with negative sentiment', async () => {
    github.context.payload = {
      pull_request: {
        number: 123,
        title: 'Fix: This feature is broken and will fail',
        body: 'I am in despair over this bug.',
      },
      repo: {
        owner: 'polsala',
        repo: 'ApocalypsAI',
      },
    };

    await run();

    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Detected 3 negative keywords. Threshold is 1.'));
    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Injecting optimism: "Keep pushing!"'));
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'polsala',
      repo: 'ApocalypsAI',
      issue_number: 123,
      body: '_A Glimmer of Optimism from ApocalypsAI_:\n\nKeep pushing!',
    });
    expect(core.setOutput).toHaveBeenCalledWith('optimism-injected', 'true');
  });

  test('should inject optimism for an Issue with negative sentiment', async () => {
    github.context.payload = {
      issue: {
        number: 456,
        title: 'Bug: This is a complete failure',
        body: 'The system is broken beyond repair.',
      },
      repo: {
        owner: 'polsala',
        repo: 'ApocalypsAI',
      },
    };

    await run();

    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Detected 2 negative keywords. Threshold is 1.'));
    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Injecting optimism: "Keep pushing!"'));
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'polsala',
      repo: 'ApocalypsAI',
      issue_number: 456,
      body: '_A Glimmer of Optimism from ApocalypsAI_:\n\nKeep pushing!',
    });
    expect(core.setOutput).toHaveBeenCalledWith('optimism-injected', 'true');
  });

  test('should not inject optimism if no negative sentiment is detected', async () => {
    github.context.payload = {
      pull_request: {
        number: 789,
        title: 'Feat: Add new amazing functionality',
        body: 'This will improve everything!',
      },
      repo: {
        owner: 'polsala',
        repo: 'ApocalypsAI',
      },
    };

    await run();

    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Detected 0 negative keywords. Threshold is 1.'));
    expect(core.info).toHaveBeenCalledWith('No significant negative sentiment detected. No optimism injected.');
    expect(createCommentMock).not.toHaveBeenCalled();
    expect(core.setOutput).toHaveBeenCalledWith('optimism-injected', 'false');
  });

  test('should not inject optimism if negative keywords are below threshold', async () => {
    when(core.getInput)
      .calledWith('threshold')
      .mockReturnValue('2'); // Set threshold to 2

    github.context.payload = {
      pull_request: {
        number: 101,
        title: 'Bug: This is a failure', // Only one negative keyword
        body: 'It needs fixing.',
      },
      repo: {
        owner: 'polsala',
        repo: 'ApocalypsAI',
      },
    };

    await run();

    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Detected 1 negative keywords. Threshold is 2.'));
    expect(core.info).toHaveBeenCalledWith('No significant negative sentiment detected. No optimism injected.');
    expect(createCommentMock).not.toHaveBeenCalled();
    expect(core.setOutput).toHaveBeenCalledWith('optimism-injected', 'false');
  });

  test('should handle empty body gracefully', async () => {
    github.context.payload = {
      pull_request: {
        number: 112,
        title: 'Bug: This is broken',
        body: null, // Empty body
      },
      repo: {
        owner: 'polsala',
        repo: 'ApocalypsAI',
      },
    };

    await run();

    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Detected 1 negative keywords. Threshold is 1.'));
    expect(createCommentMock).toHaveBeenCalled();
    expect(core.setOutput).toHaveBeenCalledWith('optimism-injected', 'true');
  });

  test('should handle non-PR/Issue events gracefully', async () => {
    github.context.payload = {
      push: {
        ref: 'refs/heads/main',
      },
      repo: {
        owner: 'polsala',
        repo: 'ApocalypsAI',
      },
    };

    await run();

    expect(core.info).toHaveBeenCalledWith('This action only runs on pull_request or issue events. Skipping.');
    expect(createCommentMock).not.toHaveBeenCalled();
    expect(core.setOutput).not.toHaveBeenCalled(); // No output set if skipped
  });

  test('should handle action failure', async () => {
    createCommentMock.mockImplementation(() => {
      throw new Error('API Error');
    });

    github.context.payload = {
      pull_request: {
        number: 123,
        title: 'Fix: This feature is broken and will fail',
        body: 'I am in despair over this bug.',
      },
      repo: {
        owner: 'polsala',
        repo: 'ApocalypsAI',
      },
    };

    await run();

    expect(core.setFailed).toHaveBeenCalledWith('API Error');
  });
});
