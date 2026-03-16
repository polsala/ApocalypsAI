const { run } = require('../dist/index.js'); // Assuming your build process outputs to dist/index.js
const core = require('@actions/core');

// Mocking @actions/core
jest.mock('@actions/core', () => ({
  getInput: jest.fn(),
  setOutput: jest.fn(),
  setFailed: jest.fn()
}));

// Mocking Math.random for deterministic tests
let mockMath = Object.create(Math);
mockMath.random = jest.fn();
global.Math = mockMath;

describe('Chaos Reporter Action', () => {
  let mockGetInput;
  let mockSetOutput;
  let mockSetFailed;

  beforeEach(() => {
    jest.clearAllMocks();
    mockGetInput = core.getInput;
    mockSetOutput = core.setOutput;
    mockSetFailed = core.setFailed;

    // Reset Math.random mock for each test
    mockMath.random.mockReset();
  });

  test('generates a poetic report with default settings', () => {
    // Mock Math.random to return a specific value for deterministic output
    mockMath.random.mockReturnValue(0.1); // This should pick the first element in the array

    mockGetInput.mockReturnValue(''); // Default chaos_level and reporting_style

    run();

    expect(mockSetOutput).toHaveBeenCalledWith('chaos_report', expect.stringContaining('Hark, brave adventurers of the digital realm!'));
    expect(mockSetOutput).toHaveBeenCalledWith('chaos_report', expect.stringContaining('a rogue semicolon danced')); // Based on mockMath.random returning 0.1
  });

  test('generates a technical report with high chaos', () => {
    mockMath.random.mockReturnValue(0.8); // This should pick an element later in the array for high chaos

    mockGetInput.mockImplementation((name) => {
      if (name === 'chaos_level') return 'high';
      if (name === 'reporting_style') return 'technical';
      return '';
    });

    run();

    expect(mockSetOutput).toHaveBeenCalledWith('chaos_report', expect.stringContaining('**Chaos Event Report**'));
    expect(mockSetOutput).toHaveBeenCalledWith('chaos_report', expect.stringContaining('**Chaos Level:** HIGH'));
    expect(mockSetOutput).toHaveBeenCalledWith('chaos_report', expect.stringContaining('AI model exhibited emergent behavior deviating from training parameters.')); // Based on mockMath.random returning 0.8
  });

  test('generates a humorous report with moderate chaos', () => {
    mockMath.random.mockReturnValue(0.4); // This should pick an element in the middle for moderate chaos

    mockGetInput.mockImplementation((name) => {
      if (name === 'chaos_level') return 'moderate';
      if (name === 'reporting_style') return 'humorous';
      return '';
    });

    run();

    expect(mockSetOutput).toHaveBeenCalledWith('chaos_report', expect.stringContaining('**Well, This is Awkward... A Chaos Report!**'));
    expect(mockSetOutput).toHaveBeenCalledWith('chaos_report', expect.stringContaining('The office hamster decided to re-route the network cables for a better view.')); // Based on mockMath.random returning 0.4
  });

  test('sets failed status on error', () => {
    const testError = new Error('Something went terribly wrong!');
    mockGetInput.mockImplementation(() => {
      throw testError;
    });

    run();

    expect(mockSetFailed).toHaveBeenCalledWith('Something terribly wrong!');
  });
});
