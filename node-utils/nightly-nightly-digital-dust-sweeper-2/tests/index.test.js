const assert = require('assert');
const sinon = require('sinon');
const fs = require('fs').promises;
const path = require('path');
const { program } = require('commander'); // Import program to mock its help method
const chalk = require('chalk'); // Import chalk to disable its colors for testing

// Mock chalk to remove color codes from output for easier assertion
chalk.level = 0;

// Mock console.log and console.error to capture output
let consoleLogStub;
let consoleErrorStub;

// Helper to reset commander and capture output
function setupTest() {
    consoleLogStub = sinon.stub(console, 'log');
    consoleErrorStub = sinon.stub(console, 'error');
    // Reset commander's internal state for each test
    program.commands = [];
    program._optionValues = {};
    program._args = [];
    program._name = 'dust-sweeper'; // Reset name
    program._description = 'A whimsical utility to sweep away digital dust bunnies (old files).';
    program._version = '1.0.0';

    // Re-require the main script to re-initialize commander with fresh commands
    // This is a bit hacky but necessary to ensure commander is clean for each test
    delete require.cache[require.resolve('../src/index.js')];
    require('../src/index.js');
}

function teardownTest() {
    consoleLogStub.restore();
    consoleErrorStub.restore();
}

describe('Nightly Digital Dust Bunny Sweeper', () => {
    let readdirStub;
    let statStub;
    let mkdirStub;
    let renameStub;

    beforeEach(() => {
        setupTest();
        readdirStub = sinon.stub(fs, 'readdir');
        statStub = sinon.stub(fs, 'stat');
        mkdirStub = sinon.stub(fs, 'mkdir');
        renameStub = sinon.stub(fs, 'rename');
    });

    afterEach(() => {
        teardownTest();
        sinon.restore(); // Restore all stubs
    });

    // Mock rationale: We need to simulate file system interactions without actually touching the disk.
    // `fs.readdir` is mocked to control directory contents.
    // `fs.stat` is mocked to control file metadata like modification time.
    // `fs.mkdir` and `fs.rename` are mocked to prevent actual directory creation/file movement.

    it('should list old files correctly in scan mode', async () => {
        const testDir = '/test/scan_dir';
        const now = Date.now();
        const oldFileTime = new Date(now - 100 * 24 * 60 * 60 * 1000); // 100 days ago
        const newFileTime = new Date(now - 10 * 24 * 60 * 60 * 1000);  // 10 days ago

        readdirStub.withArgs(testDir, { withFileTypes: true }).returns(Promise.resolve([
            { name: 'old_file.txt', isFile: () => true, isDirectory: () => false },
            { name: 'new_file.txt', isFile: () => true, isDirectory: () => false },
            { name: 'subdir', isFile: () => false, isDirectory: () => true }
        ]));
        readdirStub.withArgs(path.join(testDir, 'subdir'), { withFileTypes: true }).returns(Promise.resolve([
            { name: 'another_old_file.log', isFile: () => true, isDirectory: () => false }
        ]));
        statStub.withArgs(path.join(testDir, 'old_file.txt')).returns(Promise.resolve({ mtime: oldFileTime }));
        statStub.withArgs(path.join(testDir, 'new_file.txt')).returns(Promise.resolve({ mtime: newFileTime }));
        statStub.withArgs(path.join(testDir, 'subdir', 'another_old_file.log')).returns(Promise.resolve({ mtime: oldFileTime }));

        await program.parseAsync(['node', 'src/index.js', 'scan', testDir, '--age', '90']);

        assert(consoleLogStub.calledWithMatch('Found 2 digital dust bunnies:'));
        assert(consoleLogStub.calledWithMatch(`- ${path.join(testDir, 'old_file.txt')} (Modified: ${oldFileTime.toLocaleDateString()}, Age: 100 days)`));
        assert(consoleLogStub.calledWithMatch(`- ${path.join(testDir, 'subdir', 'another_old_file.log')} (Modified: ${oldFileTime.toLocaleDateString()}, Age: 100 days)`));
        assert.strictEqual(consoleErrorStub.callCount, 0);
    });

    it('should not list new files in scan mode', async () => {
        const testDir = '/test/scan_dir_new';
        const now = Date.now();
        const newFileTime = new Date(now - 10 * 24 * 60 * 60 * 1000); // 10 days ago

        readdirStub.withArgs(testDir, { withFileTypes: true }).returns(Promise.resolve([
            { name: 'new_file.txt', isFile: () => true, isDirectory: () => false }
        ]));
        statStub.withArgs(path.join(testDir, 'new_file.txt')).returns(Promise.resolve({ mtime: newFileTime }));

        await program.parseAsync(['node', 'src/index.js', 'scan', testDir, '--age', '90']);

        assert(consoleLogStub.calledWithMatch('No digital dust bunnies found! Your directory is sparkling clean. \u2728'));
        assert.strictEqual(consoleErrorStub.callCount, 0);
    });

    it('should quarantine old files correctly', async () => {
        const sourceDir = '/test/source';
        const quarantineDir = '/test/quarantine';
        const now = Date.now();
        const oldFileTime = new Date(now - 100 * 24 * 60 * 60 * 1000); // 100 days ago

        readdirStub.withArgs(sourceDir, { withFileTypes: true }).returns(Promise.resolve([
            { name: 'old_document.pdf', isFile: () => true, isDirectory: () => false }
        ]));
        statStub.withArgs(path.join(sourceDir, 'old_document.pdf')).returns(Promise.resolve({ mtime: oldFileTime }));
        mkdirStub.withArgs(quarantineDir, { recursive: true }).returns(Promise.resolve());
        renameStub.withArgs(path.join(sourceDir, 'old_document.pdf'), path.join(quarantineDir, 'old_document.pdf')).returns(Promise.resolve());

        await program.parseAsync(['node', 'src/index.js', 'quarantine', sourceDir, '--age', '90', '--output', quarantineDir]);

        assert(mkdirStub.calledWith(quarantineDir, { recursive: true }));
        assert(renameStub.calledWith(path.join(sourceDir, 'old_document.pdf'), path.join(quarantineDir, 'old_document.pdf')));
        assert(consoleLogStub.calledWithMatch('Attempting to quarantine 1 digital dust bunnies:'));
        assert(consoleLogStub.calledWithMatch(`- ${path.join(sourceDir, 'old_document.pdf')} -> ${path.join(quarantineDir, 'old_document.pdf')}`));
        assert.strictEqual(consoleErrorStub.callCount, 0);
    });

    it('should handle errors during file system operations gracefully', async () => {
        const testDir = '/test/error_dir';
        const now = Date.now();
        const oldFileTime = new Date(now - 100 * 24 * 60 * 60 * 1000); // 100 days ago

        readdirStub.withArgs(testDir, { withFileTypes: true }).returns(Promise.resolve([
            { name: 'problem_file.txt', isFile: () => true, isDirectory: () => false }
        ]));
        statStub.withArgs(path.join(testDir, 'problem_file.txt')).returns(Promise.resolve({ mtime: oldFileTime }));
        mkdirStub.withArgs('/test/quarantine', { recursive: true }).returns(Promise.resolve());
        renameStub.withArgs(path.join(testDir, 'problem_file.txt'), path.join('/test/quarantine', 'problem_file.txt'))
            .returns(Promise.reject(new Error('Permission denied'))); // Simulate an error

        await program.parseAsync(['node', 'src/index.js', 'quarantine', testDir, '--age', '90', '--output', '/test/quarantine']);

        assert(consoleErrorStub.calledWithMatch('Error quarantining /test/error_dir/problem_file.txt: Permission denied'));
        assert(consoleLogStub.calledWithMatch('Quarantine operation complete. Review files in the quarantine directory.')); // Still completes for other files
    });

    it('should show help if --age is missing for scan command', async () => {
        const helpStub = sinon.stub(program, 'help'); // Mock program.help()
        await program.parseAsync(['node', 'src/index.js', 'scan', '/test/dir']);

        assert(consoleErrorStub.calledWithMatch('Error: --age is required for scanning.'));
        assert(helpStub.calledOnce);
        helpStub.restore(); // Restore the stub
    });

    it('should show help if --age or --output is missing for quarantine command', async () => {
        const helpStub = sinon.stub(program, 'help'); // Mock program.help()
        await program.parseAsync(['node', 'src/index.js', 'quarantine', '/test/dir', '--age', '90']); // Missing --output

        assert(consoleErrorStub.calledWithMatch('Error: --age and --output are required for quarantining.'));
        assert(helpStub.calledOnce);
        helpStub.restore(); // Restore the stub
    });

    it('should show verbose output when --verbose is used', async () => {
        const testDir = '/test/verbose_dir';
        const now = Date.now();
        const oldFileTime = new Date(now - 100 * 24 * 60 * 60 * 1000); // 100 days ago
        const newFileTime = new Date(now - 10 * 24 * 60 * 60 * 1000);  // 10 days ago

        readdirStub.withArgs(testDir, { withFileTypes: true }).returns(Promise.resolve([
            { name: 'old.txt', isFile: () => true, isDirectory: () => false },
            { name: 'new.txt', isFile: () => true, isDirectory: () => false }
        ]));
        statStub.withArgs(path.join(testDir, 'old.txt')).returns(Promise.resolve({ mtime: oldFileTime }));
        statStub.withArgs(path.join(testDir, 'new.txt')).returns(Promise.resolve({ mtime: newFileTime }));

        await program.parseAsync(['node', 'src/index.js', 'scan', testDir, '--age', '90', '--verbose']);

        assert(consoleLogStub.calledWithMatch('Verbose mode enabled.'));
        assert(consoleLogStub.calledWithMatch(`  Skipping: ${path.join(testDir, 'new.txt')} (too new)`));
        assert(consoleLogStub.calledWithMatch(`- ${path.join(testDir, 'old.txt')} (Modified: ${oldFileTime.toLocaleDateString()}, Age: 100 days)`));
    });
});
