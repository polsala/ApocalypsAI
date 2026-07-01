const core = require('@actions/core');
const github = require('@actions/github');
const { when } = require('jest-when');

// Mock the GitHub Actions toolkit
jest.mock('@actions/core');
jest.mock('@actions/github');

const run = require('../src/index');

describe('Nightly Workflow Chrono-Sentry', () => {
  let listJobsForWorkflowRunMock;

  beforeEach(() => {
    jest.clearAllMocks();

    // # Mock rationale: Simulates the GitHub context available to the action.
    github.context = {
      repo: {
        owner: 'test-owner',
        repo: 'test-repo',
      },
      runId: 12345,
    };

    // # Mock rationale: Simulates the Octokit client for GitHub API interactions.
    listJobsForWorkflowRunMock = jest.fn();
    github.getOctokit.mockReturnValue({
      rest: {
        actions: {
          listJobsForWorkflowRun: listJobsForWorkflowRunMock,
        },
      },
    });

    // # Mock rationale: Simulates inputs provided to the GitHub Action.
    when(core.getInput)
      .calledWith('github_token', expect.anything())
      .mockReturnValue('mock-token');
    when(core.getInput)
      .calledWith('threshold_multiplier')
      .mockReturnValue('2.0');
    when(core.getInput)
      .calledWith('min_duration_seconds')
      .mockReturnValue('5');
  });

  it('should detect a temporal distortion when a step is too long', async () => {
    const now = new Date();
    const jobStartTime = new Date(now.getTime() - 60 * 1000); // 60 seconds ago

    listJobsForWorkflowRunMock.mockResolvedValue({
      data: {
        jobs: [
          {
            id: 1,
            name: 'Build Job',
            status: 'completed',
            started_at: jobStartTime.toISOString(),
            completed_at: now.toISOString(),
            steps: [
              {
                name: 'Setup',
                status: 'completed',
                started_at: new Date(jobStartTime.getTime() + 1000).toISOString(), // 1s
                completed_at: new Date(jobStartTime.getTime() + 2000).toISOString(),
              },
              {
                name: 'Run Tests',
                status: 'completed',
                started_at: new Date(jobStartTime.getTime() + 2000).toISOString(), // 5s
                completed_at: new Date(jobStartTime.getTime() + 7000).toISOString(),
              },
              {
                name: 'Deploy',
                status: 'completed',
                started_at: new Date(jobStartTime.getTime() + 7000).toISOString(), // 40s (anomaly: 40s > 2 * avg(1,5,40) = 2 * 15.33 = 30.66)
                completed_at: new Date(jobStartTime.getTime() + 47000).toISOString(),
              },
              {
                name: 'Cleanup',
                status: 'completed',
                started_at: new Date(jobStartTime.getTime() + 47000).toISOString(), // 1s
                completed_at: new Date(jobStartTime.getTime() + 48000).toISOString(),
              },
            ],
          },
        ],
      },
    });

    await run();

    expect(core.setFailed).toHaveBeenCalledTimes(1);
    expect(core.setFailed).toHaveBeenCalledWith(expect.stringContaining('Temporal distortions detected'));
    expect(core.setOutput).toHaveBeenCalledWith('anomalies_detected', true);
    // # Mock rationale: `core.getOutput` is mocked to retrieve the value set by the action.
    const anomalyReport = JSON.parse(core.getOutput.mock.calls.find(call => call[0] === 'anomaly_report')[1]);
    expect(anomalyReport).toHaveLength(1);
    expect(anomalyReport[0].step_name).toBe('Deploy');
    expect(core.warning).toHaveBeenCalledWith(expect.stringContaining('A chronal anomaly!'));
  });

  it('should not detect anomalies if all steps are within threshold', async () => {
    const now = new Date();
    const jobStartTime = new Date(now.getTime() - 30 * 1000);

    listJobsForWorkflowRunMock.mockResolvedValue({
      data: {
        jobs: [
          {
            id: 1,
            name: 'Build Job',
            status: 'completed',
            started_at: jobStartTime.toISOString(),
            completed_at: now.toISOString(),
            steps: [
              {
                name: 'Setup',
                status: 'completed',
                started_at: new Date(jobStartTime.getTime() + 1000).toISOString(), // 1s
                completed_at: new Date(jobStartTime.getTime() + 2000).toISOString(),
              },
              {
                name: 'Run Tests',
                status: 'completed',
                started_at: new Date(jobStartTime.getTime() + 2000).toISOString(), // 10s
                completed_at: new Date(jobStartTime.getTime() + 12000).toISOString(),
              },
              {
                name: 'Deploy',
                status: 'completed',
                started_at: new Date(jobStartTime.getTime() + 12000).toISOString(), // 15s
                completed_at: new Date(jobStartTime.getTime() + 27000).toISOString(),
              },
            ],
          },
        ],
      },
    });

    await run();

    expect(core.setFailed).not.toHaveBeenCalled();
    expect(core.setOutput).toHaveBeenCalledWith('anomalies_detected', false);
    expect(core.setOutput).toHaveBeenCalledWith('anomaly_report', '[]');
    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('No distortions detected!'));
  });

  it('should ignore steps below min_duration_seconds', async () => {
    when(core.getInput)
      .calledWith('min_duration_seconds')
      .mockReturnValue('10'); // Set min duration to 10s

    const now = new Date();
    const jobStartTime = new Date(now.getTime() - 60 * 1000);

    listJobsForWorkflowRunMock.mockResolvedValue({
      data: {
        jobs: [
          {
            id: 1,
            name: 'Build Job',
            status: 'completed',
            started_at: jobStartTime.toISOString(),
            completed_at: now.toISOString(),
            steps: [
              {
                name: 'Setup',
                status: 'completed',
                started_at: new Date(jobStartTime.getTime() + 1000).toISOString(), // 1s (ignored)
                completed_at: new Date(jobStartTime.getTime() + 2000).toISOString(),
              },
              {
                name: 'Run Tests',
                status: 'completed',
                started_at: new Date(jobStartTime.getTime() + 2000).toISOString(), // 12s
                completed_at: new Date(jobStartTime.getTime() + 14000).toISOString(),
              },
              {
                name: 'Deploy',
                status: 'completed',
                started_at: new Date(jobStartTime.getTime() + 14000).toISOString(), // 30s (avg of 12,30 is 21. 30 < 2*21=42. Not an anomaly with 2.0 multiplier)
                completed_at: new Date(jobStartTime.getTime() + 44000).toISOString(),
              },
            ],
          },
        ],
      },
    });

    await run();

    expect(core.setFailed).not.toHaveBeenCalled(); // No anomaly here with 2.0 multiplier
    expect(core.setOutput).toHaveBeenCalledWith('anomalies_detected', false);
    expect(core.setOutput).toHaveBeenCalledWith('anomaly_report', '[]');
  });

  it('should handle jobs with no completed steps', async () => {
    listJobsForWorkflowRunMock.mockResolvedValue({
      data: {
        jobs: [
          {
            id: 1,
            name: 'Pending Job',
            status: 'queued',
            steps: [],
          },
          {
            id: 2,
            name: 'Empty Job',
            status: 'completed',
            steps: [],
          },
        ],
      },
    });

    await run();

    expect(core.setFailed).not.toHaveBeenCalled();
    expect(core.setOutput).toHaveBeenCalledWith('anomalies_detected', false);
    expect(core.setOutput).toHaveBeenCalledWith('anomaly_report', '[]');
    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('no significant completed steps to analyze.'));
  });

  it('should handle API errors gracefully', async () => {
    listJobsForWorkflowRunMock.mockRejectedValue(new Error('API rate limit exceeded'));

    await run();

    expect(core.setFailed).toHaveBeenCalledTimes(1);
    expect(core.setFailed).toHaveBeenCalledWith(expect.stringContaining('API rate limit exceeded'));
    expect(core.setOutput).not.toHaveBeenCalledWith('anomalies_detected', expect.any(Boolean));
  });
});
