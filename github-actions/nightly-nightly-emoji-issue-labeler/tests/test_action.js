// Mock rationale: we mock @actions/core and @actions/github to simulate GitHub environment.

jest.mock('@actions/core');
jest.mock('@actions/github');

const core = require('@actions/core');
const github = require('@actions/github');

describe('Emoji Issue Labeler', () => {
  beforeEach(() => {
    jest.resetAllMocks();
    delete process.env.GITHUB_TOKEN;
    core.getInput.mockImplementation(name => {
      if (name === 'emoji') return '⚡';
      if (name === 'label') return 'high-priority';
      return '';
    });
  });

  test('fails when GITHUB_TOKEN is missing', async () => {
    const { run } = require('../src/index');
    await run();
    expect(core.setFailed).toHaveBeenCalledWith('GITHUB_TOKEN is required');
  });
});
