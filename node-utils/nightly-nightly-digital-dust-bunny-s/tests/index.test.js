const assert = require('assert');
const { test, mock } = require('node:test');
const { findDigitalDustBunnies, getFilesAndDirs, isDirectoryEmpty } = require('../src/index');
const path = require('path');

// Mock rationale: We need to simulate a file system without actually creating/deleting files
// on the disk, making tests deterministic and offline.
const mockFs = {
    '/mock_root': {
        'old_file.txt': {
            isFile: true,
            isDirectory: false,
            mtimeMs: Date.now() - (366 * 24 * 60 * 60 * 1000) // Older than 1 year
        },
        'recent_file.txt': {
            isFile: true,
            isDirectory: false,
            mtimeMs: Date.now() - (10 * 24 * 60 * 60 * 1000) // Newer than 1 year
        },
        'empty_dir': {
            isFile: false,
            isDirectory: true,
            content: {}
        },
        'non_empty_dir': {
            isFile: false,
            isDirectory: true,
            content: {
                'sub_file.log': {
                    isFile: true,
                    isDirectory: false,
                    mtimeMs: Date.now() - (400 * 24 * 60 * 60 * 1000)
                }
            }
        },
        'nested_empty_dir': {
            isFile: false,
            isDirectory: true,
            content: {
                'another_empty': {
                    isFile: false,
                    isDirectory: true,
                    content: {}
                }
            }
        },
        'permission_denied_dir': {
            isFile: false,
            isDirectory: true,
            content: {},
            accessError: 'EACCES'
        },
        'non_existent_dir': {
            isFile: false,
            isDirectory: true,
            content: {},
            accessError: 'ENOENT'
        }
    }
};

// Recursive mock readdirSync
function mockReaddirSync(currentPath, options) {
    let current = mockFs;
    const parts = currentPath.split(path.sep).filter(p => p !== '');
    for (const part of parts) {
        if (!current[part]) {
            const error = new Error(`ENOENT: no such file or directory, scandir '${currentPath}'`);
            error.code = 'ENOENT';
            throw error;
        }
        current = current[part].content || current[part];
    }

    if (current.accessError) {
        const error = new Error(`EACCES: permission denied, scandir '${currentPath}'`);
        error.code = current.accessError;
        throw error;
    }

    const entries = Object.keys(current).map(name => {
        const entry = current[name];
        return {
            name: name,
            isFile: () => entry.isFile,
            isDirectory: () => entry.isDirectory
        };
    });
    return entries;
}

// Recursive mock statSync
function mockStatSync(filePath) {
    let current = mockFs;
    const parts = filePath.split(path.sep).filter(p => p !== '');
    let foundEntry = null;

    for (let i = 0; i < parts.length; i++) {
        const part = parts[i];
        if (!current[part]) {
            const error = new Error(`ENOENT: no such file or directory, stat '${filePath}'`);
            error.code = 'ENOENT';
            throw error;
        }
        foundEntry = current[part];
        if (i < parts.length - 1) {
            current = current[part].content || current[part];
        }
    }

    if (foundEntry.accessError) {
        const error = new Error(`EACCES: permission denied, stat '${filePath}'`);
        error.code = foundEntry.accessError;
        throw error;
    }

    return {
        isFile: () => foundEntry.isFile,
        isDirectory: () => foundEntry.isDirectory,
        mtimeMs: foundEntry.mtimeMs || Date.now() // Default mtimeMs if not specified
    };
}

// Mock fs module
mock.module('fs', {
    readdirSync: mockReaddirSync,
    statSync: mockStatSync
});

test('getFilesAndDirs should correctly list files and directories', () => {
    const { files, dirs } = getFilesAndDirs('/mock_root');
    assert.strictEqual(files.length, 3, 'Should find 3 files');
    assert.ok(files.includes('/mock_root/old_file.txt'), 'Should include old_file.txt');
    assert.ok(files.includes('/mock_root/recent_file.txt'), 'Should include recent_file.txt');
    assert.ok(files.includes('/mock_root/non_empty_dir/sub_file.log'), 'Should include sub_file.log');
    assert.strictEqual(dirs.length, 4, 'Should find 4 directories');
    assert.ok(dirs.includes('/mock_root/empty_dir'), 'Should include empty_dir');
    assert.ok(dirs.includes('/mock_root/non_empty_dir'), 'Should include non_empty_dir');
    assert.ok(dirs.includes('/mock_root/nested_empty_dir'), 'Should include nested_empty_dir');
    assert.ok(dirs.includes('/mock_root/nested_empty_dir/another_empty'), 'Should include nested_empty_dir/another_empty');
});

test('isDirectoryEmpty should correctly identify empty and non-empty directories', () => {
    assert.strictEqual(isDirectoryEmpty('/mock_root/empty_dir'), true, 'empty_dir should be empty');
    assert.strictEqual(isDirectoryEmpty('/mock_root/non_empty_dir'), false, 'non_empty_dir should not be empty');
    assert.strictEqual(isDirectoryEmpty('/mock_root/nested_empty_dir/another_empty'), true, 'nested_empty_dir/another_empty should be empty');
    assert.strictEqual(isDirectoryEmpty('/mock_root/non_existent_dir'), false, 'non_existent_dir should be treated as not empty due to error handling');
});

test('findDigitalDustBunnies should identify stale files and empty directories', () => {
    const { staleFiles, emptyDirs } = findDigitalDustBunnies('/mock_root', 365); // 1 year threshold

    assert.strictEqual(staleFiles.length, 2, 'Should find 2 stale files');
    assert.ok(staleFiles.some(f => f.path === '/mock_root/old_file.txt'), 'Should include old_file.txt as stale');
    assert.ok(staleFiles.some(f => f.path === '/mock_root/non_empty_dir/sub_file.log'), 'Should include sub_file.log as stale');
    assert.strictEqual(emptyDirs.length, 2, 'Should find 2 empty directories');
    assert.ok(emptyDirs.includes('/mock_root/empty_dir'), 'Should include empty_dir');
    assert.ok(emptyDirs.includes('/mock_root/nested_empty_dir/another_empty'), 'Should include nested_empty_dir/another_empty');
});

test('findDigitalDustBunnies should handle permission denied directories gracefully', () => {
    const { staleFiles, emptyDirs } = findDigitalDustBunnies('/mock_root/permission_denied_dir', 365);
    assert.strictEqual(staleFiles.length, 0, 'Should find no stale files in permission denied dir');
    assert.strictEqual(emptyDirs.length, 0, 'Should find no empty dirs in permission denied dir (due to error handling)');
});

test('findDigitalDustBunnies should handle non-existent directories gracefully', () => {
    const { staleFiles, emptyDirs } = findDigitalDustBunnies('/mock_root/non_existent_dir', 365);
    assert.strictEqual(staleFiles.length, 0, 'Should find no stale files in non-existent dir');
    assert.strictEqual(emptyDirs.length, 0, 'Should find no empty dirs in non-existent dir');
});

test('findDigitalDustBunnies with a shorter threshold', () => {
    const { staleFiles, emptyDirs } = findDigitalDustBunnies('/mock_root', 5); // 5 days threshold
    assert.strictEqual(staleFiles.length, 3, 'Should find 3 stale files with 5-day threshold');
    assert.ok(staleFiles.some(f => f.path === '/mock_root/old_file.txt'), 'old_file.txt should be stale');
    assert.ok(staleFiles.some(f => f.path === '/mock_root/recent_file.txt'), 'recent_file.txt should be stale');
    assert.ok(staleFiles.some(f => f.path === '/mock_root/non_empty_dir/sub_file.log'), 'sub_file.log should be stale');
    assert.strictEqual(emptyDirs.length, 2, 'Should find 2 empty directories');
});
