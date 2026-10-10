const fs = require('fs');
const path = require('path');
const os = require('os');

jest.mock('fs');

const { addMood, showStats, getLogPath } = require('../src/index');

// Helper to capture console output
function captureConsole(fn) {
  const originalLog = console.log;
  const originalError = console.error;
  let output = '';
  console.log = (msg) => { output += msg + '\n'; };
  console.error = (msg) => { output += msg + '\n'; };
  try {
    fn();
  } finally {
    console.log = originalLog;
    console.error = originalError;
  }
  return output.trim();
}

describe('emoji mood tracker', () => {
  const fakeHome = '/fake/home';
  const fakeLogPath = path.join(fakeHome, '.emoji_mood_log.json');

  beforeAll(() => {
    // Mock os.homedir() to return a deterministic path
    jest.spyOn(os, 'homedir').mockReturnValue(fakeHome);
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  test('addMood writes entry to log', () => {
    // Mock readFileSync to throw (file not existing) and writeFileSync to be a spy
    fs.readFileSync.mockImplementation(() => { throw new Error('ENOENT'); });
    fs.writeFileSync.mockImplementation(() => {});

    const output = captureConsole(() => addMood('😊'));
    expect(output).toBe('Logged mood 😊');
    expect(fs.writeFileSync).toHaveBeenCalledTimes(1);
    const [calledPath, data] = fs.writeFileSync.mock.calls[0];
    expect(calledPath).toBe(fakeLogPath);
    const parsed = JSON.parse(data);
    expect(parsed).toHaveLength(1);
    expect(parsed[0].mood).toBe('😊');
  });

  test('showStats prints aggregated counts', () => {
    const fakeData = [
      { date: '2023-01-01T00:00:00.000Z', mood: '😊' },
      { date: '2023-01-02T00:00:00.000Z', mood: '😴' },
      { date: '2023-01-03T00:00:00.000Z', mood: '😊' }
    ];
    fs.readFileSync.mockReturnValue(JSON.stringify(fakeData, null, 2));

    const output = captureConsole(() => showStats());
    const lines = output.split('\n');
    expect(lines[0]).toBe('Mood statistics:');
    // Order of object keys is not guaranteed; check inclusion
    expect(lines).toEqual(expect.arrayContaining(['😊: 2', '😴: 1']));
  });

  test('showStats handles empty log gracefully', () => {
    fs.readFileSync.mockImplementation(() => { throw new Error('ENOENT'); });
    const output = captureConsole(() => showStats());
    expect(output).toBe('No moods logged yet.');
  });
});
