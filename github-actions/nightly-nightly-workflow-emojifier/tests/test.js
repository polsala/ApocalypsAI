const core = require('@actions/core');
const process = require('process');
const cp = require('child_process');
const path = require('path');

// Mock the GitHub Actions core library
const mockGetInput = jest.spyOn(core, 'getInput').mockImplementation();
const mockSetOutput = jest.spyOn(core, 'setOutput').mockImplementation();
const mockSetFailed = jest.spyOn(core, 'setFailed').mockImplementation();
const mockInfo = jest.spyOn(core, 'info').mockImplementation();

describe('Nightly Workflow Emojifier', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should output 🎉 for success status', async () => {
    // Mock rationale: Simulating GitHub Actions input for 'status'.
    mockGetInput.mockImplementation((name) => {
      if (name === 'status') return 'success';
      if (name === 'default-emoji') return '❓';
      return '';
    });

    const ip = path.join(__dirname, '..', 'src', 'main.js');
    await require(ip); // Execute the action

    expect(mockSetOutput).toHaveBeenCalledWith('emoji', '🎉');
    expect(mockSetFailed).not.toHaveBeenCalled();
    expect(mockInfo).toHaveBeenCalledWith("Status 'success' translated to emoji: 🎉");
  });

  it('should output 💥 for failure status', async () => {
    // Mock rationale: Simulating GitHub Actions input for 'status'.
    mockGetInput.mockImplementation((name) => {
      if (name === 'status') return 'failure';
      if (name === 'default-emoji') return '❓';
      return '';
    });

    const ip = path.join(__dirname, '..', 'src', 'main.js');
    await require(ip); // Execute the action

    expect(mockSetOutput).toHaveBeenCalledWith('emoji', '💥');
    expect(mockSetFailed).not.toHaveBeenCalled();
    expect(mockInfo).toHaveBeenCalledWith("Status 'failure' translated to emoji: 💥");
  });

  it('should output 🛑 for cancelled status', async () => {
    // Mock rationale: Simulating GitHub Actions input for 'status'.
    mockGetInput.mockImplementation((name) => {
      if (name === 'status') return 'cancelled';
      if (name === 'default-emoji') return '❓';
      return '';
    });

    const ip = path.join(__dirname, '..', 'src', 'main.js');
    await require(ip); // Execute the action

    expect(mockSetOutput).toHaveBeenCalledWith('emoji', '🛑');
    expect(mockSetFailed).not.toHaveBeenCalled();
    expect(mockInfo).toHaveBeenCalledWith("Status 'cancelled' translated to emoji: 🛑");
  });

  it('should output ⏭️ for skipped status', async () => {
    // Mock rationale: Simulating GitHub Actions input for 'status'.
    mockGetInput.mockImplementation((name) => {
      if (name === 'status') return 'skipped';
      if (name === 'default-emoji') return '❓';
      return '';
    });

    const ip = path.join(__dirname, '..', 'src', 'main.js');
    await require(ip); // Execute the action

    expect(mockSetOutput).toHaveBeenCalledWith('emoji', '⏭️');
    expect(mockSetFailed).not.toHaveBeenCalled();
    expect(mockInfo).toHaveBeenCalledWith("Status 'skipped' translated to emoji: ⏭️");
  });

  it('should output ⚪ for neutral status', async () => {
    // Mock rationale: Simulating GitHub Actions input for 'status'.
    mockGetInput.mockImplementation((name) => {
      if (name === 'status') return 'neutral';
      if (name === 'default-emoji') return '❓';
      return '';
    });

    const ip = path.join(__dirname, '..', 'src', 'main.js');
    await require(ip); // Execute the action

    expect(mockSetOutput).toHaveBeenCalledWith('emoji', '⚪');
    expect(mockSetFailed).not.toHaveBeenCalled();
    expect(mockInfo).toHaveBeenCalledWith("Status 'neutral' translated to emoji: ⚪");
  });

  it('should output ⏳ for waiting status', async () => {
    // Mock rationale: Simulating GitHub Actions input for 'status'.
    mockGetInput.mockImplementation((name) => {
      if (name === 'status') return 'waiting';
      if (name === 'default-emoji') return '❓';
      return '';
    });

    const ip = path.join(__dirname, '..', 'src', 'main.js');
    await require(ip); // Execute the action

    expect(mockSetOutput).toHaveBeenCalledWith('emoji', '⏳');
    expect(mockSetFailed).not.toHaveBeenCalled();
    expect(mockInfo).toHaveBeenCalledWith("Status 'waiting' translated to emoji: ⏳");
  });

  it('should output 🏃 for running status', async () => {
    // Mock rationale: Simulating GitHub Actions input for 'status'.
    mockGetInput.mockImplementation((name) => {
      if (name === 'status') return 'running';
      if (name === 'default-emoji') return '❓';
      return '';
    });

    const ip = path.join(__dirname, '..', 'src', 'main.js');
    await require(ip); // Execute the action

    expect(mockSetOutput).toHaveBeenCalledWith('emoji', '🏃');
    expect(mockSetFailed).not.toHaveBeenCalled();
    expect(mockInfo).toHaveBeenCalledWith("Status 'running' translated to emoji: 🏃");
  });

  it('should use default-emoji for unknown status', async () => {
    // Mock rationale: Simulating GitHub Actions input for an unrecognized 'status'.
    mockGetInput.mockImplementation((name) => {
      if (name === 'status') return 'unknown_status';
      if (name === 'default-emoji') return '🤔'; // Custom default
      return '';
    });

    const ip = path.join(__dirname, '..', 'src', 'main.js');
    await require(ip); // Execute the action

    expect(mockSetOutput).toHaveBeenCalledWith('emoji', '🤔');
    expect(mockSetFailed).not.toHaveBeenCalled();
    expect(mockInfo).toHaveBeenCalledWith("Status 'unknown_status' translated to emoji: 🤔");
  });

  it('should use default default-emoji if not provided for unknown status', async () => {
    // Mock rationale: Simulating GitHub Actions input for an unrecognized 'status' without providing 'default-emoji'.
    mockGetInput.mockImplementation((name) => {
      if (name === 'status') return 'unforeseen_event';
      // default-emoji is not provided, so it should fall back to the action.yml default '❓'
      return '';
    });

    const ip = path.join(__dirname, '..', 'src', 'main.js');
    await require(ip); // Execute the action

    expect(mockSetOutput).toHaveBeenCalledWith('emoji', '❓'); // The default from action.yml
    expect(mockSetFailed).not.toHaveBeenCalled();
    expect(mockInfo).toHaveBeenCalledWith("Status 'unforeseen_event' translated to emoji: ❓");
  });

  it('should call setFailed if status input is missing', async () => {
    // Mock rationale: Simulating GitHub Actions input where 'status' is required but missing.
    mockGetInput.mockImplementation((name) => {
      if (name === 'status') throw new Error("Input required and not supplied: status"); // Simulate core.getInput required error
      return '';
    });

    const ip = path.join(__dirname, '..', 'src', 'main.js');
    await require(ip); // Execute the action

    expect(mockSetFailed).toHaveBeenCalledWith("Input required and not supplied: status");
    expect(mockSetOutput).not.toHaveBeenCalled();
  });
});
