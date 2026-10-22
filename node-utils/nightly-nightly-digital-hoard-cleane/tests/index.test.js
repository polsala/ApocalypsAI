const assert = require('assert');
const { cleanHoard, getFilesOlderThan } = require('../src/index');
const fs = require('fs').promises;
const path = require('path');

// Mock fs.promises
const mockFs = {
    readdir: async (dirPath, options) => { /* Mock rationale: Simulate directory contents */ },
    stat: async (filePath) => { /* Mock rationale: Simulate file stats (mtime, isFile/isDirectory) */ },
    unlink: async (filePath) => { /* Mock rationale: Simulate file deletion */ },
    rename: async (oldPath, newPath) => { /* Mock rationale: Simulate file movement */ },
    mkdir: async (dirPath, options) => { /* Mock rationale: Simulate directory creation */ }
};

// Replace actual fs.promises with mockFs for testing
Object.assign(fs, mockFs);

// Helper to create mock stat objects
const createMockStat = (mtime, isFile = true, isDirectory = false) => ({
    mtime: new Date(mtime),
    isFile: () => isFile,
    isDirectory: () => isDirectory,
});

// Helper to capture console output
let consoleOutput = [];
const originalConsoleLog = console.log;
const originalConsoleError = console.error;
const originalConsoleWarn = console.warn;

function startCapture() {
    consoleOutput = [];
    console.log = (...args) => consoleOutput.push(args.join(' '));
    console.error = (...args) => consoleOutput.push(args.join(' '));
    console.warn = (...args) => consoleOutput.push(args.join(' '));
}

function stopCapture() {
    console.log = originalConsoleLog;
    console.error = originalConsoleError;
    console.warn = originalConsoleWarn;
}

async function runTest(name, testFn) {
    startCapture();
    try {
        await testFn();
        originalConsoleLog(`✅ ${name}`);
    } catch (error) {
        originalConsoleError(`❌ ${name}`);
        originalConsoleError(error);
        originalConsoleError('Captured Output:\n', consoleOutput.join('\n'));
        process.exit(1); // Exit on first failure
    } finally {
        stopCapture();
    }
}

// --- Tests ---

runTest('should find old files in a directory (non-recursive)', async () => {
    const testDir = '/mock/test/dir';
    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - 30); // 30 days ago

    fs.readdir = async (dirPath, options) => {
        assert.strictEqual(dirPath, testDir);
        return [
            { name: 'old_file.txt', isFile: () => true, isDirectory: () => false },
            { name: 'new_file.txt', isFile: () => true, isDirectory: () => false },
            { name: 'subdir', isFile: () => false, isDirectory: () => true },
        ];
    }; // Mock rationale: Simulate directory contents with old, new, and subdirectory entries.
    fs.stat = async (filePath) => {
        if (filePath === path.join(testDir, 'old_file.txt')) {
            return createMockStat(new Date(cutoffDate.getTime() - 86400000)); // 1 day older
        }
        if (filePath === path.join(testDir, 'new_file.txt')) {
            return createMockStat(new Date()); // Today
        }
        if (filePath === path.join(testDir, 'subdir')) {
            return createMockStat(new Date(), false, true);
        }
        throw new Error('File not found in mock stat');
    }; // Mock rationale: Simulate file stats for different files, including modification times.

    const oldFiles = await getFilesOlderThan(testDir, 30, false);
    assert.strictEqual(oldFiles.length, 1, 'Should find exactly one old file');
    assert.strictEqual(oldFiles[0].path, path.join(testDir, 'old_file.txt'), 'Should identify the correct old file');
});

runTest('should find old files recursively', async () => {
    const testDir = '/mock/test/dir';
    const subDir = path.join(testDir, 'subdir');
    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - 30);

    fs.readdir = async (dirPath, options) => {
        if (dirPath === testDir) {
            return [
                { name: 'old_root_file.txt', isFile: () => true, isDirectory: () => false },
                { name: 'subdir', isFile: () => false, isDirectory: () => true },
            ];
        }
        if (dirPath === subDir) {
            return [
                { name: 'old_sub_file.txt', isFile: () => true, isDirectory: () => false },
                { name: 'new_sub_file.txt', isFile: () => true, isDirectory: () => false },
            ];
        }
        return [];
    }; // Mock rationale: Simulate nested directory structure with old and new files.
    fs.stat = async (filePath) => {
        if (filePath === path.join(testDir, 'old_root_file.txt')) {
            return createMockStat(new Date(cutoffDate.getTime() - 86400000));
        }
        if (filePath === path.join(testDir, 'subdir')) {
            return createMockStat(new Date(), false, true);
        }
        if (filePath === path.join(subDir, 'old_sub_file.txt')) {
            return createMockStat(new Date(cutoffDate.getTime() - 86400000));
        }
        if (filePath === path.join(subDir, 'new_sub_file.txt')) {
            return createMockStat(new Date());
        }
        throw new Error('File not found in mock stat');
    }; // Mock rationale: Simulate file stats for files in root and subdirectories.

    const oldFiles = await getFilesOlderThan(testDir, 30, true);
    assert.strictEqual(oldFiles.length, 2, 'Should find two old files recursively');
    const paths = oldFiles.map(f => f.path).sort();
    assert.deepStrictEqual(paths, [
        path.join(testDir, 'old_root_file.txt'),
        path.join(subDir, 'old_sub_file.txt'),
    ].sort(), 'Should identify correct old files recursively');
});

runTest('should perform a dry run and not delete/move files', async () => {
    const testDir = '/mock/test/dir';
    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - 30);

    fs.readdir = async () => [{ name: 'old_file.txt', isFile: () => true, isDirectory: () => false }]; // Mock rationale: Simulate a directory with one old file.
    fs.stat = async () => createMockStat(new Date(cutoffDate.getTime() - 86400000)); // Mock rationale: Simulate the old file's stats.
    fs.unlink = async () => { throw new Error('Unlink should not be called in dry run'); }; // Mock rationale: Ensure unlink is not called.
    fs.rename = async () => { throw new Error('Rename should not be called in dry run'); }; // Mock rationale: Ensure rename is not called.

    const result = await cleanHoard(testDir, 30, true, null);
    assert.strictEqual(result.cleaned, 0, 'No files should be cleaned in dry run');
    assert.strictEqual(result.skipped, 1, 'One file should be skipped in dry run');
    assert(consoleOutput.some(line => line.includes('Dry run complete')), 'Should indicate dry run completion');
});

runTest('should delete old files when no compost directory is specified', async () => {
    const testDir = '/mock/test/dir';
    const oldFilePath = path.join(testDir, 'old_file_to_delete.txt');
    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - 30);

    fs.readdir = async () => [{ name: 'old_file_to_delete.txt', isFile: () => true, isDirectory: () => false }]; // Mock rationale: Simulate a directory with one old file.
    fs.stat = async () => createMockStat(new Date(cutoffDate.getTime() - 86400000)); // Mock rationale: Simulate the old file's stats.

    let unlinkCalled = false;
    fs.unlink = async (filePath) => {
        assert.strictEqual(filePath, oldFilePath, 'Unlink should be called with the correct file path');
        unlinkCalled = true;
    }; // Mock rationale: Capture unlink call to verify deletion.
    fs.rename = async () => { throw new Error('Rename should not be called for deletion'); }; // Mock rationale: Ensure rename is not called.

    const result = await cleanHoard(testDir, 30, false, null);
    assert.strictEqual(result.cleaned, 1, 'One file should be deleted');
    assert.strictEqual(unlinkCalled, true, 'fs.unlink should have been called');
    assert(consoleOutput.some(line => line.includes('Deleted')), 'Should log deletion');
});

runTest('should move old files to compost directory', async () => {
    const testDir = '/mock/test/dir';
    const compostDir = '/mock/compost';
    const oldFilePath = path.join(testDir, 'old_file_to_compost.txt');
    const compostFilePath = path.join(compostDir, 'old_file_to_compost.txt');
    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - 30);

    fs.readdir = async () => [{ name: 'old_file_to_compost.txt', isFile: () => true, isDirectory: () => false }]; // Mock rationale: Simulate a directory with one old file.
    fs.stat = async () => createMockStat(new Date(cutoffDate.getTime() - 86400000)); // Mock rationale: Simulate the old file's stats.

    let renameCalled = false;
    fs.rename = async (oldPath, newPath) => {
        assert.strictEqual(oldPath, oldFilePath, 'Rename old path mismatch');
        assert.strictEqual(newPath, compostFilePath, 'Rename new path mismatch');
        renameCalled = true;
    }; // Mock rationale: Capture rename call to verify movement.
    fs.mkdir = async (dirPath, options) => {
        assert.strictEqual(dirPath, compostDir, 'mkdir should be called for compost dir');
        assert.deepStrictEqual(options, { recursive: true }, 'mkdir should be recursive');
    }; // Mock rationale: Capture mkdir call to verify compost directory creation.
    fs.unlink = async () => { throw new Error('Unlink should not be called for composting'); }; // Mock rationale: Ensure unlink is not called.

    const result = await cleanHoard(testDir, 30, false, compostDir);
    assert.strictEqual(result.cleaned, 1, 'One file should be composted');
    assert.strictEqual(renameCalled, true, 'fs.rename should have been called');
    assert(consoleOutput.some(line => line.includes('Moved')), 'Should log movement to compost');
});

runTest('should handle errors during file processing', async () => {
    const testDir = '/mock/test/dir';
    const oldFilePath = path.join(testDir, 'unreachable_file.txt');
    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - 30);

    fs.readdir = async () => [{ name: 'unreachable_file.txt', isFile: () => true, isDirectory: () => false }]; // Mock rationale: Simulate a directory with one old file.
    fs.stat = async () => createMockStat(new Date(cutoffDate.getTime() - 86400000)); // Mock rationale: Simulate the old file's stats.
    fs.unlink = async () => { throw new Error('Permission denied'); }; // Mock rationale: Simulate a permission denied error during unlink.

    const result = await cleanHoard(testDir, 30, false, null);
    assert.strictEqual(result.cleaned, 0, 'No files should be cleaned due to error');
    assert.strictEqual(result.errors, 1, 'One error should be reported');
    assert(consoleOutput.some(line => line.includes('Failed to process')), 'Should log processing failure');
});

runTest('should return empty array if directory does not exist for getFilesOlderThan', async () => {
    const testDir = '/mock/nonexistent/dir';
    fs.readdir = async () => { throw new Error('ENOENT: no such file or directory'); }; // Mock rationale: Simulate a non-existent directory.

    const oldFiles = await getFilesOlderThan(testDir, 30, false);
    assert.deepStrictEqual(oldFiles, [], 'Should return empty array for nonexistent directory');
    assert(consoleOutput.some(line => line.includes('Error accessing directory')), 'Should log directory access error');
});

runTest('should report no files found if directory is empty', async () => {
    const testDir = '/mock/empty/dir';
    fs.readdir = async () => []; // Mock rationale: Simulate an empty directory.
    fs.stat = async () => { throw new Error('Should not be called'); }; // Mock rationale: Ensure stat is not called on an empty directory.

    const result = await cleanHoard(testDir, 30, false, null);
    assert.strictEqual(result.cleaned, 0, 'No files should be cleaned');
    assert.strictEqual(result.skipped, 0, 'No files should be skipped');
    assert.strictEqual(result.errors, 0, 'No errors should occur');
    assert(consoleOutput.some(line => line.includes('No digital dust bunnies found')), 'Should log no files found');
});

runTest('should handle stat errors gracefully during scan', async () => {
    const testDir = '/mock/test/dir';
    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - 30);

    fs.readdir = async () => [
        { name: 'good_file.txt', isFile: () => true, isDirectory: () => false },
        { name: 'bad_file.txt', isFile: () => true, isDirectory: () => false },
    ]; // Mock rationale: Simulate a directory with one good file and one problematic file.
    fs.stat = async (filePath) => {
        if (filePath.includes('good_file.txt')) {
            return createMockStat(new Date(cutoffDate.getTime() - 86400000));
        }
        if (filePath.includes('bad_file.txt')) {
            throw new Error('EACCES: Permission denied'); // Mock rationale: Simulate a stat error for a specific file.
        }
        throw new Error('File not found in mock stat');
    }; // Mock rationale: Simulate stat results, including an error for 'bad_file.txt'.

    const oldFiles = await getFilesOlderThan(testDir, 30, false);
    assert.strictEqual(oldFiles.length, 1, 'Should find only the good file');
    assert.strictEqual(oldFiles[0].path, path.join(testDir, 'good_file.txt'), 'Should identify the correct old file');
    // No console.warn for stat errors, as per current implementation (silent skip)
});
