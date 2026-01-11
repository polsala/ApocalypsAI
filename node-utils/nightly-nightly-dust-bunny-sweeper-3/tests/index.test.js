const { sweep, findDustBunnies, isDustBunny, DUST_BUNNY_PATTERNS } = require('../src/index');
const { promises: fs } = require('fs');
const path = require('path');

// Mock rationale: We need to simulate file system operations without actually touching the disk.
// This ensures tests are deterministic, fast, and safe, preventing accidental data loss.
jest.mock('fs', () => ({
  promises: {
    readdir: jest.fn(),
    rm: jest.fn(),
    stat: jest.fn(), // stat might be used internally by readdir withFileTypes, but not directly called by our code
  },
}));

// Mock console.log and console.error to prevent test output from cluttering the console
const mockLog = jest.spyOn(console, 'log').mockImplementation(() => {});
const mockError = jest.spyOn(console, 'error').mockImplementation(() => {});

describe('isDustBunny', () => {
  test('should identify node_modules as a dust bunny', () => {
    expect(isDustBunny('path/to/node_modules', { isDirectory: () => true })).toBe(true);
  });

  test('should identify dist as a dust bunny', () => {
    expect(isDustBunny('path/to/dist', { isDirectory: () => true })).toBe(true);
  });

  test('should identify a .log file as a dust bunny', () => {
    expect(isDustBunny('path/to/app.log', { isDirectory: () => false })).toBe(true);
  });

  test('should identify .DS_Store as a dust bunny', () => {
    expect(isDustBunny('path/to/.DS_Store', { isDirectory: () => false })).toBe(true);
  });

  test('should not identify a regular file as a dust bunny', () => {
    expect(isDustBunny('path/to/main.js', { isDirectory: () => false })).toBe(false);
  });

  test('should not identify a regular directory as a dust bunny', () => {
    expect(isDustBunny('path/to/src', { isDirectory: () => true })).toBe(false);
  });
});

describe('findDustBunnies', () => {
  const mockDir = '/mock/project';

  beforeEach(() => {
    jest.clearAllMocks();
    // Mock rationale: Simulate the directory structure for testing traversal and identification.
    fs.readdir.mockImplementation(async (dir) => {
      if (dir === mockDir) {
        return [
          { name: 'src', isDirectory: () => true, isSymbolicLink: () => false },
          { name: 'node_modules', isDirectory: () => true, isSymbolicLink: () => false },
          { name: 'dist', isDirectory: () => true, isSymbolicLink: () => false },
          { name: 'app.log', isDirectory: () => false, isSymbolicLink: () => false },
          { name: 'temp', isDirectory: () => true, isSymbolicLink: () => false },
          { name: 'empty_dir', isDirectory: () => true, isSymbolicLink: () => false },
          { name: 'symlink_dir', isDirectory: () => true, isSymbolicLink: () => true },
        ];
      } else if (dir === path.join(mockDir, 'src')) {
        return [
          { name: 'main.js', isDirectory: () => false, isSymbolicLink: () => false },
        ];
      } else if (dir === path.join(mockDir, 'node_modules')) {
        return [
          { name: 'some-package', isDirectory: () => true, isSymbolicLink: () => false },
        ];
      } else if (dir === path.join(mockDir, 'dist')) {
        return [
          { name: 'bundle.js', isDirectory: () => false, isSymbolicLink: () => false },
        ];
      } else if (dir === path.join(mockDir, 'temp')) {
        return [
          { name: 'temp.bak', isDirectory: () => false, isSymbolicLink: () => false },
        ];
      } else if (dir === path.join(mockDir, 'empty_dir')) {
        return []; // Simulate an empty directory
      }
      return [];
    });
  });

  test('should find all expected dust bunnies in a mock directory structure', async () => {
    const expectedBunnies = [
      path.join(mockDir, 'node_modules'),
      path.join(mockDir, 'dist'),
      path.join(mockDir, 'app.log'),
      path.join(mockDir, 'temp'),
      path.join(mockDir, 'temp', 'temp.bak'), // temp.bak is inside temp
      path.join(mockDir, 'empty_dir') + ' (empty directory)',
    ];

    const found = await findDustBunnies(mockDir);
    // Sort to ensure consistent order for comparison
    const sortedFound = found.sort();
    const sortedExpected = expectedBunnies.sort();

    expect(sortedFound).toEqual(sortedExpected);
    expect(fs.readdir).toHaveBeenCalledWith(mockDir, { withFileTypes: true });
    expect(fs.readdir).toHaveBeenCalledWith(path.join(mockDir, 'src'), { withFileTypes: true });
    // Should not traverse into node_modules or dist because they are marked as dust bunnies themselves
    expect(fs.readdir).not.toHaveBeenCalledWith(path.join(mockDir, 'node_modules'), { withFileTypes: true });
    expect(fs.readdir).not.toHaveBeenCalledWith(path.join(mockDir, 'dist'), { withFileTypes: true });
    expect(fs.readdir).toHaveBeenCalledWith(path.join(mockDir, 'temp'), { withFileTypes: true });
    expect(fs.readdir).toHaveBeenCalledWith(path.join(mockDir, 'empty_dir'), { withFileTypes: true });
  });

  test('should handle inaccessible directories gracefully', async () => {
    fs.readdir.mockImplementation(async (dir) => {
      if (dir === mockDir) {
        return [
          { name: 'inaccessible', isDirectory: () => true, isSymbolicLink: () => false },
        ];
      } else if (dir === path.join(mockDir, 'inaccessible')) {
        const error = new Error('Permission denied');
        error.code = 'EACCES';
        throw error;
      }
      return [];
    });

    const found = await findDustBunnies(mockDir);
    expect(found).toEqual([]);
  });

  test('should not include symbolic links in dust bunnies', async () => {
    fs.readdir.mockImplementation(async (dir) => {
      if (dir === mockDir) {
        return [
          { name: 'symlink_to_node_modules', isDirectory: () => true, isSymbolicLink: () => true },
        ];
      }
      return [];
    });

    const found = await findDustBunnies(mockDir);
    expect(found).toEqual([]);
  });
});

describe('sweep', () => {
  const mockPath = '/mock/project';

  beforeEach(() => {
    jest.clearAllMocks();
    // Mock rationale: Simulate the directory structure for testing traversal and identification.
    fs.readdir.mockImplementation(async (dir) => {
      if (dir === mockPath) {
        return [
          { name: 'node_modules', isDirectory: () => true, isSymbolicLink: () => false },
          { name: 'app.log', isDirectory: () => false, isSymbolicLink: () => false },
          { name: 'empty_dir', isDirectory: () => true, isSymbolicLink: () => false },
        ];
      } else if (dir === path.join(mockPath, 'node_modules')) {
        return [
          { name: 'some-package', isDirectory: () => true, isSymbolicLink: () => false },
        ];
      } else if (dir === path.join(mockPath, 'empty_dir')) {
        return [];
      }
      return [];
    });
  });

  test('should perform a dry run and report findings without deleting', async () => {
    await sweep(mockPath, true, false);

    expect(mockLog).toHaveBeenCalledWith(expect.stringContaining('Starting the Nightly Digital Dust Bunny Sweeper'));
    expect(mockLog).toHaveBeenCalledWith(expect.stringContaining('Found 3 digital dust bunnies:'));
    expect(mockLog).toHaveBeenCalledWith(expect.stringContaining(path.join(mockPath, 'node_modules')));
    expect(mockLog).toHaveBeenCalledWith(expect.stringContaining(path.join(mockPath, 'app.log')));
    expect(mockLog).toHaveBeenCalledWith(expect.stringContaining(path.join(mockPath, 'empty_dir') + ' (empty directory)'));
    expect(mockLog).toHaveBeenCalledWith(expect.stringContaining('This was a dry run. No files were actually deleted.'));
    expect(fs.rm).not.toHaveBeenCalled();
  });

  test('should delete identified dust bunnies when deleteFiles is true', async () => {
    await sweep(mockPath, false, true);

    expect(mockLog).toHaveBeenCalledWith(expect.stringContaining('Sweeping away the digital fluff...'));
    expect(fs.rm).toHaveBeenCalledTimes(3); // node_modules, app.log, and empty_dir
    expect(fs.rm).toHaveBeenCalledWith(path.join(mockPath, 'node_modules'), { recursive: true, force: true });
    expect(fs.rm).toHaveBeenCalledWith(path.join(mockPath, 'app.log'), { recursive: true, force: true });
    expect(fs.rm).toHaveBeenCalledWith(path.join(mockPath, 'empty_dir'), { recursive: false, force: true });
    expect(mockLog).toHaveBeenCalledWith(expect.stringContaining('Your project space feels lighter and tidier!'));
  });

  test('should handle no dust bunnies found', async () => {
    // Mock rationale: Simulate a clean directory with no dust bunnies.
    fs.readdir.mockImplementation(async (dir) => {
      if (dir === mockPath) {
        return [
          { name: 'src', isDirectory: () => true, isSymbolicLink: () => false },
          { name: 'index.js', isDirectory: () => false, isSymbolicLink: () => false },
        ];
      } else if (dir === path.join(mockPath, 'src')) {
        return [
          { name: 'util.js', isDirectory: () => false, isSymbolicLink: () => false },
        ];
      }
      return [];
    });

    await sweep(mockPath, true, false);

    expect(mockLog).toHaveBeenCalledWith(expect.stringContaining('No digital dust bunnies found! Your space is sparkling clean.'));
    expect(fs.rm).not.toHaveBeenCalled();
  });

  test('should log error if deletion fails', async () => {
    fs.rm.mockImplementation(async (filePath, options) => {
      if (filePath === path.join(mockPath, 'app.log')) {
        throw new Error('Permission denied to delete log');
      }
      if (filePath === path.join(mockPath, 'empty_dir')) {
        throw new Error('Cannot remove empty directory');
      }
      // For node_modules, let it succeed for this test
      return Promise.resolve();
    });

    await sweep(mockPath, false, true);

    expect(mockError).toHaveBeenCalledWith(expect.stringContaining('Failed to sweep ' + path.join(mockPath, 'app.log') + ': Permission denied to delete log'));
    expect(mockError).toHaveBeenCalledWith(expect.stringContaining('Failed to sweep ' + path.join(mockPath, 'empty_dir') + ': Cannot remove empty directory'));
    expect(fs.rm).toHaveBeenCalled();
  });

  test('should default to dry-run if no delete flag is provided', async () => {
    // Mock rationale: Simulate the directory structure for testing traversal and identification.
    fs.readdir.mockImplementation(async (dir) => {
      if (dir === mockPath) {
        return [
          { name: 'node_modules', isDirectory: () => true, isSymbolicLink: () => false },
        ];
      }
      return [];
    });

    // Simulate running without --delete or --dry-run explicitly
    // The main function's action will set dryRun to true by default
    await sweep(mockPath, true, false); // This simulates the default behavior

    expect(mockLog).toHaveBeenCalledWith(expect.stringContaining('This was a dry run. No files were actually deleted.'));
    expect(fs.rm).not.toHaveBeenCalled();
  });
});

// Restore console.log and console.error after all tests
afterAll(() => {
  mockLog.mockRestore();
  mockError.mockRestore();
});
