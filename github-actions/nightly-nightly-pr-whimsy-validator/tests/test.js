const core = require('@actions/core');
const github = require('@actions/github');
const { when } = require('jest-when'); // For more flexible mocking

// Mock rationale: We need to mock GitHub Actions toolkit functions
// to prevent actual API calls and control input/output for deterministic testing.
jest.mock('@actions/core');
jest.mock('@actions/github');

// Mock the octokit rest API for comments
const mockCreateComment = jest.fn();
github.getOctokit.mockReturnValue({
  rest: {
    issues: {
      createComment: mockCreateComment,
    },
  },
});

describe('Nightly PR Whimsy Validator', () => {
  let run;

  beforeEach(() => {
    jest.clearAllMocks();
    // Mock rationale: Resetting mocks before each test ensures isolation.
    // We need to dynamically import `main.js` to ensure `run()` is re-evaluated
    // with fresh mocks for each test, as it's a top-level script.
    run = require('../src/main').run;

    // Mock rationale: Set default GitHub context for PR events.
    github.context = {
      payload: {
        pull_request: {
          number: 123,
          title: 'A delightful new feature!',
          body: 'This feature brings joy and sparkle to the application.',
        },
      },
      repo: {
        owner: 'test-owner',
        repo: 'test-repo',
      },
    };

    // Mock rationale: Provide default inputs for the action.
    when(core.getInput)
      .calledWith('github-token', expect.anything())
      .thenReturn('mock-token')
      .calledWith('whimsy-keywords')
      .thenReturn('sparkle, joy, delightful, cheerful, fantastic, wondrous, magical, whimsical, gleeful, radiant')
      .calledWith('grim-keywords')
      .thenReturn('bug, error, failure, broken, grim, despair, apocalypse, doom, catastrophe')
      .calledWith('min-whimsy-count')
      .thenReturn('1')
      .calledWith('fail-on-grim')
      .thenReturn('true');
  });

  test('should succeed when PR has enough whimsy and no grim words', async () => {
    await run();

    expect(core.setOutput).toHaveBeenCalledWith('whimsy-score', 3); // delightful, joy, sparkle
    expect(core.setOutput).toHaveBeenCalledWith('grim-found', false);
    expect(core.setOutput).toHaveBeenCalledWith('validation-status', 'success');
    expect(core.setFailed).not.toHaveBeenCalled();
    expect(core.warning).not.toHaveBeenCalled();
    expect(mockCreateComment).not.toHaveBeenCalled();
  });

  test('should warn when PR does not meet minimum whimsy count', async () => {
    github.context.payload.pull_request.title = 'A new feature.';
    github.context.payload.pull_request.body = 'This feature is good.';
    when(core.getInput).calledWith('min-whimsy-count').thenReturn('2');

    await run();

    expect(core.setOutput).toHaveBeenCalledWith('whimsy-score', 0);
    expect(core.setOutput).toHaveBeenCalledWith('grim-found', false);
    expect(core.setOutput).toHaveBeenCalledWith('validation-status', 'warning');
    expect(core.warning).toHaveBeenCalledWith(expect.stringContaining('PR does not meet minimum whimsy count (0/2).'));
    expect(mockCreateComment).toHaveBeenCalledWith(expect.objectContaining({
      body: expect.stringContaining('Your PR needs more sparkle! Found 0 whimsical keywords, but at least 2 are required.')
    }));
  });

  test('should fail when grim words are found and fail-on-grim is true', async () => {
    github.context.payload.pull_request.title = 'Fixing a critical bug.';
    github.context.payload.pull_request.body = 'This resolves a major error that caused despair.';
    when(core.getInput).calledWith('fail-on-grim').thenReturn('true');

    await run();

    expect(core.setOutput).toHaveBeenCalledWith('whimsy-score', 0);
    expect(core.setOutput).toHaveBeenCalledWith('grim-found', true);
    expect(core.setOutput).toHaveBeenCalledWith('validation-status', 'failure');
    expect(core.setFailed).toHaveBeenCalledWith(expect.stringContaining('Grim keywords found: bug, error, despair. Failing check as \'fail-on-grim\' is true.'));
    expect(mockCreateComment).toHaveBeenCalledWith(expect.objectContaining({
      body: expect.stringContaining('Grimness Detected! \uD83D\uDC80\n\nFound grim keywords: `bug`, `error`, `despair`. Let\'s keep things cheerful!')
    }));
  });

  test('should warn when grim words are found and fail-on-grim is false', async () => {
    github.context.payload.pull_request.title = 'Fixing a critical bug.';
    github.context.payload.pull_request.body = 'This resolves a major error that caused despair.';
    when(core.getInput).calledWith('fail-on-grim').thenReturn('false');

    await run();

    expect(core.setOutput).toHaveBeenCalledWith('whimsy-score', 0);
    expect(core.setOutput).toHaveBeenCalledWith('grim-found', true);
    expect(core.setOutput).toHaveBeenCalledWith('validation-status', 'warning');
    expect(core.warning).toHaveBeenCalledWith(expect.stringContaining('Grim keywords found: bug, error, despair. This is a warning.'));
    expect(core.setFailed).not.toHaveBeenCalled();
    expect(mockCreateComment).toHaveBeenCalledWith(expect.objectContaining({
      body: expect.stringContaining('Grimness Detected! \uD83D\uDC80\n\nFound grim keywords: `bug`, `error`, `despair`. Let\'s keep things cheerful!')
    }));
  });

  test('should handle empty PR title and body gracefully', async () => {
    github.context.payload.pull_request.title = '';
    github.context.payload.pull_request.body = '';
    when(core.getInput).calledWith('min-whimsy-count').thenReturn('1');

    await run();

    expect(core.setOutput).toHaveBeenCalledWith('whimsy-score', 0);
    expect(core.setOutput).toHaveBeenCalledWith('grim-found', false);
    expect(core.setOutput).toHaveBeenCalledWith('validation-status', 'warning');
    expect(core.warning).toHaveBeenCalledWith(expect.stringContaining('PR does not meet minimum whimsy count (0/1).'));
    expect(mockCreateComment).toHaveBeenCalled();
  });

  test('should handle no pull_request payload', async () => {
    github.context.payload.pull_request = undefined;

    await run();

    expect(core.setFailed).toHaveBeenCalledWith('This action only runs on pull_request events.');
    expect(core.setOutput).not.toHaveBeenCalled();
    expect(mockCreateComment).not.toHaveBeenCalled();
  });

  test('should handle case-insensitivity for keywords', async () => {
    github.context.payload.pull_request.title = 'A DELIGHTFUL feature with SPARKLE.';
    github.context.payload.pull_request.body = 'No GRIMness here.';

    await run();

    expect(core.setOutput).toHaveBeenCalledWith('whimsy-score', 2); // DELIGHTFUL, SPARKLE
    expect(core.setOutput).toHaveBeenCalledWith('grim-found', true); // GRIMness
    expect(core.setOutput).toHaveBeenCalledWith('validation-status', 'failure'); // fail-on-grim is true by default
    expect(core.setFailed).toHaveBeenCalledWith(expect.stringContaining('Grim keywords found: grim. Failing check as \'fail-on-grim\' is true.'));
  });

  test('should handle empty keyword lists', async () => {
    when(core.getInput).calledWith('whimsy-keywords').thenReturn('');
    when(core.getInput).calledWith('grim-keywords').thenReturn('');
    when(core.getInput).calledWith('min-whimsy-count').thenReturn('0'); // No whimsy required

    await run();

    expect(core.setOutput).toHaveBeenCalledWith('whimsy-score', 0);
    expect(core.setOutput).toHaveBeenCalledWith('grim-found', false);
    expect(core.setOutput).toHaveBeenCalledWith('validation-status', 'success');
    expect(core.setFailed).not.toHaveBeenCalled();
    expect(core.warning).not.toHaveBeenCalled();
    expect(mockCreateComment).not.toHaveBeenCalled();
  });

  test('should handle multiple occurrences of the same keyword', async () => {
    github.context.payload.pull_request.title = 'A delightful and delightful feature.';
    github.context.payload.pull_request.body = 'It brings joy, joy, and more joy!';
    when(core.getInput).calledWith('min-whimsy-count').thenReturn('5');

    await run();

    expect(core.setOutput).toHaveBeenCalledWith('whimsy-score', 5); // delightful (2), joy (3)
    expect(core.setOutput).toHaveBeenCalledWith('grim-found', false);
    expect(core.setOutput).toHaveBeenCalledWith('validation-status', 'success');
    expect(core.setFailed).not.toHaveBeenCalled();
    expect(core.warning).not.toHaveBeenCalled();
    expect(mockCreateComment).not.toHaveBeenCalled();
  });
});
