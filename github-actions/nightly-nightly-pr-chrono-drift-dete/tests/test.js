const core = require('@actions/core');
const github = require('@actions/github');

// Mock the GitHub Actions toolkit
jest.mock('@actions/core');
jest.mock('@actions/github');

const run = require('../src/main'); // The action's main function

describe('Nightly PR Chrono-Drift Detector', () => {
  let setFailedMock;
  let warningMock;
  let infoMock;
  let setOutputMock;

  beforeEach(() => {
    jest.clearAllMocks();
    setFailedMock = jest.spyOn(core, 'setFailed');
    warningMock = jest.spyOn(core, 'warning');
    infoMock = jest.spyOn(core, 'info');
    setOutputMock = jest.spyOn(core, 'setOutput');

    // Mock rationale:
    // @actions/core: We mock core.getInput, core.setFailed, core.warning, core.info, and core.setOutput
    // to control action inputs and observe its outputs/failures without actually interacting
    // with the GitHub Actions runner environment. This ensures deterministic, offline testing.
    // @actions/github: We mock github.context to simulate the event payload (e.g., pull_request data)
    // and github.getOctokit to prevent actual API calls, ensuring tests are fast and isolated.

    // Mock inputs
    core.getInput.mockImplementation((name) => {
      switch (name) {
        case 'github-token': return 'mock-token';
        case 'future-date-threshold-days': return '7';
        case 'stale-pr-threshold-days': return '30';
        case 'ignore-drafts': return 'true';
        default: return '';
      }
    });

    // Mock github context
    github.context = {
      repo: {
        owner: 'test-owner',
        repo: 'test-repo',
      },
      payload: {
        pull_request: {
          number: 123,
          title: 'Test PR',
          body: 'This is a test PR body.',
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
          draft: false,
        },
      },
    };

    // Mock octokit (not strictly used in current main.js, but good practice for GitHub Actions tests)
    github.getOctokit.mockReturnValue({
      rest: {
        pulls: {
          get: jest.fn().mockResolvedValue({ data: { /* mock PR data if needed */ } }),
        },
      },
    });
  });

  test('should not detect drift for a normal PR', async () => {
    await run();
    expect(setFailedMock).not.toHaveBeenCalled();
    expect(warningMock).not.toHaveBeenCalled();
    expect(setOutputMock).toHaveBeenCalledWith('chrono-drift-detected', false);
    expect(setOutputMock).toHaveBeenCalledWith('drift-details', '[]');
  });

  test('should detect future-dated claim', async () => {
    const futureDate = new Date();
    futureDate.setDate(futureDate.getDate() + 10); // 10 days in future, > 7 day threshold
    github.context.payload.pull_request.body = `This PR is for a feature launching on ${futureDate.toISOString().split('T')[0]}.`;

    await run();

    expect(setFailedMock).toHaveBeenCalledWith('Chrono-Drift detected! Please review the PR for temporal inconsistencies.');
    expect(warningMock).toHaveBeenCalledTimes(1);
    expect(warningMock).toHaveBeenCalledWith(expect.stringContaining('Found a date'));
    expect(setOutputMock).toHaveBeenCalledWith('chrono-drift-detected', true);
    const driftDetails = JSON.parse(setOutputMock.mock.calls[1][1]);
    expect(driftDetails[0].type).toBe('future-dated-claim');
    expect(driftDetails[0].date).toBe(futureDate.toISOString().split('T')[0]);
  });

  test('should not detect future-dated claim if within threshold', async () => {
    const futureDate = new Date();
    futureDate.setDate(futureDate.getDate() + 5); // 5 days in future, <= 7 day threshold
    github.context.payload.pull_request.body = `This PR is for a feature launching on ${futureDate.toISOString().split('T')[0]}.`;

    await run();

    expect(setFailedMock).not.toHaveBeenCalled();
    expect(warningMock).not.toHaveBeenCalled();
    expect(setOutputMock).toHaveBeenCalledWith('chrono-drift-detected', false);
  });

  test('should detect stale PR', async () => {
    const now = new Date();
    const thirtyOneDaysAgo = new Date(now);
    thirtyOneDaysAgo.setDate(now.getDate() - 31); // 31 days ago, > 30 day threshold

    github.context.payload.pull_request.created_at = thirtyOneDaysAgo.toISOString();
    github.context.payload.pull_request.updated_at = thirtyOneDaysAgo.toISOString(); // No recent activity

    await run();

    expect(setFailedMock).toHaveBeenCalledWith('Chrono-Drift detected! Please review the PR for temporal inconsistencies.');
    expect(warningMock).toHaveBeenCalledTimes(1);
    expect(warningMock).toHaveBeenCalledWith(expect.stringContaining('PR has been open for'));
    expect(setOutputMock).toHaveBeenCalledWith('chrono-drift-detected', true);
    const driftDetails = JSON.parse(setOutputMock.mock.calls[1][1]);
    expect(driftDetails[0].type).toBe('stale-pr');
    expect(driftDetails[0].pr_age_days).toBeGreaterThanOrEqual(31);
  });

  test('should not detect stale PR if recently updated', async () => {
    const now = new Date();
    const thirtyOneDaysAgo = new Date(now);
    thirtyOneDaysAgo.setDate(now.getDate() - 31);

    github.context.payload.pull_request.created_at = thirtyOneDaysAgo.toISOString();
    github.context.payload.pull_request.updated_at = now.toISOString(); // Updated today

    await run();

    expect(setFailedMock).not.toHaveBeenCalled();
    expect(warningMock).not.toHaveBeenCalled();
    expect(setOutputMock).toHaveBeenCalledWith('chrono-drift-detected', false);
  });

  test('should ignore stale check for draft PRs if ignore-drafts is true', async () => {
    core.getInput.mockImplementation((name) => {
      if (name === 'ignore-drafts') return 'true';
      if (name === 'github-token') return 'mock-token';
      if (name === 'future-date-threshold-days') return '7';
      if (name === 'stale-pr-threshold-days') return '30';
      return '';
    });

    const now = new Date();
    const thirtyOneDaysAgo = new Date(now);
    thirtyOneDaysAgo.setDate(now.getDate() - 31);

    github.context.payload.pull_request.created_at = thirtyOneDaysAgo.toISOString();
    github.context.payload.pull_request.updated_at = thirtyOneDaysAgo.toISOString();
    github.context.payload.pull_request.draft = true; // This is a draft PR

    await run();

    expect(infoMock).toHaveBeenCalledWith('PR is a draft and ignore-drafts is true. Skipping stale PR check.');
    expect(setFailedMock).not.toHaveBeenCalled();
    expect(warningMock).not.toHaveBeenCalled();
    expect(setOutputMock).toHaveBeenCalledWith('chrono-drift-detected', false);
  });

  test('should detect stale check for draft PRs if ignore-drafts is false', async () => {
    core.getInput.mockImplementation((name) => {
      if (name === 'ignore-drafts') return 'false'; // Do not ignore drafts
      if (name === 'github-token') return 'mock-token';
      if (name === 'future-date-threshold-days') return '7';
      if (name === 'stale-pr-threshold-days') return '30';
      return '';
    });

    const now = new Date();
    const thirtyOneDaysAgo = new Date(now);
    thirtyOneDaysAgo.setDate(now.getDate() - 31);

    github.context.payload.pull_request.created_at = thirtyOneDaysAgo.toISOString();
    github.context.payload.pull_request.updated_at = thirtyOneDaysAgo.toISOString();
    github.context.payload.pull_request.draft = true; // This is a draft PR

    await run();

    expect(infoMock).not.toHaveBeenCalledWith('PR is a draft and ignore-drafts is true. Skipping stale PR check.');
    expect(setFailedMock).toHaveBeenCalled();
    expect(warningMock).toHaveBeenCalledTimes(1);
    expect(setOutputMock).toHaveBeenCalledWith('chrono-drift-detected', true);
  });

  test('should handle multiple drifts', async () => {
    const futureDate = new Date();
    futureDate.setDate(futureDate.getDate() + 10);
    const now = new Date();
    const thirtyOneDaysAgo = new Date(now);
    thirtyOneDaysAgo.setDate(now.getDate() - 31);

    github.context.payload.pull_request.title = `Future feature on ${futureDate.toISOString().split('T')[0]}`;
    github.context.payload.pull_request.created_at = thirtyOneDaysAgo.toISOString();
    github.context.payload.pull_request.updated_at = thirtyOneDaysAgo.toISOString();

    await run();

    expect(setFailedMock).toHaveBeenCalled();
    expect(warningMock).toHaveBeenCalledTimes(2);
    expect(setOutputMock).toHaveBeenCalledWith('chrono-drift-detected', true);
    const driftDetails = JSON.parse(setOutputMock.mock.calls[1][1]);
    expect(driftDetails.length).toBe(2);
    expect(driftDetails[0].type).toBe('future-dated-claim');
    expect(driftDetails[1].type).toBe('stale-pr');
  });

  test('should warn and exit if not a pull_request event', async () => {
    github.context.payload.pull_request = undefined; // Not a PR event

    await run();

    expect(warningMock).toHaveBeenCalledWith('This action only runs on pull_request events. Skipping.');
    expect(setFailedMock).not.toHaveBeenCalled();
    expect(setOutputMock).not.toHaveBeenCalledWith('chrono-drift-detected', expect.any(Boolean));
  });

  test('should set failed on unexpected error', async () => {
    core.getInput.mockImplementation(() => {
      throw new Error('Test error');
    });

    await run();

    expect(setFailedMock).toHaveBeenCalledWith('Test error');
  });
});
