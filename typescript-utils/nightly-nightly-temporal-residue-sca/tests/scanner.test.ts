import { TemporalResidueScanner } from '../src/scanner';
import { ScanOptions, ResidueItem } from '../src/types';
import * as fs from 'fs';
import * as path from 'path';

// Mock rationale: We need to control the filesystem state and file modification times
// to ensure deterministic tests without actually creating/deleting files on disk.
// This allows us to test the scanning logic in isolation and avoid side effects.
jest.mock('fs', () => ({
  promises: {
    readdir: jest.fn(),
    stat: jest.fn(),
  },
}));

const mockFsPromises = fs.promises as jest.Mocked<typeof fs.promises>;

describe('TemporalResidueScanner', () => {
  const baseScanOptions: ScanOptions = {
    path: '/mock/project',
    minAgeDays: 30,
    ignorePatterns: ['node_modules', '.git'],
    includePatterns: [],
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should identify old files and directories as residue', async () => {
    const now = new Date('2023-10-26T12:00:00Z');
    const oldDate = new Date('2023-09-01T12:00:00Z'); // Older than 30 days
    const recentDate = new Date('2023-10-15T12:00:00Z'); // Newer than 30 days

    // Mock filesystem structure
    mockFsPromises.readdir.mockImplementation(async (dirPath: fs.PathLike, options: any) => {
      if (dirPath === '/mock/project') {
        return [
          { name: 'old-file.txt', isFile: () => true, isDirectory: () => false },
          { name: 'recent-file.txt', isFile: () => true, isDirectory: () => false },
          { name: 'old-dir', isFile: () => false, isDirectory: () => true },
          { name: 'recent-dir', isFile: () => false, isDirectory: () => true },
          { name: 'node_modules', isFile: () => false, isDirectory: () => true }, // Ignored by default
        ];
      }
      if (dirPath === '/mock/project/old-dir') {
        return [
          { name: 'nested-old-file.log', isFile: () => true, isDirectory: () => false },
        ];
      }
      if (dirPath === '/mock/project/recent-dir') {
        return []; // Empty recent directory
      }
      return [];
    });

    // Mock file stats
    mockFsPromises.stat.mockImplementation(async (filePath: fs.PathLike) => {
      const fileName = path.basename(filePath.toString());
      switch (fileName) {
        case 'old-file.txt':
          return { mtime: oldDate, isFile: () => true, isDirectory: () => false } as fs.Stats;
        case 'recent-file.txt':
          return { mtime: recentDate, isFile: () => true, isDirectory: () => false } as fs.Stats;
        case 'old-dir':
          return { mtime: oldDate, isFile: () => false, isDirectory: () => true } as fs.Stats;
        case 'recent-dir':
          return { mtime: recentDate, isFile: () => false, isDirectory: () => true } as fs.Stats;
        case 'node_modules':
          return { mtime: oldDate, isFile: () => false, isDirectory: () => true } as fs.Stats;
        case 'nested-old-file.log':
          return { mtime: oldDate, isFile: () => true, isDirectory: () => false } as fs.Stats;
        default:
          throw new Error('File not found in mock');
      }
    });

    // Mock Date.now() for consistent age calculation
    const spy = jest.spyOn(global, 'Date').mockImplementation(() => now as any);

    const scanner = new TemporalResidueScanner(baseScanOptions);
    const residues = await scanner.scan();

    expect(residues).toHaveLength(3); // old-file.txt, old-dir, nested-old-file.log

    const residuePaths = residues.map(r => r.path).sort();
    expect(residuePaths).toEqual([
      '/mock/project/nested-old-file.log',
      '/mock/project/old-dir',
      '/mock/project/old-file.txt',
    ]);

    expect(residues).toContainEqual(
      expect.objectContaining({
        path: '/mock/project/old-file.txt',
        type: 'file',
        lastModified: oldDate,
        reason: 'File older than 30 days.',
      })
    );
    expect(residues).toContainEqual(
      expect.objectContaining({
        path: '/mock/project/old-dir',
        type: 'directory',
        lastModified: oldDate,
        reason: 'Directory older than 30 days.',
      })
    );
    expect(residues).toContainEqual(
      expect.objectContaining({
        path: '/mock/project/nested-old-file.log',
        type: 'file',
        lastModified: oldDate,
        reason: 'File older than 30 days.',
      })
    );

    // Ensure ignored directory was not scanned
    expect(mockFsPromises.readdir).not.toHaveBeenCalledWith('/mock/project/node_modules', expect.any(Object));

    spy.mockRestore();
  });

  it('should return empty array if no residue is found', async () => {
    const now = new Date('2023-10-26T12:00:00Z');
    const recentDate = new Date('2023-10-15T12:00:00Z'); // Newer than 30 days

    mockFsPromises.readdir.mockImplementation(async (dirPath: fs.PathLike, options: any) => {
      if (dirPath === '/mock/project') {
        return [
          { name: 'recent-file.txt', isFile: () => true, isDirectory: () => false },
          { name: 'recent-dir', isFile: () => false, isDirectory: () => true },
        ];
      }
      return [];
    });

    mockFsPromises.stat.mockImplementation(async (filePath: fs.PathLike) => {
      const fileName = path.basename(filePath.toString());
      switch (fileName) {
        case 'recent-file.txt':
          return { mtime: recentDate, isFile: () => true, isDirectory: () => false } as fs.Stats;
        case 'recent-dir':
          return { mtime: recentDate, isFile: () => false, isDirectory: () => true } as fs.Stats;
        default:
          throw new Error('File not found in mock');
      }
    });

    const spy = jest.spyOn(global, 'Date').mockImplementation(() => now as any);

    const scanner = new TemporalResidueScanner(baseScanOptions);
    const residues = await scanner.scan();

    expect(residues).toHaveLength(0);
    spy.mockRestore();
  });

  it('should handle non-existent path gracefully', async () => {
    mockFsPromises.readdir.mockImplementation(async (dirPath: fs.PathLike, options: any) => {
      if (dirPath === '/mock/non-existent') {
        throw new Error('ENOENT: no such file or directory');
      }
      return [];
    });
    mockFsPromises.stat.mockImplementation(async (filePath: fs.PathLike) => {
      throw new Error('ENOENT: no such file or directory');
    });

    const scanner = new TemporalResidueScanner({ ...baseScanOptions, path: '/mock/non-existent' });
    const residues = await scanner.scan();

    expect(residues).toHaveLength(0); // Should not throw, just return empty
  });

  it('should respect ignore patterns for nested directories', async () => {
    const now = new Date('2023-10-26T12:00:00Z');
    const oldDate = new Date('2023-09-01T12:00:00Z');

    mockFsPromises.readdir.mockImplementation(async (dirPath: fs.PathLike, options: any) => {
      if (dirPath === '/mock/project') {
        return [
          { name: 'src', isFile: () => false, isDirectory: () => true },
          { name: 'dist', isFile: () => false, isDirectory: () => true }, // Ignored
        ];
      }
      if (dirPath === '/mock/project/src') {
        return [
          { name: 'main.ts', isFile: () => true, isDirectory: () => false },
        ];
      }
      // Should not attempt to read 'dist' because it's ignored
      return [];
    });

    mockFsPromises.stat.mockImplementation(async (filePath: fs.PathLike) => {
      const fileName = path.basename(filePath.toString());
      switch (fileName) {
        case 'src':
          return { mtime: oldDate, isFile: () => false, isDirectory: () => true } as fs.Stats;
        case 'main.ts':
          return { mtime: oldDate, isFile: () => true, isDirectory: () => false } as fs.Stats;
        case 'dist':
          return { mtime: oldDate, isFile: () => false, isDirectory: () => true } as fs.Stats;
        default:
          throw new Error('File not found in mock');
      }
    });

    const spy = jest.spyOn(global, 'Date').mockImplementation(() => now as any);

    const scanner = new TemporalResidueScanner({ ...baseScanOptions, ignorePatterns: ['dist'] });
    const residues = await scanner.scan();

    expect(residues).toHaveLength(2); // src (dir), main.ts (file)
    expect(residues.map(r => r.path)).not.toContain('/mock/project/dist');
    expect(mockFsPromises.readdir).not.toHaveBeenCalledWith('/mock/project/dist', expect.any(Object));

    spy.mockRestore();
  });
});
