import { CosmicCompass } from '../src/index';
import * as fs from 'fs';
import * as path from 'path';

// Mock rationale: We need to simulate file system operations without actually touching the disk
// to ensure tests are deterministic, fast, and can run offline in any environment.
jest.mock('fs', () => ({
  promises: {
    readdir: jest.fn(),
  },
  // Keep other fs functions if needed, but for this utility, readdir is the primary interaction.
  ...jest.requireActual('fs'),
}));

// Mock rationale: We need to control the path resolution for consistent testing
// of the utility's interaction with the file system. This ensures that relative paths
// are calculated predictably within the mocked environment.
jest.mock('path', () => ({
  ...jest.requireActual('path'), // Use actual path functions for join, extname, etc.
  resolve: jest.fn((p: string) => p), // Mock resolve to return path as is for simplicity in tests
  relative: jest.fn((from: string, to: string) => {
    // Simple relative path calculation for mock, assuming 'to' is always a descendant of 'from'
    if (to.startsWith(from)) {
      const relative = to.substring(from.length);
      return relative.startsWith('/') ? relative.substring(1) : relative;
    }
    return to; // Fallback if not a descendant, though not expected in current tests
  }),
}));

const mockReaddir = fs.promises.readdir as jest.MockedFunction<typeof fs.promises.readdir>;
const mockPathResolve = path.resolve as jest.MockedFunction<typeof path.resolve>;
const mockPathRelative = path.relative as jest.MockedFunction<typeof path.relative>;

describe('CosmicCompass', () => {
  const mockRootPath = '/mock/project';

  beforeEach(() => {
    jest.clearAllMocks();
    mockPathResolve.mockImplementation((p: string) => p); // Ensure path.resolve returns the path directly for tests
    mockPathRelative.mockImplementation((from: string, to: string) => {
      if (to.startsWith(from)) {
        const relative = to.substring(from.length);
        return relative.startsWith('/') ? relative.substring(1) : relative;
      }
      return to;
    });
  });

  it('should build an atlas for a simple directory structure', async () => {
    mockReaddir.mockResolvedValueOnce([
      { name: 'file1.txt', isDirectory: () => false, isFile: () => true, isBlockDevice: () => false, isCharacterDevice: () => false, isFIFO: () => false, isSocket: () => false, isSymbolicLink: () => false },
      { name: 'dirA', isDirectory: () => true, isFile: () => false, isBlockDevice: () => false, isCharacterDevice: () => false, isFIFO: () => false, isSocket: () => false, isSymbolicLink: () => false },
    ]);
    mockReaddir.mockResolvedValueOnce([ // For dirA
      { name: 'fileA1.js', isDirectory: () => false, isFile: () => true, isBlockDevice: () => false, isCharacterDevice: () => false, isFIFO: () => false, isSocket: () => false, isSymbolicLink: () => false },
    ]);

    const compass = new CosmicCompass(mockRootPath);
    await compass.buildAtlas();
    const atlas = compass.getAtlas();

    expect(atlas['file1.txt']).toEqual({ path: 'file1.txt', name: 'file1.txt', type: 'file' });
    expect(atlas['dirA']).toEqual({ path: 'dirA', name: 'dirA', type: 'directory' });
    expect(atlas['dirA/fileA1.js']).toEqual({ path: 'dirA/fileA1.js', name: 'fileA1.js', type: 'file' });
    expect(Object.keys(atlas).length).toBe(3);
  });

  it('should handle empty directories', async () => {
    mockReaddir.mockResolvedValueOnce([
      { name: 'emptyDir', isDirectory: () => true, isFile: () => false, isBlockDevice: () => false, isCharacterDevice: () => false, isFIFO: () => false, isSocket: () => false, isSymbolicLink: () => false },
    ]);
    mockReaddir.mockResolvedValueOnce([]); // For emptyDir

    const compass = new CosmicCompass(mockRootPath);
    await compass.buildAtlas();
    const atlas = compass.getAtlas();

    expect(atlas['emptyDir']).toEqual({ path: 'emptyDir', name: 'emptyDir', type: 'directory' });
    expect(Object.keys(atlas).length).toBe(1);
  });

  it('should search for keywords in file and directory names', async () => {
    mockReaddir.mockResolvedValueOnce([
      { name: 'component.ts', isDirectory: () => false, isFile: () => true, isBlockDevice: () => false, isCharacterDevice: () => false, isFIFO: () => false, isSocket: () => false, isSymbolicLink: () => false },
      { name: 'utils', isDirectory: () => true, isFile: () => false, isBlockDevice: () => false, isCharacterDevice: () => false, isFIFO: () => false, isSocket: () => false, isSymbolicLink: () => false },
    ]);
    mockReaddir.mockResolvedValueOnce([ // For utils
      { name: 'helper.js', isDirectory: () => false, isFile: () => true, isBlockDevice: () => false, isCharacterDevice: () => false, isFIFO: () => false, isSocket: () => false, isSymbolicLink: () => false },
    ]);

    const compass = new CosmicCompass(mockRootPath);
    await compass.buildAtlas();

    let results = compass.searchAtlas(['comp']);
    expect(results.length).toBe(1);
    expect(results[0].celestialBody.name).toBe('component.ts');

    results = compass.searchAtlas(['util']);
    expect(results.length).toBe(1);
    expect(results[0].celestialBody.name).toBe('utils');

    results = compass.searchAtlas(['js']);
    expect(results.length).toBe(1);
    expect(results[0].celestialBody.name).toBe('helper.js');

    results = compass.searchAtlas(['nonexistent']);
    expect(results.length).toBe(0);
  });

  it('should be case-insensitive when searching', async () => {
    mockReaddir.mockResolvedValueOnce([
      { name: 'README.md', isDirectory: () => false, isFile: () => true, isBlockDevice: () => false, isCharacterDevice: () => false, isFIFO: () => false, isSocket: () => false, isSymbolicLink: () => false },
    ]);

    const compass = new CosmicCompass(mockRootPath);
    await compass.buildAtlas();

    let results = compass.searchAtlas(['readme']);
    expect(results.length).toBe(1);
    expect(results[0].celestialBody.name).toBe('README.md');

    results = compass.searchAtlas(['README']);
    expect(results.length).toBe(1);
    expect(results[0].celestialBody.name).toBe('README.md');
  });

  it('should handle readdir errors gracefully during atlas build', async () => {
    mockReaddir.mockRejectedValueOnce(new Error('Permission denied'));
    mockReaddir.mockResolvedValueOnce([
      { name: 'file.txt', isDirectory: () => false, isFile: () => true, isBlockDevice: () => false, isCharacterDevice: () => false, isFIFO: () => false, isSocket: () => false, isSymbolicLink: () => false },
    ]);

    const consoleWarnSpy = jest.spyOn(console, 'warn').mockImplementation(() => {}); // Mock console.warn

    const compass = new CosmicCompass(mockRootPath);
    await compass.buildAtlas();
    const atlas = compass.getAtlas();

    expect(consoleWarnSpy).toHaveBeenCalledWith(expect.stringContaining('Cosmic Compass Warning: Could not read stellar path'));
    expect(Object.keys(atlas).length).toBe(1); // Only file.txt should be in atlas, as the root read failed but subsequent reads might be mocked to succeed

    consoleWarnSpy.mockRestore();
  });
});
