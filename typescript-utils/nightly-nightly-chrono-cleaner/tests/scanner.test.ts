import { scanForTemporalEchoes } from '../src/scanner';
import { ChronoCleanerConfig, TemporalEcho } from '../src/types';
import { promises as fsPromises } from 'fs';
import * as path from 'path';

// Mock rationale: We need to control the file system state (files, directories, modification times, content)
// to ensure deterministic and offline testing of the scanner logic without actual disk I/O.
jest.mock('fs', () => ({
  promises: {
    readdir: jest.fn(),
    stat: jest.fn(),
    readFile: jest.fn(),
  },
}));

const mockReaddir = fsPromises.readdir as jest.Mock;
const mockStat = fsPromises.stat as jest.Mock;
const mockReadFile = fsPromises.readFile as jest.Mock;

describe('scanForTemporalEchoes', () => {
  const baseConfig: ChronoCleanerConfig = {
    scanPath: '/mock-project',
    staleDays: 30,
    ignorePatterns: [],
    reportFormat: 'text',
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should find no echoes in an empty directory', async () => {
    mockReaddir.mockResolvedValueOnce([]); // Root directory is empty

    const echoes = await scanForTemporalEchoes(baseConfig);
    expect(echoes).toEqual([]);
    expect(mockReaddir).toHaveBeenCalledWith(baseConfig.scanPath, { withFileTypes: true });
  });

  it('should find a stale file', async () => {
    const now = new Date();
    const thirtyOneDaysAgo = new Date(now.getTime() - (31 * 24 * 60 * 60 * 1000));

    mockReaddir.mockResolvedValueOnce([
      { name: 'stale.txt', isDirectory: () => false, isFile: () => true },
    ]);
    mockStat.mockResolvedValueOnce({ mtime: thirtyOneDaysAgo, isFile: () => true });
    mockReadFile.mockRejectedValue(new Error('Not a text file or irrelevant')); // Don't care about content for staleness

    const echoes = await scanForTemporalEchoes(baseConfig);
    expect(echoes).toHaveLength(1);
    expect(echoes[0].filePath).toBe(path.join(baseConfig.scanPath, 'stale.txt'));
    expect(echoes[0].reason).toBe('stale');
    expect(echoes[0].ageDays).toBe(31);
    expect(echoes[0].lastModified?.toISOString()).toBe(thirtyOneDaysAgo.toISOString());
  });

  it('should not find a fresh file as stale', async () => {
    const now = new Date();
    const twentyDaysAgo = new Date(now.getTime() - (20 * 24 * 60 * 60 * 1000));

    mockReaddir.mockResolvedValueOnce([
      { name: 'fresh.txt', isDirectory: () => false, isFile: () => true },
    ]);
    mockStat.mockResolvedValueOnce({ mtime: twentyDaysAgo, isFile: () => true });
    mockReadFile.mockRejectedValue(new Error('Not a text file or irrelevant'));

    const echoes = await scanForTemporalEchoes(baseConfig);
    expect(echoes).toEqual([]);
  });

  it('should find a file with a deprecated marker', async () => {
    const now = new Date();
    const freshDate = new Date(now.getTime() - (5 * 24 * 60 * 60 * 1000)); // Not stale

    mockReaddir.mockResolvedValueOnce([
      { name: 'deprecated.ts', isDirectory: () => false, isFile: () => true },
    ]);
    mockStat.mockResolvedValueOnce({ mtime: freshDate, isFile: () => true });
    mockReadFile.mockResolvedValueOnce('// This is some code\n// DEPRECATED: Use new function instead\nconst oldFunc = () => {};');

    const echoes = await scanForTemporalEchoes(baseConfig);
    expect(echoes).toHaveLength(1);
    expect(echoes[0].filePath).toBe(path.join(baseConfig.scanPath, 'deprecated.ts'));
    expect(echoes[0].reason).toBe('deprecated-marker');
    expect(echoes[0].markerContent).toBe('// DEPRECATED');
  });

  it('should find both stale and deprecated files', async () => {
    const now = new Date();
    const staleDate = new Date(now.getTime() - (40 * 24 * 60 * 60 * 1000));
    const deprecatedDate = new Date(now.getTime() - (10 * 24 * 60 * 60 * 1000));

    mockReaddir.mockResolvedValueOnce([
      { name: 'stale.js', isDirectory: () => false, isFile: () => true },
      { name: 'deprecated.py', isDirectory: () => false, isFile: () => true },
    ]);
    mockStat.mockImplementation((filePath) => {
      if (filePath.includes('stale.js')) {
        return Promise.resolve({ mtime: staleDate, isFile: () => true });
      }
      if (filePath.includes('deprecated.py')) {
        return Promise.resolve({ mtime: deprecatedDate, isFile: () => true });
      }
      return Promise.reject(new Error('File not found'));
    });
    mockReadFile.mockImplementation((filePath) => {
      if (filePath.includes('deprecated.py')) {
        return Promise.resolve('# ARCHIVED: This script is no longer used');
      }
      return Promise.reject(new Error('Not a text file or irrelevant'));
    });

    const echoes = await scanForTemporalEchoes(baseConfig);
    expect(echoes).toHaveLength(2);
    expect(echoes).toContainEqual(expect.objectContaining({
      filePath: path.join(baseConfig.scanPath, 'stale.js'),
      reason: 'stale',
      ageDays: 40,
    }));
    expect(echoes).toContainEqual(expect.objectContaining({
      filePath: path.join(baseConfig.scanPath, 'deprecated.py'),
      reason: 'deprecated-marker',
      markerContent: '# ARCHIVED',
    }));
  });

  it('should ignore files matching ignore patterns', async () => {
    const now = new Date();
    const staleDate = new Date(now.getTime() - (40 * 24 * 60 * 60 * 1000));

    mockReaddir.mockResolvedValueOnce([
      { name: 'node_modules', isDirectory: () => true, isFile: () => false },
      { name: 'dist', isDirectory: () => true, isFile: () => false },
      { name: 'src', isDirectory: () => true, isFile: () => false },
    ]);
    mockReaddir.mockResolvedValueOnce([ // inside src
      { name: 'stale.js', isDirectory: () => false, isFile: () => true },
    ]);
    mockStat.mockResolvedValueOnce({ mtime: staleDate, isFile: () => true });
    mockReadFile.mockRejectedValue(new Error('Not a text file or irrelevant'));

    const configWithIgnore: ChronoCleanerConfig = {
      ...baseConfig,
      ignorePatterns: ['node_modules', 'dist'],
    };

    const echoes = await scanForTemporalEchoes(configWithIgnore);
    expect(echoes).toHaveLength(1); // Only stale.js in src should be found
    expect(echoes[0].filePath).toBe(path.join(baseConfig.scanPath, 'src', 'stale.js'));
    expect(mockReaddir).toHaveBeenCalledWith(path.join(baseConfig.scanPath, 'src'), { withFileTypes: true });
    expect(mockReaddir).not.toHaveBeenCalledWith(path.join(baseConfig.scanPath, 'node_modules'), { withFileTypes: true });
    expect(mockReaddir).not.toHaveBeenCalledWith(path.join(baseConfig.scanPath, 'dist'), { withFileTypes: true });
  });

  it('should handle nested directories', async () => {
    const now = new Date();
    const staleDate = new Date(now.getTime() - (50 * 24 * 60 * 60 * 1000));

    mockReaddir.mockResolvedValueOnce([
      { name: 'folder1', isDirectory: () => true, isFile: () => false },
    ]);
    mockReaddir.mockResolvedValueOnce([ // inside folder1
      { name: 'nested_stale.txt', isDirectory: () => false, isFile: () => true },
    ]);
    mockStat.mockResolvedValueOnce({ mtime: staleDate, isFile: () => true });
    mockReadFile.mockRejectedValue(new Error('Not a text file or irrelevant'));

    const echoes = await scanForTemporalEchoes(baseConfig);
    expect(echoes).toHaveLength(1);
    expect(echoes[0].filePath).toBe(path.join(baseConfig.scanPath, 'folder1', 'nested_stale.txt'));
    expect(echoes[0].reason).toBe('stale');
  });

  it('should gracefully handle unreadable directories', async () => {
    mockReaddir.mockRejectedValueOnce(new Error('Permission denied')); // Root directory unreadable

    const echoes = await scanForTemporalEchoes(baseConfig);
    expect(echoes).toEqual([]);
    expect(mockReaddir).toHaveBeenCalledWith(baseConfig.scanPath, { withFileTypes: true });
  });

  it('should gracefully handle unreadable files for stat', async () => {
    const now = new Date();
    const staleDate = new Date(now.getTime() - (50 * 24 * 60 * 60 * 1000));

    mockReaddir.mockResolvedValueOnce([
      { name: 'unreadable.txt', isDirectory: () => false, isFile: () => true },
      { name: 'readable.txt', isDirectory: () => false, isFile: () => true },
    ]);
    mockStat.mockImplementation((filePath) => {
      if (filePath.includes('unreadable.txt')) {
        return Promise.reject(new Error('Permission denied'));
      }
      if (filePath.includes('readable.txt')) {
        return Promise.resolve({ mtime: staleDate, isFile: () => true });
      }
      return Promise.reject(new Error('File not found'));
    });
    mockReadFile.mockRejectedValue(new Error('Not a text file or irrelevant'));

    const echoes = await scanForTemporalEchoes(baseConfig);
    expect(echoes).toHaveLength(1);
    expect(echoes[0].filePath).toBe(path.join(baseConfig.scanPath, 'readable.txt'));
  });

  it('should gracefully handle unreadable files for content scan', async () => {
    const now = new Date();
    const freshDate = new Date(now.getTime() - (5 * 24 * 60 * 60 * 1000));

    mockReaddir.mockResolvedValueOnce([
      { name: 'binary.bin', isDirectory: () => false, isFile: () => true },
      { name: 'text.txt', isDirectory: () => false, isFile: () => true },
    ]);
    mockStat.mockResolvedValue({ mtime: freshDate, isFile: () => true }); // Both fresh
    mockReadFile.mockImplementation((filePath) => {
      if (filePath.includes('binary.bin')) {
        return Promise.reject(new Error('Encoding not supported')); // Simulates binary file
      }
      if (filePath.includes('text.txt')) {
        return Promise.resolve('This is a normal text file.');
      }
      return Promise.reject(new Error('File not found'));
    });

    const echoes = await scanForTemporalEchoes(baseConfig);
    expect(echoes).toEqual([]); // No deprecated markers, and not stale
  });

  it('should detect @deprecated JSDoc marker', async () => {
    const now = new Date();
    const freshDate = new Date(now.getTime() - (5 * 24 * 60 * 60 * 1000));

    mockReaddir.mockResolvedValueOnce([
      { name: 'jsdoc.js', isDirectory: () => false, isFile: () => true },
    ]);
    mockStat.mockResolvedValueOnce({ mtime: freshDate, isFile: () => true });
    mockReadFile.mockResolvedValueOnce('/**\n * @deprecated This function is old.\n */\nfunction oldFn() {}');

    const echoes = await scanForTemporalEchoes(baseConfig);
    expect(echoes).toHaveLength(1);
    expect(echoes[0].filePath).toBe(path.join(baseConfig.scanPath, 'jsdoc.js'));
    expect(echoes[0].reason).toBe('deprecated-marker');
    expect(echoes[0].markerContent).toBe('@deprecated');
  });
});
