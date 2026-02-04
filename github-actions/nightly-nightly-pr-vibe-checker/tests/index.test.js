const core = require('@actions/core');
const github = require('@actions/github');
const { when } = require('jest-when');

// Mock the GitHub Actions toolkit
jest.mock('@actions/core');
jest.mock('@actions/github');

const run = require('../src/index'); // The action's main file

describe('PR Vibe Checker', () => {
  let createCommentMock;

  beforeEach(() => {
    jest.clearAllMocks();

    // Mock rationale: Simulate core.getInput for various action inputs.
    when(core.getInput)
      .calledWith('github-token', expect.any(Object))
      .mockReturnValue('mock-token');
    when(core.getInput)
      .calledWith('threshold')
      .mockReturnValue('0');
    when(core.getInput)
      .calledWith('positive-keywords')
      .mockReturnValue('awesome,great,fantastic,delightful,joy,happy,success,celebrate,win,progress,exciting,superb,excellent,brilliant,hooray');
    when(core.getInput)
      .calledWith('negative-keywords')
      .mockReturnValue('bug,error,issue,problem,fix,fail,broken,struggle,difficult,challenge,bad,sad,frustrate,annoy,regret');
    when(core.getInput)
      .calledWith('check-title')
      .mockReturnValue('true');
    when(core.getInput)
      .calledWith('check-body')
      .mockReturnValue('true');

    // Mock rationale: Simulate GitHub API interaction for posting comments.
    createCommentMock = jest.fn();
    github.getOctokit.mockReturnValue({
      rest: {
        issues: {
          createComment: createCommentMock,
        },
      },
    });

    // Mock rationale: Simulate GitHub context for pull request data.
    github.context = {
      repo: {
        owner: 'test-owner',
        repo: 'test-repo',
      },
      payload: {
        pull_request: {
          number: 123,
          title: 'Feat: Add an awesome new feature',
          body: 'This is a great feature that fixes a problem and brings much joy.',
        },
      },
    };
  });

  test('should set outputs for high vibe score and not post a comment', async () => {
    await run();

    expect(core.setOutput).toHaveBeenCalledWith('vibe-score', 5); // awesome, great, joy, great, joy (problem is negative, but positive outweighs)
    expect(core.setOutput).toHaveBeenCalledWith('vibe-status', 'High');
    expect(core.setOutput).toHaveBeenCalledWith('suggestion', 'The vibes are strong with this one! Keep up the positive energy!');
    expect(createCommentMock).not.toHaveBeenCalled();
    expect(core.setFailed).not.toHaveBeenCalled();
    expect(core.warning).not.toHaveBeenCalled();
  });

  test('should set outputs for low vibe score and post a comment', async () => {
    github.context.payload.pull_request.title = 'Fix: Critical bug causing major issues';
    github.context.payload.pull_request.body = 'This fixes a problem that was causing a lot of struggle and frustration. It was a difficult bug to track down.';
    when(core.getInput)
      .calledWith('threshold')
      .mockReturnValue('0'); // Still using default threshold

    await run();

    // bug, issues, fixes, problem, struggle, frustration, difficult, bug
    // fixes is not in positive keywords.
    // bug (2), issues (1), problem (1), struggle (1), frustration (1), difficult (1) = -7
    expect(core.setOutput).toHaveBeenCalledWith('vibe-score', -7);
    expect(core.setOutput).toHaveBeenCalledWith('vibe-status', 'Low');
    expect(core.setOutput).toHaveBeenCalledWith('suggestion', 'Oh dear, the vibes are a bit low. Perhaps a cheerful emoji or a positive affirmation could help?');
    expect(createCommentMock).toHaveBeenCalledTimes(1);
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      issue_number: 123,
      body: expect.stringContaining('✨ **Vibe Check Alert!** ✨\n\nIt seems the vibes in this PR are a bit low (-7).\n\nOh dear, the vibes are a bit low. Perhaps a cheerful emoji or a positive affirmation could help?\n\nLet\'s keep our spirits high and our code even higher! 🚀'),
    });
    expect(core.warning).toHaveBeenCalledWith('PR vibes are low (-7). A suggestion has been posted.');
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('should handle custom keywords', async () => {
    when(core.getInput)
      .calledWith('positive-keywords')
      .mockReturnValue('yay,woohoo');
    when(core.getInput)
      .calledWith('negative-keywords')
      .mockReturnValue('boo,ugh');
    github.context.payload.pull_request.title = 'Yay, a new feature!';
    github.context.payload.pull_request.body = 'This is great, no boo-boos here. Woohoo!';

    await run();

    // yay (1), woohoo (1) = 2
    expect(core.setOutput).toHaveBeenCalledWith('vibe-score', 2);
    expect(core.setOutput).toHaveBeenCalledWith('vibe-status', 'High');
    expect(createCommentMock).not.toHaveBeenCalled();
  });

  test('should handle no PR title or body to analyze', async () => {
    github.context.payload.pull_request.title = '';
    github.context.payload.pull_request.body = '';
    when(core.getInput)
      .calledWith('check-title')
      .mockReturnValue('true');
    when(core.getInput)
      .calledWith('check-body')
      .mockReturnValue('true');

    await run();

    expect(core.warning).toHaveBeenCalledWith('No title or body to analyze based on inputs. Skipping vibe check.');
    expect(core.setOutput).toHaveBeenCalledWith('vibe-score', 0);
    expect(core.setOutput).toHaveBeenCalledWith('vibe-status', 'Neutral');
    expect(core.setOutput).toHaveBeenCalledWith('suggestion', 'No text was analyzed.');
    expect(createCommentMock).not.toHaveBeenCalled();
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('should handle only checking title', async () => {
    when(core.getInput)
      .calledWith('check-title')
      .mockReturnValue('true');
    when(core.getInput)
      .calledWith('check-body')
      .mockReturnValue('false');
    github.context.payload.pull_request.title = 'Awesome new feature';
    github.context.payload.pull_request.body = 'This is a bug fix.';

    await run();

    // awesome (1) = 1
    expect(core.setOutput).toHaveBeenCalledWith('vibe-score', 1);
    expect(core.setOutput).toHaveBeenCalledWith('vibe-status', 'High');
    expect(createCommentMock).not.toHaveBeenCalled();
  });

  test('should handle only checking body', async () => {
    when(core.getInput)
      .calledWith('check-title')
      .mockReturnValue('false');
    when(core.getInput)
      .calledWith('check-body')
      .mockReturnValue('true');
    github.context.payload.pull_request.title = 'Bug fix';
    github.context.payload.pull_request.body = 'This is an awesome new feature.';

    await run();

    // awesome (1) = 1
    expect(core.setOutput).toHaveBeenCalledWith('vibe-score', 1);
    expect(core.setOutput).toHaveBeenCalledWith('vibe-status', 'High');
    expect(createCommentMock).not.toHaveBeenCalled();
  });

  test('should set failed if not a pull_request event', async () => {
    github.context.payload.pull_request = undefined;

    await run();

    expect(core.setFailed).toHaveBeenCalledWith('This action only runs on pull_request events.');
    expect(core.setOutput).not.toHaveBeenCalled();
    expect(createCommentMock).not.toHaveBeenCalled();
  });

  test('should handle empty keyword lists gracefully', async () => {
    when(core.getInput)
      .calledWith('positive-keywords')
      .mockReturnValue('');
    when(core.getInput)
      .calledWith('negative-keywords')
      .mockReturnValue('');
    github.context.payload.pull_request.title = 'Just a normal PR';
    github.context.payload.pull_request.body = 'No special words here.';

    await run();

    expect(core.setOutput).toHaveBeenCalledWith('vibe-score', 0);
    expect(core.setOutput).toHaveBeenCalledWith('vibe-status', 'High'); // 0 >= 0 threshold
    expect(createCommentMock).not.toHaveBeenCalled();
  });

  test('should handle threshold correctly for medium vibe', async () => {
    github.context.payload.pull_request.title = 'Good progress, but some challenges.'; // good (+1), challenges (-1) = 0
    github.context.payload.pull_request.body = 'This is a great step forward.'; // great (+1) = 1
    when(core.getInput)
      .calledWith('threshold')
      .mockReturnValue('2'); // Threshold is 2

    await run();
    // Total score: 1
    // Threshold: 2
    // Medium condition: vibeScore >= threshold / 2 (1 >= 2 / 2 => 1 >= 1) -> true
    expect(core.setOutput).toHaveBeenCalledWith('vibe-score', 1);
    expect(core.setOutput).toHaveBeenCalledWith('vibe-status', 'Medium');
    expect(core.setOutput).toHaveBeenCalledWith('suggestion', 'The vibes are okay, but a little sparkle could make them shine brighter!');
    expect(createCommentMock).not.toHaveBeenCalled(); // No comment for Medium
  });
});
