// Mock rationale: Simulates GitHub API interactions without network calls
const { afterEach, beforeEach, describe, it, expect, jest } = require('@jest/globals');
const { createMockContext } = require('@actions/github/test-utils');
const { createMockOctokit } = require('./__mocks__/octokit');

jest.mock('@actions/github');
jest.mock('@actions/core');

const core = require('@actions/core');
const github = require('@actions/github');

const action = require('../action');

describe('Apocalypse Quote Bot', () => {
  beforeEach(() => {
    createMockContext({
      event: {
        issue: { number: 123 }
      }
    });
  });

  it('should post a random quote', async () => {
    const mockOctokit = createMockOctokit();
    const mockCreateComment = jest.fn();
    mockOctokit.rest.issues.createComment = mockCreateComment;

    const mockGetInput = jest.spyOn(core, 'getInput').mockImplementation((name) => {
      if (name === 'token') return 'mock-token';
      if (name === 'issue_number') return '123';
      if (name === 'quotes') return 'Quote 1\nQuote 2';
      return '';
    });

    await action();

    expect(mockCreateComment).toHaveBeenCalledWith({
      owner: 'mock-owner',
      repo: 'mock-repo',
      issue_number: 123,
      body: expect.stringContaining('🔔 **Daily Apocalypse Quote**')
    });

    mockGetInput.mockRestore();
  });
});
