const { generateSchedule } = require('../src/schedule');
const originalRandom = Math.random;

// Mock random to ensure deterministic tests
beforeEach(() => {
  Math.random = () => 0.5; // Consistent random for testing
});

afterEach(() => {
  Math.random = originalRandom;
});

test('schedule has 12 time-blocked tasks', () => {
  const schedule = generateSchedule();
  expect(schedule.times.length).toBe(12);
  expect(schedule.times.every(item => item.time && item.task)).toBe(true);
});

test('calendar ASCII art has 7 rows with one X marker', () => {
  const schedule = generateSchedule();
  const lines = schedule.asciiArt.split('\n');
  expect(lines.length).toBe(7);
  expect(lines.some(line => line.includes('X'))).toBe(true);
});
