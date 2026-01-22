// Mock rationale: We mock time and randomness to ensure deterministic test behavior.
jest.useFakeTimers();
Math.random = jest.fn();

global.console = { log: jest.fn() };

const { default: chaosClock } = require = null; // Not used due to direct mocking
const { random } = require('lodash');

let chaosClockModule;

beforeEach(() => {
  jest.resetModules();
  jest.clearAllMocks();
  Math.random.mockReset();
  console.log.mockClear();
  chaosClockModule = require('../src/chaos-clock.js');
});

describe('chaos-clock', () => {
  test('displays normal time when no chaos', () => {
    Math.random.mockReturnValue(0.5); // No chaos
    jest.setSystemTime(new Date('2025-04-05T12:34:56'));
    
    const now = new Date();
    const timeStr = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}`;
    
    expect(console.log).toHaveBeenCalledWith(`🕒 ${timeStr}`);
  });

  test('displays chaos message when triggered', () => {
    Math.random.mockReturnValue(0.05); // Trigger chaos
    jest.setSystemTime(new Date('2025-04-05T12:34:56'));
    
    require('../src/chaos-clock.js');
    expect(console.log).toHaveBeenCalledWith(expect.stringMatching(/(🌀|👽|👾|👻|🤖|🦄|🌮|⏰|🕰️|🎉)/));
  });
});
