const core = require('@actions/core');
const github = require('@actions/github');
const run = require('../src/index');

// Mock the GitHub Actions core library
let getInputMock;
let setOutputMock;
let setFailedMock;
let infoMock;

// Mock the GitHub Actions github library
let createCommentMock;

describe('Cosmic PR Aligner', () => {
  beforeEach(() => {
    jest.clearAllMocks();

    getInputMock = jest.spyOn(core, 'getInput').mockImplementation((name) => {
      switch (name) {
        case 'github-token': return 'mock-token';
        case 'aligned-keywords': return 'feat,fix,stellar';
        case 'misaligned-keywords': return 'WIP,ugh,broken';
        case 'alignment-threshold': return '1';
        case 'misalignment-threshold': return '1';
        case 'comment-on-alignment': return 'true';
        case 'comment-on-misalignment': return 'true';
        default: return '';
      }
    });
    setOutputMock = jest.spyOn(core, 'setOutput');
    setFailedMock = jest.spyOn(core, 'setFailed');
    infoMock = jest.spyOn(core, 'info');

    createCommentMock = jest.fn();
    jest.spyOn(github, 'getOctokit').mockImplementation(() => ({
      rest: {
        issues: {
          createComment: createCommentMock,
        },
      },
    }));

    // Mock rationale: We need to simulate the GitHub context for a pull request event.
    // This includes the repository information and the pull request payload itself.
    github.context.repo = { owner: 'test-owner', repo: 'test-repo' };
    github.context.payload = {
      pull_request: {
        number: 123,
        title: 'feat: Add new cosmic feature',
        body: 'This is a stellar new feature.',
      },
    };
  });

  test('sets is-aligned to true and comments for an aligned PR', async () => {
    await run();

    expect(setOutputMock).toHaveBeenCalledWith('is-aligned', true);
    expect(createCommentMock).toHaveBeenCalledTimes(1);
    expect(createCommentMock).toHaveBeenCalledWith(expect.objectContaining({
      issue_number: 123,
      body: expect.stringContaining('Stellar Contribution Detected!'),
    }));
    expect(setFailedMock).not.toHaveBeenCalled();
  });

  test('sets is-aligned to false and comments for a misaligned PR', async () => {
    github.context.payload.pull_request.title = 'WIP: Work in progress';
    github.context.payload.pull_request.body = 'Ugh, this is broken.';

    await run();

    expect(setOutputMock).toHaveBeenCalledWith('is-aligned', false);
    expect(createCommentMock).toHaveBeenCalledTimes(1);
    expect(createCommentMock).toHaveBeenCalledWith(expect.objectContaining({
      issue_number: 123,
      body: expect.stringContaining('Cosmic Alignment Alert!'),
    }));
    expect(setFailedMock).not.toHaveBeenCalled();
  });

  test('sets is-aligned to false and comments for a neutral PR (no strong alignment/misalignment)', async () => {
    github.context.payload.pull_request.title = 'Update documentation';
    github.context.payload.pull_request.body = 'Just a simple update.';

    await run();

    expect(setOutputMock).toHaveBeenCalledWith('is-aligned', false);
    expect(createCommentMock).toHaveBeenCalledTimes(1);
    expect(createCommentMock).toHaveBeenCalledWith(expect.objectContaining({
      issue_number: 123,
      body: expect.stringContaining('A Whisper from the Void'),
    }));
    expect(setFailedMock).not.toHaveBeenCalled();
  });

  test('does not comment if comment-on-alignment is false', async () => {
    getInputMock.mockImplementation((name) => {
      if (name === 'comment-on-alignment') return 'false';
      if (name === 'github-token') return 'mock-token';
      if (name === 'aligned-keywords') return 'feat,fix,stellar';
      if (name === 'misaligned-keywords') return 'WIP,ugh,broken';
      if (name === 'alignment-threshold') return '1';
      if (name === 'misalignment-threshold') return '1';
      if (name === 'comment-on-misalignment') return 'true';
      return '';
    });

    await run();

    expect(setOutputMock).toHaveBeenCalledWith('is-aligned', true);
    expect(createCommentMock).not.toHaveBeenCalled();
  });

  test('does not comment if comment-on-misalignment is false', async () => {
    github.context.payload.pull_request.title = 'WIP: Work in progress';
    github.context.payload.pull_request.body = 'Ugh, this is broken.';
    getInputMock.mockImplementation((name) => {
      if (name === 'comment-on-misalignment') return 'false';
      if (name === 'github-token') return 'mock-token';
      if (name === 'aligned-keywords') return 'feat,fix,stellar';
      if (name === 'misaligned-keywords') return 'WIP,ugh,broken';
      if (name === 'alignment-threshold') return '1';
      if (name === 'misalignment-threshold') return '1';
      if (name === 'comment-on-alignment') return 'true';
      return '';
    });

    await run();

    expect(setOutputMock).toHaveBeenCalledWith('is-aligned', false);
    expect(createCommentMock).not.toHaveBeenCalled();
  });

  test('handles missing pull_request payload gracefully', async () => {
    github.context.payload.pull_request = undefined;

    await run();

    expect(setFailedMock).toHaveBeenCalledWith('This action only runs on pull_request events.');
    expect(setOutputMock).not.toHaveBeenCalled();
    expect(createCommentMock).not.toHaveBeenCalled();
  });

  test('handles errors during execution', async () => {
    getInputMock.mockImplementation(() => { throw new Error('Test error'); });

    await run();

    expect(setFailedMock).toHaveBeenCalledWith('Test error');
    expect(setOutputMock).not.toHaveBeenCalled();
    expect(createCommentMock).not.toHaveBeenCalled();
  });

  test('handles multiple aligned keywords', async () => {
    github.context.payload.pull_request.title = 'feat: A stellar new feature';
    github.context.payload.pull_request.body = 'This is a truly stellar contribution.';

    await run();

    expect(setOutputMock).toHaveBeenCalledWith('is-aligned', true);
    expect(createCommentMock).toHaveBeenCalledTimes(1);
  });

  test('handles multiple misaligned keywords', async () => {
    github.context.payload.pull_request.title = 'WIP: Broken and ugh';
    github.context.payload.pull_request.body = 'This is a broken WIP.';

    await run();

    expect(setOutputMock).toHaveBeenCalledWith('is-aligned', false);
    expect(createCommentMock).toHaveBeenCalledTimes(1);
  });

  test('prioritizes misalignment over alignment if both present', async () => {
    github.context.payload.pull_request.title = 'feat: WIP stellar feature';
    github.context.payload.pull_request.body = 'This is a broken but stellar contribution.';

    await run();

    expect(setOutputMock).toHaveBeenCalledWith('is-aligned', false);
    expect(createCommentMock).toHaveBeenCalledTimes(1);
    expect(createCommentMock).toHaveBeenCalledWith(expect.objectContaining({
      issue_number: 123,
      body: expect.stringContaining('Cosmic Alignment Alert!'),
    }));
  });

  test('handles empty body gracefully', async () => {
    github.context.payload.pull_request.title = 'feat: New feature';
    github.context.payload.pull_request.body = null;

    await run();

    expect(setOutputMock).toHaveBeenCalledWith('is-aligned', true);
    expect(createCommentMock).toHaveBeenCalledTimes(1);
  });

  test('handles custom thresholds', async () => {
    getInputMock.mockImplementation((name) => {
      if (name === 'alignment-threshold') return '2';
      if (name === 'misalignment-threshold') return '2';
      if (name === 'github-token') return 'mock-token';
      if (name === 'aligned-keywords') return 'feat,fix,stellar';
      if (name === 'misaligned-keywords') return 'WIP,ugh,broken';
      if (name === 'comment-on-alignment') return 'true';
      if (name === 'comment-on-misalignment') return 'true';
      return '';
    });

    // PR with 1 aligned keyword, below threshold 2
    github.context.payload.pull_request.title = 'feat: New feature';
    github.context.payload.pull_request.body = 'Simple change.';
    await run();
    expect(setOutputMock).toHaveBeenCalledWith('is-aligned', false);
    expect(createCommentMock).toHaveBeenCalledWith(expect.objectContaining({
      body: expect.stringContaining('A Whisper from the Void'),
    }));
    createCommentMock.mockClear();
    setOutputMock.mockClear();

    // PR with 2 aligned keywords, meets threshold 2
    github.context.payload.pull_request.title = 'feat: Stellar new feature';
    github.context.payload.pull_request.body = 'This is a simple change.';
    await run();
    expect(setOutputMock).toHaveBeenCalledWith('is-aligned', true);
    expect(createCommentMock).toHaveBeenCalledWith(expect.objectContaining({
      body: expect.stringContaining('Stellar Contribution Detected!'),
    }));
  });
});
