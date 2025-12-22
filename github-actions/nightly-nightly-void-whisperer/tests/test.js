const core = require('@actions/core');
const github = require('@actions/github');
const { when } = require('jest-when'); // For more specific mocking

// Mock the GitHub Actions toolkit
jest.mock('@actions/core');
jest.mock('@actions/github');

const run = require('../src/main'); // Assuming main.js is the entry point

describe('Nightly Void Whisperer', () => {
  let createCommentMock;
  let listCommentsMock;
  let listPullsMock;

  beforeEach(() => {
    jest.clearAllMocks();

    // Mock core inputs
    when(core.getInput)
      .calledWith('github-token', expect.anything())
      .mockReturnValue('mock-token');
    when(core.getInput)
      .calledWith('messages')
      .mockReturnValue(`"Whisper 1"\n"Whisper 2"`);
    when(core.getBooleanInput)
      .calledWith('trigger-on-first-pr')
      .mockReturnValue(false); // Default to false for most tests
    when(core.getBooleanInput)
      .calledWith('trigger-on-no-comments')
      .mockReturnValue(true); // Default to true for most tests

    // Mock github context
    github.context = {
      repo: {
        owner: 'test-owner',
        repo: 'test-repo',
      },
      payload: {
        pull_request: {
          number: 123,
          user: { login: 'test-user', type: 'User' },
        },
      },
    };

    // Mock Octokit API calls
    createCommentMock = jest.fn();
    listCommentsMock = jest.fn();
    listPullsMock = jest.fn();

    github.getOctokit.mockReturnValue({
      rest: {
        issues: {
          createComment: createCommentMock,
          listComments: listCommentsMock,
        },
        pulls: {
          list: listPullsMock,
        },
      },
    });

    // Mock Math.random to make tests deterministic
    jest.spyOn(Math, 'random').mockReturnValue(0.5); // Always pick the second message
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  // Mock rationale:
  // @actions/core: Mocks input/output functions to control action parameters and capture outputs without actual GitHub interaction.
  // @actions/github: Mocks the GitHub context and Octokit client to simulate repository events and API responses, ensuring tests are offline and deterministic.
  // Octokit API calls (createComment, listComments, listPulls): Mocks these specific API methods to control the data returned by GitHub and verify interactions.
  // Math.random: Mocks the random number generator to ensure a predictable message is chosen from the list, making tests deterministic.

  test('should whisper if no human comments and not first PR', async () => {
    listCommentsMock.mockResolvedValue({ data: [{ user: { type: 'Bot' }, body: 'Bot comment' }] }); // Only bot comments
    listPullsMock.mockResolvedValue({ data: [{ number: 122, user: { login: 'test-user' } }] }); // User has previous PRs

    await run();

    expect(listCommentsMock).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      issue_number: 123,
    });
    expect(listPullsMock).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      state: 'all',
      creator: 'test-user',
    });
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      issue_number: 123,
      body: 'Whisper 2', // Due to Math.random mock
    });
    expect(core.setOutput).toHaveBeenCalledWith('whispered', 'true');
    expect(core.setOutput).toHaveBeenCalledWith('message', 'Whisper 2');
  });

  test('should not whisper if human comments exist and trigger-on-no-comments is true', async () => {
    listCommentsMock.mockResolvedValue({ data: [{ user: { type: 'User' }, body: 'Human comment' }] });
    when(core.getBooleanInput).calledWith('trigger-on-no-comments').mockReturnValue(true);

    await run();

    expect(listCommentsMock).toHaveBeenCalled();
    expect(createCommentMock).not.toHaveBeenCalled();
    expect(core.setOutput).toHaveBeenCalledWith('whispered', 'false');
  });

  test('should whisper if human comments exist but trigger-on-no-comments is false', async () => {
    listCommentsMock.mockResolvedValue({ data: [{ user: { type: 'User' }, body: 'Human comment' }] });
    when(core.getBooleanInput).calledWith('trigger-on-no-comments').mockReturnValue(false);
    when(core.getBooleanInput).calledWith('trigger-on-first-pr').mockReturnValue(false); // Ensure this is false to not block

    await run();

    expect(listCommentsMock).not.toHaveBeenCalled(); // Because triggerOnNoComments is false
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      issue_number: 123,
      body: 'Whisper 2',
    });
    expect(core.setOutput).toHaveBeenCalledWith('whispered', 'true');
  });

  test('should whisper if first-time contributor and trigger-on-first-pr is true', async () => {
    when(core.getBooleanInput).calledWith('trigger-on-first-pr').mockReturnValue(true);
    when(core.getBooleanInput).calledWith('trigger-on-no-comments').mockReturnValue(false); // Don't block on comments
    listPullsMock.mockResolvedValue({ data: [] }); // No previous PRs

    await run();

    expect(listPullsMock).toHaveBeenCalled();
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      issue_number: 123,
      body: 'Whisper 2',
    });
    expect(core.setOutput).toHaveBeenCalledWith('whispered', 'true');
  });

  test('should not whisper if not first-time contributor and trigger-on-first-pr is true', async () => {
    when(core.getBooleanInput).calledWith('trigger-on-first-pr').mockReturnValue(true);
    when(core.getBooleanInput).calledWith('trigger-on-no-comments').mockReturnValue(false); // Don't block on comments
    listPullsMock.mockResolvedValue({ data: [{ number: 122, user: { login: 'test-user' } }] }); // User has previous PRs

    await run();

    expect(listPullsMock).toHaveBeenCalled();
    expect(createCommentMock).not.toHaveBeenCalled();
    expect(core.setOutput).toHaveBeenCalledWith('whispered', 'false');
  });

  test('should handle empty messages input gracefully', async () => {
    when(core.getInput).calledWith('messages').mockReturnValue('');

    await run();

    expect(core.warning).toHaveBeenCalledWith('No messages provided. Skipping.');
    expect(createCommentMock).not.toHaveBeenCalled();
    expect(core.setOutput).not.toHaveBeenCalledWith('whispered', expect.any(String)); // No output if skipped
  });

  test('should set failed status on error', async () => {
    listCommentsMock.mockRejectedValue(new Error('API Error'));

    await run();

    expect(core.setFailed).toHaveBeenCalledWith('API Error');
    expect(createCommentMock).not.toHaveBeenCalled();
  });

  test('should whisper if both trigger-on-first-pr and trigger-on-no-comments are true and conditions met', async () => {
    when(core.getBooleanInput).calledWith('trigger-on-first-pr').mockReturnValue(true);
    when(core.getBooleanInput).calledWith('trigger-on-no-comments').mockReturnValue(true);
    listCommentsMock.mockResolvedValue({ data: [{ user: { type: 'Bot' }, body: 'Bot comment' }] }); // No human comments
    listPullsMock.mockResolvedValue({ data: [] }); // First-time contributor

    await run();

    expect(listCommentsMock).toHaveBeenCalled();
    expect(listPullsMock).toHaveBeenCalled();
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      issue_number: 123,
      body: 'Whisper 2',
    });
    expect(core.setOutput).toHaveBeenCalledWith('whispered', 'true');
  });

  test('should not whisper if trigger-on-first-pr is true but not first-time contributor', async () => {
    when(core.getBooleanInput).calledWith('trigger-on-first-pr').mockReturnValue(true);
    when(core.getBooleanInput).calledWith('trigger-on-no-comments').mockReturnValue(true);
    listCommentsMock.mockResolvedValue({ data: [{ user: { type: 'Bot' }, body: 'Bot comment' }] }); // No human comments
    listPullsMock.mockResolvedValue({ data: [{ number: 122, user: { login: 'test-user' } }] }); // Not first-time

    await run();

    expect(listCommentsMock).toHaveBeenCalled();
    expect(listPullsMock).toHaveBeenCalled();
    expect(createCommentMock).not.toHaveBeenCalled();
    expect(core.setOutput).toHaveBeenCalledWith('whispered', 'false');
  });

  test('should not whisper if trigger-on-no-comments is true but human comments exist', async () => {
    when(core.getBooleanInput).calledWith('trigger-on-first-pr').mockReturnValue(true);
    when(core.getBooleanInput).calledWith('trigger-on-no-comments').mockReturnValue(true);
    listCommentsMock.mockResolvedValue({ data: [{ user: { type: 'User' }, body: 'Human comment' }] }); // Human comments exist
    listPullsMock.mockResolvedValue({ data: [] }); // First-time contributor (this check will be skipped if no-comments fails)

    await run();

    expect(listCommentsMock).toHaveBeenCalled();
    expect(listPullsMock).not.toHaveBeenCalled(); // Because no-comments condition failed first
    expect(createCommentMock).not.toHaveBeenCalled();
    expect(core.setOutput).toHaveBeenCalledWith('whispered', 'false');
  });
});
