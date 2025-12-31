const path = require('path');
const { run, scanDirectory, loadState, saveState, compareStates, generateReport } = require('../src/index');

// # Mock rationale: We are replacing the actual Node.js 'fs' module
// with a controlled in-memory version to ensure deterministic tests
// without touching the real file system. This allows simulating
// various file system states (new, modified, deleted files, no state file)
// and verifying the utility's behavior and output.
const mockFs = {
    _files: new Map(), // Map<filePath, {content: string, stats: {mtimeMs: number, size: number}}>
    _dirs: new Map(),  // Map<dirPath, string[]> (list of entry names)
    _writtenFiles: new Map(), // Map<filePath, string> (content written)

    reset() {
        this._files.clear();
        this._dirs.clear();
        this._writtenFiles.clear();
    },

    addFile(filePath, content, mtimeMs, size) {
        this._files.set(filePath, { content, stats: { mtimeMs, size } });
        const dir = path.dirname(filePath);
        if (!this._dirs.has(dir)) this._dirs.set(dir, []);
        const dirEntries = this._dirs.get(dir);
        if (!dirEntries.includes(path.basename(filePath))) {
            dirEntries.push(path.basename(filePath));
        }
    },

    addDir(dirPath) {
        if (!this._dirs.has(dirPath)) this._dirs.set(dirPath, []);
    },

    readdirSync(dirPath, options) {
        if (this._dirs.has(dirPath)) {
            const entries = this._dirs.get(dirPath);
            if (options && options.withFileTypes) {
                return entries.map(name => {
                    const fullPath = path.join(dirPath, name);
                    const isDirectory = this._dirs.has(fullPath);
                    const isFile = this._files.has(fullPath);
                    return {
                        name: name,
                        isDirectory: () => isDirectory,
                        isFile: () => isFile
                    };
                });
            }
            return entries;
        }
        throw Object.assign(new Error(`ENOENT: no such file or directory, scandir '${dirPath}'`), { code: 'ENOENT' });
    },

    statSync(filePath) {
        if (this._files.has(filePath)) {
            return {
                isDirectory: () => false,
                isFile: () => true,
                mtimeMs: this._files.get(filePath).stats.mtimeMs,
                size: this._files.get(filePath).stats.size
            };
        }
        if (this._dirs.has(filePath)) {
            return {
                isDirectory: () => true,
                isFile: () => false,
                mtimeMs: 0, // Not relevant for dirs in this util
                size: 0
            };
        }
        throw Object.assign(new Error(`ENOENT: no such file or directory, stat '${filePath}'`), { code: 'ENOENT' });
    },

    readFileSync(filePath, encoding) {
        if (this._files.has(filePath)) {
            return this._files.get(filePath).content;
        }
        throw Object.assign(new Error(`ENOENT: no such file or directory, open '${filePath}'`), { code: 'ENOENT' });
    },

    writeFileSync(filePath, data, encoding) {
        this._writtenFiles.set(filePath, data);
    },

    existsSync(filePath) {
        return this._files.has(filePath) || this._dirs.has(filePath);
    }
};

// Simple assertion functions
function assert(condition, message) {
    if (!condition) {
        throw new Error(`Assertion Failed: ${message}`);
    }
}

function assertEquals(actual, expected, message) {
    assert(actual === expected, `${message} Expected: ${expected}, Actual: ${actual}`);
}

function assertDeepEquals(actual, expected, message) {
    assert(JSON.stringify(actual) === JSON.stringify(expected), `${message} Expected: ${JSON.stringify(expected)}, Actual: ${JSON.stringify(actual)}`);
}

function assertContains(array, item, message) {
    assert(array.includes(item), `${message} Array does not contain: ${item}`);
}

function assertNotContains(array, item, message) {
    assert(!array.includes(item), `${message} Array unexpectedly contains: ${item}`);
}

function test(name, fn) {
    try {
        fn();
        console.log(`✅ ${name}`);
    } catch (error) {
        console.error(`❌ ${name}`);
        console.error(error);
        process.exit(1);
    }
}

// Mock console.log to capture output
let consoleOutput = [];
const originalConsoleLog = console.log;
const originalConsoleWarn = console.warn;
const originalConsoleError = console.error;

function mockConsole() {
    consoleOutput = [];
    console.log = (...args) => consoleOutput.push(args.join(' '));
    console.warn = (...args) => consoleOutput.push(args.join(' '));
    console.error = (...args) => consoleOutput.push(args.join(' '));
}

function restoreConsole() {
    console.log = originalConsoleLog;
    console.warn = originalConsoleWarn;
    console.error = originalConsoleError;
}

// --- Test Cases ---

test('scanDirectory correctly identifies files and directories', () => {
    mockFs.reset();
    mockFs.addDir('/garden');
    mockFs.addFile('/garden/file1.txt', 'content1', 1000, 10);
    mockFs.addDir('/garden/sub');
    mockFs.addFile('/garden/sub/file2.js', 'content2', 2000, 20);

    const result = scanDirectory('/garden', mockFs);

    assertEquals(result.size, 2, 'Should find 2 files');
    assert(result.has('file1.txt'), 'Should contain file1.txt');
    assert(result.has(path.join('sub', 'file2.js')), 'Should contain sub/file2.js');
    assertDeepEquals(result.get('file1.txt'), { mtimeMs: 1000, size: 10 }, 'file1.txt stats should match');
});

test('loadState returns empty map if state file does not exist', () => {
    mockFs.reset();
    const state = loadState('/garden/.garden_state.json', mockFs);
    assertEquals(state.size, 0, 'State should be empty');
});

test('loadState correctly loads existing state', () => {
    mockFs.reset();
    const stateContent = JSON.stringify([
        { path: 'fileA.txt', mtimeMs: 100, size: 5 },
        { path: 'fileB.js', mtimeMs: 200, size: 10 }
    ]);
    mockFs.addFile('/garden/.garden_state.json', stateContent, 50, stateContent.length);

    const state = loadState('/garden/.garden_state.json', mockFs);
    assertEquals(state.size, 2, 'State should have 2 entries');
    assert(state.has('fileA.txt'), 'State should contain fileA.txt');
    assertDeepEquals(state.get('fileA.txt'), { mtimeMs: 100, size: 5 }, 'fileA.txt stats should match');
});

test('saveState correctly writes current state', () => {
    mockFs.reset();
    const currentState = new Map([
        ['fileC.txt', { mtimeMs: 300, size: 15 }]
    ]);
    saveState(currentState, '/garden/.garden_state.json', mockFs);

    const writtenContent = mockFs._writtenFiles.get('/garden/.garden_state.json');
    assert(writtenContent, 'State file should have been written');
    const parsed = JSON.parse(writtenContent);
    assertEquals(parsed.length, 1, 'Written state should have 1 entry');
    assertEquals(parsed[0].path, 'fileC.txt', 'Written state path should match');
});

test('compareStates identifies new files', () => {
    const previous = new Map();
    const current = new Map([
        ['new_file.txt', { mtimeMs: 100, size: 10 }]
    ]);
    const changes = compareStates(previous, current);
    assertEquals(changes.newFiles.length, 1, 'Should have 1 new file');
    assertContains(changes.newFiles, 'new_file.txt', 'new_file.txt should be in new files');
    assertEquals(changes.modifiedFiles.length, 0, 'Should have 0 modified files');
    assertEquals(changes.deletedFiles.length, 0, 'Should have 0 deleted files');
});

test('compareStates identifies modified files', () => {
    const previous = new Map([
        ['existing.txt', { mtimeMs: 100, size: 10 }]
    ]);
    const current = new Map([
        ['existing.txt', { mtimeMs: 101, size: 10 }] // mtimeMs changed
    ]);
    const changes = compareStates(previous, current);
    assertEquals(changes.newFiles.length, 0, 'Should have 0 new files');
    assertEquals(changes.modifiedFiles.length, 1, 'Should have 1 modified file');
    assertContains(changes.modifiedFiles, 'existing.txt', 'existing.txt should be in modified files');
    assertEquals(changes.deletedFiles.length, 0, 'Should have 0 deleted files');
});

test('compareStates identifies deleted files', () => {
    const previous = new Map([
        ['old_file.txt', { mtimeMs: 100, size: 10 }]
    ]);
    const current = new Map();
    const changes = compareStates(previous, current);
    assertEquals(changes.newFiles.length, 0, 'Should have 0 new files');
    assertEquals(changes.modifiedFiles.length, 0, 'Should have 0 modified files');
    assertEquals(changes.deletedFiles.length, 1, 'Should have 1 deleted file');
    assertContains(changes.deletedFiles, 'old_file.txt', 'old_file.txt should be in deleted files');
});

test('compareStates identifies no changes', () => {
    const previous = new Map([
        ['stable.txt', { mtimeMs: 100, size: 10 }]
    ]);
    const current = new Map([
        ['stable.txt', { mtimeMs: 100, size: 10 }]
    ]);
    const changes = compareStates(previous, current);
    assertEquals(changes.newFiles.length, 0, 'Should have 0 new files');
    assertEquals(changes.modifiedFiles.length, 0, 'Should have 0 modified files');
    assertEquals(changes.deletedFiles.length, 0, 'Should have 0 deleted files');
});

test('generateReport prints correct output for all change types', () => {
    mockConsole();
    const changes = {
        newFiles: ['file_a.md'],
        modifiedFiles: ['file_b.js'],
        deletedFiles: ['file_c.txt']
    };
    generateReport(changes);
    restoreConsole();

    const output = consoleOutput.join('\n');
    assert(output.includes('🌱 New Sprouts (Freshly Planted):'), 'Output should mention new sprouts');
    assert(output.includes('  - file_a.md'), 'Output should list new file_a.md');
    assert(output.includes('🌼 Blooming Beauties (Flourishing & Changed):'), 'Output should mention blooming beauties');
    assert(output.includes('  - file_b.js'), 'Output should list modified file_b.js');
    assert(output.includes('🍂 Wilted Wonders (Faded Away):'), 'Output should mention wilted wonders');
    assert(output.includes('  - file_c.txt'), 'Output should list deleted file_c.txt');
});

test('generateReport prints correct output for no changes', () => {
    mockConsole();
    const changes = {
        newFiles: [],
        modifiedFiles: [],
        deletedFiles: []
    };
    generateReport(changes);
    restoreConsole();

    const output = consoleOutput.join('\n');
    assert(output.includes('✨ Quiet Corners (No Major Changes Detected). The garden rests peacefully.'), 'Output should mention quiet corners');
    assert(!output.includes('🌱 New Sprouts'), 'Output should not mention new sprouts');
});

test('run function handles first execution (no state file)', () => {
    mockFs.reset();
    const targetDir = '/garden';
    mockFs.addDir(targetDir);
    mockFs.addFile(path.join(targetDir, 'initial.txt'), 'hello', 100, 5);

    mockConsole();
    run(targetDir, mockFs);
    restoreConsole();

    const output = consoleOutput.join('\n');
    assert(output.includes('🌱 New Sprouts (Freshly Planted):'), 'First run should report initial files as new sprouts');
    assert(output.includes('  - initial.txt'), 'initial.txt should be listed as new');

    const stateFileContent = mockFs._writtenFiles.get(path.join(targetDir, '.garden_state.json'));
    assert(stateFileContent, 'State file should be created');
    const parsedState = JSON.parse(stateFileContent);
    assertEquals(parsedState.length, 1, 'State file should contain 1 entry');
    assertEquals(parsedState[0].path, 'initial.txt', 'State file should record initial.txt');
});

test('run function handles subsequent execution with changes', () => {
    mockFs.reset();
    const targetDir = '/garden';
    mockFs.addDir(targetDir);

    // Simulate initial state
    const initialStateContent = JSON.stringify([
        { path: 'existing.txt', mtimeMs: 100, size: 10 },
        { path: 'to_modify.txt', mtimeMs: 200, size: 20 }
    ]);
    mockFs.addFile(path.join(targetDir, '.garden_state.json'), initialStateContent, 50, initialStateContent.length);
    mockFs.addFile(path.join(targetDir, 'existing.txt'), 'content', 100, 10);
    mockFs.addFile(path.join(targetDir, 'to_modify.txt'), 'old content', 200, 20);

    // Simulate changes for the next run
    mockFs.addFile(path.join(targetDir, 'new_file.md'), 'new content', 300, 15); // New
    mockFs.addFile(path.join(targetDir, 'to_modify.txt'), 'updated content', 201, 25); // Modified
    // 'existing.txt' remains unchanged
    // A file that was in state but not present now will be deleted

    mockConsole();
    run(targetDir, mockFs);
    restoreConsole();

    const output = consoleOutput.join('\n');
    assert(output.includes('🌱 New Sprouts (Freshly Planted):'), 'Output should report new sprouts');
    assert(output.includes('  - new_file.md'), 'new_file.md should be listed as new');
    assert(output.includes('🌼 Blooming Beauties (Flourishing & Changed):'), 'Output should report modified files');
    assert(output.includes('  - to_modify.txt'), 'to_modify.txt should be listed as modified');
    assert(output.includes('🍂 Wilted Wonders (Faded Away):'), 'Output should report deleted files');
    assert(output.includes('  - existing.txt'), 'existing.txt should be listed as deleted (because it was in previous state but not in current mockFs)');

    const newStateFileContent = mockFs._writtenFiles.get(path.join(targetDir, '.garden_state.json'));
    assert(newStateFileContent, 'State file should be updated');
    const parsedNewState = JSON.parse(newStateFileContent);
    assertEquals(parsedNewState.length, 2, 'New state file should contain 2 entries (new_file.md, to_modify.txt)');
    assertContains(parsedNewState.map(f => f.path), 'new_file.md', 'New state should record new_file.md');
    assertContains(parsedNewState.map(f => f.path), 'to_modify.txt', 'New state should record to_modify.txt');
    assertNotContains(parsedNewState.map(f => f.path), 'existing.txt', 'New state should not record existing.txt');
});

test('run function handles execution with no changes', () => {
    mockFs.reset();
    const targetDir = '/garden';
    mockFs.addDir(targetDir);

    // Simulate initial state
    const initialStateContent = JSON.stringify([
        { path: 'stable.txt', mtimeMs: 100, size: 10 }
    ]);
    mockFs.addFile(path.join(targetDir, '.garden_state.json'), initialStateContent, 50, initialStateContent.length);
    mockFs.addFile(path.join(targetDir, 'stable.txt'), 'content', 100, 10);

    mockConsole();
    run(targetDir, mockFs);
    restoreConsole();

    const output = consoleOutput.join('\n');
    assert(output.includes('✨ Quiet Corners (No Major Changes Detected). The garden rests peacefully.'), 'Output should indicate no changes');
    assert(!output.includes('🌱 New Sprouts'), 'Output should not mention new sprouts');
    assert(!output.includes('🌼 Blooming Beauties'), 'Output should not mention modified files');
    assert(!output.includes('🍂 Wilted Wonders'), 'Output should not mention deleted files');

    const newStateFileContent = mockFs._writtenFiles.get(path.join(targetDir, '.garden_state.json'));
    assert(newStateFileContent, 'State file should be updated');
    const parsedNewState = JSON.parse(newStateFileContent);
    assertEquals(parsedNewState.length, 1, 'New state file should contain 1 entry');
    assertEquals(parsedNewState[0].path, 'stable.txt', 'New state should record stable.txt');
});

console.log('\nAll tests passed!\n');
