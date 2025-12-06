const assert = require('assert');
const path = require('path');
const { scanDirectory, loadState, saveState, generateReport, run } = require('../src/main');

// # Mock rationale: fs operations are non-deterministic and involve I/O.
// Mocks ensure tests are deterministic, offline, and fast.
const mockFs = {
    _files: {}, // { 'path/to/file': { isFile: true, isDirectory: false, size: N, mtimeMs: M } }
    _content: {}, // { 'path/to/file': 'file content' }
    _exists: {}, // { 'path/to/file': true/false }

    reset() {
        this._files = {};
        this._content = {};
        this._exists = {};
    },

    // Helper to add a file or directory to the mock file system
    addEntry(fullPath, type, size = 0, mtimeMs = Date.now(), content = '') {
        this._exists[fullPath] = true;
        if (type === 'file') {
            this._files[fullPath] = {
                isFile: () => true,
                isDirectory: () => false,
                size: size,
                mtimeMs: mtimeMs
            };
            this._content[fullPath] = content;
        } else if (type === 'directory') {
            this._files[fullPath] = {
                isFile: () => false,
                isDirectory: () => true,
                size: 0, // Directories don't have size in stat
                mtimeMs: mtimeMs
            };
        }
    },

    existsSync(p) {
        return this._exists[p] || false;
    },

    readdirSync(p, options) {
        if (!this.existsSync(p) || !this._files[p] || !this._files[p].isDirectory()) {
            // Simulate ENOENT for non-existent or non-directory paths
            const error = new Error(`ENOENT: no such file or directory, scandir '${p}'`);
            error.code = 'ENOENT';
            throw error;
        }
        const entries = [];
        for (const fullPath in this._files) {
            if (path.dirname(fullPath) === p) {
                const name = path.basename(fullPath);
                entries.push({
                    name: name,
                    isFile: this._files[fullPath].isFile,
                    isDirectory: this._files[fullPath].isDirectory
                });
            }
        }
        return entries;
    },

    statSync(p) {
        if (!this.existsSync(p)) {
            // Simulate ENOENT for non-existent paths
            const error = new Error(`ENOENT: no such file or directory, stat '${p}'`);
            error.code = 'ENOENT';
            throw error;
        }
        return this._files[p];
    },

    readFileSync(p, encoding) {
        if (!this.existsSync(p) || !this._files[p].isFile()) {
            // Simulate ENOENT for non-existent or non-file paths
            const error = new Error(`ENOENT: no such file or directory, open '${p}'`);
            error.code = 'ENOENT';
            throw error;
        }
        return this._content[p];
    },

    writeFileSync(p, data, encoding) {
        this.addEntry(p, 'file', data.length, Date.now(), data);
    },

    mkdirSync(p, options) {
        this.addEntry(p, 'directory');
    }
};

// Replace actual fs with mockFs
const originalFs = { ...fs };
Object.keys(mockFs).forEach(key => {
    if (typeof mockFs[key] === 'function') {
        fs[key] = mockFs[key].bind(mockFs);
    }
});

console.log('Running tests for Data Echo Collector...');

function runTest(name, testFunction) {
    mockFs.reset(); // Reset mock FS before each test
    console.log(`  Running: ${name}`);
    try {
        testFunction();
        console.log(`  ✅ ${name} PASSED`);
    } catch (error) {
        console.error(`  ❌ ${name} FAILED:`, error.message);
        console.error(error.stack);
        process.exit(1); // Exit on first failure
    }
}

// --- Test Cases ---

runTest('scanDirectory should correctly scan files and subdirectories', () => {
    mockFs.addEntry('/monitored', 'directory');
    mockFs.addEntry('/monitored/dir1', 'directory');
    mockFs.addEntry('/monitored/dir1/fileA.txt', 'file', 100, 1000);
    mockFs.addEntry('/monitored/dir1/subdir', 'directory');
    mockFs.addEntry('/monitored/dir1/subdir/fileB.log', 'file', 200, 2000);
    mockFs.addEntry('/monitored/dir2', 'directory');
    mockFs.addEntry('/monitored/dir2/fileC.json', 'file', 300, 3000);

    const result = scanDirectory('/monitored');
    assert.deepStrictEqual(result, {
        '/monitored/dir1/fileA.txt': { size: 100, mtimeMs: 1000 },
        '/monitored/dir1/subdir/fileB.log': { size: 200, mtimeMs: 2000 },
        '/monitored/dir2/fileC.json': { size: 300, mtimeMs: 3000 }
    });
});

runTest('loadState should load existing state or return empty object', () => {
    const stateContent = JSON.stringify({
        '/data/file1.txt': { size: 50, mtimeMs: 1000 }
    });
    mockFs.addEntry('/output/echo_state.json', 'file', stateContent.length, Date.now(), stateContent);

    const state = loadState('/output/echo_state.json');
    assert.deepStrictEqual(state, {
        '/data/file1.txt': { size: 50, mtimeMs: 1000 }
    });

    mockFs.reset(); // Clear state for next part
    const emptyState = loadState('/output/non_existent_state.json');
    assert.deepStrictEqual(emptyState, {});
});

runTest('saveState should correctly write state to a file', () => {
    const currentState = {
        '/data/file2.txt': { size: 150, mtimeMs: 2000 }
    };
    const stateFilePath = '/output/echo_state.json';
    saveState(stateFilePath, currentState);

    const savedContent = mockFs.readFileSync(stateFilePath, 'utf8');
    assert.deepStrictEqual(JSON.parse(savedContent), currentState);
});

runTest('generateReport should identify new, modified, and deleted files', () => {
    const previousState = {
        '/data/file1.txt': { size: 100, mtimeMs: 1000 },
        '/data/file2.txt': { size: 200, mtimeMs: 2000 },
        '/data/file3.txt': { size: 300, mtimeMs: 3000 } // Will be deleted
    };
    const currentState = {
        '/data/file1.txt': { size: 100, mtimeMs: 1000 }, // Unchanged
        '/data/file2.txt': { size: 250, mtimeMs: 2500 }, // Modified size and mtime
        '/data/file4.txt': { size: 400, mtimeMs: 4000 }  // New file
    };

    const report = generateReport(previousState, currentState);
    assert.ok(report.includes('[NEW] /data/file4.txt (Size: 400 bytes)'));
    assert.ok(report.includes('[MODIFIED] /data/file2.txt (Old Size: 200, New Size: 250)'));
    assert.ok(report.includes('[DELETED] /data/file3.txt'));
    assert.ok(report.includes('New Files: 1'));
    assert.ok(report.includes('Modified Files: 1'));
    assert.ok(report.includes('Deleted Files: 1'));
    assert.ok(!report.includes('/data/file1.txt')); // Unchanged file should not be in report details
});

runTest('run function should correctly execute the full workflow', () => {
    const outputDir = '/output';
    const monitorDir = '/monitor';
    const stateFilePath = path.join(outputDir, 'echo_state.json');
    const reportFilePath = path.join(outputDir, 'echo_report.txt');

    // --- First run: Initial state, all files are new ---
    mockFs.addEntry(outputDir, 'directory');
    mockFs.addEntry(monitorDir, 'directory');
    mockFs.addEntry(path.join(monitorDir, 'initial.txt'), 'file', 10, 1000);

    run([monitorDir], outputDir);

    let reportContent = mockFs.readFileSync(reportFilePath, 'utf8');
    let stateContent = JSON.parse(mockFs.readFileSync(stateFilePath, 'utf8'));

    assert.ok(reportContent.includes('[NEW] /monitor/initial.txt (Size: 10 bytes)'));
    assert.ok(reportContent.includes('New Files: 1'));
    assert.ok(reportContent.includes('Modified Files: 0'));
    assert.ok(reportContent.includes('Deleted Files: 0'));
    assert.deepStrictEqual(stateContent, {
        '/monitor/initial.txt': { size: 10, mtimeMs: 1000 }
    });

    // --- Second run: File modified, new file added, old file deleted ---
    mockFs.reset(); // Clear mock FS for a fresh state for the *current* scan
    mockFs.addEntry(outputDir, 'directory'); // Re-create output dir
    // Manually set the previous state file content for the second run
    mockFs.addEntry(stateFilePath, 'file', JSON.stringify({
        '/monitor/file_to_delete.txt': { size: 50, mtimeMs: 5000 },
        '/monitor/file_to_modify.txt': { size: 60, mtimeMs: 6000 },
        '/monitor/initial.txt': { size: 10, mtimeMs: 1000 } // From previous run
    }).length, Date.now(), JSON.stringify({
        '/monitor/file_to_delete.txt': { size: 50, mtimeMs: 5000 },
        '/monitor/file_to_modify.txt': { size: 60, mtimeMs: 6000 },
        '/monitor/initial.txt': { size: 10, mtimeMs: 1000 }
    }));

    mockFs.addEntry(monitorDir, 'directory');
    mockFs.addEntry(path.join(monitorDir, 'file_to_modify.txt'), 'file', 65, 6500); // Modified
    mockFs.addEntry(path.join(monitorDir, 'new_file.txt'), 'file', 70, 7000); // New
    // 'file_to_delete.txt' is intentionally not added to the current mock FS, simulating deletion
    // 'initial.txt' is also not added, simulating its deletion or absence in the current scan

    run([monitorDir], outputDir);

    reportContent = mockFs.readFileSync(reportFilePath, 'utf8');
    stateContent = JSON.parse(mockFs.readFileSync(stateFilePath, 'utf8'));

    assert.ok(reportContent.includes('[DELETED] /monitor/file_to_delete.txt'));
    assert.ok(reportContent.includes('[DELETED] /monitor/initial.txt'));
    assert.ok(reportContent.includes('[MODIFIED] /monitor/file_to_modify.txt (Old Size: 60, New Size: 65)'));
    assert.ok(reportContent.includes('[NEW] /monitor/new_file.txt (Size: 70 bytes)'));
    assert.ok(reportContent.includes('New Files: 1'));
    assert.ok(reportContent.includes('Modified Files: 1'));
    assert.ok(reportContent.includes('Deleted Files: 2'));

    // Verify the new state reflects the current file system
    assert.deepStrictEqual(stateContent, {
        '/monitor/file_to_modify.txt': { size: 65, mtimeMs: 6500 },
        '/monitor/new_file.txt': { size: 70, mtimeMs: 7000 }
    });
});

console.log('\nAll tests passed!');

// Restore original fs (optional, but good practice if other modules might use it)
Object.keys(originalFs).forEach(key => {
    fs[key] = originalFs[key];
});
