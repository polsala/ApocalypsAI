const assert = require('assert');
const path = require('path');
const { getFilesOlderThan } = require('../src/main');

// --- Mock fs module for deterministic, offline testing ---
const mockFs = {
    _files: {}, // { 'path/to/file': { isFile: true, mtimeMs: timestamp } }
    _exists: {}, // { 'path/to/dir': true }
    _deleted: [],

    existsSync: function(p) {
        // Mock rationale: Simulate directory existence without actual file system interaction.
        return this._exists[p] || false;
    },
    readdirSync: function(dirPath) {
        // Mock rationale: Simulate reading directory contents without actual file system interaction.
        const filesInDir = Object.keys(this._files)
            .filter(filePath => path.dirname(filePath) === dirPath)
            .map(filePath => path.basename(filePath));
        return filesInDir;
    },
    statSync: function(filePath) {
        // Mock rationale: Simulate file stats (like modification time) without actual file system interaction.
        if (this._files[filePath]) {
            return {
                isFile: () => this._files[filePath].isFile,
                mtimeMs: this._files[filePath].mtimeMs
            };
        }
        throw new Error(`File not found: ${filePath}`);
    },
    unlinkSync: function(filePath) {
        // Mock rationale: Simulate file deletion without actual file system interaction.
        if (this._files[filePath]) {
            delete this._files[filePath];
            this._deleted.push(filePath);
        } else {
            throw new Error(`File not found for deletion: ${filePath}`);
        }
    },
    reset: function() {
        this._files = {};
        this._exists = {};
        this._deleted = [];
    },
    addFile: function(filePath, mtimeMs, isFile = true) {
        this._files[filePath] = { isFile, mtimeMs };
        this._exists[path.dirname(filePath)] = true; // Ensure parent directory exists for readdirSync
    },
    addDirectory: function(dirPath) {
        this._exists[dirPath] = true;
    }
};

// Replace the actual fs module with our mock for testing
// This is a direct overwrite for simplicity in a self-contained utility.
// In a larger project, a dedicated test runner (e.g., Jest) or dependency injection would be preferred.
const originalFs = require('fs');
Object.assign(require('fs'), mockFs);

console.log('Running tests for Nightly Data-Dust Sweeper...');

function runTest(name, testFunction) {
    mockFs.reset(); // Reset mocks before each test
    try {
        testFunction();
        console.log(`✅ ${name}`);
    } catch (error) {
        console.error(`❌ ${name}`);
        console.error(error);
        process.exit(1);
    }
}

runTest('should identify old files in dry run mode', () => {
    const testDir = '/mock/data-cache';
    const now = Date.now();
    const oneDayMs = 24 * 60 * 60 * 1000;

    mockFs.addDirectory(testDir);
    mockFs.addFile(path.join(testDir, 'old_log.txt'), now - (5 * oneDayMs)); // 5 days old
    mockFs.addFile(path.join(testDir, 'recent_report.pdf'), now - (0.5 * oneDayMs)); // 0.5 days old
    mockFs.addFile(path.join(testDir, 'ancient_data.bak'), now - (10 * oneDayMs)); // 10 days old

    const oldFiles = getFilesOlderThan(testDir, 3, true); // Look for files older than 3 days

    assert.strictEqual(oldFiles.length, 2, 'Should find 2 old files');
    assert.ok(oldFiles.some(f => f.path.includes('old_log.txt')), 'Should include old_log.txt');
    assert.ok(oldFiles.some(f => f.path.includes('ancient_data.bak')), 'Should include ancient_data.bak');
    assert.ok(!oldFiles.some(f => f.path.includes('recent_report.pdf')), 'Should not include recent_report.pdf');
    assert.strictEqual(mockFs._deleted.length, 0, 'No files should be deleted in dry run');
});

runTest('should delete old files in sweep mode', () => {
    const testDir = '/mock/data-cache';
    const now = Date.now();
    const oneDayMs = 24 * 60 * 60 * 1000;

    mockFs.addDirectory(testDir);
    mockFs.addFile(path.join(testDir, 'old_temp.tmp'), now - (7 * oneDayMs)); // 7 days old
    mockFs.addFile(path.join(testDir, 'keep_me.txt'), now - (1 * oneDayMs)); // 1 day old
    const fileToDelete = path.join(testDir, 'another_old.log');
    mockFs.addFile(fileToDelete, now - (4 * oneDayMs)); // 4 days old

    getFilesOlderThan(testDir, 3, false); // Look for files older than 3 days and sweep

    assert.strictEqual(mockFs._deleted.length, 2, 'Should delete 2 files');
    assert.ok(mockFs._deleted.includes(path.join(testDir, 'old_temp.tmp')), 'old_temp.tmp should be deleted');
    assert.ok(mockFs._deleted.includes(fileToDelete), 'another_old.log should be deleted');
    assert.ok(!mockFs._files[path.join(testDir, 'old_temp.tmp')], 'old_temp.tmp should no longer exist in mock fs');
    assert.ok(mockFs._files[path.join(testDir, 'keep_me.txt')], 'keep_me.txt should still exist');
});

runTest('should handle non-existent directory gracefully', () => {
    const testDir = '/mock/non-existent-cache';
    const oldFiles = getFilesOlderThan(testDir, 10, true);
    assert.strictEqual(oldFiles.length, 0, 'Should return empty array for non-existent directory');
    assert.strictEqual(mockFs._deleted.length, 0, 'No files should be deleted');
});

runTest('should not delete files newer than threshold', () => {
    const testDir = '/mock/fresh-cache';
    const now = Date.now();
    const oneDayMs = 24 * 60 * 60 * 1000;

    mockFs.addDirectory(testDir);
    mockFs.addFile(path.join(testDir, 'new_file.txt'), now - (0.5 * oneDayMs));
    mockFs.addFile(path.join(testDir, 'another_new.log'), now - (1 * oneDayMs));

    getFilesOlderThan(testDir, 2, false); // Sweep files older than 2 days

    assert.strictEqual(mockFs._deleted.length, 0, 'No files should be deleted as all are new');
    assert.ok(mockFs._files[path.join(testDir, 'new_file.txt')], 'new_file.txt should still exist');
});

console.log('\nAll tests completed.');

// Restore original fs module (optional, but good practice if other parts of the system rely on it)
Object.assign(require('fs'), originalFs);
