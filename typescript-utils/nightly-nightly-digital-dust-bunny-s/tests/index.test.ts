import * as fs from 'fs';
import * as path from 'path';
import { scanDirectory } from '../src/fileScanner';
import { formatReport } from '../src/reporter';
import { FileInfo, DustBunnyReport } from '../src/types';

// Mock rationale: fs.promises operations are non-deterministic and depend on the actual file system state.
// Mocking them allows for controlled, repeatable tests without creating temporary files or relying on system time.
jest.mock('fs', () => ({
  promises: {
    readdir: jest.fn(),
    stat: jest.fn(),
  },
  Dirent: class {
    name: string;
    isDirectoryFlag: boolean;
    constructor(name: string, isDirectory: boolean) {
      this.name = name;
      this.isDirectoryFlag = isDirectory;
    }
    isDirectory() { return this.isDirectoryFlag; }
  },
}));

const mockReaddir = fs.promises.readdir as jest.Mock;
const mockStat = fs.promises.stat as jest.Mock;

describe('fileScanner', () => {
  const MOCK_ROOT = '/mock/project';
  const NOW = new Date('2023-10-26T12:00:00Z'); // Fixed current time for deterministic age calculation

  beforeEach(() => {
    jest.clearAllMocks();
    jest.spyOn(global, 'Date').mockImplementation(() => NOW); // Mock Date constructor
  });

  afterEach(() => {
    jest.restoreAllMocks(); // Restore Date mock
  });

  it('should find no dust bunnies in an empty directory', async () => {
    mockReaddir.mockResolvedValue([]);
    const files = await scanDirectory(MOCK_ROOT, 90, []);
    expect(files).toEqual([]);
    expect(mockReaddir).toHaveBeenCalledWith(MOCK_ROOT, { withFileTypes: true });
  });

  it('should find a single old file', async () => {
    const oldFileDate = new Date(NOW.getTime() - (100 * 24 * 60 * 60 * 1000)); // 100 days old
    mockReaddir.mockResolvedValue([new fs.Dirent('old_file.txt', false)]);
    mockStat.mockResolvedValue({ mtime: oldFileDate, isDirectory: () => false });

    const files = await scanDirectory(MOCK_ROOT, 90, []);
    expect(files.length).toBe(1);
    expect(files[0].name).toBe('old_file.txt');
    expect(files[0].ageDays).toBeCloseTo(100);
  });

  it('should ignore a new file', async () => {
    const newFileDate = new Date(NOW.getTime() - (50 * 24 * 60 * 60 * 1000)); // 50 days old
    mockReaddir.mockResolvedValue([new fs.Dirent('new_file.txt', false)]);
    mockStat.mockResolvedValue({ mtime: newFileDate, isDirectory: () => false });

    const files = await scanDirectory(MOCK_ROOT, 90, []);
    expect(files).toEqual([]);
  });

  it('should find old files and ignore new ones', async () => {
    const oldFileDate = new Date(NOW.getTime() - (100 * 24 * 60 * 60 * 1000));
    const newFileDate = new Date(NOW.getTime() - (50 * 24 * 60 * 60 * 1000));

    mockReaddir
      .mockResolvedValueOnce([
        new fs.Dirent('old_file.txt', false),
        new fs.Dirent('new_file.txt', false),
      ]);
    mockStat
      .mockResolvedValueOnce({ mtime: oldFileDate, isDirectory: () => false })
      .mockResolvedValueOnce({ mtime: newFileDate, isDirectory: () => false });

    const files = await scanDirectory(MOCK_ROOT, 90, []);
    expect(files.length).toBe(1);
    expect(files[0].name).toBe('old_file.txt');
  });

  it('should handle nested directories and find old items', async () => {
    const oldFileDate = new Date(NOW.getTime() - (100 * 24 * 60 * 60 * 1000));
    const oldDirDate = new Date(NOW.getTime() - (120 * 24 * 60 * 60 * 1000));
    const newFileDate = new Date(NOW.getTime() - (50 * 24 * 60 * 60 * 1000));

    mockReaddir
      .mockResolvedValueOnce([ // MOCK_ROOT
        new fs.Dirent('old_dir', true),
        new fs.Dirent('new_file.txt', false),
      ])
      .mockResolvedValueOnce([ // MOCK_ROOT/old_dir
        new fs.Dirent('nested_old_file.txt', false),
      ]);

    mockStat
      .mockResolvedValueOnce({ mtime: oldDirDate, isDirectory: () => true }) // old_dir
      .mockResolvedValueOnce({ mtime: newFileDate, isDirectory: () => false }) // new_file.txt
      .mockResolvedValueOnce({ mtime: oldFileDate, isDirectory: () => false }); // nested_old_file.txt

    const files = await scanDirectory(MOCK_ROOT, 90, []);
    expect(files.length).toBe(2);
    expect(files.map(f => f.name)).toEqual(expect.arrayContaining(['old_dir', 'nested_old_file.txt']));
    expect(files.find(f => f.name === 'old_dir')?.ageDays).toBeCloseTo(120);
    expect(files.find(f => f.name === 'nested_old_file.txt')?.ageDays).toBeCloseTo(100);
  });

  it('should respect ignore patterns', async () => {
    const oldFileDate = new Date(NOW.getTime() - (100 * 24 * 60 * 60 * 1000));
    const oldIgnoredFileDate = new Date(NOW.getTime() - (150 * 24 * 60 * 60 * 1000));

    mockReaddir.mockResolvedValueOnce([
      new fs.Dirent('old_file.txt', false),
      new fs.Dirent('node_modules', true),
    ]);
    mockReaddir.mockResolvedValueOnce([ // node_modules
      new fs.Dirent('ignored_package.js', false),
    ]);

    mockStat
      .mockResolvedValueOnce({ mtime: oldFileDate, isDirectory: () => false }) // old_file.txt
      .mockResolvedValueOnce({ mtime: oldIgnoredFileDate, isDirectory: () => true }) // node_modules
      .mockResolvedValueOnce({ mtime: oldIgnoredFileDate, isDirectory: () => false }); // ignored_package.js

    const files = await scanDirectory(MOCK_ROOT, 90, ['node_modules']);
    expect(files.length).toBe(1);
    expect(files[0].name).toBe('old_file.txt');
  });

  it('should handle errors during readdir gracefully', async () => {
    mockReaddir.mockRejectedValue(new Error('Permission denied'));
    const files = await scanDirectory(MOCK_ROOT, 90, []);
    expect(files).toEqual([]);
  });

  it('should handle errors during stat gracefully', async () => {
    const oldFileDate = new Date(NOW.getTime() - (100 * 24 * 60 * 60 * 1000));
    mockReaddir.mockResolvedValue([new fs.Dirent('problem_file.txt', false)]);
    mockStat.mockRejectedValue(new Error('File not found'));

    const files = await scanDirectory(MOCK_ROOT, 90, []);
    expect(files).toEqual([]);
  });
});

describe('reporter', () => {
  it('should format a report with no dust bunnies in text format', () => {
    const report: DustBunnyReport = {
      scannedPath: '/test/path',
      thresholdDays: 90,
      ignoredPatterns: [],
      dustBunnyCount: 0,
      dustBunnyFiles: [],
    };
    const output = formatReport(report, 'text');
    expect(output).toContain('No digital dust bunnies found! Your project is sparkling clean.');
    expect(output).toContain('Total Dust Bunnies Found: 0');
  });

  it('should format a report with dust bunnies in text format', () => {
    const now = new Date('2023-10-26T12:00:00Z');
    const oldFileDate = new Date(now.getTime() - (100 * 24 * 60 * 60 * 1000));
    const olderFileDate = new Date(now.getTime() - (150 * 24 * 60 * 60 * 1000));

    const files: FileInfo[] = [
      { path: '/test/path/old_file.txt', name: 'old_file.txt', isDir: false, lastModified: oldFileDate, ageDays: 100 },
      { path: '/test/path/older_dir', name: 'older_dir', isDir: true, lastModified: olderFileDate, ageDays: 150 },
    ];
    const report: DustBunnyReport = {
      scannedPath: '/test/path',
      thresholdDays: 90,
      ignoredPatterns: ['temp'],
      dustBunnyCount: 2,
      dustBunnyFiles: files,
    };
    const output = formatReport(report, 'text');
    expect(output).toContain('Total Dust Bunnies Found: 2');
    expect(output).toContain('[FILE] /test/path/old_file.txt (Last modified:');
    expect(output).toContain('[DIR] /test/path/older_dir (Last modified:');
    expect(output).toContain('150 days old'); // Older file should appear first due to sort
    expect(output).toContain('100 days old');
    expect(output).toContain('Ignored Patterns: temp');
  });

  it('should format a report in JSON format', () => {
    const now = new Date('2023-10-26T12:00:00Z');
    const oldFileDate = new Date(now.getTime() - (100 * 24 * 60 * 60 * 1000));

    const files: FileInfo[] = [
      { path: '/test/path/old_file.txt', name: 'old_file.txt', isDir: false, lastModified: oldFileDate, ageDays: 100 },
    ];
    const report: DustBunnyReport = {
      scannedPath: '/test/path',
      thresholdDays: 90,
      ignoredPatterns: [],
      dustBunnyCount: 1,
      dustBunnyFiles: files,
    };
    const output = formatReport(report, 'json');
    const parsedOutput = JSON.parse(output);
    expect(parsedOutput.scannedPath).toBe('/test/path');
    expect(parsedOutput.dustBunnyCount).toBe(1);
    expect(parsedOutput.dustBunnyFiles[0].name).toBe('old_file.txt');
    expect(parsedOutput.dustBunnyFiles[0].ageDays).toBe(100);
  });
});
