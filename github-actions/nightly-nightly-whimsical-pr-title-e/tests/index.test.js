const core = require('@actions/core');
const github = require('@actions/github');

// Mock the GitHub Actions toolkit
jest.mock('@actions/core');
jest.mock('@actions/github');

describe('Whimsical PR Title Enforcer', () => {
  let setFailedMock;
  let setOutputMock;
  let infoMock;
  let warningMock;

  beforeEach(() => {
    setFailedMock = jest.spyOn(core, 'setFailed').mockImplementation(() => {});
    setOutputMock = jest.spyOn(core, 'setOutput').mockImplementation(() => {});
    infoMock = jest.spyOn(core, 'info').mockImplementation(() => {});
    warningMock = jest.spyOn(core, 'warning').mockImplementation(() => {});

    // Mock rationale: We need to control the inputs and the GitHub context for deterministic testing.
    // @actions/core.getInput is mocked to return specific values for each test case.
    // @actions/github.context is mocked to simulate a pull_request event payload.
    jest.spyOn(core, 'getInput').mockImplementation((name) => {
      switch (name) {
        case 'github-token': return 'mock-token';
        case 'pattern': return '^(Whisper of the Void|Temporal Tear|Cosmic Quirk): .+$';
        case 'min-length': return '20';
        case 'fail-on-mismatch': return 'true';
        default: return '';
      }
    });

    // Mock rationale: The GitHub context is crucial for getting the PR title.
    // We mock it to provide a consistent PR title for our tests.
    github.context = {
      eventName: 'pull_request',
      payload: {
        pull_request: {
          title: 'Default Whimsical Title: A test of cosmic proportions'
        }
      }
    };
  });

  afterEach(() => {
    jest.restoreAllMocks();
    jest.clearModules(); // Clear module cache to re-run the action script for each test
  });

  test('should pass for a whimsical title matching pattern and length', async () => {
    github.context.payload.pull_request.title = 'Whisper of the Void: A truly whimsical update';
    await require('../src/index'); // Run the action

    expect(setFailedMock).not.toHaveBeenCalled();
    expect(setOutputMock).toHaveBeenCalledWith('is-whimsical', true);
    expect(setOutputMock).toHaveBeenCalledWith('message', 'PR title "Whisper of the Void: A truly whimsical update" is wonderfully whimsical!');
    expect(infoMock).toHaveBeenCalledWith('PR title "Whisper of the Void: A truly whimsical update" is wonderfully whimsical!');
  });

  test('should fail if title does not match pattern', async () => {
    github.context.payload.pull_request.title = 'Regular Update: Just a normal change';
    await require('../src/index');

    expect(setFailedMock).toHaveBeenCalledWith(expect.stringContaining('Title does not match required pattern'));
    expect(setOutputMock).toHaveBeenCalledWith('is-whimsical', false);
    expect(setOutputMock).toHaveBeenCalledWith('message', expect.stringContaining('Title does not match required pattern'));
    expect(warningMock).toHaveBeenCalledWith(expect.stringContaining('Title does not match required pattern'));
  });

  test('should fail if title is too short', async () => {
    github.context.payload.pull_request.title = 'Temporal Tear: Hi'; // Length 17, min-length is 20
    await require('../src/index');

    expect(setFailedMock).toHaveBeenCalledWith(expect.stringContaining('Title is too short'));
    expect(setOutputMock).toHaveBeenCalledWith('is-whimsical', false);
    expect(setOutputMock).toHaveBeenCalledWith('message', expect.stringContaining('Title is too short'));
    expect(warningMock).toHaveBeenCalledWith(expect.stringContaining('Title is too short'));
  });

  test('should not fail if fail-on-mismatch is false', async () => {
    jest.spyOn(core, 'getInput').mockImplementation((name) => {
      switch (name) {
        case 'github-token': return 'mock-token';
        case 'pattern': return '^(Whisper of the Void|Temporal Tear|Cosmic Quirk): .+$';
        case 'min-length': return '20';
        case 'fail-on-mismatch': return 'false'; // Important for this test
        default: return '';
      }
    });
    github.context.payload.pull_request.title = 'Not Whimsical: A short title'; // Fails both pattern and length
    await require('../src/index');

    expect(setFailedMock).not.toHaveBeenCalled(); // Should not call setFailed
    expect(setOutputMock).toHaveBeenCalledWith('is-whimsical', false);
    expect(setOutputMock).toHaveBeenCalledWith('message', expect.stringContaining('Title does not match required pattern; Title is too short'));
    expect(warningMock).toHaveBeenCalledWith(expect.stringContaining('Title does not match required pattern; Title is too short'));
  });

  test('should handle missing PR title gracefully', async () => {
    github.context.payload.pull_request = null; // Simulate no PR context
    await require('../src/index');

    expect(setFailedMock).toHaveBeenCalledWith('Could not retrieve PR title. This action only runs on pull_request events.');
    expect(setOutputMock).toHaveBeenCalledWith('is-whimsical', false);
    expect(setOutputMock).toHaveBeenCalledWith('message', 'Could not retrieve PR title. This action only runs on pull_request events.');
  });

  test('should handle action error gracefully', async () => {
    // Force an error, e.g., by making minLength parsing fail
    jest.spyOn(core, 'getInput').mockImplementation((name) => {
      if (name === 'min-length') return 'not-a-number';
      return jest.requireActual('@actions/core').getInput(name); // Use actual for others
    });
    github.context.payload.pull_request.title = 'Whisper of the Void: A test';
    await require('../src/index');

    expect(setFailedMock).toHaveBeenCalledWith(expect.stringContaining('NaN')); // Error from parseInt
    expect(setOutputMock).toHaveBeenCalledWith('is-whimsical', false);
    expect(setOutputMock).toHaveBeenCalledWith('message', expect.stringContaining('Action failed with error'));
  });
});
