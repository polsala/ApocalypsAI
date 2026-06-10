const core = require('@actions/core');
const github = require('@actions/github');
const run = require('../src/index');

// Mock the GitHub Actions core library
let debugMock;
let warningMock;
let errorMock;
let infoMock;
let getInputMock;
let getBooleanInputMock;
let setFailedMock;
let setOutputMock;

// Mock the GitHub Actions github library
let getOctokitMock;
let createCommentMock;

describe('Nightly Lore Keeper Action', () => {
  beforeEach(() => {
    jest.clearAllMocks();

    debugMock = jest.spyOn(core, 'debug').mockImplementation();
    warningMock = jest.spyOn(core, 'warning').mockImplementation();
    errorMock = jest.spyOn(core, 'error').mockImplementation();
    infoMock = jest.spyOn(core, 'info').mockImplementation();
    getInputMock = jest.spyOn(core, 'getInput').mockImplementation();
    getBooleanInputMock = jest.spyOn(core, 'getBooleanInput').mockImplementation();
    setFailedMock = jest.spyOn(core, 'setFailed').mockImplementation();
    setOutputMock = jest.spyOn(core, 'setOutput').mockImplementation();

    createCommentMock = jest.fn();
    getOctokitMock = jest.spyOn(github, 'getOctokit').mockReturnValue({
      rest: {
        issues: {
          createComment: createCommentMock,
        },
      },
    });

    // Mock github.context
    github.context.repo = { owner: 'test-owner', repo: 'test-repo' };
    github.context.payload = {};
  });

  // Mock rationale:
  // - `@actions/core`: Mocked to control inputs, capture outputs, and verify error/info messages without actual console interaction or GitHub Actions runner environment.
  // - `@actions/github`: Mocked to simulate GitHub API interactions (like getting PR context and creating comments) without requiring a real GitHub token or network requests.

  test('should skip if not a pull_request event', async () => {
    // No pull_request in payload
    getInputMock.mockReturnValueOnce('mock-token'); // github-token
    getInputMock.mockReturnValueOnce('Lore'); // lore-keywords
    getBooleanInputMock.mockReturnValue(true); // check-pr-title, check-pr-body, fail-on-mismatch

    await run();

    expect(warningMock).toHaveBeenCalledWith('This action only runs on pull_request events. Skipping.');
    expect(setOutputMock).toHaveBeenCalledWith('lore-compliant', true);
    expect(setFailedMock).not.toHaveBeenCalled();
    expect(createCommentMock).not.toHaveBeenCalled();
  });

  test('should pass if all keywords are found in title and body', async () => {
    github.context.payload.pull_request = {
      number: 123,
      title: 'A new Temporal Anomaly detected in the Wasteland',
      body: 'This PR introduces changes related to a Void Whisper and Chronal Drift.',
    };
    getInputMock.mockReturnValueOnce('mock-token'); // github-token
    getInputMock.mockReturnValueOnce('Temporal Anomaly,Void Whisper,Wasteland,Chronal Drift'); // lore-keywords
    getBooleanInputMock.mockReturnValue(true); // check-pr-title
    getBooleanInputMock.mockReturnValue(true); // check-pr-body
    getBooleanInputMock.mockReturnValue(false); // fail-on-mismatch

    await run();

    expect(infoMock).toHaveBeenCalledWith('Lore compliance check passed. Your contribution resonates with the echoes of the void.');
    expect(setOutputMock).toHaveBeenCalledWith('lore-compliant', true);
    expect(setFailedMock).not.toHaveBeenCalled();
    expect(createCommentMock).not.toHaveBeenCalled();
  });

  test('should comment and not fail if keywords are missing and fail-on-mismatch is false', async () => {
    github.context.payload.pull_request = {
      number: 123,
      title: 'A new feature update',
      body: 'This PR fixes a bug.',
    };
    getInputMock.mockReturnValueOnce('mock-token'); // github-token
    getInputMock.mockReturnValueOnce('Temporal Anomaly,Void Whisper'); // lore-keywords
    getBooleanInputMock.mockReturnValue(true); // check-pr-title
    getBooleanInputMock.mockReturnValue(true); // check-pr-body
    getBooleanInputMock.mockReturnValue(false); // fail-on-mismatch

    await run();

    expect(setOutputMock).toHaveBeenCalledWith('lore-compliant', false);
    expect(setFailedMock).not.toHaveBeenCalled();
    expect(createCommentMock).toHaveBeenCalledTimes(1);
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      issue_number: 123,
      body: expect.stringContaining('Temporal Anomaly') && expect.stringContaining('Void Whisper'),
    });
  });

  test('should comment and fail if keywords are missing and fail-on-mismatch is true', async () => {
    github.context.payload.pull_request = {
      number: 123,
      title: 'Simple update',
      body: 'Just some code.',
    };
    getInputMock.mockReturnValueOnce('mock-token'); // github-token
    getInputMock.mockReturnValueOnce('Wasteland,Scavenger'); // lore-keywords
    getBooleanInputMock.mockReturnValue(true); // check-pr-title
    getBooleanInputMock.mockReturnValue(true); // check-pr-body
    getBooleanInputMock.mockReturnValue(true); // fail-on-mismatch

    await run();

    expect(setOutputMock).toHaveBeenCalledWith('lore-compliant', false);
    expect(setFailedMock).toHaveBeenCalledWith('Lore compliance check failed. Missing required lore keywords.');
    expect(createCommentMock).toHaveBeenCalledTimes(1);
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      issue_number: 123,
      body: expect.stringContaining('Wasteland') && expect.stringContaining('Scavenger'),
    });
  });

  test('should only check PR title if check-pr-body is false', async () => {
    github.context.payload.pull_request = {
      number: 123,
      title: 'Temporal Anomaly detected',
      body: 'This body contains Void Whisper but should not be checked.',
    };
    getInputMock.mockReturnValueOnce('mock-token'); // github-token
    getInputMock.mockReturnValueOnce('Temporal Anomaly,Void Whisper'); // lore-keywords
    getBooleanInputMock.mockReturnValue(true); // check-pr-title
    getBooleanInputMock.mockReturnValue(false); // check-pr-body
    getBooleanInputMock.mockReturnValue(false); // fail-on-mismatch

    await run();

    expect(setOutputMock).toHaveBeenCalledWith('lore-compliant', false);
    expect(createCommentMock).toHaveBeenCalledTimes(1);
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      issue_number: 123,
      body: expect.stringContaining('Void Whisper'), // Only Void Whisper should be missing as body is ignored
    });
    expect(setFailedMock).not.toHaveBeenCalled();
  });

  test('should only check PR body if check-pr-title is false', async () => {
    github.context.payload.pull_request = {
      number: 123,
      title: 'Title contains Temporal Anomaly but should not be checked.',
      body: 'A new Void Whisper is heard.',
    };
    getInputMock.mockReturnValueOnce('mock-token'); // github-token
    getInputMock.mockReturnValueOnce('Temporal Anomaly,Void Whisper'); // lore-keywords
    getBooleanInputMock.mockReturnValue(false); // check-pr-title
    getBooleanInputMock.mockReturnValue(true); // check-pr-body
    getBooleanInputMock.mockReturnValue(false); // fail-on-mismatch

    await run();

    expect(setOutputMock).toHaveBeenCalledWith('lore-compliant', false);
    expect(createCommentMock).toHaveBeenCalledTimes(1);
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      issue_number: 123,
      body: expect.stringContaining('Temporal Anomaly'), // Only Temporal Anomaly should be missing as title is ignored
    });
    expect(setFailedMock).not.toHaveBeenCalled();
  });

  test('should handle empty lore-keywords gracefully', async () => {
    github.context.payload.pull_request = {
      number: 123,
      title: 'Any title',
      body: 'Any body',
    };
    getInputMock.mockReturnValueOnce('mock-token'); // github-token
    getInputMock.mockReturnValueOnce(''); // lore-keywords
    getBooleanInputMock.mockReturnValue(true); // check-pr-title
    getBooleanInputMock.mockReturnValue(true); // check-pr-body
    getBooleanInputMock.mockReturnValue(false); // fail-on-mismatch

    await run();

    expect(infoMock).toHaveBeenCalledWith('Lore compliance check passed. Your contribution resonates with the echoes of the void.');
    expect(setOutputMock).toHaveBeenCalledWith('lore-compliant', true);
    expect(setFailedMock).not.toHaveBeenCalled();
    expect(createCommentMock).not.toHaveBeenCalled();
  });

  test('should handle regex keywords', async () => {
    github.context.payload.pull_request = {
      number: 123,
      title: 'A new Temporal Anomaly [v1.0] detected',
      body: 'This PR introduces changes related to a Void Whisper and Chronal Drift.',
    };
    getInputMock.mockReturnValueOnce('mock-token'); // github-token
    getInputMock.mockReturnValueOnce('Temporal Anomaly \[v[0-9]\.[0-9]\]|Void Whisper'); // lore-keywords with regex
    getBooleanInputMock.mockReturnValue(true); // check-pr-title
    getBooleanInputMock.mockReturnValue(true); // check-pr-body
    getBooleanInputMock.mockReturnValue(false); // fail-on-mismatch

    await run();

    expect(infoMock).toHaveBeenCalledWith('Lore compliance check passed. Your contribution resonates with the echoes of the void.');
    expect(setOutputMock).toHaveBeenCalledWith('lore-compliant', true);
    expect(setFailedMock).not.toHaveBeenCalled();
    expect(createCommentMock).not.toHaveBeenCalled();
  });

  test('should fail on error', async () => {
    getInputMock.mockImplementation(() => {
      throw new Error('Test error');
    });

    await run();

    expect(setFailedMock).toHaveBeenCalledWith('Test error');
    expect(setOutputMock).not.toHaveBeenCalledWith('lore-compliant', expect.any(Boolean));
  });
});
