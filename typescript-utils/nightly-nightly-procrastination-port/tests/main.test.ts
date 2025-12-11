import * as fs from 'fs';
import * as path from 'path';
import { Command } from 'commander';
import chalk from 'chalk';

// Mock fs and path modules
jest.mock('fs');
jest.mock('path', () => ({
  ...jest.requireActual('path'),
  join: jest.fn((...args) => args.join('/')), // Simplify join for testing
  homedir: jest.fn(() => '/home/testuser'),
}));

// Mock chalk for testing output
jest.mock('chalk', () => ({
  green: jest.fn(msg => msg),
  red: jest.fn(msg => msg),
  yellow: jest.fn(msg => msg),
  cyan: jest.fn(msg => msg),
  magenta: jest.fn(msg => msg),
}));

// Mock console.log and console.error
const mockConsoleLog = jest.spyOn(console, 'log').mockImplementation(() => {});
const mockConsoleError = jest.spyOn(console, 'error').mockImplementation(() => {});

// Mock process.exit
const mockProcessExit = jest.spyOn(process, 'exit').mockImplementation((() => {}) as any);

// Mock Date.now() for deterministic time
const MOCK_DATE = 1678886400000; // March 15, 2023 12:00:00 PM UTC
const mockDateNow = jest.spyOn(Date, 'now').mockReturnValue(MOCK_DATE);

// Mock setTimeout and clearTimeout
jest.useFakeTimers();

// Import the module to be tested AFTER mocks are set up
// We need to re-import or re-require to get the mocked versions
// For simplicity in this single file, we'll just ensure the mocks are global before the test suite runs
// In a real project, you'd import the functions directly from their respective files.

// Helper to get the module under test, ensuring mocks are applied
const getModule = () => {
  // Clear module cache to ensure fresh import with mocks
  jest.resetModules();
  return require('../src/main');
};

describe('Nightly Procrastination Portal Blocker', () => {
  let mainModule: any;
  let mockHostsContent: string;
  let mockState: any;

  beforeEach(() => {
    mockHostsContent = '127.0.0.1\tlocalhost\n::1\tlocalhost';
    mockState = {
      blockedSites: [],
      originalHostsContent: null,
      unblockTimeoutId: null,
    };

    // Reset all mocks
    jest.clearAllMocks();
    jest.runOnlyPendingTimers(); // Clear any timers from previous tests

    // Setup fs mocks
    (fs.readFileSync as jest.Mock).mockReturnValue(mockHostsContent);
    (fs.writeFileSync as jest.Mock).mockImplementation(() => {});
    (fs.existsSync as jest.Mock).mockReturnValue(false); // Default: no state file, no NPPB dir
    (fs.mkdirSync as jest.Mock).mockImplementation(() => {});

    // Setup path mocks
    (path.join as jest.Mock).mockImplementation((...args) => args.join('/'));
    (path.homedir as jest.Mock).mockReturnValue('/home/testuser');

    // Re-import the module to ensure it uses the fresh mocks
    mainModule = getModule();

    // Mock loadState and saveState within the module context if needed, or ensure fs mocks handle it
    // For this test, we'll directly mock fs.readFileSync/writeFileSync for the state file.
    (fs.existsSync as jest.Mock).withArgs('/home/testuser/.nppb').mockReturnValue(true);
    (fs.existsSync as jest.Mock).withArgs('/home/testuser/.nppb/state.json').mockReturnValue(false);
  });

  afterEach(() => {
    mockDateNow.mockRestore();
    jest.runOnlyPendingTimers();
  });

  describe('parseDuration', () => {
    it('should parse seconds correctly', () => {
      expect(mainModule.parseDuration('30s')).toBe(30 * 1000);
    });

    it('should parse minutes correctly', () => {
      expect(mainModule.parseDuration('15m')).toBe(15 * 60 * 1000);
    });

    it('should parse hours correctly', () => {
      expect(mainModule.parseDuration('2h')).toBe(2 * 60 * 60 * 1000);
    });

    it('should parse combined durations correctly', () => {
      expect(mainModule.parseDuration('1h30m')).toBe(1 * 60 * 60 * 1000 + 30 * 60 * 1000);
      expect(mainModule.parseDuration('2h15m30s')).toBe(2 * 60 * 60 * 1000 + 15 * 60 * 1000 + 30 * 1000);
    });

    it('should throw error for invalid duration', () => {
      expect(() => mainModule.parseDuration('invalid')).toThrow('Invalid duration format');
      expect(() => mainModule.parseDuration('1x')).toThrow('Invalid duration format');
      expect(() => mainModule.parseDuration('')).toThrow('Invalid duration format');
    });
  });

  describe('blockPortals', () => {
    it('should block sites and modify hosts file', async () => {
      await mainModule.blockPortals('1h', ['example.com', 'test.org']);

      expect(fs.readFileSync).toHaveBeenCalledWith('/etc/hosts', 'utf8');
      expect(fs.writeFileSync).toHaveBeenCalledWith(
        '/etc/hosts',
        `${mockHostsContent}\n# --- NPPB Blocked Portals ---\n127.0.0.1\texample.com\n127.0.0.1\ttest.org\n# --- End NPPB Blocked Portals ---`,
        'utf8'
      );

      // Check state saving
      expect(fs.writeFileSync).toHaveBeenCalledWith(
        '/home/testuser/.nppb/state.json',
        expect.stringContaining('"site": "example.com"'),
        'utf8'
      );
      expect(fs.writeFileSync).toHaveBeenCalledWith(
        '/home/testuser/.nppb/state.json',
        expect.stringContaining('"site": "test.org"'),
        'utf8'
      );
      expect(fs.writeFileSync).toHaveBeenCalledWith(
        '/home/testuser/.nppb/state.json',
        expect.stringContaining(`"originalHostsContent": "${mockHostsContent.replace(/\n/g, '\\n')}"`),
        'utf8'
      );

      expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Poof! The following portals have been sealed for 1h'));
      expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('- example.com'));
      expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('- test.org'));
    });

    it('should not block if portals are already blocked', async () => {
      // Mock rationale: Simulate a pre-existing blocked state to test the early exit condition.
      (fs.existsSync as jest.Mock).withArgs('/home/testuser/.nppb/state.json').mockReturnValue(true);
      (fs.readFileSync as jest.Mock).withArgs('/home/testuser/.nppb/state.json', 'utf8').mockReturnValue(JSON.stringify({
        blockedSites: [{ site: 'existing.com', blockedUntil: MOCK_DATE + 3600000 }],
        originalHostsContent: mockHostsContent,
        unblockTimeoutId: null,
      }));

      await mainModule.blockPortals('1h', ['new.com']);

      expect(fs.writeFileSync).not.toHaveBeenCalledWith('/etc/hosts', expect.any(String), 'utf8');
      expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Some portals are already blocked. Unblock them first or wait for them to expire.'));
    });

    it('should handle hosts file read error', async () => {
      // Mock rationale: Simulate a scenario where the hosts file cannot be read, e.g., due to permissions.
      (fs.readFileSync as jest.Mock).withArgs('/etc/hosts', 'utf8').mockImplementation(() => {
        throw new Error('Permission denied');
      });

      await mainModule.blockPortals('1h', ['example.com']);

      expect(mockConsoleError).toHaveBeenCalledWith(expect.stringContaining('Error reading hosts file'));
      expect(mockProcessExit).toHaveBeenCalledWith(1);
    });

    it('should set a timeout for automatic unblocking', async () => {
      await mainModule.blockPortals('1h', ['example.com']);
      expect(setTimeout).toHaveBeenCalledTimes(1);
      expect(setTimeout).toHaveBeenCalledWith(expect.any(Function), 3600000); // 1 hour
    });
  });

  describe('unblockPortals', () => {
    it('should restore hosts file and clear state', async () => {
      // Mock rationale: Simulate a blocked state that needs to be unblocked.
      (fs.existsSync as jest.Mock).withArgs('/home/testuser/.nppb/state.json').mockReturnValue(true);
      (fs.readFileSync as jest.Mock).withArgs('/home/testuser/.nppb/state.json', 'utf8').mockReturnValue(JSON.stringify({
        blockedSites: [{ site: 'example.com', blockedUntil: MOCK_DATE + 3600000 }],
        originalHostsContent: mockHostsContent,
        unblockTimeoutId: 123, // Simulate a timeout ID
      }));

      await mainModule.unblockPortals();

      expect(fs.writeFileSync).toHaveBeenCalledWith('/etc/hosts', mockHostsContent, 'utf8');
      expect(fs.writeFileSync).toHaveBeenCalledWith(
        '/home/testuser/.nppb/state.json',
        JSON.stringify(mockState, null, 2),
        'utf8'
      );
      expect(clearTimeout).toHaveBeenCalledWith(123);
      expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('All digital portals have been restored!'));
    });

    it('should do nothing if no portals are blocked', async () => {
      await mainModule.unblockPortals();

      expect(fs.writeFileSync).not.toHaveBeenCalledWith('/etc/hosts', expect.any(String), 'utf8');
      expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('No portals are currently blocked by NPPB. All clear!'));
    });
  });

  describe('showStatus', () => {
    it('should display blocked sites and remaining time', () => {
      // Mock rationale: Simulate a blocked state to verify status output.
      (fs.existsSync as jest.Mock).withArgs('/home/testuser/.nppb/state.json').mockReturnValue(true);
      (fs.readFileSync as jest.Mock).withArgs('/home/testuser/.nppb/state.json', 'utf8').mockReturnValue(JSON.stringify({
        blockedSites: [
          { site: 'example.com', blockedUntil: MOCK_DATE + 3600000 + 10000 }, // 1h 10s from MOCK_DATE
          { site: 'test.org', blockedUntil: MOCK_DATE + 60000 }, // 1m from MOCK_DATE
        ],
        originalHostsContent: mockHostsContent,
        unblockTimeoutId: null,
      }));

      mainModule.showStatus();

      expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Current Portal Lockdown Status:'));
      expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('- example.com: Locked for 1h 0m 10s'));
      expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('- test.org: Locked for 1m 0s'));
    });

    it('should display message if no portals are blocked', () => {
      mainModule.showStatus();
      expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('No portals are currently blocked by NPPB. All clear!'));
    });

    it('should unblock automatically if a site has expired', () => {
      // Mock rationale: Simulate an expired block to test automatic unblocking on status check.
      (fs.existsSync as jest.Mock).withArgs('/home/testuser/.nppb/state.json').mockReturnValue(true);
      (fs.readFileSync as jest.Mock).withArgs('/home/testuser/.nppb/state.json', 'utf8').mockReturnValue(JSON.stringify({
        blockedSites: [{ site: 'expired.com', blockedUntil: MOCK_DATE - 1000 }], // Expired 1 second ago
        originalHostsContent: mockHostsContent,
        unblockTimeoutId: null,
      }));

      mainModule.showStatus();

      expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('- expired.com: Expired. Will unblock on next command.'));
      expect(fs.writeFileSync).toHaveBeenCalledWith('/etc/hosts', mockHostsContent, 'utf8'); // Should have called unblockPortals
      expect(fs.writeFileSync).toHaveBeenCalledWith(
        '/home/testuser/.nppb/state.json',
        JSON.stringify(mockState, null, 2),
        'utf8'
      );
    });
  });

  describe('initial block check', () => {
    it('should unblock expired sites on initial load', () => {
      // Mock rationale: Simulate an expired block existing when the script first runs.
      (fs.existsSync as jest.Mock).withArgs('/home/testuser/.nppb/state.json').mockReturnValue(true);
      (fs.readFileSync as jest.Mock).withArgs('/home/testuser/.nppb/state.json', 'utf8').mockReturnValue(JSON.stringify({
        blockedSites: [{ site: 'expired.com', blockedUntil: MOCK_DATE - 1000 }],
        originalHostsContent: mockHostsContent,
        unblockTimeoutId: null,
      }));

      // Re-import the module to trigger the initial check
      mainModule = getModule();

      expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Detected expired portal blocks. Automatically unblocking...'));
      expect(fs.writeFileSync).toHaveBeenCalledWith('/etc/hosts', mockHostsContent, 'utf8');
      expect(fs.writeFileSync).toHaveBeenCalledWith(
        '/home/testuser/.nppb/state.json',
        JSON.stringify(mockState, null, 2),
        'utf8'
      );
    });
  });
});
