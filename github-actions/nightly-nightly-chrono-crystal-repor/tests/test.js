const core = require('@actions/core');

// Mock rationale: We need to mock GitHub Actions toolkit functions to run tests offline
// without actual GitHub environment or API calls. This ensures determinism and isolation.
const mockInputs = {};
const mockOutputs = {};
const mockSummary = {
  _content: '',
  addRaw: function(text) { this._content += text; return this; },
  write: function() { /* In a real scenario, this would write to GITHUB_STEP_SUMMARY */ }
};

jest.mock('@actions/core', () => ({
  getInput: jest.fn((name, options) => {
    if (options && options.required && !mockInputs[name]) {
      throw new Error(`Input required and not supplied: ${name}`);
    }
    return mockInputs[name];
  }),
  setFailed: jest.fn(),
  setOutput: jest.fn((name, value) => { mockOutputs[name] = value; }),
  summary: mockSummary,
}));

// Mock rationale: Math.random is mocked to ensure deterministic test outcomes
// when selecting a random omen from the predefined lists.
const mockMath = Object.create(global.Math);
mockMath.random = () => 0.5; // Always pick the middle omen for deterministic tests
global.Math = mockMath;

describe('Chrono-Crystal Status Report Action', () => {
  beforeEach(() => {
    // Clear mocks and reset state before each test
    jest.clearAllMocks();
    mockInputs.status = '';
    mockInputs['repo-token'] = 'mock-token';
    mockOutputs.reportMessage = '';
    mockSummary._content = '';
    global.Math.random = () => 0.5; // Reset mock random
  });

  it('should generate a success report', () => {
    mockInputs.status = 'success';
    require('../src/main'); // Run the action

    expect(core.getInput).toHaveBeenCalledWith('status', { required: true });
    expect(core.getInput).toHaveBeenCalledWith('repo-token', { required: true });
    expect(core.setFailed).not.toHaveBeenCalled();
    expect(core.setOutput).toHaveBeenCalledWith(
      'report-message',
      expect.stringContaining('✨ **Chrono-Crystal Status Report:** A shimmering aura emanates from the Chrono-Crystal. The future is bright, the past is secure. Success is etched in time!')
    );
    expect(core.summary.addRaw).toHaveBeenCalledWith(
      expect.stringContaining('✨ **Chrono-Crystal Status Report:** A shimmering aura emanates from the Chrono-Crystal. The future is bright, the past is secure. Success is etched in time!')
    );
  });

  it('should generate a failure report', () => {
    mockInputs.status = 'failure';
    require('../src/main'); // Run the action

    expect(core.setFailed).not.toHaveBeenCalled();
    expect(core.setOutput).toHaveBeenCalledWith(
      'report-message',
      expect.stringContaining('🚨 **Chrono-Crystal Status Report:** Dark fissures appear within the Chrono-Crystal. A ripple in the timeline, a shadow of chaos. Recalibration is urgently needed!')
    );
    expect(core.summary.addRaw).toHaveBeenCalledWith(
      expect.stringContaining('🚨 **Chrono-Crystal Status Report:** Dark fissures appear within the Chrono-Crystal. A ripple in the timeline, a shadow of chaos. Recalibration is urgently needed!')
    );
  });

  it('should generate a cancelled report', () => {
    mockInputs.status = 'cancelled';
    require('../src/main'); // Run the action

    expect(core.setFailed).not.toHaveBeenCalled();
    expect(core.setOutput).toHaveBeenCalledWith(
      'report-message',
      expect.stringContaining('⏸️ **Chrono-Crystal Status Report:** A faint echo lingers in the Chrono-Crystal. The journey was cut short, the prophecy unwritten. A pause in the temporal tapestry.')
    );
    expect(core.summary.addRaw).toHaveBeenCalledWith(
      expect.stringContaining('⏸️ **Chrono-Crystal Status Report:** A faint echo lingers in the Chrono-Crystal. The journey was cut short, the prophecy unwritten. A pause in the temporal tapestry.')
    );
  });

  it('should generate a skipped report', () => {
    mockInputs.status = 'skipped';
    require('../src/main'); // Run the action

    expect(core.setFailed).not.toHaveBeenCalled();
    expect(core.setOutput).toHaveBeenCalledWith(
      'report-message',
      expect.stringContaining('⏭️ **Chrono-Crystal Status Report:** The Chrono-Crystal observes a skipped temporal path. No omens are revealed for this untraveled timeline.')
    );
    expect(core.summary.addRaw).toHaveBeenCalledWith(
      expect.stringContaining('⏭️ **Chrono-Crystal Status Report:** The Chrono-Crystal observes a skipped temporal path. No omens are revealed for this untraveled timeline.')
    );
  });

  it('should generate a neutral report', () => {
    mockInputs.status = 'neutral';
    require('../src/main'); // Run the action

    expect(core.setFailed).not.toHaveBeenCalled();
    expect(core.setOutput).toHaveBeenCalledWith(
      'report-message',
      expect.stringContaining('😐 **Chrono-Crystal Status Report:** The Chrono-Crystal remains neutral, observing the temporal flow without strong omens. All is in balance.')
    );
    expect(core.summary.addRaw).toHaveBeenCalledWith(
      expect.stringContaining('😐 **Chrono-Crystal Status Report:** The Chrono-Crystal remains neutral, observing the temporal flow without strong omens. All is in balance.')
    );
  });

  it('should handle unknown status', () => {
    mockInputs.status = 'unknown_state';
    require('../src/main'); // Run the action

    expect(core.setFailed).not.toHaveBeenCalled();
    expect(core.setOutput).toHaveBeenCalledWith(
      'report-message',
      expect.stringContaining('❓ **Chrono-Crystal Status Report:** The Chrono-Crystal observes an unknown temporal state: \'unknown_state\'. Its omens are yet unwritten.')
    );
    expect(core.summary.addRaw).toHaveBeenCalledWith(
      expect.stringContaining('❓ **Chrono-Crystal Status Report:** The Chrono-Crystal observes an unknown temporal state: \'unknown_state\'. Its omens are yet unwritten.')
    );
  });

  it('should call setFailed if status input is missing', () => {
    mockInputs.status = undefined; // Simulate missing input
    // The require('../src/main') call will throw an error because getInput is mocked to throw
    // if required input is missing. This error will be caught by the try/catch in main.js
    // and then core.setFailed will be called.
    require('../src/main');

    expect(core.setFailed).toHaveBeenCalledWith('Input required and not supplied: status');
    expect(core.setOutput).not.toHaveBeenCalled();
    expect(core.summary.addRaw).not.toHaveBeenCalled();
  });
});
