const core = require('@actions/core');

// Mock the @actions/core library
let getInputMock;
let setOutputMock;
let setFailedMock;
let warningMock;
let infoMock;

describe('Nightly Chrono-Guard', () => {
  beforeEach(() => {
    jest.clearAllMocks();

    getInputMock = jest.spyOn(core, 'getInput').mockImplementation((name) => {
      if (name === 'pr-title') return 'Default PR Title';
      if (name === 'commit-messages') return 'Default commit message';
      if (name === 'current-year') return '2024'; // Default current year for deterministic tests
      return '';
    });
    setOutputMock = jest.spyOn(core, 'setOutput').mockImplementation(() => {});
    setFailedMock = jest.spyOn(core, 'setFailed').mockImplementation(() => {});
    warningMock = jest.spyOn(core, 'warning').mockImplementation(() => {});
    infoMock = jest.spyOn(core, 'info').mockImplementation(() => {});
  });

  // Mock rationale: We need to control the inputs and capture outputs/failures
  // without actually interacting with the GitHub Actions environment.
  // This allows for deterministic testing of the action's logic.

  it('should detect no anomalies for normal PRs', async () => {
    getInputMock.mockImplementation((name) => {
      if (name === 'pr-title') return 'Feature: Add new user profile page';
      if (name === 'commit-messages') return 'feat: initial commit\nfix: address review comments';
      if (name === 'current-year') return '2024';
      return '';
    });

    // Require the main action file to run it
    require('../src/main');

    expect(setOutputMock).toHaveBeenCalledWith('is-anomalous', false);
    expect(setOutputMock).toHaveBeenCalledWith('anomaly-details', '');
    expect(infoMock).toHaveBeenCalledWith('No temporal anomalies detected. Chronology is stable.');
    expect(warningMock).not.toHaveBeenCalled();
    expect(setFailedMock).not.toHaveBeenCalled();
  });

  it('should detect keyword anomaly in PR title', async () => {
    getInputMock.mockImplementation((name) => {
      if (name === 'pr-title') return 'Fix: Implement a time travel feature';
      if (name === 'commit-messages') return 'feat: add time travel logic';
      if (name === 'current-year') return '2024';
      return '';
    });

    require('../src/main');

    expect(setOutputMock).toHaveBeenCalledWith('is-anomalous', true);
    expect(setOutputMock).toHaveBeenCalledWith(
      'anomaly-details',
      expect.stringContaining('Keyword anomaly detected in PR Title: "time travel" found.')
    );
    expect(warningMock).toHaveBeenCalledWith('Temporal anomalies detected! Please review the PR for chronological consistency.');
    expect(setFailedMock).not.toHaveBeenCalled();
  });

  it('should detect keyword anomaly in commit message', async () => {
    getInputMock.mockImplementation((name) => {
      if (name === 'pr-title') return 'Refactor: Improve data fetching';
      if (name === 'commit-messages') return 'refactor: optimize queries\nfeat: add flux capacitor integration';
      if (name === 'current-year') return '2024';
      return '';
    });

    require('../src/main');

    expect(setOutputMock).toHaveBeenCalledWith('is-anomalous', true);
    expect(setOutputMock).toHaveBeenCalledWith(
      'anomaly-details',
      expect.stringContaining('Keyword anomaly detected in Commit Message #2: "flux capacitor" found.')
    );
    expect(warningMock).toHaveBeenCalled();
    expect(setFailedMock).not.toHaveBeenCalled();
  });

  it('should detect future year anomaly', async () => {
    getInputMock.mockImplementation((name) => {
      if (name === 'pr-title') return 'Plan: Release new feature in 2027';
      if (name === 'commit-messages') return 'docs: update roadmap';
      if (name === 'current-year') return '2024';
      return '';
    });

    require('../src/main');

    expect(setOutputMock).toHaveBeenCalledWith('is-anomalous', true);
    expect(setOutputMock).toHaveBeenCalledWith(
      'anomaly-details',
      expect.stringContaining('Future year anomaly detected in PR Title: "2027" is 3 years in the future.')
    );
    expect(warningMock).toHaveBeenCalled();
    expect(setFailedMock).not.toHaveBeenCalled();
  });

  it('should detect past year anomaly', async () => {
    getInputMock.mockImplementation((name) => {
      if (name === 'pr-title') return 'Fix: Bug from 2018 resurfaced';
      if (name === 'commit-messages') return 'fix: address old bug';
      if (name === 'current-year') return '2024';
      return '';
    });

    require('../src/main');

    expect(setOutputMock).toHaveBeenCalledWith('is-anomalous', true);
    expect(setOutputMock).toHaveBeenCalledWith(
      'anomaly-details',
      expect.stringContaining('Past year anomaly detected in PR Title: "2018" is 6 years in the past.')
    );
    expect(warningMock).toHaveBeenCalled();
    expect(setFailedMock).not.toHaveBeenCalled();
  });

  it('should handle multiple anomalies', async () => {
    getInputMock.mockImplementation((name) => {
      if (name === 'pr-title') return 'Urgent: Time-warp fix for 2030 issue';
      if (name === 'commit-messages') return 'feat: add retroactive patch from 2015';
      if (name === 'current-year') return '2024';
      return '';
    });

    require('../src/main');

    expect(setOutputMock).toHaveBeenCalledWith('is-anomalous', true);
    const details = setOutputMock.mock.calls.find(call => call[0] === 'anomaly-details')[1];
    expect(details).toContain('Keyword anomaly detected in PR Title: "time-warp" found.');
    expect(details).toContain('Future year anomaly detected in PR Title: "2030" is 6 years in the future.');
    expect(details).toContain('Keyword anomaly detected in Commit Message #1: "retroactive patch" found.');
    expect(details).toContain('Past year anomaly detected in Commit Message #1: "2015" is 9 years in the past.');
    expect(warningMock).toHaveBeenCalled();
    expect(setFailedMock).not.toHaveBeenCalled();
  });

  it('should not flag years within acceptable range', async () => {
    getInputMock.mockImplementation((name) => {
      if (name === 'pr-title') return 'Update: Docs for 2025 roadmap';
      if (name === 'commit-messages') return 'fix: minor issue from 2023';
      if (name === 'current-year') return '2024';
      return '';
    });

    require('../src/main');

    expect(setOutputMock).toHaveBeenCalledWith('is-anomalous', false);
    expect(setOutputMock).toHaveBeenCalledWith('anomaly-details', '');
    expect(infoMock).toHaveBeenCalledWith('No temporal anomalies detected. Chronology is stable.');
    expect(warningMock).not.toHaveBeenCalled();
    expect(setFailedMock).not.toHaveBeenCalled();
  });

  it('should use current system year if current-year input is empty', async () => {
    getInputMock.mockImplementation((name) => {
      if (name === 'pr-title') return 'Fix: Bug from 2018 resurfaced';
      if (name === 'commit-messages') return 'fix: address old bug';
      if (name === 'current-year') return ''; // Empty input
      return '';
    });

    // Mock Date.getFullYear for this specific test
    const mockGetFullYear = jest.spyOn(Date.prototype, 'getFullYear').mockReturnValue(2024);

    require('../src/main');

    expect(setOutputMock).toHaveBeenCalledWith('is-anomalous', true);
    expect(setOutputMock).toHaveBeenCalledWith(
      'anomaly-details',
      expect.stringContaining('Past year anomaly detected in PR Title: "2018" is 6 years in the past.')
    );
    mockGetFullYear.mockRestore(); // Restore original Date.getFullYear
  });

  it('should handle errors gracefully', async () => {
    getInputMock.mockImplementation((name) => {
      if (name === 'pr-title') throw new Error('Failed to get PR title');
      return '';
    });

    require('../src/main');

    expect(setFailedMock).toHaveBeenCalledWith('Failed to get PR title');
    expect(setOutputMock).not.toHaveBeenCalledWith('is-anomalous', expect.any(Boolean));
  });
});
