const core = require('@actions/core');
const github = require('@actions/github');
const { run } = require('../src/main');
const haikus = require('../src/haikus.json');

describe('Nightly Merge Haiku Herald', () => {
  let getInputMock;
  let setFailedMock;
  let setOutputMock;
  let infoMock;
  let createCommentMock;
  let graphqlMock;

  beforeEach(() => {
    jest.clearAllMocks();
    jest.resetModules(); // Reset modules before each test to ensure fresh imports

    getInputMock = jest.spyOn(core, 'getInput').mockImplementation((name, options) => {
      if (name === 'github-token') return 'mock-token';
      if (name === 'target-type') return 'issue';
      if (name === 'target-id') return '123';
      return '';
    });
    setFailedMock = jest.spyOn(core, 'setFailed').mockImplementation(() => {});
    setOutputMock = jest.spyOn(core, 'setOutput').mockImplementation(() => {});
    infoMock = jest.spyOn(core, 'info').mockImplementation(() => {});

    createCommentMock = jest.fn();
    graphqlMock = jest.fn().mockImplementation((query, variables) => {
      // Mock rationale: Simulate GraphQL responses for discussion ID lookup and comment creation.
      if (query.includes('query($owner: String!, $repo: String!, $discussionNumber: Int!)')) {
        return Promise.resolve({
          repository: {
            discussion: {
              id: 'D_kwDOJ_w_c84AAa_A' // Mock discussion node ID
            }
          }
        });
      }
      if (query.includes('mutation($discussionId: ID!, $body: String!)')) {
        return Promise.resolve({
          addDiscussionComment: {
            comment: {
              id: 'DIC_kwDOJ_w_c84AAa_B' // Mock comment ID
            }
          }
        });
      }
      return Promise.resolve({});
    });

    jest.spyOn(github, 'getOctokit').mockReturnValue({
      rest: {
        issues: {
          createComment: createCommentMock,
        },
      },
      graphql: graphqlMock,
    });

    github.context.repo = { // Mock github.context.repo for deterministic owner/repo values
      owner: 'mock-owner',
      repo: 'mock-repo',
    };

    // Mock Math.random to ensure deterministic haiku selection for tests
    // Mock rationale: Ensures tests are deterministic by always selecting the first haiku.
    jest.spyOn(global.Math, 'random').mockReturnValue(0);
  });

  it('should post a haiku to an issue by default', async () => {
    await run();

    expect(getInputMock).toHaveBeenCalledWith('github-token', { required: true });
    expect(getInputMock).toHaveBeenCalledWith('target-type');
    expect(getInputMock).toHaveBeenCalledWith('target-id', { required: true });
    expect(createCommentMock).toHaveBeenCalledTimes(1);
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: github.context.repo.owner,
      repo: github.context.repo.repo,
      issue_number: 123,
      body: expect.stringContaining(haikus[0])
    });
    expect(setOutputMock).toHaveBeenCalledWith('haiku-posted', true);
    expect(setFailedMock).not.toHaveBeenCalled();
  });

  it('should post a haiku to a discussion when target-type is discussion', async () => {
    getInputMock.mockImplementation((name) => {
      if (name === 'github-token') return 'mock-token';
      if (name === 'target-type') return 'discussion';
      if (name === 'target-id') return '456';
      return '';
    });

    await run();

    expect(getInputMock).toHaveBeenCalledWith('github-token', { required: true });
    expect(getInputMock).toHaveBeenCalledWith('target-type');
    expect(getInputMock).toHaveBeenCalledWith('target-id', { required: true });
    expect(graphqlMock).toHaveBeenCalledTimes(2); // One for discussion ID, one for comment
    expect(graphqlMock).toHaveBeenCalledWith(
      expect.stringContaining('query($owner: String!, $repo: String!, $discussionNumber: Int!)'),
      expect.objectContaining({ discussionNumber: 456 })
    );
    expect(graphqlMock).toHaveBeenCalledWith(
      expect.stringContaining('mutation($discussionId: ID!, $body: String!)'),
      expect.objectContaining({
        discussionId: 'D_kwDOJ_w_c84AAa_A', // Mocked discussion node ID
        body: expect.stringContaining(haikus[0])
      })
    );
    expect(createCommentMock).not.toHaveBeenCalled(); // Should not call issue comment API
    expect(setOutputMock).toHaveBeenCalledWith('haiku-posted', true);
    expect(setFailedMock).not.toHaveBeenCalled();
  });

  it('should set failed if github-token is missing', async () => {
    getInputMock.mockImplementation((name, options) => {
      if (name === 'github-token' && options.required) throw new Error('Input required and not supplied: github-token');
      if (name === 'target-type') return 'issue';
      if (name === 'target-id') return '123';
      return '';
    });

    await run();

    expect(setFailedMock).toHaveBeenCalledWith(expect.stringContaining('Input required and not supplied: github-token'));
    expect(setOutputMock).toHaveBeenCalledWith('haiku-posted', false);
  });

  it('should set failed if target-id is missing', async () => {
    getInputMock.mockImplementation((name, options) => {
      if (name === 'github-token') return 'mock-token';
      if (name === 'target-type') return 'issue';
      if (name === 'target-id' && options.required) throw new Error('Input required and not supplied: target-id');
      return '';
    });

    await run();

    expect(setFailedMock).toHaveBeenCalledWith(expect.stringContaining('Input required and not supplied: target-id'));
    expect(setOutputMock).toHaveBeenCalledWith('haiku-posted', false);
  });

  it('should set failed for invalid target-type', async () => {
    getInputMock.mockImplementation((name) => {
      if (name === 'github-token') return 'mock-token';
      if (name === 'target-type') return 'invalid-type';
      if (name === 'target-id') return '123';
      return '';
    });

    await run();

    expect(setFailedMock).toHaveBeenCalledWith("Invalid target-type: invalid-type. Must be 'issue' or 'discussion'.");
    expect(setOutputMock).toHaveBeenCalledWith('haiku-posted', false);
  });
});
