const core = require('@actions/core');
const path = require('path');

// Mock the @actions/core library
const mockGetInput = jest.fn();
const mockSetFailed = jest.fn();
const mockInfo = jest.fn();
const mockAddRaw = jest.fn();

jest.mock('@actions/core', () => ({
  getInput: mockGetInput,
  setFailed: mockSetFailed,
  info: mockInfo,
  summary: {
    addRaw: mockAddRaw,
  },
}));

describe('Nightly Failure Fortifier', () => {
  let originalMathRandom;

  beforeAll(() => {
    // Store original Math.random
    originalMathRandom = Math.random;
  });

  beforeEach(() => {
    jest.clearAllMocks();
    // Mock Math.random for deterministic tests
    // Mock rationale: Ensures random message selection is predictable for testing.
    Math.random = jest.fn(() => 0.5); // Always pick the middle element if possible
  });

  afterAll(() => {
    // Restore original Math.random
    Math.random = originalMathRandom;
  });

  it('should post a random message from the input list to the summary', () => {
    mockGetInput.mockImplementation((name) => {
      if (name === 'messages') {
        return 'Message 1\nMessage 2\nMessage 3';
      } else if (name === 'fallback_message') {
        return 'Fallback';
      }
      return '';
    });

    // Load the action's main script, which executes the run() function
    require('../src/main.js');

    // Math.random() returns 0.5, so for 3 messages, it should pick index 1 (Message 2)
    // floor(0.5 * 3) = floor(1.5) = 1
    expect(mockAddRaw).toHaveBeenCalledWith(expect.stringContaining('Message 2'));
    expect(mockInfo).toHaveBeenCalledWith('Fortifying message added to workflow summary.');
    expect(mockSetFailed).not.toHaveBeenCalled();
  });

  it('should use the fallback message if messages input is empty', () => {
    mockGetInput.mockImplementation((name) => {
      if (name === 'messages') {
        return '';
      } else if (name === 'fallback_message') {
        return 'This is the fallback message.';
      }
      return '';
    });

    require('../src/main.js');

    expect(mockAddRaw).toHaveBeenCalledWith(expect.stringContaining('This is the fallback message.'));
    expect(mockInfo).toHaveBeenCalledWith('No valid messages provided. Using fallback message.');
    expect(mockSetFailed).not.toHaveBeenCalled();
  });

  it('should use the fallback message if messages input contains only whitespace/empty lines', () => {
    mockGetInput.mockImplementation((name) => {
      if (name === 'messages') {
        return '\n \t \n';
      } else if (name === 'fallback_message') {
        return 'Whitespace fallback.';
      }
      return '';
    });

    require('../src/main.js');

    expect(mockAddRaw).toHaveBeenCalledWith(expect.stringContaining('Whitespace fallback.'));
    expect(mockInfo).toHaveBeenCalledWith('No valid messages provided. Using fallback message.');
    expect(mockSetFailed).not.toHaveBeenCalled();
  });

  it('should handle messages with surrounding quotes correctly', () => {
    mockGetInput.mockImplementation((name) => {
      if (name === 'messages') {
        return '"Quoted Message 1"\n"Quoted Message 2"';
      } else if (name === 'fallback_message') {
        return 'Fallback';
      }
      return '';
    });

    require('../src/main.js');

    // Math.random() returns 0.5, so for 2 messages, it should pick index 1 (Quoted Message 2)
    // floor(0.5 * 2) = floor(1) = 1
    expect(mockAddRaw).toHaveBeenCalledWith(expect.stringContaining('Quoted Message 2'));
    expect(mockInfo).toHaveBeenCalledWith('Fortifying message added to workflow summary.');
    expect(mockSetFailed).not.toHaveBeenCalled();
  });

  it('should call setFailed if an error occurs', () => {
    mockGetInput.mockImplementation((name) => {
      if (name === 'messages') {
        throw new Error('Test error during input retrieval');
      }
      return '';
    });

    require('../src/main.js');

    expect(mockSetFailed).toHaveBeenCalledWith('Action failed with error: Test error during input retrieval');
    expect(mockAddRaw).not.toHaveBeenCalled();
  });
});
