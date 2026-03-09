const { findDustBunnies, getFileStats, main } = require('../src/index');
const assert = require('assert');
const path = require('path');

// Mock fs.promises module
const mockFs = {
  readdir: async (dirPath, options) => {
    // Mock rationale: Simulate file system structure for deterministic testing.
    if (dirPath === '/mock/root') {
      return [
        { name: 'old_large_file.txt', isFile: () => true, isDirectory: () => false },
        { name: 'new_small_file.txt', isFile: () => true, isDirectory: () => false },
        { name: 'old_small_file.txt', isFile: () => true, isDirectory: () => false },
        { name: 'new_large_file.txt', isFile: () => true, isDirectory: () => false },
        { name: 'subdir', isFile: () => false, isDirectory: () => true },
        { name: 'inaccessible_file.txt', isFile: () => true, isDirectory: () => false },
      ];
    } else if (dirPath === '/mock/root/subdir') {
      return [
        { name: 'nested_old_large.log', isFile: () => true, isDirectory: () => false },
      ];
    } else if (dirPath === '/mock/empty') {
      return [];
    } else if (dirPath === '/mock/inaccessible_dir') {
      throw new Error('Permission denied');
    }
    return [];
  },
  stat: async (filePath) => {
    // Mock rationale: Provide consistent file stats for testing age and size criteria.
    const now = Date.now();
    const oneYearAgo = now - (365 * 24 * 60 * 60 * 1000);
    const sixMonthsAgo = now - (180 * 24 * 60 * 60 * 1000);

    switch (filePath) {
      case '/mock/root':
        return { mtimeMs: now, size: 4096, isFile: () => false, isDirectory: () => true };
      case '/mock/empty':
        return { mtimeMs: now, size: 4096, isFile: () => false, isDirectory: () => true };
      case '/mock/inaccessible_dir':
        return { mtimeMs: now, size: 4096, isFile: () => false, isDirectory: () => true };
      case '/mock/root_is_file':
        return { mtimeMs: now, size: 100, isFile: () => true, isDirectory: () => false };
      case '/mock/root/old_large_file.txt':
        return { mtimeMs: oneYearAgo - 1000, size: 150 * 1024 * 1024, isFile: () => true, isDirectory: () => false }; // Old and Large
      case '/mock/root/new_small_file.txt':
        return { mtimeMs: sixMonthsAgo, size: 50 * 1024 * 1024, isFile: () => true, isDirectory: () => false }; // New and Small
      case '/mock/root/old_small_file.txt':
        return { mtimeMs: oneYearAgo - 1000, size: 50 * 1024 * 1024, isFile: () => true, isDirectory: () => false }; // Old but Small
      case '/mock/root/new_large_file.txt':
        return { mtimeMs: sixMonthsAgo, size: 150 * 1024 * 1024, isFile: () => true, isDirectory: () => false }; // New but Large
      case '/mock/root/subdir':
        return { mtimeMs: now, size: 4096, isFile: () => false, isDirectory: () => true };
      case '/mock/root/subdir/nested_old_large.log':
        return { mtimeMs: oneYearAgo - 5000, size: 200 * 1024 * 1024, isFile: () => true, isDirectory: () => false }; // Nested Old and Large
      case '/mock/root/inaccessible_file.txt':
        throw new Error('Permission denied for inaccessible_file.txt');
      case '/mock/nonexistent':
        throw new Error('ENOENT: no such file or directory, stat \'/mock/nonexistent\'');
      default:
        return { mtimeMs: now, size: 10, isFile: () => true, isDirectory: () => false }; // Default for unexpected paths
    }
  }
};

// Override fs.promises with our mock
const originalFs = require('fs').promises;
require('fs').promises = mockFs;

describe('Digital Dust Bunny Sweeper', () => {
  const defaultAge = 365; // 1 year
  const defaultSize = 100; // 100 MB

  it('should find old and large files (dust bunnies) with default thresholds', async () => {
    const bunnies = await findDustBunnies('/mock/root', defaultAge, defaultSize);
    assert.strictEqual(bunnies.length, 2, 'Should find 2 dust bunnies');
    assert.ok(bunnies.some(b => b.path === '/mock/root/old_large_file.txt'), 'Should include old_large_file.txt');
    assert.ok(bunnies.some(b => b.path === '/mock/root/subdir/nested_old_large.log'), 'Should include nested_old_large.log');
  });

  it('should find no dust bunnies if directory is empty', async () => {
    const bunnies = await findDustBunnies('/mock/empty', defaultAge, defaultSize);
    assert.strictEqual(bunnies.length, 0, 'Should find no dust bunnies in an empty directory');
  });

  it('should handle inaccessible files gracefully', async () => {
    // The inaccessible_file.txt should be ignored, not cause a crash.
    const bunnies = await findDustBunnies('/mock/root', defaultAge, defaultSize);
    assert.strictEqual(bunnies.length, 2, 'Should still find other dust bunnies and ignore inaccessible file');
  });

  it('should return no dust bunnies if no files match criteria', async () => {
    // With very high thresholds, nothing should match
    const bunnies = await findDustBunnies('/mock/root', 10000, 10000);
    assert.strictEqual(bunnies.length, 0, 'Should find no dust bunnies with very high thresholds');
  });

  it('should return no dust bunnies if files are old but small', async () => {
    // old_small_file.txt is old but not large enough
    const bunnies = await findDustBunnies('/mock/root', defaultAge, defaultSize);
    assert.ok(!bunnies.some(b => b.path === '/mock/root/old_small_file.txt'), 'Should not include old_small_file.txt');
  });

  it('should return no dust bunnies if files are large but new', async () => {
    // new_large_file.txt is large but not old enough
    const bunnies = await findDustBunnies('/mock/root', defaultAge, defaultSize);
    assert.ok(!bunnies.some(b => b.path === '/mock/root/new_large_file.txt'), 'Should not include new_large_file.txt');
  });

  it('should handle non-existent directory gracefully (via main function error handling)', async () => {
    // Mock rationale: Test CLI argument parsing and error handling for invalid directory paths.
    const originalArgv = process.argv;
    const originalConsoleError = console.error;
    const originalProcessExit = process.exit;
    let errorMessage = '';
    let exitCode = 0;

    process.argv = ['node', 'src/index.js', '/mock/nonexistent'];
    console.error = (msg) => { errorMessage += msg + '\n'; };
    process.exit = (code) => { exitCode = code; throw new Error('ProcessExit'); }; // Throw to stop execution

    try {
      await main();
    } catch (e) {
      if (e.message !== 'ProcessExit') throw e;
    }

    assert.strictEqual(exitCode, 1, 'Should exit with code 1 for non-existent directory');
    assert.ok(errorMessage.includes('Error: Directory \'/mock/nonexistent\' not found or inaccessible'), 'Should log an error message');

    // Restore originals
    process.argv = originalArgv;
    console.error = originalConsoleError;
    process.exit = originalProcessExit;
  });

  it('should handle directory path being a file gracefully (via main function error handling)', async () => {
    // Mock rationale: Test CLI argument parsing and error handling when the provided path is a file, not a directory.
    const originalArgv = process.argv;
    const originalConsoleError = console.error;
    const originalProcessExit = process.exit;
    let errorMessage = '';
    let exitCode = 0;

    process.argv = ['node', 'src/index.js', '/mock/root_is_file'];
    console.error = (msg) => { errorMessage += msg + '\n'; };
    process.exit = (code) => { exitCode = code; throw new Error('ProcessExit'); };

    try {
      await main();
    } catch (e) {
      if (e.message !== 'ProcessExit') throw e;
    }

    assert.strictEqual(exitCode, 1, 'Should exit with code 1 for directory path being a file');
    assert.ok(errorMessage.includes('Error: \'/mock/root_is_file\' is not a directory.'), 'Should log an error message for file as directory');

    // Restore originals
    process.argv = originalArgv;
    console.error = originalConsoleError;
    process.exit = originalProcessExit;
  });

  it('should handle invalid age/size arguments gracefully (via main function error handling)', async () => {
    // Mock rationale: Test CLI argument parsing and error handling for non-numeric or invalid age/size thresholds.
    const originalArgv = process.argv;
    const originalConsoleError = console.error;
    const originalProcessExit = process.exit;
    let errorMessage = '';
    let exitCode = 0;

    process.argv = ['node', 'src/index.js', '/mock/root', '--age', 'invalid'];
    console.error = (msg) => { errorMessage += msg + '\n'; };
    process.exit = (code) => { exitCode = code; throw new Error('ProcessExit'); };

    try {
      await main();
    } catch (e) {
      if (e.message !== 'ProcessExit') throw e;
    }

    assert.strictEqual(exitCode, 1, 'Should exit with code 1 for invalid age argument');
    assert.ok(errorMessage.includes('Error: --age must be a positive number.'), 'Should log an error message for invalid age');

    errorMessage = '';
    exitCode = 0;
    process.argv = ['node', 'src/index.js', '/mock/root', '--size', 'invalid'];
    try {
      await main();
    } catch (e) {
      if (e.message !== 'ProcessExit') throw e;
    }
    assert.strictEqual(exitCode, 1, 'Should exit with code 1 for invalid size argument');
    assert.ok(errorMessage.includes('Error: --size must be a positive number.'), 'Should log an error message for invalid size');

    // Restore originals
    process.argv = originalArgv;
    console.error = originalConsoleError;
    process.exit = originalProcessExit;
  });

  // Restore original fs.promises after all tests
  after(() => {
    require('fs').promises = originalFs;
  });
});
