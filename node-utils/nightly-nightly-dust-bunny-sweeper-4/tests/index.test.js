const assert = require('assert');
const { getDustBunnies, formatBytes, main, _rl } = require('../src/index');
const { readdir, stat, unlink, mkdir, rename } = require('fs/promises');
const path = require('path');

// # Mock rationale: Mocking fs/promises to prevent actual file system operations during tests.
// This ensures tests are deterministic, fast, and don't leave side effects.
jest.mock('fs/promises', () => ({
  readdir: jest.fn(),
  stat: jest.fn(),
  unlink: jest.fn(),
  mkdir: jest.fn(),
  rename: jest.fn()
}));

// # Mock rationale: Mocking readline interface to control user input for interactive prompts.
// This allows testing different user responses (e.g., 'yes' or 'no') deterministically.
const mockQuestion = jest.fn();
_rl.question = mockQuestion;
_rl.close = jest.fn();

describe('Nightly Dust Bunny Sweeper', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    // Reset process.argv for each test to ensure clean CLI parsing
    process.argv = ['node', 'src/index.js'];
  });

  describe('formatBytes', () => {
    test('should format bytes correctly', () => {
      assert.strictEqual(formatBytes(0), '0 Bytes');
      assert.strictEqual(formatBytes(1023), '1023 Bytes');
      assert.strictEqual(formatBytes(1024), '1.00 KB');
      assert.strictEqual(formatBytes(1536), '1.50 KB');
      assert.strictEqual(formatBytes(1024 * 1024), '1.00 MB');
      assert.strictEqual(formatBytes(1024 * 1024 * 1024), '1.00 GB');
      assert.strictEqual(formatBytes(1024 * 1024 * 1024 * 1024), '1.00 TB');
    });
  });

  describe('getDustBunnies', () => {
    test('should return files older than the age threshold', async () => {
      const now = Date.now();
      const directory = '/test/dir';
      const ageThresholdDays = 30;

      readdir.mockResolvedValueOnce([
        { name: 'old_file.txt', isFile: () => true },
        { name: 'recent_file.log', isFile: () => true },
        { name: 'folder', isFile: () => false, isDirectory: () => true }
      ]);

      stat.mockImplementation(async (filePath) => {
        if (filePath.includes('old_file.txt')) {
          return { mtimeMs: now - (ageThresholdDays + 10) * 24 * 60 * 60 * 1000, size: 1000 };
        } else if (filePath.includes('recent_file.log')) {
          return { mtimeMs: now - (ageThresholdDays - 10) * 24 * 60 * 60 * 1000, size: 500 };
        }
        throw new Error('File not found');
      });

      const bunnies = await getDustBunnies(directory, ageThresholdDays);

      assert.strictEqual(bunnies.length, 1);
      assert.strictEqual(bunnies[0].name, 'old_file.txt');
      assert(bunnies[0].ageDays > ageThresholdDays);
      assert.strictEqual(bunnies[0].size, 1000);
    });

    test('should handle errors when stat fails for a file', async () => {
      const now = Date.now();
      const directory = '/test/dir';
      const ageThresholdDays = 30;

      readdir.mockResolvedValueOnce([
        { name: 'valid_file.txt', isFile: () => true },
        { name: 'error_file.txt', isFile: () => true }
      ]);

      stat.mockImplementation(async (filePath) => {
        if (filePath.includes('valid_file.txt')) {
          return { mtimeMs: now - (ageThresholdDays + 10) * 24 * 60 * 60 * 1000, size: 1000 };
        } else if (filePath.includes('error_file.txt')) {
          throw new Error('Permission denied');
        }
      });

      const consoleWarnSpy = jest.spyOn(console, 'warn').mockImplementation(() => {});

      const bunnies = await getDustBunnies(directory, ageThresholdDays);

      assert.strictEqual(bunnies.length, 1);
      assert.strictEqual(bunnies[0].name, 'valid_file.txt');
      expect(consoleWarnSpy).toHaveBeenCalledWith(expect.stringContaining('Could not stat file'));
      consoleWarnSpy.mockRestore();
    });

    test('should return empty array if no dust bunnies found', async () => {
      const now = Date.now();
      const directory = '/test/dir';
      const ageThresholdDays = 30;

      readdir.mockResolvedValueOnce([
        { name: 'recent_file.log', isFile: () => true }
      ]);

      stat.mockResolvedValueOnce({
        mtimeMs: now - (ageThresholdDays - 10) * 24 * 60 * 60 * 1000, size: 500
      });

      const bunnies = await getDustBunnies(directory, ageThresholdDays);
      assert.strictEqual(bunnies.length, 0);
    });

    test('should handle readdir errors', async () => {
      const directory = '/nonexistent/dir';
      const ageThresholdDays = 30;

      readdir.mockRejectedValueOnce(new Error('No such directory'));

      const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
      const processExitSpy = jest.spyOn(process, 'exit').mockImplementation(() => {});

      await getDustBunnies(directory, ageThresholdDays);

      expect(consoleErrorSpy).toHaveBeenCalledWith(expect.stringContaining('Error reading directory'));
      expect(processExitSpy).toHaveBeenCalledWith(1);

      consoleErrorSpy.mockRestore();
      processExitSpy.mockRestore();
    });
  });

  describe('main CLI execution', () => {
    const mockConsoleLog = jest.spyOn(console, 'log').mockImplementation(() => {});
    const mockConsoleError = jest.spyOn(console, 'error').mockImplementation(() => {});
    const mockProcessExit = jest.spyOn(process, 'exit').mockImplementation(() => {});

    beforeEach(() => {
      mockConsoleLog.mockClear();
      mockConsoleError.mockClear();
      mockProcessExit.mockClear();
      mockQuestion.mockClear();
      _rl.close.mockClear();
    });

    afterAll(() => {
      mockConsoleLog.mockRestore();
      mockConsoleError.mockRestore();
      mockProcessExit.mockRestore();
    });

    test('should report dust bunnies in default mode', async () => {
      const now = Date.now();
      const directory = '/test/dir';
      process.argv.push(directory);

      readdir.mockResolvedValueOnce([
        { name: 'old_file.txt', isFile: () => true }
      ]);
      stat.mockResolvedValueOnce({
        mtimeMs: now - (30 + 10) * 24 * 60 * 60 * 1000, size: 1000
      });

      await main();

      expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Found 1 digital dust bunnies'));
      expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Mode is \"report\". No actions taken.'));
      expect(_rl.close).toHaveBeenCalled();
    });

    test('should delete dust bunnies when mode is delete and confirmed', async () => {
      const now = Date.now();
      const directory = '/test/dir';
      process.argv.push(directory, '--mode', 'delete');

      readdir.mockResolvedValueOnce([
        { name: 'old_file.txt', isFile: () => true }
      ]);
      stat.mockResolvedValueOnce({
        mtimeMs: now - (30 + 10) * 24 * 60 * 60 * 1000, size: 1000
      });
      mockQuestion.mockResolvedValueOnce('yes'); // User confirms

      await main();

      expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Swept away: old_file.txt'));
      expect(unlink).toHaveBeenCalledWith(path.join(directory, 'old_file.txt'));
      expect(_rl.close).toHaveBeenCalledTimes(2); // One for prompt, one for end
    });

    test('should archive dust bunnies when mode is archive and confirmed', async () => {
      const now = Date.now();
      const directory = '/test/dir';
      const archiveDir = path.join(directory, 'archive_dust_bunnies');
      process.argv.push(directory, '--mode', 'archive');

      readdir.mockResolvedValueOnce([
        { name: 'old_file.txt', isFile: () => true }
      ]);
      stat.mockResolvedValueOnce({
        mtimeMs: now - (30 + 10) * 24 * 60 * 60 * 1000, size: 1000
      });
      mockQuestion.mockResolvedValueOnce('yes'); // User confirms

      await main();

      expect(mkdir).toHaveBeenCalledWith(archiveDir, { recursive: true });
      expect(rename).toHaveBeenCalledWith(path.join(directory, 'old_file.txt'), path.join(archiveDir, 'old_file.txt'));
      expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining(`Archived: old_file.txt to ${archiveDir}`));
      expect(_rl.close).toHaveBeenCalledTimes(2);
    });

    test('should skip confirmation with --yes flag for delete mode', async () => {
      const now = Date.now();
      const directory = '/test/dir';
      process.argv.push(directory, '--mode', 'delete', '--yes');

      readdir.mockResolvedValueOnce([
        { name: 'old_file.txt', isFile: () => true }
      ]);
      stat.mockResolvedValueOnce({
        mtimeMs: now - (30 + 10) * 24 * 60 * 60 * 1000, size: 1000
      });

      await main();

      expect(mockQuestion).not.toHaveBeenCalled(); // No prompt
      expect(unlink).toHaveBeenCalledWith(path.join(directory, 'old_file.txt'));
      expect(_rl.close).toHaveBeenCalledTimes(1); // Only at the end
    });

    test('should exit if invalid age is provided', async () => {
      process.argv.push('/test/dir', '--age', '-5');
      await main();
      expect(mockConsoleError).toHaveBeenCalledWith('Error: Age must be a non-negative number of days.');
      expect(mockProcessExit).toHaveBeenCalledWith(1);
      expect(_rl.close).not.toHaveBeenCalled(); // Should exit before closing readline
    });

    test('should exit if invalid mode is provided', async () => {
      process.argv.push('/test/dir', '--mode', 'invalid');
      await main();
      expect(mockConsoleError).toHaveBeenCalledWith('Error: Invalid mode. Choose from \"report\", \"delete\", or \"archive\".');
      expect(mockProcessExit).toHaveBeenCalledWith(1);
      expect(_rl.close).not.toHaveBeenCalled();
    });

    test('should handle no dust bunnies found gracefully', async () => {
      const now = Date.now();
      const directory = '/test/dir';
      process.argv.push(directory);

      readdir.mockResolvedValueOnce([
        { name: 'recent_file.txt', isFile: () => true }
      ]);
      stat.mockResolvedValueOnce({
        mtimeMs: now - (30 - 10) * 24 * 60 * 60 * 1000, size: 1000
      });

      await main();

      expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('No digital dust bunnies found!'));
      expect(_rl.close).toHaveBeenCalled();
    });

    test('should cancel operation if user declines', async () => {
      const now = Date.now();
      const directory = '/test/dir';
      process.argv.push(directory, '--mode', 'delete');

      readdir.mockResolvedValueOnce([
        { name: 'old_file.txt', isFile: () => true }
      ]);
      stat.mockResolvedValueOnce({
        mtimeMs: now - (30 + 10) * 24 * 60 * 60 * 1000, size: 1000
      });
      mockQuestion.mockResolvedValueOnce('no'); // User declines

      await main();

      expect(mockConsoleLog).toHaveBeenCalledWith('Operation cancelled.');
      expect(unlink).not.toHaveBeenCalled();
      expect(_rl.close).toHaveBeenCalledTimes(2);
    });
  });
});
