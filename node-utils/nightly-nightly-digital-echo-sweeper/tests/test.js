const { getFilesOlderThan, moveFile } = require('../src/index');
const { promises: fs } = require('fs');
const path = require('path');

// Mock rationale: fs/promises functions need to be mocked to prevent actual file system operations
// during tests, ensuring determinism and isolation. This allows simulating different directory
// structures, file ages, and error conditions without touching the real file system.
jest.mock('fs', () => ({
  promises: {
    readdir: jest.fn(),
    stat: jest.fn(),
    mkdir: jest.fn(),
    rename: jest.fn(),
  },
}));

describe('nightly-digital-echo-sweeper', () => {
  // Consistent "now" for tests to ensure age calculations are deterministic.
  const MOCK_NOW = new Date('2024-01-15T12:00:00Z').getTime();

  beforeEach(() => {
    jest.clearAllMocks();
    // Mock rationale: Override Date.now() to return a fixed timestamp, ensuring that file age
    // calculations are consistent across test runs and not dependent on the actual current time.
    jest.spyOn(Date, 'now').mockReturnValue(MOCK_NOW);
  });

  afterAll(() => {
    // Restore the original Date.now() function after all tests are complete.
    jest.restoreAllMocks();
  });

  describe('getFilesOlderThan', () => {
    const sourceDir = '/mock/source';
    const ageDays = 30;
    const thresholdMs = ageDays * 24 * 60 * 60 * 1000;

    it('should return an empty array if no files are found', async () => {
      // Mock rationale: Simulate an empty directory by having readdir return an empty array.
      fs.readdir.mockResolvedValueOnce([]);
      const oldFiles = await getFilesOlderThan(sourceDir, ageDays);
      expect(oldFiles).toEqual([]);
      expect(fs.readdir).toHaveBeenCalledWith(sourceDir, { withFileTypes: true });
    });

    it('should return files older than the specified age, including in subdirectories', async () => {
      const file1Path = path.join(sourceDir, 'old_file.txt');
      const file2Path = path.join(sourceDir, 'recent_file.txt');
      const subdirPath = path.join(sourceDir, 'subdir');
      const file3Path = path.join(subdirPath, 'another_old.log');

      // Mock rationale: Simulate a directory structure with files and a subdirectory.
      fs.readdir.mockResolvedValueOnce([
        { name: 'old_file.txt', isDirectory: () => false, isFile: () => true },
        { name: 'recent_file.txt', isDirectory: () => false, isFile: () => true },
        { name: 'subdir', isDirectory: () => true, isFile: () => false },
      ]);
      // Mock rationale: Simulate the content of the subdirectory.
      fs.readdir.mockResolvedValueOnce([
        { name: 'another_old.log', isDirectory: () => false, isFile: () => true },
      ]);

      // Mock rationale: Provide specific mtimeMs for each file to control their age relative to MOCK_NOW.
      fs.stat
        .mockImplementation((filePath) => {
          if (filePath === file1Path) {
            return Promise.resolve({ mtimeMs: MOCK_NOW - thresholdMs - 1000, isFile: () => true }); // Older
          }
          if (filePath === file2Path) {
            return Promise.resolve({ mtimeMs: MOCK_NOW - thresholdMs + 1000, isFile: () => true }); // Newer
          }
          if (filePath === file3Path) {
            return Promise.resolve({ mtimeMs: MOCK_NOW - thresholdMs - 5000, isFile: () => true }); // Older in subdir
          }
          return Promise.reject(new Error('Mock: File not found'));
        });

      const oldFiles = await getFilesOlderThan(sourceDir, ageDays);
      expect(oldFiles.length).toBe(2);
      expect(oldFiles[0].path).toBe(file1Path);
      expect(oldFiles[1].path).toBe(file3Path);
      expect(fs.stat).toHaveBeenCalledTimes(3); // For old_file.txt, recent_file.txt, another_old.log
    });

    it('should handle directory access errors gracefully', async () => {
      // Mock rationale: Simulate a directory that cannot be read due to permissions or other issues.
      fs.readdir.mockRejectedValueOnce(new Error('Permission denied'));
      // Mock rationale: Suppress console error output during this specific test to avoid polluting test logs.
      const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});

      const oldFiles = await getFilesOlderThan(sourceDir, ageDays);
      expect(oldFiles).toEqual([]);
      expect(consoleErrorSpy).toHaveBeenCalledWith(
        expect.stringContaining('ApocalypsAI: Cannot access directory'),
        'Permission denied'
      );
      consoleErrorSpy.mockRestore();
    });

    it('should handle file stat errors gracefully', async () => {
      const file1Path = path.join(sourceDir, 'file_with_error.txt');
      // Mock rationale: Simulate a directory with one file.
      fs.readdir.mockResolvedValueOnce([
        { name: 'file_with_error.txt', isDirectory: () => false, isFile: () => true },
      ]);
      // Mock rationale: Simulate a file whose stats cannot be retrieved (e.g., corrupted inode).
      fs.stat.mockRejectedValueOnce(new Error('File corrupted'));
      // Mock rationale: Suppress console error output.
      const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});

      const oldFiles = await getFilesOlderThan(sourceDir, ageDays);
      expect(oldFiles).toEqual([]);
      expect(consoleErrorSpy).toHaveBeenCalledWith(
        expect.stringContaining('ApocalypsAI: Cannot stat file'),
        'File corrupted'
      );
      consoleErrorSpy.mockRestore();
    });
  });

  describe('moveFile', () => {
    const sourcePath = '/mock/source/file.txt';
    const targetDir = '/mock/archive';
    const destinationPath = path.join(targetDir, 'file.txt');

    it('should successfully move a file', async () => {
      // Mock rationale: Simulate successful directory creation (if needed) and file renaming.
      fs.mkdir.mockResolvedValueOnce(undefined);
      fs.rename.mockResolvedValueOnce(undefined);

      const result = await moveFile(sourcePath, targetDir);
      expect(fs.mkdir).toHaveBeenCalledWith(targetDir, { recursive: true });
      expect(fs.rename).toHaveBeenCalledWith(sourcePath, destinationPath);
      expect(result).toBe(`Rehomed digital echo: ${sourcePath} -> ${destinationPath}`);
    });

    it('should return an error message if move fails', async () => {
      // Mock rationale: Simulate successful directory creation but a failure during file renaming.
      fs.mkdir.mockResolvedValueOnce(undefined);
      fs.rename.mockRejectedValueOnce(new Error('Disk full'));

      const result = await moveFile(sourcePath, targetDir);
      expect(fs.mkdir).toHaveBeenCalledWith(targetDir, { recursive: true });
      expect(fs.rename).toHaveBeenCalledWith(sourcePath, destinationPath);
      expect(result).toBe(`Failed to rehome digital echo ${sourcePath}: Disk full`);
    });

    it('should return an error message if directory creation fails', async () => {
      // Mock rationale: Simulate a failure during directory creation.
      fs.mkdir.mockRejectedValueOnce(new Error('No space left on device'));
      // Mock rationale: rename should not be called if mkdir fails.
      fs.rename.mockResolvedValueOnce(undefined);

      const result = await moveFile(sourcePath, targetDir);
      expect(fs.mkdir).toHaveBeenCalledWith(targetDir, { recursive: true });
      expect(fs.rename).not.toHaveBeenCalled();
      expect(result).toBe(`Failed to rehome digital echo ${sourcePath}: No space left on device`);
    });
  });
});
