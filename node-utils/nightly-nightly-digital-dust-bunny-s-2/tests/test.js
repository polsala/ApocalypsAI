const { test, mock } = require('node:test');
const assert = require('node:assert');
const { findDustBunnies } = require('../src/index.js');
const path = require('node:path');

// Mock rationale: To ensure deterministic and offline testing,
// file system operations (readdirSync, statSync) are mocked.
// This prevents actual disk I/O and makes tests fast and reliable.

test('findDustBunnies identifies old files', (t) => {
    const now = Date.now();
    const oneYearAgo = now - (366 * 24 * 60 * 60 * 1000); // More than 365 days
    const oneMonthAgo = now - (30 * 24 * 60 * 60 * 1000); // Less than 365 days

    mock.method(require('fs'), 'readdirSync', (dirPath, options) => {
        if (dirPath === '/mock/root') {
            return [
                { name: 'old_file.txt', isDirectory: () => false },
                { name: 'new_file.txt', isDirectory: () => false },
                { name: 'subdir', isDirectory: () => true }
            ];
        }
        if (dirPath === '/mock/root/subdir') {
            return [
                { name: 'another_old_file.log', isDirectory: () => false }
            ];
        }
        return [];
    });

    mock.method(require('fs'), 'statSync', (filePath) => {
        if (filePath === '/mock/root/old_file.txt') {
            return { isFile: () => true, isDirectory: () => false, mtimeMs: oneYearAgo };
        }
        if (filePath === '/mock/root/new_file.txt') {
            return { isFile: () => true, isDirectory: () => false, mtimeMs: oneMonthAgo };
        }
        if (filePath === '/mock/root/subdir') {
            return { isFile: () => false, isDirectory: () => true, mtimeMs: oneYearAgo }; // mtime for dir doesn't matter for this test
        }
        if (filePath === '/mock/root/subdir/another_old_file.log') {
            return { isFile: () => true, isDirectory: () => false, mtimeMs: oneYearAgo };
        }
        throw new Error(`File not found in mock: ${filePath}`);
    });

    const bunnies = findDustBunnies('/mock/root', 365);

    assert.strictEqual(bunnies.length, 2, 'Should find two old files');
    assert.ok(bunnies.some(b => b.path === '/mock/root/old_file.txt'), 'Should include old_file.txt');
    assert.ok(bunnies.some(b => b.path === '/mock/root/subdir/another_old_file.log'), 'Should include another_old_file.log');
    assert.ok(!bunnies.some(b => b.path === '/mock/root/new_file.txt'), 'Should not include new_file.txt');
});

test('findDustBunnies returns empty array for empty directory', (t) => {
    mock.method(require('fs'), 'readdirSync', (dirPath, options) => {
        if (dirPath === '/mock/empty') {
            return [];
        }
        return [];
    });
    mock.method(require('fs'), 'statSync', (filePath) => {
        throw new Error('Should not call statSync for empty dir');
    });

    const bunnies = findDustBunnies('/mock/empty', 30);
    assert.strictEqual(bunnies.length, 0, 'Should return an empty array for an empty directory');
});

test('findDustBunnies handles non-existent directory gracefully', (t) => {
    mock.method(require('fs'), 'readdirSync', (dirPath, options) => {
        if (dirPath === '/mock/nonexistent') {
            const error = new Error('ENOENT: no such file or directory, scandir \'/mock/nonexistent\'');
            error.code = 'ENOENT';
            throw error;
        }
        return [];
    });
    // Mock rationale: Suppress console.warn output from the utility during this specific test
    // to prevent test output pollution when a non-existent directory is handled.
    const originalWarn = console.warn;
    console.warn = () => {}; 

    const bunnies = findDustBunnies('/mock/nonexistent', 30);
    assert.strictEqual(bunnies.length, 0, 'Should return an empty array for a non-existent directory');

    console.warn = originalWarn; // Restore console.warn
});

test('findDustBunnies ignores directories themselves', (t) => {
    const now = Date.now();
    const oneYearAgo = now - (366 * 24 * 60 * 60 * 1000);

    mock.method(require('fs'), 'readdirSync', (dirPath, options) => {
        if (dirPath === '/mock/dir_only') {
            return [
                { name: 'old_dir', isDirectory: () => true }
            ];
        }
        return [];
    });

    mock.method(require('fs'), 'statSync', (filePath) => {
        if (filePath === '/mock/dir_only/old_dir') {
            return { isFile: () => false, isDirectory: () => true, mtimeMs: oneYearAgo };
        }
        throw new Error(`File not found in mock: ${filePath}`);
    });

    const bunnies = findDustBunnies('/mock/dir_only', 365);
    assert.strictEqual(bunnies.length, 0, 'Should not include directories as dust bunnies');
});

test('findDustBunnies handles files with stat errors gracefully', (t) => {
    const now = Date.now();
    const oneYearAgo = now - (366 * 24 * 60 * 60 * 1000);

    mock.method(require('fs'), 'readdirSync', (dirPath, options) => {
        if (dirPath === '/mock/error_dir') {
            return [
                { name: 'good_file.txt', isDirectory: () => false },
                { name: 'bad_file.txt', isDirectory: () => false }
            ];
        }
        return [];
    });

    mock.method(require('fs'), 'statSync', (filePath) => {
        if (filePath === '/mock/error_dir/good_file.txt') {
            return { isFile: () => true, isDirectory: () => false, mtimeMs: oneYearAgo };
        }
        if (filePath === '/mock/error_dir/bad_file.txt') {
            const error = new Error('EACCES: permission denied, stat \'/mock/error_dir/bad_file.txt\'');
            error.code = 'EACCES';
            throw error;
        }
        throw new Error(`File not found in mock: ${filePath}`);
    });

    // Mock rationale: Suppress console.warn output from the utility during this specific test
    // to prevent test output pollution when a file cannot be stat-ed.
    const originalWarn = console.warn;
    console.warn = () => {}; 

    const bunnies = findDustBunnies('/mock/error_dir', 365);
    assert.strictEqual(bunnies.length, 1, 'Should find only the good file');
    assert.ok(bunnies.some(b => b.path === '/mock/error_dir/good_file.txt'), 'Should include good_file.txt');
    assert.ok(!bunnies.some(b => b.path === '/mock/error_dir/bad_file.txt'), 'Should not include bad_file.txt');

    console.warn = originalWarn; // Restore console.warn
});
