import * as fs from 'fs';
import * as path from 'path';
import { MoraleData, MoraleEntry, Mood } from '../src/types';

// Mock fs module
const mockMoraleData: MoraleData = { entries: [] };
const mockFilePath = path.join(process.cwd(), 'morale.json');

jest.mock('fs', () => ({
  existsSync: jest.fn((p) => p === mockFilePath),
  readFileSync: jest.fn((p) => {
    if (p === mockFilePath) {
      return JSON.stringify(mockMoraleData); // # Mock rationale: Simulate reading the morale data file.
    }
    throw new Error('File not found');
  }),
  writeFileSync: jest.fn((p, data) => {
    if (p === mockFilePath) {
      Object.assign(mockMoraleData, JSON.parse(data)); // # Mock rationale: Simulate writing to the morale data file.
    }
  }),
}));

// Mock console.log and console.error to capture output
const mockConsoleLog = jest.spyOn(console, 'log').mockImplementation(() => {}); // # Mock rationale: Prevent console output during tests and allow assertion on messages.
const mockConsoleError = jest.spyOn(console, 'error').mockImplementation(() => {}); // # Mock rationale: Prevent console output during tests and allow assertion on error messages.

// Helper to run the main script with mocked argv
function runMain(argv: string[]) {
  // Clear module cache to ensure fresh import with mocked process.argv
  jest.resetModules();
  process.argv = ['node', 'index.ts', ...argv]; // # Mock rationale: Simulate command-line arguments for the CLI.
  require('../src/index'); // This will execute the main function
}

describe('Nightly Morale Monitor CLI', () => {
  beforeEach(() => {
    // Reset mock data and console logs before each test
    mockMoraleData.entries = [];
    (fs.existsSync as jest.Mock).mockClear();
    (fs.readFileSync as jest.Mock).mockClear();
    (fs.writeFileSync as jest.Mock).mockClear();
    mockConsoleLog.mockClear();
    mockConsoleError.mockClear();
  });

  it('should display help when no command is given', () => {
    runMain([]);
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Nightly Morale Monitor'));
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Usage:'));
  });

  it('should display help for "help" command', () => {
    runMain(['help']);
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Nightly Morale Monitor'));
  });

  it('should add a morale entry', () => {
    const testMood: Mood = "Hopeful as a Seedling";
    const testNotes = "Found a new water source!";
    runMain(['add', testMood, testNotes]);

    expect(fs.writeFileSync).toHaveBeenCalledTimes(1);
    expect(mockMoraleData.entries.length).toBe(1);
    expect(mockMoraleData.entries[0].mood).toBe(testMood);
    expect(mockMoraleData.entries[0].notes).toBe(testNotes);
    expect(mockMoraleData.entries[0].date).toBe(new Date().toISOString().split('T')[0]);
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining(`Morale entry added for ${new Date().toISOString().split('T')[0]}: ${testMood}`));
  });

  it('should add a morale entry without notes', () => {
    const testMood: Mood = "Neutral as a Deactivated Sentry";
    runMain(['add', testMood]);

    expect(fs.writeFileSync).toHaveBeenCalledTimes(1);
    expect(mockMoraleData.entries.length).toBe(1);
    expect(mockMoraleData.entries[0].mood).toBe(testMood);
    expect(mockMoraleData.entries[0].notes).toBeUndefined();
  });

  it('should error on invalid mood', () => {
    runMain(['add', 'Invalid Mood']);
    expect(mockConsoleError).toHaveBeenCalledWith(expect.stringContaining('Error: Invalid mood "Invalid Mood"'));
    expect(fs.writeFileSync).not.toHaveBeenCalled();
  });

  it('should list morale entries', () => {
    const today = new Date().toISOString().split('T')[0];
    mockMoraleData.entries.push({ date: today, mood: "Radiant as a Supernova", notes: "Good day" });
    mockMoraleData.entries.push({ date: today, mood: "Gloomy as a Nuclear Winter" });

    runMain(['list']);
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('--- Morale Log ---'));
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining(`${today} - Radiant as a Supernova (Good day)`));
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining(`${today} - Gloomy as a Nuclear Winter`));
  });

  it('should report no entries when empty', () => {
    runMain(['list']);
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('No morale entries logged yet.'));
  });

  it('should generate a morale report', () => {
    const today = new Date().toISOString().split('T')[0];
    mockMoraleData.entries.push({ date: today, mood: "Hopeful as a Seedling" }); // Score 4
    mockMoraleData.entries.push({ date: today, mood: "Radiant as a Supernova" }); // Score 5

    runMain(['report']);
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('--- Morale Report ---'));
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Total entries: 2'));
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Average morale score: 4.50'));
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Current trend: Morale is on the rise!'));
  });

  it('should generate a morale report with dipping trend', () => {
    const today = new Date().toISOString().split('T')[0];
    mockMoraleData.entries.push({ date: today, mood: "Radiant as a Supernova" }); // Score 5
    mockMoraleData.entries.push({ date: today, mood: "Hopeful as a Seedling" }); // Score 4

    runMain(['report']);
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Current trend: Morale seems to be dipping.'));
  });

  it('should generate a morale report with stable trend', () => {
    const today = new Date().toISOString().split('T')[0];
    mockMoraleData.entries.push({ date: today, mood: "Hopeful as a Seedling" }); // Score 4
    mockMoraleData.entries.push({ date: today, mood: "Hopeful as a Seedling" }); // Score 4

    runMain(['report']);
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Current trend: Morale is stable.'));
  });

  it('should report insufficient entries for trend', () => {
    mockMoraleData.entries.push({ date: '2023-01-01', mood: "Hopeful as a Seedling" });
    runMain(['report']);
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Need at least two entries to generate a trend report.'));
  });

  it('should clear all morale entries with --force', () => {
    mockMoraleData.entries.push({ date: '2023-01-01', mood: "Hopeful as a Seedling" });
    runMain(['clear', '--force']);
    expect(fs.writeFileSync).toHaveBeenCalledTimes(1);
    expect(mockMoraleData.entries.length).toBe(0);
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('All morale entries have been purged.'));
  });

  it('should not clear entries without --force', () => {
    mockMoraleData.entries.push({ date: '2023-01-01', mood: "Hopeful as a Seedling" });
    runMain(['clear']);
    expect(fs.writeFileSync).not.toHaveBeenCalled();
    expect(mockMoraleData.entries.length).toBe(1);
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining("To clear all entries, run 'nmm clear --force'."));
  });

  it('should handle unknown command', () => {
    runMain(['unknown-command']);
    expect(mockConsoleError).toHaveBeenCalledWith(expect.stringContaining('Error: Unknown command "unknown-command".'));
  });
});
