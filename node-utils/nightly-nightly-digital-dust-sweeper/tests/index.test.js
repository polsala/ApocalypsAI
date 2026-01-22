const fs = require('fs');
const path = require('path');
const { getFilesRecursively, getFileAgeInDays, sweepDigitalDust } = require('../src/index'); // Assuming functions are exported or tested via CLI mock

// Mock rationale: We need to simulate file system operations without actually touching the disk.
// This allows for deterministic and isolated testing of the utility's logic.

// Mock console.log and console.error to prevent output during tests and to spy on messages
const mockLog = jest.spyOn(console, 'log').mockImplementation(() => {});
const mockWarn = jest.spyOn(console, 'warn').mockImplementation(() => {});
const mockError = jest.spyOn(console, 'error').mockImplementation(() => {});

describe('Digital Dust Sweeper', () => {
  let mockFsState;
  let mockReaddirMap;

  beforeEach(() => {
    // Reset mock state for each test
    mockFsState = {
      '/test/dir/old_file.txt': { isDirectory: () => false, mtime: new Date(Date.now() - 60 * 24 * 60 * 60 * 1000) }, // 60 days old
      '/test/dir/recent_file.txt': { isDirectory: () => false, mtime: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000) },  // 5 days old
      '/test/dir/subdir': { isDirectory: () => true, mtime: new Date() },
      '/test/dir/subdir/another_old_file.log': { isDirectory: () => false, mtime: new Date(Date.now() - 90 * 24 * 60 * 60 * 1000) }, // 90 days old
      '/test/dir/subdir/recent_log.log': { isDirectory: () => false, mtime: new Date(Date.now() - 10 * 24 * 60 * 60 * 1000) }, // 10 days old
      '/test/dir/empty_subdir': { isDirectory: () => true, mtime: new Date() },
      '/test/quarantine': { isDirectory: () => true, mtime: new Date() }, // Mock existing quarantine dir
    };

    mockReaddirMap = {
      '/test/dir': ['old_file.txt', 'recent_file.txt', 'subdir', 'empty_subdir'],
      '/test/dir/subdir': ['another_old_file.log', 'recent_log.log'],
      '/test/dir/empty_subdir': [],
      '/test/quarantine': [],
    };

    fs.readdirSync.mockImplementation((p) => {
      if (mockReaddirMap[p]) return mockReaddirMap[p];
      throw new Error(`ENOENT: no such file or directory, scandir '${p}'`);
    });
    fs.statSync.mockImplementation((p) => {
      if (mockFsState[p]) return mockFsState[p];
      throw new Error(`ENOENT: no such file or directory, stat '${p}'`);
    });
    fs.unlinkSync.mockClear().mockImplementation((p) => {
      if (!mockFsState[p]) throw new Error(`ENOENT: no such file or directory, unlink '${p}'`);
      delete mockFsState[p];
    });
    fs.renameSync.mockClear().mockImplementation((oldPath, newPath) => {
      if (!mockFsState[oldPath]) throw new Error(`ENOENT: no such file or directory, rename '${oldPath}'`);
      mockFsState[newPath] = mockFsState[oldPath];
      delete mockFsState[oldPath];
    });
    fs.mkdirSync.mockClear().mockImplementation((p, options) => {
      if (mockFsState[p] && mockFsState[p].isDirectory()) return; // Already exists
      mockFsState[p] = { isDirectory: () => true, mtime: new Date() };
      mockReaddirMap[p] = [];
    });
    fs.existsSync.mockClear().mockImplementation((p) => !!mockFsState[p] || !!mockReaddirMap[p]);

    mockLog.mockClear();
    mockWarn.mockClear();
    mockError.mockClear();

    // Mock path.resolve and path.join to simplify testing absolute paths
    jest.spyOn(path, 'resolve').mockImplementation((...args) => args.join('/'));
    jest.spyOn(path, 'join').mockImplementation((...args) => args.join('/'));
  });

  afterEach(() => {
    jest.restoreAllMocks(); // Restore console and path mocks
  });

  test('getFilesRecursively should return all file paths', () => {
    const files = getFilesRecursively('/test/dir');
    expect(files).toEqual(expect.arrayContaining([
      '/test/dir/old_file.txt',
      '/test/dir/recent_file.txt',
      '/test/dir/subdir/another_old_file.log',
      '/test/dir/subdir/recent_log.log',
    ]));
    expect(files.length).toBe(4);
  });

  test('getFileAgeInDays should calculate correct age', () => {
    const stats = { mtime: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000) }; // 30 days ago
    expect(getFileAgeInDays(stats)).toBe(30);

    const statsRecent = { mtime: new Date(Date.now() - 0.5 * 24 * 60 * 60 * 1000) }; // 0.5 days ago
    expect(getFileAgeInDays(statsRecent)).toBe(1); // Should ceil to 1 day
  });

  test('should report old files in dry run mode without modifying anything', async () => {
    await sweepDigitalDust('/test/dir', 30, true, null, false);

    expect(mockLog).toHaveBeenCalledWith(expect.stringContaining('Found 2 digital dust bunnies'));
    expect(mockLog).toHaveBeenCalledWith(expect.stringContaining('/test/dir/old_file.txt'));
    expect(mockLog).toHaveBeenCalledWith(expect.stringContaining('/test/dir/subdir/another_old_file.log'));
    expect(fs.unlinkSync).not.toHaveBeenCalled();
    expect(fs.renameSync).not.toHaveBeenCalled();
    expect(fs.mkdirSync).not.toHaveBeenCalled();
    expect(mockFsState['/test/dir/old_file.txt']).toBeDefined(); // File should still exist in mock state
  });

  test('should move old files to quarantine directory', async () => {
    await sweepDigitalDust('/test/dir', 30, false, '/test/quarantine', false);

    expect(mockLog).toHaveBeenCalledWith(expect.stringContaining('Quarantine Mode'));
    expect(fs.mkdirSync).not.toHaveBeenCalled(); // Quarantine dir already exists in mock
    expect(fs.renameSync).toHaveBeenCalledTimes(2);
    expect(fs.renameSync).toHaveBeenCalledWith('/test/dir/old_file.txt', '/test/quarantine/old_file.txt');
    expect(fs.renameSync).toHaveBeenCalledWith('/test/dir/subdir/another_old_file.log', '/test/quarantine/another_old_file.log');
    expect(fs.unlinkSync).not.toHaveBeenCalled();
    expect(mockFsState['/test/dir/old_file.txt']).toBeUndefined(); // File should be moved from mock state
    expect(mockFsState['/test/quarantine/old_file.txt']).toBeDefined(); // File should be in quarantine
  });

  test('should create quarantine directory if it does not exist', async () => {
    delete mockFsState['/test/quarantine']; // Simulate non-existent quarantine dir
    fs.existsSync.mockImplementation((p) => p === '/test/dir' || p === '/test/dir/subdir'); // Only target dir exists

    await sweepDigitalDust('/test/dir', 30, false, '/test/new_quarantine', false);

    expect(fs.mkdirSync).toHaveBeenCalledWith('/test/new_quarantine', { recursive: true });
    expect(mockLog).toHaveBeenCalledWith(expect.stringContaining('Created quarantine zone: /test/new_quarantine'));
    expect(fs.renameSync).toHaveBeenCalledTimes(2);
  });

  test('should delete old files directly when --delete is used', async () => {
    await sweepDigitalDust('/test/dir', 30, false, '/test/quarantine', true);

    expect(mockLog).toHaveBeenCalledWith(expect.stringContaining('Deletion Mode'));
    expect(fs.unlinkSync).toHaveBeenCalledTimes(2);
    expect(fs.unlinkSync).toHaveBeenCalledWith('/test/dir/old_file.txt');
    expect(fs.unlinkSync).toHaveBeenCalledWith('/test/dir/subdir/another_old_file.log');
    expect(fs.renameSync).not.toHaveBeenCalled();
    expect(mockFsState['/test/dir/old_file.txt']).toBeUndefined(); // File should be deleted from mock state
  });

  test('should handle no dust bunnies found', async () => {
    await sweepDigitalDust('/test/dir', 100, true, null, false); // Threshold higher than any file age

    expect(mockLog).toHaveBeenCalledWith(expect.stringContaining('No digital dust bunnies found!'));
    expect(fs.unlinkSync).not.toHaveBeenCalled();
    expect(fs.renameSync).not.toHaveBeenCalled();
  });

  test('should log error if target directory does not exist', async () => {
    await sweepDigitalDust('/nonexistent/dir', 30, true, null, false);

    expect(mockError).toHaveBeenCalledWith(expect.stringContaining('Error: Could not read directory /nonexistent/dir'));
    expect(mockLog).not.toHaveBeenCalledWith(expect.stringContaining('Found'));
  });

  test('should warn if a file cannot be statted', async () => {
    fs.statSync.mockImplementation((p) => {
      if (p === '/test/dir/old_file.txt') throw new Error('Permission denied');
      if (mockFsState[p]) return mockFsState[p];
      throw new Error(`ENOENT: no such file or directory, stat '${p}'`);
    });

    await sweepDigitalDust('/test/dir', 30, true, null, false);

    expect(mockWarn).toHaveBeenCalledWith(expect.stringContaining('Warning: Could not get stats for /test/dir/old_file.txt'));
    expect(mockLog).toHaveBeenCalledWith(expect.stringContaining('Found 1 digital dust bunnies')); // Only 'another_old_file.log' should be found
  });
});

// Mock the entire fs module
jest.mock('fs', () => ({
  readdirSync: jest.fn(),
  statSync: jest.fn(),
  unlinkSync: jest.fn(),
  renameSync: jest.fn(),
  mkdirSync: jest.fn(),
  existsSync: jest.fn(),
}));
