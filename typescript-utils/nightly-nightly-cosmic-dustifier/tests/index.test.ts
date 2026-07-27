import { scanAndIdentifyDust, performDustification } from '../src/fileScanner';
import { DustificationOptions, FileInfo } from '../src/types';
import * as fs from 'fs/promises';
import * as path from 'path';

// Mock fs/promises and path modules
jest.mock('fs/promises');
jest.mock('path', () => ({
  ...jest.requireActual('path'), // Import and retain default behavior
  resolve: jest.fn((p) => p), // Mock resolve to return path as is for testing
  join: jest.fn((...args) => args.join('/')), // Mock join for consistent paths
  basename: jest.fn((p) => p.split('/').pop()), // Mock basename
}));

// Mock rationale: We need to control file system interactions (reading directories, getting file stats, moving/deleting files)
// to ensure tests are deterministic and don't affect the actual file system.
// fs.readdir, fs.stat, fs.unlink, fs.rename, fs.mkdir are all mocked.
// path.resolve, path.join, path.basename are mocked to simplify path handling in tests.

describe('Cosmic Dustifier Core Logic', () => {
  const MOCK_CURRENT_TIME = new Date('2023-10-26T12:00:00Z').getTime(); // Fixed current time for deterministic tests

  beforeAll(() => {
    jest.spyOn(Date, 'now').mockReturnValue(MOCK_CURRENT_TIME);
  });

  afterAll(() => {
    jest.restoreAllMocks();
  });

  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('scanAndIdentifyDust', () => {
    it('should identify files older than the threshold', async () => {
      // Mock rationale: Simulate a directory with files of different modification times.
      (fs.readdir as jest.Mock).mockResolvedValueOnce([
        { name: 'old_file.txt', isFile: () => true, isDirectory: () => false },
        { name: 'recent_file.txt', isFile: () => true, isDirectory: () => false },
        { name: 'another_old.log', isFile: () => true, isDirectory: () => false },
        { name: 'subdir', isFile: () => false, isDirectory: () => true }, // Should be ignored by default
      ]);

      // Mock rationale: Provide specific stat data for each mocked file.
      (fs.stat as jest.Mock)
        .mockImplementation((filePath) => {
          if (filePath === 'test_dir/old_file.txt') {
            // 60 days old
            return Promise.resolve({ mtimeMs: MOCK_CURRENT_TIME - (60 * 24 * 60 * 60 * 1000), birthtimeMs: 0 });
          }
          if (filePath === 'test_dir/recent_file.txt') {
            // 10 days old
            return Promise.resolve({ mtimeMs: MOCK_CURRENT_TIME - (10 * 24 * 60 * 60 * 1000), birthtimeMs: 0 });
          }
          if (filePath === 'test_dir/another_old.log') {
            // 40 days old
            return Promise.resolve({ mtimeMs: MOCK_CURRENT_TIME - (40 * 24 * 60 * 60 * 1000), birthtimeMs: 0 });
          }
          return Promise.reject(new Error('File not found in mock'));
        });

      const options: DustificationOptions = {
        path: 'test_dir',
        thresholdDays: 30,
        action: 'list',
        dryRun: true,
      };

      const result = await scanAndIdentifyDust(options);

      expect(result).toHaveLength(2);
      expect(result[0].name).toBe('old_file.txt');
      expect(result[0].ageDays).toBe(60);
      expect(result[1].name).toBe('another_old.log');
      expect(result[1].ageDays).toBe(40);
      expect(fs.readdir).toHaveBeenCalledWith('test_dir', { withFileTypes: true });
      expect(fs.stat).toHaveBeenCalledTimes(3); // For the three files
    });

    it('should return an empty array if no files are older than the threshold', async () => {
      // Mock rationale: Simulate a directory where all files are newer than the threshold.
      (fs.readdir as jest.Mock).mockResolvedValueOnce([
        { name: 'recent_file_1.txt', isFile: () => true, isDirectory: () => false },
        { name: 'recent_file_2.txt', isFile: () => true, isDirectory: () => false },
      ]);

      (fs.stat as jest.Mock)
        .mockImplementation((filePath) => {
          if (filePath === 'test_dir/recent_file_1.txt') {
            return Promise.resolve({ mtimeMs: MOCK_CURRENT_TIME - (5 * 24 * 60 * 60 * 1000), birthtimeMs: 0 });
          }
          if (filePath === 'test_dir/recent_file_2.txt') {
            return Promise.resolve({ mtimeMs: MOCK_CURRENT_TIME - (15 * 24 * 60 * 60 * 1000), birthtimeMs: 0 });
          }
          return Promise.reject(new Error('File not found in mock'));
        });

      const options: DustificationOptions = {
        path: 'test_dir',
        thresholdDays: 20,
        action: 'list',
        dryRun: true,
      };

      const result = await scanAndIdentifyDust(options);
      expect(result).toHaveLength(0);
    });

    it('should handle errors when reading directory', async () => {
      // Mock rationale: Simulate a file system error when trying to read a directory.
      (fs.readdir as jest.Mock).mockRejectedValueOnce(new Error('Permission denied'));
      const options: DustificationOptions = {
        path: 'non_existent_dir',
        thresholdDays: 30,
        action: 'list',
        dryRun: true,
      };
      await expect(scanAndIdentifyDust(options)).rejects.toThrow('Permission denied');
    });
  });

  describe('performDustification', () => {
    const mockFileInfo: FileInfo = {
      path: 'test_dir/dusty_file.txt',
      name: 'dusty_file.txt',
      birthtimeMs: 0,
      mtimeMs: MOCK_CURRENT_TIME - (50 * 24 * 60 * 60 * 1000),
      ageDays: 50,
    };

    it('should return list message for "list" action', async () => {
      const options: DustificationOptions = {
        path: 'test_dir',
        thresholdDays: 30,
        action: 'list',
        dryRun: false,
      };
      const result = await performDustification(mockFileInfo, options);
      expect(result).toContain("Identified 'test_dir/dusty_file.txt' (modified 50 days ago)");
      expect(fs.unlink).not.toHaveBeenCalled();
      expect(fs.rename).not.toHaveBeenCalled();
    });

    it('should simulate archive for "archive" action in dry run', async () => {
      const options: DustificationOptions = {
        path: 'test_dir',
        thresholdDays: 30,
        action: 'archive',
        archiveDir: 'archive_vault',
        dryRun: true,
      };
      const result = await performDustification(mockFileInfo, options);
      expect(result).toContain("[DRY RUN] Would archive test_dir/dusty_file.txt");
      expect(fs.mkdir).not.toHaveBeenCalled();
      expect(fs.rename).not.toHaveBeenCalled();
    });

    it('should archive file for "archive" action', async () => {
      // Mock rationale: Ensure that the archive directory is created and the file is moved.
      (fs.mkdir as jest.Mock).mockResolvedValueOnce(undefined);
      (fs.rename as jest.Mock).mockResolvedValueOnce(undefined);

      const options: DustificationOptions = {
        path: 'test_dir',
        thresholdDays: 30,
        action: 'archive',
        archiveDir: 'archive_vault',
        dryRun: false,
      };
      const result = await performDustification(mockFileInfo, options);
      expect(result).toContain("Archived 'test_dir/dusty_file.txt' to 'archive_vault/dusty_file.txt'");
      expect(fs.mkdir).toHaveBeenCalledWith('archive_vault', { recursive: true });
      expect(fs.rename).toHaveBeenCalledWith('test_dir/dusty_file.txt', 'archive_vault/dusty_file.txt');
    });

    it('should simulate delete for "delete" action in dry run', async () => {
      const options: DustificationOptions = {
        path: 'test_dir',
        thresholdDays: 30,
        action: 'delete',
        dryRun: true,
      };
      const result = await performDustification(mockFileInfo, options);
      expect(result).toContain("[DRY RUN] Would delete test_dir/dusty_file.txt");
      expect(fs.unlink).not.toHaveBeenCalled();
    });

    it('should delete file for "delete" action', async () => {
      // Mock rationale: Ensure that fs.unlink is called.
      (fs.unlink as jest.Mock).mockResolvedValueOnce(undefined);

      const options: DustificationOptions = {
        path: 'test_dir',
        thresholdDays: 30,
        action: 'delete',
        dryRun: false,
      };
      const result = await performDustification(mockFileInfo, options);
      expect(result).toContain("Deleted 'test_dir/dusty_file.txt'");
      expect(fs.unlink).toHaveBeenCalledWith('test_dir/dusty_file.txt');
    });

    it('should handle errors during archive action', async () => {
      // Mock rationale: Simulate a file system error during the rename operation.
      (fs.mkdir as jest.Mock).mockResolvedValueOnce(undefined);
      (fs.rename as jest.Mock).mockRejectedValueOnce(new Error('Archive failed'));

      const options: DustificationOptions = {
        path: 'test_dir',
        thresholdDays: 30,
        action: 'archive',
        archiveDir: 'archive_vault',
        dryRun: false,
      };
      const result = await performDustification(mockFileInfo, options);
      expect(result).toContain("Failed to archive 'test_dir/dusty_file.txt': Archive failed");
    });

    it('should handle errors during delete action', async () => {
      // Mock rationale: Simulate a file system error during the unlink operation.
      (fs.unlink as jest.Mock).mockRejectedValueOnce(new Error('Delete failed'));

      const options: DustificationOptions = {
        path: 'test_dir',
        thresholdDays: 30,
        action: 'delete',
        dryRun: false,
      };
      const result = await performDustification(mockFileInfo, options);
      expect(result).toContain("Failed to delete 'test_dir/dusty_file.txt': Delete failed");
    });
  });
});
