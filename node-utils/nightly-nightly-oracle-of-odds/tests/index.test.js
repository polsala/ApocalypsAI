const { getProphecy, whimsicalMessages } = require('../src/index');
const chalk = require('chalk');

// Mock chalk to prevent color codes in test output and simplify assertions
// Mock rationale: Chalk is a presentation library. We want to test the logic,
// not the ANSI escape codes it generates. Mocking it ensures deterministic
// string comparisons without worrying about terminal-specific color output.
jest.mock('chalk', () => ({
  bold: jest.fn((text) => `BOLD_${text}_BOLD`),
  red: jest.fn((text) => `RED_${text}_RED`),
  yellow: jest.fn((text) => `YELLOW_${text}_YELLOW`),
  cyan: {
    bold: jest.fn((text) => `CYAN_BOLD_${text}_CYAN_BOLD`)
  },
}));

describe('getProphecy', () => {
  const originalMathRandom = Math.random;

  beforeEach(() => {
    // Reset chalk mocks before each test
    chalk.bold.mockClear();
    chalk.red.mockClear();
    chalk.yellow.mockClear();
    chalk.cyan.bold.mockClear();
  });

  afterEach(() => {
    Math.random = originalMathRandom; // Restore original Math.random
  });

  test('should return a prophecy for a single option', () => {
    // Mock rationale: Math.random is non-deterministic. To make tests reliable,
    // we mock it to return a predictable value (0 in this case) so that the
    // first option and first message template are always chosen.
    Math.random = jest.fn(() => 0); // Always pick the first option and first message

    const options = ['Survive'];
    const prophecy = getProphecy(options);

    const expectedOption = 'Survive';
    const expectedMessageTemplate = whimsicalMessages[0](`BOLD_${expectedOption}_BOLD`);

    expect(prophecy).toBe(expectedMessageTemplate);
    expect(chalk.bold).toHaveBeenCalledWith(expectedOption);
  });

  test('should return a prophecy for multiple options, picking the first', () => {
    // Mock rationale: See above. Predictable Math.random ensures deterministic choice.
    Math.random = jest.fn(() => 0); // Always pick the first option and first message

    const options = ['Option A', 'Option B', 'Option C'];
    const prophecy = getProphecy(options);

    const expectedOption = 'Option A';
    const expectedMessageTemplate = whimsicalMessages[0](`BOLD_${expectedOption}_BOLD`);

    expect(prophecy).toBe(expectedMessageTemplate);
    expect(chalk.bold).toHaveBeenCalledWith(expectedOption);
  });

  test('should return a prophecy for multiple options, picking the last', () => {
    // Mock rationale: See above. Predictable Math.random ensures deterministic choice.
    Math.random = jest.fn(() => 0.999); // Always pick the last option and last message

    const options = ['Option A', 'Option B', 'Option C'];
    const prophecy = getProphecy(options);

    const expectedOption = 'Option C';
    const expectedMessageTemplate = whimsicalMessages[whimsicalMessages.length - 1](`BOLD_${expectedOption}_BOLD`);

    expect(prophecy).toBe(expectedMessageTemplate);
    expect(chalk.bold).toHaveBeenCalledWith(expectedOption);
  });

  test('should return an error message for no options', () => {
    const options = [];
    const prophecy = getProphecy(options);
    expect(prophecy).toBe('RED_The Oracle finds no options to ponder. Its wisdom is silent._RED');
    expect(chalk.red).toHaveBeenCalledWith('The Oracle finds no options to ponder. Its wisdom is silent.');
  });

  test('should use different message templates based on random choice', () => {
    // Mock rationale: We want to ensure that the message template selection logic works.
    // By setting Math.random to specific values, we can control which template is chosen.
    const options = ['Test Option'];

    // Test picking the first message template
    Math.random = jest.fn(() => 0); // Pick first option, first message
    let prophecy = getProphecy(options);
    expect(prophecy).toBe(whimsicalMessages[0]('BOLD_Test Option_BOLD'));

    // Test picking a middle message template (e.g., index 3 out of 7 templates)
    Math.random = jest.fn(() => 3 / whimsicalMessages.length); // Pick first option, 4th message (index 3)
    prophecy = getProphecy(options);
    expect(prophecy).toBe(whimsicalMessages[3]('BOLD_Test Option_BOLD'));

    // Test picking the last message template
    Math.random = jest.fn(() => 0.999); // Pick first option, last message
    prophecy = getProphecy(options);
    expect(prophecy).toBe(whimsicalMessages[whimsicalMessages.length - 1]('BOLD_Test Option_BOLD'));
  });
});
