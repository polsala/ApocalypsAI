const assert = require('assert');
const path = require('path');
const { runSweeper, getFileAgeInDays, scanDirectory } = require('../src/dust-bunny-sweeper');
const fs = require('fs');

// # Mock rationale: We need to simulate a file system with specific file ages
// # and structures without actually creating files on disk. This ensures tests
// # are deterministic, fast, and don't rely on external file system state.
const originalReaddirSync = fs.readdirSync;
const originalStatSync = fs.statSync;
const originalExistsSync = fs.existsSync;
const originalConsoleLog = console.log;

let mockFs = {}; // Structure: { 'path/to/file': { isDirectory: boolean, mtime: Date, size: number } }

function mockReaddirSync(dirPath, options) {
    const entries = [];
    for (const p in mockFs) {
        // Check if 'p' is a direct child of 'dirPath'
        if (path.dirname(p) === dirPath && p !== dirPath) {
            const base = path.basename(p);
            entries.push({
                name: base,
                isDirectory: () => mockFs[p].isDirectory,
                isFile: () => !mockFs[p].isDirectory
            });
        }
    }
    return entries;
}

function mockStatSync(filePath) {
    if (mockFs[filePath]) {
        return {
            isDirectory: () => mockFs[filePath].isDirectory,
            isFile: () => !mockFs[filePath].isDirectory,
            mtime: mockFs[filePath].mtime,
            size: mockFs[filePath].size || 0
        };
    }
    throw new Error(`ENOENT: no such file or directory, stat '${filePath}'`);
}

function mockExistsSync(filePath) {
    return !!mockFs[filePath];
}

function setupMockFs(structure) {
    mockFs = {};
    for (const p in structure) {
        mockFs[p] = structure[p];
    }
    fs.readdirSync = mockReaddirSync;
    fs.statSync = mockStatSync;
    fs.existsSync = mockExistsSync;
}

function restoreFs() {
    fs.readdirSync = originalReaddirSync;
    fs.statSync = originalStatSync;
    fs.existsSync = originalExistsSync;
    mockFs = {};
}

let consoleOutput = [];
function mockConsoleLog(...args) {
    consoleOutput.push(args.join(' '));
}

// Simple test runner for Node.js
function describe(name, fn) {
    console.log(`\n${name}`);
    fn();
}

function it(name, fn) {
    try {
        fn();
        console.log(`  ✓ ${name}`);
    } catch (error) {
        console.error(`  ✗ ${name}`);
        console.error(error);
        process.exit(1); // Exit with error on first failure
    }
}

describe('Digital Dust Bunny Sweeper', () => {
    beforeEach(() => {
        consoleOutput = [];
        console.log = mockConsoleLog;
    });

    afterEach(() => {
        restoreFs();
        console.log = originalConsoleLog;
    });

    it('should correctly calculate file age in days', () => {
        // # Mock rationale: We need to control the file modification time
        // # to ensure age calculation is deterministic.
        const mockFilePath = '/mock/file.txt';
        const now = new Date();
        const twoDaysAgo = new Date(now.getTime() - (2 * 24 * 60 * 60 * 1000));
        setupMockFs({
            [mockFilePath]: { isDirectory: false, mtime: twoDaysAgo, size: 100 }
        });
        const age = getFileAgeInDays(mockFilePath);
        assert.strictEqual(age, 2, 'File age should be 2 days');
    });

    it('should find no files if directory is empty', () => {
        // # Mock rationale: Simulate an empty directory to test edge cases.
        const now = new Date();
        setupMockFs({
            '/empty_dir': { isDirectory: true, mtime: now, size: 0 }
        });
        const findings = scanDirectory('/empty_dir', 90);
        assert.strictEqual(findings.length, 0, 'Should find no files in an empty directory');
    });

    it('should find no files if all are recent', () => {
        // # Mock rationale: Simulate a directory with only recent files.
        const now = new Date();
        const oneDayAgo = new Date(now.getTime() - (1 * 24 * 60 * 60 * 1000));
        setupMockFs({
            '/recent_dir': { isDirectory: true, mtime: now, size: 0 },
            '/recent_dir/file1.txt': { isDirectory: false, mtime: oneDayAgo, size: 100 },
            '/recent_dir/file2.js': { isDirectory: false, mtime: oneDayAgo, size: 200 }
        });
        const findings = scanDirectory('/recent_dir', 90);
        assert.strictEqual(findings.length, 0, 'Should find no files if all are recent');
    });

    it('should find old files and categorize them correctly', () => {
        // # Mock rationale: Simulate a directory with files of various ages
        // # to test age-based categorization.
        const now = new Date();
        const ninetyDaysAgo = new Date(now.getTime() - (90 * 24 * 60 * 60 * 1000));
        const oneHundredDaysAgo = new Date(now.getTime() - (100 * 24 * 60 * 60 * 1000));
        const twoHundredDaysAgo = new Date(now.getTime() - (200 * 24 * 60 * 60 * 1000));
        const fourHundredDaysAgo = new Date(now.getTime() - (400 * 24 * 60 * 60 * 1000));

        setupMockFs({
            '/project': { isDirectory: true, mtime: now, size: 0 },
            '/project/src': { isDirectory: true, mtime: now, size: 0 },
            '/project/src/recent.js': { isDirectory: false, mtime: ninetyDaysAgo, size: 50 }, // Exactly 90 days, should be included
            '/project/old_config.json': { isDirectory: false, mtime: oneHundredDaysAgo, size: 150 },
            '/project/docs': { isDirectory: true, mtime: now, size: 0 },
            '/project/docs/ancient_report.pdf': { isDirectory: false, mtime: fourHundredDaysAgo, size: 1024 },
            '/project/node_modules': { isDirectory: true, mtime: now, size: 0 },
            '/project/node_modules/dep.js': { isDirectory: false, mtime: twoHundredDaysAgo, size: 300 }
        });

        const findings = scanDirectory('/project', 90);
        assert.strictEqual(findings.length, 4, 'Should find 4 old files');

        const oldConfig = findings.find(f => f.path === '/project/old_config.json');
        assert.ok(oldConfig, 'old_config.json should be found');
        assert.strictEqual(oldConfig.category, 'Digital Dust Bunny', 'old_config.json category incorrect');
        assert.strictEqual(oldConfig.age, 100, 'old_config.json age incorrect');

        const ancientReport = findings.find(f => f.path === '/project/docs/ancient_report.pdf');
        assert.ok(ancientReport, 'ancient_report.pdf should be found');
        assert.strictEqual(ancientReport.category, 'Ancient Relic', 'ancient_report.pdf category incorrect');
        assert.strictEqual(ancientReport.age, 400, 'ancient_report.pdf age incorrect');

        const depJs = findings.find(f => f.path === '/project/node_modules/dep.js');
        assert.ok(depJs, 'dep.js should be found');
        assert.strictEqual(depJs.category, 'Forgotten Scroll', 'dep.js category incorrect');
        assert.strictEqual(depJs.age, 200, 'dep.js age incorrect');

        const recentJs = findings.find(f => f.path === '/project/src/recent.js');
        assert.ok(recentJs, 'recent.js should be found');
        assert.strictEqual(recentJs.category, 'Digital Dust Bunny', 'recent.js category incorrect');
        assert.strictEqual(recentJs.age, 90, 'recent.js age incorrect');
    });

    it('should throw error if target path does not exist', () => {
        // # Mock rationale: Simulate a non-existent path to test error handling.
        setupMockFs({}); // Empty mock FS
        assert.throws(() => runSweeper('/nonexistent', 90), /Path not found/, 'Should throw error for nonexistent path');
    });

    it('should throw error if target path is a file, not a directory', () => {
        // # Mock rationale: Simulate a file being passed as the target path.
        const now = new Date();
        setupMockFs({
            '/a_file.txt': { isDirectory: false, mtime: now, size: 10 }
        });
        assert.throws(() => runSweeper('/a_file.txt', 90), /Target path must be a directory/, 'Should throw error for file path');
    });

    it('should print "All clear" message when no dust bunnies are found', () => {
        // # Mock rationale: Verify the output message for a clean directory.
        const now = new Date();
        const oneDayAgo = new Date(now.getTime() - (1 * 24 * 60 * 60 * 1000));
        setupMockFs({
            '/clean_dir': { isDirectory: true, mtime: now, size: 0 },
            '/clean_dir/new_file.txt': { isDirectory: false, mtime: oneDayAgo, size: 100 }
        });
        runSweeper('/clean_dir', 90);
        assert.ok(consoleOutput.some(line => line.includes('All clear! No digital dust bunnies found.')), 'Should log "All clear" message');
    });

    it('should print findings when dust bunnies are found', () => {
        // # Mock rationale: Verify the output message when old files are detected.
        const now = new Date();
        const oneHundredDaysAgo = new Date(now.getTime() - (100 * 24 * 60 * 60 * 1000));
        setupMockFs({
            '/dusty_dir': { isDirectory: true, mtime: now, size: 0 },
            '/dusty_dir/old_file.txt': { isDirectory: false, mtime: oneHundredDaysAgo, size: 250 }
        });
        runSweeper('/dusty_dir', 90);
        assert.ok(consoleOutput.some(line => line.includes('Found the following digital dust bunnies:')), 'Should log findings header');
        assert.ok(consoleOutput.some(line => line.includes('[Digital Dust Bunny] /dusty_dir/old_file.txt (Age: 100 days, Size: 250 bytes)')), 'Should log details of old file');
        assert.ok(consoleOutput.some(line => line.includes('Total 1 digital dust bunnies detected.')), 'Should log total count');
    });
});
