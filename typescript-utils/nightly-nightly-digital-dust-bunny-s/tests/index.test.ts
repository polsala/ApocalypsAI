import { DigitalDustBunnySweeper } from '../src/index';
import { DustBunnyConfig, FileMetadata } from '../src/types';
import * as fs from 'fs';
import * as path from 'path';

// Mock rationale: We need to simulate file system interactions (reading directories, getting file stats)
// without actually creating or modifying files on the disk. This ensures tests are fast, deterministic,
// and don't have side effects on the host system.
jest.mock('fs', () => ({
  promises: {
    readdir: jest.fn(),
    stat: jest.fn(),
  },
}));

const mockReaddir = fs.promises.readdir as jest.Mock;
const mockStat = fs.promises.stat as jest.Mock;

describe('DigitalDustBunnySweeper', () => {
  const baseConfig: DustBunnyConfig = {
    targetDir: '/mock/test/dir',
    ageThresholdDays: 90,
    dustPatterns: ['temp', 'backup'],
    recursive: false,
    outputFormat: 'text',
    minDustScore: 1,
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should find no dust bunnies if directory is empty', async () => {
    mockReaddir.mockResolvedValue([]);
    const sweeper = new DigitalDustBunnySweeper(baseConfig);
    const result = await sweeper.sweep();
    expect(result).toEqual([]);
    expect(mockReaddir).toHaveBeenCalledWith(baseConfig.targetDir, { withFileTypes: true });
  });

  it('should find files older than the age threshold', async () => {
    const now = Date.now();
    const oldFileTime = now - (baseConfig.ageThresholdDays + 1) * 24 * 60 * 60 * 1000; // 91 days ago
    const newFileTime = now - (baseConfig.ageThresholdDays - 1) * 24 * 60 * 60 * 1000; // 89 days ago

    mockReaddir.mockResolvedValue([
      { name: 'old_document.txt', isDirectory: () => false, isFile: () => true },
      { name: 'recent_report.pdf', isDirectory: () => false, isFile: () => true },
    ]);

    mockStat.mockImplementation((filePath: string) => {
      if (filePath.includes('old_document.txt')) {
        return Promise.resolve({ mtimeMs: oldFileTime, isFile: () => true });
      }
      if (filePath.includes('recent_report.pdf')) {
        return Promise.resolve({ mtimeMs: newFileTime, isFile: () => true });
      }
      return Promise.reject(new Error('File not found'));
    });

    const sweeper = new DigitalDustBunnySweeper(baseConfig);
    const result = await sweeper.sweep();

    expect(result).toHaveLength(1);
    expect(result[0].name).toBe('old_document.txt');
    expect(result[0].ageDays).toBeGreaterThanOrEqual(baseConfig.ageThresholdDays);
    expect(result[0].dustScore).toBe(0); // No pattern match
    expect(result[0].suggestion).toContain('age');
  });

  it('should find files matching dust patterns', async () => {
    const now = Date.now();
    const recentTime = now - 10 * 24 * 60 * 60 * 1000; // 10 days ago

    mockReaddir.mockResolvedValue([
      { name: 'project_notes.md', isDirectory: () => false, isFile: () => true },
      { name: 'temp_log.txt', isDirectory: () => false, isFile: () => true },
      { name: 'backup_config.json', isDirectory: () => false, isFile: () => true },
    ]);

    mockStat.mockImplementation((filePath: string) => {
      return Promise.resolve({ mtimeMs: recentTime, isFile: () => true });
    });

    const sweeper = new DigitalDustBunnySweeper(baseConfig);
    const result = await sweeper.sweep();

    expect(result).toHaveLength(2);
    expect(result.map(f => f.name)).toEqual(expect.arrayContaining(['temp_log.txt', 'backup_config.json']));
    expect(result.find(f => f.name === 'temp_log.txt')?.dustScore).toBe(1);
    expect(result.find(f => f.name === 'backup_config.json')?.dustScore).toBe(1);
    expect(result.find(f => f.name === 'temp_log.txt')?.suggestion).toContain('Filename suggests');
  });

  it('should handle recursive scanning', async () => {
    const now = Date.now();
    const oldFileTime = now - (baseConfig.ageThresholdDays + 1) * 24 * 60 * 60 * 1000; // 91 days ago

    mockReaddir.mockImplementation((dirPath: string) => {
      if (dirPath === '/mock/test/dir') {
        return Promise.resolve([
          { name: 'subdir', isDirectory: () => true, isFile: () => false },
          { name: 'root_file.txt', isDirectory: () => false, isFile: () => true },
        ]);
      }
      if (dirPath === '/mock/test/dir/subdir') {
        return Promise.resolve([
          { name: 'temp_nested.log', isDirectory: () => false, isFile: () => true },
          { name: 'another_old_file.doc', isDirectory: () => false, isFile: () => true },
        ]);
      }
      return Promise.resolve([]);
    });

    mockStat.mockImplementation((filePath: string) => {
      if (filePath.includes('root_file.txt')) {
        return Promise.resolve({ mtimeMs: now - 5 * 24 * 60 * 60 * 1000, isFile: () => true }); // Recent, no pattern
      }
      if (filePath.includes('temp_nested.log')) {
        return Promise.resolve({ mtimeMs: now - 10 * 24 * 60 * 60 * 1000, isFile: () => true }); // Recent, pattern
      }
      if (filePath.includes('another_old_file.doc')) {
        return Promise.resolve({ mtimeMs: oldFileTime, isFile: () => true }); // Old, no pattern
      }
      return Promise.reject(new Error('File not found'));
    });

    const recursiveConfig = { ...baseConfig, recursive: true };
    const sweeper = new DigitalDustBunnySweeper(recursiveConfig);
    const result = await sweeper.sweep();

    expect(result).toHaveLength(2);
    expect(result.map(f => path.basename(f.path))).toEqual(expect.arrayContaining(['temp_nested.log', 'another_old_file.doc']));
    expect(mockReaddir).toHaveBeenCalledWith('/mock/test/dir', { withFileTypes: true });
    expect(mockReaddir).toHaveBeenCalledWith('/mock/test/dir/subdir', { withFileTypes: true });
  });

  it('should sort results by dust score then age', async () => {
    const now = Date.now();
    const veryOld = now - 200 * 24 * 60 * 60 * 1000;
    const old = now - 100 * 24 * 60 * 60 * 1000;
    const recent = now - 10 * 24 * 60 * 60 * 1000;

    mockReaddir.mockResolvedValue([
      { name: 'file_a_temp.txt', isDirectory: () => false, isFile: () => true }, // score 1, recent
      { name: 'file_b_backup_temp.txt', isDirectory: () => false, isFile: () => true }, // score 2, old
      { name: 'file_c_old.txt', isDirectory: () => false, isFile: () => true }, // score 0, very old (age only)
      { name: 'file_d_temp.txt', isDirectory: () => false, isFile: () => true }, // score 1, very old
    ]);

    mockStat.mockImplementation((filePath: string) => {
      if (filePath.includes('file_a_temp.txt')) return Promise.resolve({ mtimeMs: recent, isFile: () => true });
      if (filePath.includes('file_b_backup_temp.txt')) return Promise.resolve({ mtimeMs: old, isFile: () => true });
      if (filePath.includes('file_c_old.txt')) return Promise.resolve({ mtimeMs: veryOld, isFile: () => true });
      if (filePath.includes('file_d_temp.txt')) return Promise.resolve({ mtimeMs: veryOld, isFile: () => true });
      return Promise.reject(new Error('File not found'));
    });

    const configWithMorePatterns = { ...baseConfig, dustPatterns: ['temp', 'backup', 'old'], minDustScore: 0 }; // Set minDustScore to 0 to include age-only files
    const sweeper = new DigitalDustBunnySweeper(configWithMorePatterns);
    const result = await sweeper.sweep();

    // Expected order:
    // 1. file_b_backup_temp.txt (score 2, old)
    // 2. file_d_temp.txt (score 1, very old)
    // 3. file_a_temp.txt (score 1, recent)
    // 4. file_c_old.txt (score 0, very old)
    expect(result.map(f => f.name)).toEqual([
      'file_b_backup_temp.txt',
      'file_d_temp.txt',
      'file_a_temp.txt',
      'file_c_old.txt',
    ]);
    expect(result[0].dustScore).toBe(2);
    expect(result[1].dustScore).toBe(1);
    expect(result[2].dustScore).toBe(1);
    expect(result[3].dustScore).toBe(0); // This file is included because minDustScore is 0 and it's old enough
  });

  it('should ignore files that cannot be stat-ed', async () => {
    const now = Date.now();
    const oldFileTime = now - (baseConfig.ageThresholdDays + 1) * 24 * 60 * 60 * 1000;

    mockReaddir.mockResolvedValue([
      { name: 'valid_old_file.txt', isDirectory: () => false, isFile: () => true },
      { name: 'unreadable_file.txt', isDirectory: () => false, isFile: () => true },
    ]);

    mockStat.mockImplementation((filePath: string) => {
      if (filePath.includes('valid_old_file.txt')) {
        return Promise.resolve({ mtimeMs: oldFileTime, isFile: () => true });
      }
      if (filePath.includes('unreadable_file.txt')) {
        return Promise.reject(new Error('Permission denied'));
      }
      return Promise.reject(new Error('File not found'));
    });

    const sweeper = new DigitalDustBunnySweeper(baseConfig);
    const result = await sweeper.sweep();

    expect(result).toHaveLength(1);
    expect(result[0].name).toBe('valid_old_file.txt');
  });
});
