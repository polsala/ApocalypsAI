const assert = require('assert');
const sinon = require('sinon');
const { synchronizeTimestamps, parseDuration, getRandomDateInRange, main } = require('../src/index');
const fs = require('fs');
const path = require('path');

// Mock rationale:
// fs.existsSync, fs.readdirSync, fs.utimesSync:
// These are file system operations. Mocking them ensures tests are fast,
// deterministic, and don't modify the actual file system. It allows
// simulating different directory structures and file types without creating real files.
// path.join: Mocking ensures consistent path handling across OSes in tests.
// Date: Essential for deterministic tests when dealing with timestamps,
// especially when using "current time" or "random range from current time".
// console.log, console.error, process.exit: To capture output and prevent test termination.

describe('Nightly Starlight Synchronizer', () => {
    let sandbox;
    let consoleLogStub;
    let consoleErrorStub;
    let processExitStub;
    let fsExistsSyncStub;
    let fsReaddirSyncStub;
    let fsUtimesSyncStub;
    let pathJoinStub;
    let clock;

    beforeEach(() => {
        sandbox = sinon.createSandbox();
        consoleLogStub = sandbox.stub(console, 'log');
        consoleErrorStub = sandbox.stub(console, 'error');
        processExitStub = sandbox.stub(process, 'exit');
        fsExistsSyncStub = sandbox.stub(fs, 'existsSync');
        fsReaddirSyncStub = sandbox.stub(fs, 'readdirSync');
        fsUtimesSyncStub = sandbox.stub(fs, 'utimesSync');
        pathJoinStub = sandbox.stub(path, 'join').callsFake((...args) => args.join('/')); // Simple join for testing
        clock = sandbox.useFakeTimers(new Date('2023-10-27T10:00:00Z').getTime()); // Fixed current time
    });

    afterEach(() => {
        sandbox.restore();
    });

    describe('parseDuration', () => {
        it('should parse hours correctly', () => {
            assert.strictEqual(parseDuration('24h'), 24 * 60 * 60 * 1000);
        });

        it('should parse days correctly', () => {
            assert.strictEqual(parseDuration('7d'), 7 * 24 * 60 * 60 * 1000);
        });

        it('should parse minutes correctly', () => {
            assert.strictEqual(parseDuration('30m'), 30 * 60 * 1000);
        });

        it('should throw error for invalid format', () => {
            assert.throws(() => parseDuration('24x'), /Invalid duration format/);
            assert.throws(() => parseDuration('h'), /Invalid duration format/);
            assert.throws(() => parseDuration(''), /Invalid duration format/);
        });
    });

    describe('getRandomDateInRange', () => {
        it('should return a date within the specified range before the base date', () => {
            const baseDate = new Date('2023-10-27T10:00:00Z');
            const rangeMs = 24 * 60 * 60 * 1000; // 24 hours

            // Mock Math.random to return a specific value for deterministic test
            sandbox.stub(Math, 'random').returns(0.5); // Should be exactly half the range back

            const randomDate = getRandomDateInRange(baseDate, rangeMs);
            const expectedDate = new Date('2023-10-26T10:00:00Z'); // 24 hours back from base
            assert.strictEqual(randomDate.getTime(), expectedDate.getTime());

            // Restore Math.random before next test to avoid interference
            sandbox.restore();
            sandbox = sinon.createSandbox(); // Recreate sandbox for other stubs
            consoleLogStub = sandbox.stub(console, 'log');
            consoleErrorStub = sandbox.stub(console, 'error');
            processExitStub = sandbox.stub(process, 'exit');
            fsExistsSyncStub = sandbox.stub(fs, 'existsSync');
            fsReaddirSyncStub = sandbox.stub(fs, 'readdirSync');
            fsUtimesSyncStub = sandbox.stub(fs, 'utimesSync');
            pathJoinStub = sandbox.stub(path, 'join').callsFake((...args) => args.join('/'));
            clock = sandbox.useFakeTimers(new Date('2023-10-27T10:00:00Z').getTime());
        });

        it('should return a date at the start of the range if random is 0', () => {
            const baseDate = new Date('2023-10-27T10:00:00Z');
            const rangeMs = 24 * 60 * 60 * 1000; // 24 hours
            sandbox.stub(Math, 'random').returns(0); // Should be exactly baseDate

            const randomDate = getRandomDateInRange(baseDate, rangeMs);
            assert.strictEqual(randomDate.getTime(), baseDate.getTime());
        });

        it('should return a date at the end of the range if random is close to 1', () => {
            const baseDate = new Date('2023-10-27T10:00:00Z');
            const rangeMs = 24 * 60 * 60 * 1000; // 24 hours
            sandbox.stub(Math, 'random').returns(0.999999999999999); // Close to 1

            const randomDate = getRandomDateInRange(baseDate, rangeMs);
            const expectedDate = new Date(baseDate.getTime() - rangeMs);
            assert(randomDate.getTime() >= expectedDate.getTime() && randomDate.getTime() < baseDate.getTime());
        });
    });

    describe('synchronizeTimestamps', () => {
        it('should exit if target path does not exist', () => {
            fsExistsSyncStub.withArgs('/nonexistent').returns(false);
            synchronizeTimestamps('/nonexistent', new Date());
            assert(consoleErrorStub.calledWithMatch(/Path does not exist/));
            assert(processExitStub.calledWith(1));
        });

        it('should synchronize files to current time if no date or random range is specified', () => {
            const targetPath = '/test-dir';
            const file1 = 'file1.txt';
            const subDir = 'sub-dir';
            const file2 = 'sub-dir/file2.txt';

            fsExistsSyncStub.withArgs(targetPath).returns(true);
            fsReaddirSyncStub.withArgs(targetPath).returns([
                { name: file1, isDirectory: () => false },
                { name: subDir, isDirectory: () => true }
            ]);
            fsReaddirSyncStub.withArgs(`${targetPath}/${subDir}`).returns([
                { name: file2.split('/')[1], isDirectory: () => false }
            ]);

            const expectedDate = new Date('2023-10-27T10:00:00Z');
            synchronizeTimestamps(targetPath, expectedDate, 0);

            assert(fsUtimesSyncStub.calledWith(`${targetPath}/${file1}`, expectedDate, expectedDate));
            assert(fsUtimesSyncStub.calledWith(`${targetPath}/${subDir}`, expectedDate, expectedDate));
            assert(fsUtimesSyncStub.calledWith(`${targetPath}/${file2}`, expectedDate, expectedDate));
            assert(fsUtimesSyncStub.calledWith(targetPath, expectedDate, expectedDate)); // The root itself
            assert.strictEqual(fsUtimesSyncStub.callCount, 4);
            assert(consoleLogStub.calledWithMatch(/Starlight Synchronization complete/));
        });

        it('should synchronize files to a specific date', () => {
            const targetPath = '/test-dir';
            const file1 = 'file1.txt';
            const specificDate = new Date('2022-01-01T00:00:00Z');

            fsExistsSyncStub.withArgs(targetPath).returns(true);
            fsReaddirSyncStub.withArgs(targetPath).returns([
                { name: file1, isDirectory: () => false }
            ]);

            synchronizeTimestamps(targetPath, specificDate, 0);

            assert(fsUtimesSyncStub.calledWith(`${targetPath}/${file1}`, specificDate, specificDate));
            assert(fsUtimesSyncStub.calledWith(targetPath, specificDate, specificDate));
            assert.strictEqual(fsUtimesSyncStub.callCount, 2);
        });

        it('should synchronize files with random dates within a range', () => {
            const targetPath = '/test-dir';
            const file1 = 'file1.txt';
            const baseDate = new Date('2023-10-27T10:00:00Z');
            const randomRangeMs = 24 * 60 * 60 * 1000; // 24 hours

            fsExistsSyncStub.withArgs(targetPath).returns(true);
            fsReaddirSyncStub.withArgs(targetPath).returns([
                { name: file1, isDirectory: () => false }
            ]);

            // Mock Math.random for deterministic random dates
            const mathRandomStub = sandbox.stub(Math, 'random');
            mathRandomStub.onCall(0).returns(0.1); // For file1
            mathRandomStub.onCall(1).returns(0.9); // For targetPath

            synchronizeTimestamps(targetPath, baseDate, randomRangeMs);

            const expectedDate1 = new Date(baseDate.getTime() - (0.1 * randomRangeMs));
            const expectedDate2 = new Date(baseDate.getTime() - (0.9 * randomRangeMs));

            assert(fsUtimesSyncStub.calledWith(`${targetPath}/${file1}`, expectedDate1, expectedDate1));
            assert(fsUtimesSyncStub.calledWith(targetPath, expectedDate2, expectedDate2));
            assert.strictEqual(fsUtimesSyncStub.callCount, 2);
        });

        it('should perform a dry run without modifying files', () => {
            const targetPath = '/test-dir';
            const file1 = 'file1.txt';
            const specificDate = new Date('2022-01-01T00:00:00Z');

            fsExistsSyncStub.withArgs(targetPath).returns(true);
            fsReaddirSyncStub.withArgs(targetPath).returns([
                { name: file1, isDirectory: () => false }
            ]);

            synchronizeTimestamps(targetPath, specificDate, 0, true); // dryRun = true

            assert(fsUtimesSyncStub.notCalled);
            assert(consoleLogStub.calledWithMatch(/DRY RUN MODE/));
            assert(consoleLogStub.calledWithMatch(`[DRY RUN] Would set ${targetPath}/${file1} to ${specificDate.toISOString()}`));
            assert(consoleLogStub.calledWithMatch(`[DRY RUN] Would set ${targetPath} to ${specificDate.toISOString()}`));
        });

        it('should handle errors during utimesSync gracefully', () => {
            const targetPath = '/test-dir';
            const file1 = 'file1.txt';
            const specificDate = new Date('2022-01-01T00:00:00Z');

            fsExistsSyncStub.withArgs(targetPath).returns(true);
            fsReaddirSyncStub.withArgs(targetPath).returns([
                { name: file1, isDirectory: () => false }
            ]);
            fsUtimesSyncStub.withArgs(`${targetPath}/${file1}`, specificDate, specificDate).throws(new Error('Permission denied'));

            synchronizeTimestamps(targetPath, specificDate, 0);

            assert(consoleErrorStub.calledWithMatch(/Failed to synchronize \/test-dir\/file1.txt: Permission denied/));
            assert(fsUtimesSyncStub.calledWith(targetPath, specificDate, specificDate)); // Root dir should still be attempted
            assert.strictEqual(fsUtimesSyncStub.callCount, 2); // One call for file1 (failed), one for targetPath (succeeded)
        });
    });

    describe('main function (CLI entry point)', () => {
        it('should exit with error if no path is provided', () => {
            main([]);
            assert(consoleErrorStub.calledWithMatch(/Usage:/));
            assert(processExitStub.calledWith(1));
        });

        it('should parse --date argument correctly', () => {
            const targetPath = '/some/path';
            const dateStr = '2021-05-20T14:00:00Z';
            fsExistsSyncStub.withArgs(targetPath).returns(true);
            fsReaddirSyncStub.returns([]); // Empty dir for simplicity

            main([targetPath, '--date', dateStr]);

            const expectedDate = new Date(dateStr);
            assert(fsUtimesSyncStub.calledWith(targetPath, expectedDate, expectedDate));
        });

        it('should exit with error for invalid --date format', () => {
            const targetPath = '/some/path';
            fsExistsSyncStub.withArgs(targetPath).returns(true);
            main([targetPath, '--date', 'invalid-date']);
            assert(consoleErrorStub.calledWithMatch(/Invalid date format for --date/));
            assert(processExitStub.calledWith(1));
        });

        it('should exit with error if --date is missing value', () => {
            const targetPath = '/some/path';
            fsExistsSyncStub.withArgs(targetPath).returns(true);
            main([targetPath, '--date']);
            assert(consoleErrorStub.calledWithMatch(/--date requires a value/));
            assert(processExitStub.calledWith(1));
        });

        it('should parse --random-range argument correctly', () => {
            const targetPath = '/some/path';
            const rangeStr = '1h';
            fsExistsSyncStub.withArgs(targetPath).returns(true);
            fsReaddirSyncStub.returns([]); // Empty dir for simplicity

            const baseDate = new Date('2023-10-27T10:00:00Z'); // From clock
            const randomRangeMs = parseDuration(rangeStr);

            // Mock Math.random for deterministic random dates
            const mathRandomStub = sandbox.stub(Math, 'random');
            mathRandomStub.onCall(0).returns(0.5); // For targetPath

            main([targetPath, '--random-range', rangeStr]);

            const expectedDate = new Date(baseDate.getTime() - (0.5 * randomRangeMs));
            assert(fsUtimesSyncStub.calledWith(targetPath, expectedDate, expectedDate));
        });

        it('should exit with error for invalid --random-range format', () => {
            const targetPath = '/some/path';
            fsExistsSyncStub.withArgs(targetPath).returns(true);
            main([targetPath, '--random-range', 'invalid']);
            assert(consoleErrorStub.calledWithMatch(/Invalid duration format/));
            assert(processExitStub.calledWith(1));
        });

        it('should exit with error if --random-range is missing value', () => {
            const targetPath = '/some/path';
            fsExistsSyncStub.withArgs(targetPath).returns(true);
            main([targetPath, '--random-range']);
            assert(consoleErrorStub.calledWithMatch(/--random-range requires a value/));
            assert(processExitStub.calledWith(1));
        });

        it('should parse --dry-run argument correctly', () => {
            const targetPath = '/some/path';
            fsExistsSyncStub.withArgs(targetPath).returns(true);
            fsReaddirSyncStub.returns([]); // Empty dir for simplicity

            main([targetPath, '--dry-run']);

            assert(fsUtimesSyncStub.notCalled);
            assert(consoleLogStub.calledWithMatch(/DRY RUN MODE/));
        });

        it('should handle unknown arguments', () => {
            const targetPath = '/some/path';
            fsExistsSyncStub.withArgs(targetPath).returns(true);
            main([targetPath, '--unknown-arg']);
            assert(consoleErrorStub.calledWithMatch(/Unknown argument: --unknown-arg/));
            assert(processExitStub.calledWith(1));
        });
    });
});
