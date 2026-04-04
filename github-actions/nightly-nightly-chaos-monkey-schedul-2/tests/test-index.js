// Mock rationale: We mock Math.random to control probabilistic outcomes and Date to simulate specific times
jest.mock('crypto', () => ({
  randomInt: jest.fn().mockReturnValue(1)
}));

global.console = {
  log: jest.fn(),
  error: jest.fn()
};

describe('Chaos Monkey Scheduler', () => {
  beforeEach(() => {
    jest.resetModules();
    jest.clearAllMocks();
    
    // Mock core.getInput
    jest.mock('@actions/core', () => ({
      getInput: jest.fn(),
      getBooleanInput: jest.fn(),
      setOutput: jest.fn(),
      setFailed: jest.fn()
    }));
    
    // Mock Date
    global.Date = jest.fn(() => new Date('2023-04-01T03:00:00Z'));
    global.Date.now = jest.fn(() => new Date('2023-04-01T03:00:00Z').getTime());
    global.Date.prototype.getTime = jest.fn(() => new Date('2023-04-01T03:00:00Z').getTime());
    global.Date.prototype.getUTCHours = jest.fn(() => 3);
  });

  test('should schedule event when in off-peak and probability hits', async () => {
    jest.mock('@actions/core', () => ({
      getInput: (name) => {
        switch(name) {
          case 'probability': return '1.0';
          case 'start_hour': return '22';
          case 'end_hour': return '6';
          default: return '';
        }
      },
      getBooleanInput: (name) => {
        return name === 'dry_run' ? false : undefined;
      },
      setOutput: jest.fn(),
      setFailed: jest.fn()
    }));

    Math.random = jest.fn(() => 0.1); // Always hit probability
    
    const { run } = require('../src/index');
    await run();
    
    expect(console.log).toHaveBeenCalledWith(expect.stringContaining('Chaos event scheduled'));
  });

  test('should not schedule event when out of off-peak window', async () => {
    global.Date.prototype.getUTCHours = jest.fn(() => 15); // During business hours
    
    jest.mock('@actions/core', () => ({
      getInput: (name) => {
        switch(name) {
          case 'probability': return '1.0';
          case 'start_hour': return '22';
          case 'end_hour': return '6';
          default: return '';
        }
      },
      getBooleanInput: (name) => {
        return name === 'dry_run' ? false : undefined;
      },
      setOutput: jest.fn(),
      setFailed: jest.fn()
    }));

    Math.random = jest.fn(() => 0.1);
    
    const { run } = require('../src/index');
    await run();
    
    expect(console.log).toHaveBeenCalledWith('Not within off-peak window. Skipping chaos event.');
  });

  test('should respect probability setting', async () => {
    jest.mock('@actions/core', () => ({
      getInput: (name) => {
        switch(name) {
          case 'probability': return '0.0'; // Never schedule
          case 'start_hour': return '22';
          case 'end_hour': return '6';
          default: return '';
        }
      },
      getBooleanInput: (name) => {
        return name === 'dry_run' ? false : undefined;
      },
      setOutput: jest.fn(),
      setFailed: jest.fn()
    }));

    Math.random = jest.fn(() => 0.9); // Always miss probability
    
    const { run } = require('../src/index');
    await run();
    
    expect(console.log).toHaveBeenCalledWith('🎲 No chaos event scheduled this time.');
  });
});
