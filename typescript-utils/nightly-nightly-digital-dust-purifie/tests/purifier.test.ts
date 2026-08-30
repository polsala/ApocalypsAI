import { scanDirectory, performActions } from '../src/purifier';
import { PurifierConfig, DustBunnyReportItem } from '../src/types';
import * as fs from 'fs/promises';
import * as path from 'path';

// Mock rationale: We need to control the file system state for deterministic tests.
// Mocking fs.promises allows us to simulate directories and files without
// actually touching the disk, ensuring tests are fast, isolated, and reliable.
jest.mock('fs/promises', () => ({
  readdir: jest.fn(),
  stat: jest.fn(),
  mkdir: jest.fn(),
  rename: jest.fn(),
}));

const mockReaddir = fs.readdir as jest.MockedFunction<typeof fs.readdir>;
const mockStat = fs.stat as jest.MockedFunction<typeof fs.stat>;
const mockMkdir = fs.mkdir as jest.MockedFunction<typeof fs.mkdir>;
const mockRename = fs.rename as jest.MockedFunction<typeof fs.rename>;

describe('Nightly Digital Dust Purifier', () => {
  const baseConfig: PurifierConfig = {
    targetPath: '/mock/project',
    minAgeDays: 30,
    minSizeBytes: 0,
    excludePatterns: ['node_modules', '.git', '*.log'],
    dryRun: true,
    archiveDir: '/mock/archive',
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should identify files older than minAgeDays', async () => {
    const now = new Date();
    const oldDate = new Date(now.getTime() - (40 * 24 * 60 * 60 * 1000)); // 40 days ago
    const newDate = new Date(now.getTime() - (10 * 24 * 60 * 60 * 1000)); // 10 days ago

    mockReaddir.mockResolvedValueOnce([
      { name: 'old_file.txt', isDirectory: () => false, isFile: () => true, isBlockDevice: () => false, isCharacterDevice: () => false, isFIFO: () => false, isSocket: () => false, isSymbolicLink: () => false },
      { name: 'new_file.txt', isDirectory: () => false, isFile: () => true, isBlockDevice: () => false, isCharacterDevice: () => false, isFIFO: () => false, isSocket: () => false, isSymbolicLink: () => false },
    ] as any);

    mockStat
      .mockResolvedValueOnce({ mtime: oldDate, size: 100 } as any)
      .mockResolvedValueOnce({ mtime: newDate, size: 50 } as any);

    const config = { ...baseConfig, minAgeDays: 30, minSizeBytes: 0 };
    const dustBunnies = await scanDirectory(config.targetPath, config);

    expect(dustBunnies).toHaveLength(1);
    expect(dustBunnies[0].filePath).toBe(path.join(config.targetPath, 'old_file.txt'));
    expect(dustBunnies[0].reason).toContain('Older than 30 days');
  });

  it('should identify files larger than minSizeBytes', async () => {
    const now = new Date();
    const recentDate = new Date(now.getTime() - (5 * 24 * 60 * 60 * 1000)); // 5 days ago

    mockReaddir.mockResolvedValueOnce([
      { name: 'large_file.bin', isDirectory: () => false, isFile: () => true, isBlockDevice: () => false, isCharacterDevice: () => false, isFIFO: () => false, isSocket: () => false, isSymbolicLink: () => false },
      { name: 'small_file.txt', isDirectory: () => false, isFile: () => true, isBlockDevice: () => false, isCharacterDevice: () => false, isFIFO: () => false, isSocket: () => false, isSymbolicLink: () => false },
    ] as any);

    mockStat
      .mockResolvedValueOnce({ mtime: recentDate, size: 1024 * 1024 * 2 } as any) // 2MB
      .mockResolvedValueOnce({ mtime: recentDate, size: 100 } as any); // 100 bytes

    const config = { ...baseConfig, minAgeDays: 0, minSizeBytes: 1024 * 1024 }; // 1MB
    const dustBunnies = await scanDirectory(config.targetPath, config);

    expect(dustBunnies).toHaveLength(1);
    expect(dustBunnies[0].filePath).toBe(path.join(config.targetPath, 'large_file.bin'));
    expect(dustBunnies[0].reason).toContain('Larger than 1048576 bytes');
  });

  it('should exclude files/directories matching patterns', async () => {
    const now = new Date();
    const oldDate = new Date(now.getTime() - (40 * 24 * 60 * 60 * 1000));

    mockReaddir.mockResolvedValueOnce([
      { name: 'file.txt', isDirectory: () => false, isFile: () => true, isBlockDevice: () => false, isCharacterDevice: () => false, isFIFO: () => false, isSocket: () => false, isSymbolicLink: () => false },
      { name: 'node_modules', isDirectory: () => true, isFile: () => false, isBlockDevice: () => false, isCharacterDevice: () => false, isFIFO: () => false, isSocket: () => false, isSymbolicLink: () => false },
      { name: '.git', isDirectory: () => true, isFile: () => false, isBlockDevice: () => false, isCharacterDevice: () => false, isFIFO: () => false, isSocket: () => false, isSymbolicLink: () => false },
      { name: 'app.log', isDirectory: () => false, isFile: () => true, isBlockDevice: () => false, isCharacterDevice: () => false, isFIFO: () => false, isSocket: () => false, isSymbolicLink: () => false },
    ] as any);
    // Mock readdir for subdirectories if they were to be traversed (but they are excluded)
    mockReaddir.mockResolvedValue([]); 

    mockStat
      .mockResolvedValueOnce({ mtime: oldDate, size: 100 } as any) // for file.txt
      .mockResolvedValueOnce({ mtime: oldDate, size: 200 } as any); // for app.log (but it's excluded)

    const config = { ...baseConfig, minAgeDays: 30, excludePatterns: ['node_modules', '.git', '*.log'] };
    const dustBunnies = await scanDirectory(config.targetPath, config);

    expect(dustBunnies).toHaveLength(1); // Only 'file.txt' should be found
    expect(dustBunnies[0].filePath).toBe(path.join(config.targetPath, 'file.txt'));
  });

  it('should perform no actions in dry-run mode', async () => {
    const dustBunnies: DustBunnyReportItem[] = [
      { filePath: '/mock/project/old_file.txt', reason: 'Old', size: 100, lastModified: new Date() },
    ];
    const config = { ...baseConfig, dryRun: true };

    await performActions(dustBunnies, config);

    expect(mockMkdir).not.toHaveBeenCalled();
    expect(mockRename).not.toHaveBeenCalled();
  });

  it('should move files to archive directory in non-dry-run mode', async () => {
    const dustBunnies: DustBunnyReportItem[] = [
      { filePath: '/mock/project/old_file.txt', reason: 'Old', size: 100, lastModified: new Date() },
      { filePath: '/mock/project/another_old.log', reason: 'Old', size: 200, lastModified: new Date() },
    ];
    const config = { ...baseConfig, dryRun: false, archiveDir: '/mock/archive' };

    await performActions(dustBunnies, config);

    expect(mockMkdir).toHaveBeenCalledWith('/mock/archive', { recursive: true });
    expect(mockRename).toHaveBeenCalledTimes(2);
    expect(mockRename).toHaveBeenCalledWith('/mock/project/old_file.txt', '/mock/archive/old_file.txt');
    expect(mockRename).toHaveBeenCalledWith('/mock/project/another_old.log', '/mock/archive/another_old.log');
  });

  it('should handle errors during file operations gracefully', async () => {
    const dustBunnies: DustBunnyReportItem[] = [
      { filePath: '/mock/project/bad_file.txt', reason: 'Old', size: 100, lastModified: new Date() },
    ];
    const config = { ...baseConfig, dryRun: false, archiveDir: '/mock/archive' };

    mockMkdir.mockResolvedValueOnce(undefined);
    mockRename.mockRejectedValueOnce(new Error('Permission denied')); // Simulate error

    const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});

    await performActions(dustBunnies, config);

    expect(mockRename).toHaveBeenCalledWith('/mock/project/bad_file.txt', '/mock/archive/bad_file.txt');
    expect(consoleErrorSpy).toHaveBeenCalledWith(expect.stringContaining('Error moving /mock/project/bad_file.txt: Permission denied'));

    consoleErrorSpy.mockRestore();
  });

  it('should not perform actions if archiveDir is not specified in non-dry-run mode', async () => {
    const dustBunnies: DustBunnyReportItem[] = [
      { filePath: '/mock/project/old_file.txt', reason: 'Old', size: 100, lastModified: new Date() },
    ];
    const config = { ...baseConfig, dryRun: false, archiveDir: undefined }; // No archiveDir

    const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});

    await performActions(dustBunnies, config);

    expect(mockMkdir).not.toHaveBeenCalled();
    expect(mockRename).not.toHaveBeenCalled();
    expect(consoleErrorSpy).toHaveBeenCalledWith('Error: Archive directory not specified for non-dry-run mode. No actions performed.');

    consoleErrorSpy.mockRestore();
  });
});
