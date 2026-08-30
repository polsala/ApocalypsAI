const runQuantumChoiceCaster = require('../src/index.js');

describe('nightly-quantum-choice-caster', () => {
  let mockLog;
  let mockExit;
  let originalMathRandom;

  beforeEach(() => {
    mockLog = jest.fn();
    mockExit = jest.fn();
    originalMathRandom = Math.random;
  });

  afterEach(() => {
    Math.random = originalMathRandom;
  });

  test('should display usage and exit if no options are provided', () => {
    // Mock rationale: Simulating no options passed to the function, and mocking exit to prevent actual process termination.
    runQuantumChoiceCaster([], mockLog, mockExit);
    
    expect(mockLog).toHaveBeenCalledWith("🌌 ApocalypsAI Quantum Choice Caster 🌌");
    expect(mockLog).toHaveBeenCalledWith("Usage: nightly-quantum-choice-caster <option1> <option2> [option3...]");
    expect(mockLog).toHaveBeenCalledWith("\nExample: nightly-quantum-choice-caster \"Explore the ruins\" \"Scavenge for supplies\" \"Rest and repair\"");
    expect(mockExit).toHaveBeenCalledWith(1);
    expect(mockLog).toHaveBeenCalledTimes(3); // 3 log calls for usage
  });

  test('should choose the first option deterministically when Math.random is mocked to 0', () => {
    // Mock rationale: Math.random is mocked to ensure a deterministic outcome (always picking the first element) for testing.
    Math.random = jest.fn(() => 0); // Always pick the first element (index 0)
    const options = ['Option A', 'Option B', 'Option C'];

    runQuantumChoiceCaster(options, mockLog, mockExit);

    expect(mockExit).not.toHaveBeenCalled();
    expect(mockLog).toHaveBeenCalledWith(expect.stringContaining('Option A'));
    expect(mockLog).not.toHaveBeenCalledWith(expect.stringContaining('Option B'));
    expect(mockLog).not.toHaveBeenCalledWith(expect.stringContaining('Option C'));
    
    // Check for a whimsical message (first message in the list)
    expect(mockLog).toHaveBeenCalledWith(expect.stringContaining('The cosmic dice have rolled, revealing your path...'));
    expect(mockLog).toHaveBeenCalledWith(expect.stringContaining('May your choice lead to optimal temporal stability.'));
    expect(mockLog).toHaveBeenCalledTimes(3); // 1 whimsical message, 1 chosen option, 1 final message
  });

  test('should choose the last option deterministically when Math.random is mocked to just under 1', () => {
    // Mock rationale: Math.random is mocked to ensure a deterministic outcome (always picking the last element) for testing.
    Math.random = jest.fn(() => 0.999999999); // Always pick the last element
    const options = ['First', 'Middle', 'Last'];

    runQuantumChoiceCaster(options, mockLog, mockExit);

    expect(mockExit).not.toHaveBeenCalled();
    expect(mockLog).toHaveBeenCalledWith(expect.stringContaining('Last'));
    expect(mockLog).not.toHaveBeenCalledWith(expect.stringContaining('First'));
    expect(mockLog).not.toHaveBeenCalledWith(expect.stringContaining('Middle'));
    
    // Check for a whimsical message (last message in the list)
    expect(mockLog).toHaveBeenCalledWith(expect.stringContaining('Behold! The oracle has spoken, and it decrees...'));
    expect(mockLog).toHaveBeenCalledWith(expect.stringContaining('May your choice lead to optimal temporal stability.'));
    expect(mockLog).toHaveBeenCalledTimes(3);
  });

  test('should handle single option correctly', () => {
    // Mock rationale: Math.random is mocked to ensure a deterministic outcome even with a single option.
    Math.random = jest.fn(() => 0); 
    const options = ['Only Choice'];

    runQuantumChoiceCaster(options, mockLog, mockExit);

    expect(mockExit).not.toHaveBeenCalled();
    expect(mockLog).toHaveBeenCalledWith(expect.stringContaining('Only Choice'));
    expect(mockLog).toHaveBeenCalledWith(expect.stringContaining('The cosmic dice have rolled, revealing your path...'));
    expect(mockLog).toHaveBeenCalledWith(expect.stringContaining('May your choice lead to optimal temporal stability.'));
    expect(mockLog).toHaveBeenCalledTimes(3);
  });

  test('should select a specific whimsical message based on Math.random mock', () => {
    // Mock rationale: Math.random is mocked to ensure a deterministic outcome for both option and message selection.
    // options.length = 3, Math.random = 0.5 => index 1 (Option 2)
    // whimsicalMessages.length = 7, Math.random = 0.5 => index 3 (The Quantum Choice Caster hums...)
    Math.random = jest.fn(() => 0.5); 
    const options = ['Option 1', 'Option 2', 'Option 3'];

    runQuantumChoiceCaster(options, mockLog, mockExit);

    expect(mockExit).not.toHaveBeenCalled();
    expect(mockLog).toHaveBeenCalledWith(expect.stringContaining('Option 2'));
    expect(mockLog).toHaveBeenCalledWith(expect.stringContaining('The Quantum Choice Caster hums, and your destiny unfolds as...'));
    expect(mockLog).toHaveBeenCalledWith(expect.stringContaining('May your choice lead to optimal temporal stability.'));
    expect(mockLog).toHaveBeenCalledTimes(3);
  });
});
