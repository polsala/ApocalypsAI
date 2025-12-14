jest.mock('@actions/core', () => ({
  getInput: jest.fn(),
  setOutput: jest.fn(),
  setFailed: jest.fn(),
}));

const core = require('@actions/core');
const { run, determineLabel } = require('../src/index');

describe('determineLabel', () => {
  const mapping = {
    critical: ['crash'],
    high: ['error'],
    medium: ['slow'],
    low: ['typo']
  };
  test('matches critical', () => {
    expect(determineLabel('App Crash on start', mapping)).toBe('critical');
  });
  test('matches high when no critical', () => {
    expect(determineLabel('Error loading page', mapping)).toBe('high');
  });
  test('returns untriaged when no match', () => {
    expect(determineLabel('Random title', mapping)).toBe('untriaged');
  });
});

describe('run action', () => {
  const mapping = {
    critical: ['crash'],
    high: ['error'],
    medium: ['slow'],
    low: ['typo']
  };
  beforeEach(() => {
    jest.clearAllMocks();
  });
  test('sets output label', () => {
    core.getInput.mockImplementation((name) => {
      if (name === 'title') return 'App Crash';
      if (name === 'priority_keywords') return JSON.stringify(mapping);
    });
    run();
    expect(core.setOutput).toHaveBeenCalledWith('label', 'critical');
  });
  test('fails on invalid JSON', () => {
    core.getInput.mockImplementation((name) => {
      if (name === 'title') return 'Anything';
      if (name === 'priority_keywords') return 'notjson';
    });
    run();
    expect(core.setFailed).toHaveBeenCalledWith('priority_keywords must be valid JSON');
  });
});
