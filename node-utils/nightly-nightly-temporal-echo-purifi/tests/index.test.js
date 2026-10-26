const { parseArgs, getFileAgeInDays, scanDirectoryForEchoes, reportEchoes, main } = require('../src/index');
const fs = require('fs');
const path = require('path');

const RealDate = Date; // Capture the original Date constructor

// Mock rationale: We need to control file system interactions (reading directories, getting file stats)
// to ensure deterministic and offline testing without actual file system side effects.
jest.mock('fs', () => ({
  existsSync: jest.fn(),
  lstatSync: jest.fn(),
  readdirSync: jest.fn(),
  statSync: jest.fn(),
}));

// Mock console.log to capture output
const mockConsoleLog = jest.spyOn(console, 'log').mockImplementation(() => {});
const mockConsoleError = jest.spyOn(console, 'error').mockImplementation(() => {});

describe('parseArgs', () => {
  const originalArgv = process.argv;

  beforeEach(() => {
    process.argv = [...originalArgv.slice(0, 2)]; // Reset argv to base
  });

  afterAll(() => {
    process.argv = originalArgv;
  });

  test('should parse --path and --age arguments', () => {
    process.argv.push('--path', '/test/dir', '--age', '30');
    const args = parseArgs();
    expect(args).toEqual({ path: '/test/dir', age: '30' });
  });

  test('should handle missing values gracefully (though main() validates)', () => {
    process.argv.push('--path', '/test/dir', '--age');
    const args = parseArgs();
    expect(args).toEqual({ path: '/test/dir', age: true }); // 'age' becomes true if no value follows
  });

  test('should return empty object if no arguments', () => {
    const args = parseArgs();
    expect(args).toEqual({});
  });
});

describe('getFileAgeInDays', () => {
  test('should return correct age for an old file', () => {
    const now = new Date('2023-01-01T12:00:00Z');
    const mtime = new Date('2022-01-01T12:00:00Z'); // 365 days old
    fs.statSync.mockReturnValueOnce({ mtime });

    // Mock rationale: Temporarily override Date to control 'now' for deterministic age calculation.
    global.Date = jest.fn(() => now);
    global.Date.now = jest.fn(() => now.getTime());
    global.Date.prototype.getTime = jest.fn(() => now.getTime());

    const age = getFileAgeInDays('/some/file.txt');
    expect(age).toBe(365);

    global.Date = RealDate; // Restore original Date
  });

  test('should return 0 or 1 for a very recent file', () => {
    const now = new Date('2023-01-01T12:00:00Z');
    const mtime = new Date('2023-01-01T11:59:00Z'); // Less than a day old
    fs.statSync.mockReturnValueOnce({ mtime });

    // Mock rationale: Temporarily override Date to control 'now' for deterministic age calculation.
    global.Date = jest.fn(() => now);
    global.Date.now = jest.fn(() => now.getTime());
    global.Date.prototype.getTime = jest.fn(() => now.getTime());

    const age = getFileAgeInDays('/some/recent.txt');
    expect(age).toBe(1); // ceil(less than 1 day) is 1

    global.Date = RealDate; // Restore original Date
  });

  test('should handle stat error', () => {
    fs.statSync.mockImplementationOnce(() => {
      throw new Error('Permission denied');
    });
    const age = getFileAgeInDays('/nonexistent/file.txt');
    expect(age).toBe(-1);
    expect(mockConsoleError).toHaveBeenCalledWith(expect.stringContaining('Error getting stats'));
  });
});

describe('scanDirectoryForEchoes', () => {
  const testDirPath = '/test/data';
  const maxAge = 30;

  beforeEach(() => {
    jest.clearAllMocks();
    fs.existsSync.mockReturnValue(true);
    fs.lstatSync.mockReturnValue({ isDirectory: () => true });

    // Mock rationale: Control 'now' for deterministic age calculation across tests.
    const now = new Date('2023-01-01T12:00:00Z');
    global.Date = jest.fn(() => now);
    global.Date.now = jest.fn(() => now.getTime());
    global.Date.prototype.getTime = jest.fn(() => now.getTime());
  });

  afterEach(() => {
    global.Date = RealDate; // Restore original Date
  });

  test('should find no echoes in an empty directory', () => {
    fs.readdirSync.mockReturnValue([]);
    const echoes = scanDirectoryForEchoes(testDirPath, maxAge);
    expect(echoes).toEqual([]);
  });

  test('should find echoes for files older than maxAge', () => {
    fs.readdirSync.mockReturnValue(['old_file.txt', 'recent_file.log']);
    fs.statSync.mockImplementation((filePath) => {
      if (filePath === path.join(testDirPath, 'old_file.txt')) {
        return { mtime: new Date('2022-10-01T12:00:00Z') }; // ~92 days old
      } else if (filePath === path.join(testDirPath, 'recent_file.log')) {
        return { mtime: new Date('2022-12-20T12:00:00Z') }; // ~12 days old
      }
      return { mtime: new Date() };
    });

    const echoes = scanDirectoryForEchoes(testDirPath, maxAge);
    expect(echoes).toHaveLength(1);
    expect(echoes[0].filePath).toBe(path.join(testDirPath, 'old_file.txt'));
    expect(echoes[0].age).toBe(92);
  });

  test('should not find echoes for files younger than maxAge', () => {
    fs.readdirSync.mockReturnValue(['recent_file.log']);
    fs.statSync.mockImplementation((filePath) => {
      if (filePath === path.join(testDirPath, 'recent_file.log')) {
        return { mtime: new Date('2022-12-20T12:00:00Z') }; // ~12 days old
      }
      return { mtime: new Date() };
    });

    const echoes = scanDirectoryForEchoes(testDirPath, maxAge);
    expect(echoes).toEqual([]);
  });

  test('should handle non-existent directory', () => {
    fs.existsSync.mockReturnValue(false);
    const echoes = scanDirectoryForEchoes('/nonexistent', maxAge);
    expect(echoes).toEqual([]);
    expect(mockConsoleError).toHaveBeenCalledWith(expect.stringContaining('Directory not found'));
  });

  test('should handle path that is not a directory', () => {
    fs.existsSync.mockReturnValue(true);
    fs.lstatSync.mockReturnValue({ isDirectory: () => false });
    const echoes = scanDirectoryForEchoes('/not/a/dir/file.txt', maxAge);
    expect(echoes).toEqual([]);
    expect(mockConsoleError).toHaveBeenCalledWith(expect.stringContaining('is not a directory'));
  });

  test('should handle readdirSync error', () => {
    fs.readdirSync.mockImplementationOnce(() => {
      throw new Error('Permission denied');
    });
    const echoes = scanDirectoryForEchoes(testDirPath, maxAge);
    expect(echoes).toEqual([]);
    expect(mockConsoleError).toHaveBeenCalledWith(expect.stringContaining('Error scanning directory'));
  });
});

describe('reportEchoes', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('should report no echoes when array is empty', () => {
    reportEchoes([]);
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('No significant temporal echoes detected'));
  });

  test('should report echoes when array is not empty', () => {
    const echoes = [
      { filePath: '/path/to/old_file.txt', age: 95 },
      { filePath: '/path/to/older_file.doc', age: 120 }
    ];
    reportEchoes(echoes);
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Detected 2 temporal echoes'));
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('older_file.doc (Age: 120 days)')); // Should be sorted by age desc
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('old_file.txt (Age: 95 days)'));
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Purification Protocol: Dry Run Complete. No files were altered.'));
  });
});

describe('main', () => {
  const originalArgv = process.argv;
  const originalExit = process.exit;

  beforeEach(() => {
    jest.clearAllMocks();
    process.argv = [...originalArgv.slice(0, 2)];
    process.exit = jest.fn(); // Mock process.exit

    // Mock fs functions for main to run without errors
    fs.existsSync.mockReturnValue(true);
    fs.lstatSync.mockReturnValue({ isDirectory: () => true });
    fs.readdirSync.mockReturnValue([]);
    fs.statSync.mockReturnValue({ mtime: new Date() });

    // Mock rationale: Control 'now' for deterministic age calculation across tests.
    const now = new Date('2023-01-01T12:00:00Z');
    global.Date = jest.fn(() => now);
    global.Date.now = jest.fn(() => now.getTime());
    global.Date.prototype.getTime = jest.fn(() => now.getTime());
  });

  afterAll(() => {
    process.argv = originalArgv;
    process.exit = originalExit;
    global.Date = RealDate; // Restore original Date
  });

  test('should exit with error if --path is missing', () => {
    process.argv.push('--age', '30');
    main();
    expect(mockConsoleError).toHaveBeenCalledWith(expect.stringContaining('Usage:'));
    expect(process.exit).toHaveBeenCalledWith(1);
  });

  test('should exit with error if --age is missing or invalid', () => {
    process.argv.push('--path', '/test/dir');
    main();
    expect(mockConsoleError).toHaveBeenCalledWith(expect.stringContaining('Usage:'));
    expect(process.exit).toHaveBeenCalledWith(1);

    jest.clearAllMocks();
    process.argv = [...originalArgv.slice(0, 2), '--path', '/test/dir', '--age', 'not-a-number'];
    main();
    expect(mockConsoleError).toHaveBeenCalledWith(expect.stringContaining('Usage:'));
    expect(process.exit).toHaveBeenCalledWith(1);
  });

  test('should run successfully with valid arguments and report no echoes', () => {
    process.argv.push('--path', '/test/dir', '--age', '30');
    main();
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Scanning \'/test/dir\' for echoes older than 30 days...'));
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('No significant temporal echoes detected'));
    expect(process.exit).not.toHaveBeenCalled();
  });

  test('should run successfully with valid arguments and report echoes', () => {
    process.argv.push('--path', '/test/dir', '--age', '30');
    fs.readdirSync.mockReturnValue(['old_file.txt']);
    fs.statSync.mockReturnValue({ mtime: new Date('2022-10-01T12:00:00Z') }); // ~92 days old

    main();
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Scanning \'/test/dir\' for echoes older than 30 days...'));
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Detected 1 temporal echoes'));
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('old_file.txt (Age: 92 days)'));
    expect(process.exit).not.toHaveBeenCalled();
  });
});
