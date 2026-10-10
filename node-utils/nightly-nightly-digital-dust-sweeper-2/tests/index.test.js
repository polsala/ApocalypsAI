const assert = require('assert');
const path = require('path');

// Mock fs module
const mockFs = {
    _files: {}, // Stores file paths and their stats
    _dirs: new Set(), // Stores directory paths

    // # Mock rationale: Simulates fs.readdirSync to control directory contents for testing.
    readdirSync: function(dirPath, options) {
        if (!this._dirs.has(dirPath) && dirPath !== '/') { // '/' is root, always exists
            throw new Error(`ENOENT: no such file or directory, scandir '${dirPath}'`);
        }
        const entries = [];
        for (const filePath in this._files) {
            if (path.dirname(filePath) === dirPath) {
                const fileName = path.basename(filePath);
                entries.push({
                    name: fileName,
                    isDirectory: () => this._files[filePath].isDirectory
                });
            }
        }
        // Add mock directories as entries if they are direct children
        for (const dir of this._dirs) {
            if (path.dirname(dir) === dirPath && dir !== dirPath) {
                entries.push({
                    name: path.basename(dir),
                    isDirectory: () => true
                });
            }
        }
        return entries;
    },

    // # Mock rationale: Simulates fs.statSync to control file modification times and type for testing.
    statSync: function(filePath) {
        if (this._files[filePath]) {
            return {
                mtime: this._files[filePath].mtime,
                isDirectory: () => this._files[filePath].isDirectory
            };
        }
        if (this._dirs.has(filePath)) {
            return {
                mtime: new Date(), // Directories don't need specific mtime for this util
                isDirectory: () => true
            };
        }
        throw new Error(`ENOENT: no such file or directory, stat '${filePath}'`);
    },

    // # Mock rationale: Simulates fs.mkdirSync to track created directories without actual disk writes.
    mkdirSync: function(dirPath, options) {
        this._dirs.add(dirPath);
    },

    // # Mock rationale: Simulates fs.renameSync to track file moves without actual disk writes.
    renameSync: function(oldPath, newPath) {
        if (!this._files[oldPath]) {
            throw new Error(`ENOENT: no such file or directory, rename '${oldPath}'`);
        }
        this._files[newPath] = this._files[oldPath];
        delete this._files[oldPath];
    },

    // Helper to set up mock files/directories
    _setup: function(files, dirs) {
        this._files = {};
        this._dirs = new Set();
        for (const filePath in files) {
            this._files[filePath] = files[filePath];
            this._dirs.add(path.dirname(filePath)); // Ensure parent dir exists
        }
        for (const dirPath of dirs) {
            this._dirs.add(dirPath);
        }
    },

    // Helper to reset mock state
    _reset: function() {
        this._files = {};
        this._dirs = new Set();
    }
};

// Import the utility functions, passing the mock fs
const { scanDirectory, moveFile, suggestAction, getFileAgeInDays } = require('../src/index').createDustSweeper(mockFs);

console.log('Running tests for Nightly Digital Dust Sweeper...');

// Test Case 1: getFileAgeInDays
(function testGetFileAgeInDays() {
    mockFs._reset();
    const now = Date.now();
    const oneDay = 24 * 60 * 60 * 1000;

    mockFs._setup({
        '/test/file1.txt': { mtime: new Date(now - 5 * oneDay), isDirectory: false },
        '/test/file2.txt': { mtime: new Date(now - 0.5 * oneDay), isDirectory: false },
        '/test/file3.txt': { mtime: new Date(now - 30 * oneDay), isDirectory: false }
    }, ['/test']);

    assert.strictEqual(getFileAgeInDays('/test/file1.txt'), 5, 'Test Case 1.1 Failed: Correct age for 5 days old');
    assert.strictEqual(getFileAgeInDays('/test/file2.txt'), 1, 'Test Case 1.2 Failed: Correct age for less than 1 day old (rounds up)');
    assert.strictEqual(getFileAgeInDays('/test/file3.txt'), 30, 'Test Case 1.3 Failed: Correct age for 30 days old');
    assert.strictEqual(getFileAgeInDays('/test/nonexistent.txt'), -1, 'Test Case 1.4 Failed: Non-existent file should return -1');
    console.log('Test Case 1: getFileAgeInDays passed.');
})();

// Test Case 2: scanDirectory - no recursive
(function testScanDirectoryNoRecursive() {
    mockFs._reset();
    const now = Date.now();
    const oneDay = 24 * 60 * 60 * 1000;

    mockFs._setup({
        '/root/old_file.txt': { mtime: new Date(now - 40 * oneDay), isDirectory: false },
        '/root/new_file.txt': { mtime: new Date(now - 5 * oneDay), isDirectory: false },
        '/root/subdir/another_old.log': { mtime: new Date(now - 60 * oneDay), isDirectory: false }
    }, ['/root', '/root/subdir']);

    const dustyFiles = scanDirectory('/root', 30, false);
    assert.strictEqual(dustyFiles.length, 1, 'Test Case 2.1 Failed: Should find 1 dusty file');
    assert.strictEqual(dustyFiles[0].path, '/root/old_file.txt', 'Test Case 2.2 Failed: Should find old_file.txt');
    assert.strictEqual(dustyFiles[0].age, 40, 'Test Case 2.3 Failed: Correct age for old_file.txt');
    console.log('Test Case 2: scanDirectory (no recursive) passed.');
})();

// Test Case 3: scanDirectory - recursive
(function testScanDirectoryRecursive() {
    mockFs._reset();
    const now = Date.now();
    const oneDay = 24 * 60 * 60 * 1000;

    mockFs._setup({
        '/root/old_file.txt': { mtime: new Date(now - 40 * oneDay), isDirectory: false },
        '/root/new_file.txt': { mtime: new Date(now - 5 * oneDay), isDirectory: false },
        '/root/subdir/another_old.log': { mtime: new Date(now - 60 * oneDay), isDirectory: false },
        '/root/subdir/new_log.log': { mtime: new Date(now - 10 * oneDay), isDirectory: false }
    }, ['/root', '/root/subdir', '/root/empty_dir']);

    const dustyFiles = scanDirectory('/root', 30, true);
    assert.strictEqual(dustyFiles.length, 2, 'Test Case 3.1 Failed: Should find 2 dusty files recursively');
    const paths = dustyFiles.map(f => f.path).sort();
    assert.deepStrictEqual(paths, ['/root/old_file.txt', '/root/subdir/another_old.log'].sort(), 'Test Case 3.2 Failed: Correct dusty files found');
    console.log('Test Case 3: scanDirectory (recursive) passed.');
})();

// Test Case 4: moveFile
(function testMoveFile() {
    mockFs._reset();
    const now = Date.now();
    const oneDay = 24 * 60 * 60 * 1000;

    mockFs._setup({
        '/source/file_to_move.txt': { mtime: new Date(now - 50 * oneDay), isDirectory: false }
    }, ['/source']);

    const atticPath = '/digital_attic';
    const result = moveFile('/source/file_to_move.txt', atticPath);

    assert.ok(result.includes('Moved'), 'Test Case 4.1 Failed: Should indicate successful move');
    assert.ok(mockFs._dirs.has(atticPath), 'Test Case 4.2 Failed: Attic directory should be created');
    assert.ok(mockFs._files['/digital_attic/file_to_move.txt'], 'Test Case 4.3 Failed: File should be in attic');
    assert.strictEqual(mockFs._files['/source/file_to_move.txt'], undefined, 'Test Case 4.4 Failed: Original file should be gone');
    console.log('Test Case 4: moveFile passed.');
})();

// Test Case 5: suggestAction
(function testSuggestAction() {
    const suggestion = suggestAction('/path/to/some_file.txt');
    assert.ok(typeof suggestion === 'string' && suggestion.length > 0, 'Test Case 5.1 Failed: Suggestion should be a non-empty string');
    assert.ok(suggestion.includes('/path/to/some_file.txt'), 'Test Case 5.2 Failed: Suggestion should include the file path');
    console.log('Test Case 5: suggestAction passed.');
})();

console.log('\nAll tests completed.');
