const core = require('@actions/core');
const github = require('@actions/github');
const nock = require('nock');

// Mock rationale: we replace the real Octokit with a nocked HTTP endpoint so the test runs offline.
jest.mock('@actions/core');
jest.mock('@actions/github');

const run = require('../src/index'); // The action's entry point

describe('Nightly Apocalypse Badge Action', () => {
  const originalEnv = process.env;

  beforeEach(() => {
    jest.resetAllMocks();
    process.env = { ...originalEnv };
    // Mock inputs
    core.getInput.mockImplementation(name => {
      if (name === 'github-token') return 'fake-token';
      return '';
    });
    // Mock context payload for a PR with the apocalypse label
    github.context = {
      repo: { owner: 'octocat', repo: 'hello-world' },
      payload: {
        pull_request: {
          number: 42,
          labels: [{ name: 'apocalypse' }]
        }
      }
    };
    // Mock Octokit constructor to return an object with the needed method
    github.getOctokit.mockImplementation(() => {
      return {
        rest: {
          issues: {
            createComment: jest.fn().mockResolvedValue({ data: {} })
          }
        }
      };
    });
  });

  afterAll(() => {
    process.env = originalEnv;
  });

  test('posts a comment when apocalypse label is present', async () => {
    await run();
    const octokit = github.getOctokit();
    expect(octokit.rest.issues.createComment).toHaveBeenCalledWith({
      owner: 'octocat',
      repo: 'hello-world',
      issue_number: 42,
      body: expect.stringContaining('![Apocalypse]')
    });
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('does nothing when apocalypse label is missing', async () => {
    // Adjust payload to lack the label
    github.context.payload.pull_request.labels = [{ name: 'enhancement' }];
    await run();
    const octokit = github.getOctokit();
    expect(octokit.rest.issues.createComment).not.toHaveBeenCalled();
    expect(core.info).toHaveBeenCalledWith('Apocalypse label not present – nothing to do.');
  });

  test('exits gracefully when not a PR event', async () => {
    delete github.context.payload.pull_request;
    await run();
    expect(core.info).toHaveBeenCalledWith('No pull request payload – exiting.');
  });
});
