const { scanDirectory, processDustBunnies, parseArgs } = require('../src/index');
const fs = require('fs');
const path = require('path');

// Mock rationale: File system operations are non-deterministic and have side effects.
// Mocking 'fs' allows tests to run deterministically, quickly, and without modifying
// the actual file system, ensuring isolation and repeatability.
jest.mock('fs', () => ({
    // Mock rationale: existsSync is used to check if a directory or quarantine path exists.
    // Mocking it allows us to simulate different file system states without actual files.
    existsSync: jest.fn((p) => {
        // Simulate existence for test paths
        if (p.startsWith('/mock/dir') || p.startsWith('/mock/quarantine')) return true;
        if (p === '/mock/nonexistent') return false;
        return false; // Default to non-existent for other paths
    }),
    // Mock rationale: readdirSync is used to list files in a directory.
    // Mocking it allows us to control the contents of directories for testing scan logic.
    readdirSync: jest.fn((dir) => {
        if (dir === '/mock/dir') return ['file1.txt', 'old_log.log', 'large_file.dat', 'subdir'];
        if (dir === '/mock/dir/subdir') return ['temp.tmp', 'recent.txt'];
        return [];
    }),
    // Mock rationale: statSync is used to get file metadata (size, mtime).
    // Mocking it allows us to define specific file properties for test scenarios.
    statSync: jest.fn((filePath) => {
        const now = Date.now();
        const oneDayMs = 24 * 60 * 60 * 1000;

        switch (filePath) {
            case '/mock/dir/file1.txt':
                return { isDirectory: () => false, isFile: () => true, mtimeMs: now - (5 * oneDayMs), size: 100 };
            case '/mock/dir/old_log.log':
                return { isDirectory: () => false, isFile: () => true, mtimeMs: now - (35 * oneDayMs), size: 500 };
            case '/mock/dir/large_file.dat':
                return { isDirectory: () => false, isFile: () => true, mtimeMs: now - (10 * oneDayMs), size: 2 * 1024 * 1024 }; // 2MB
            case '/mock/dir/subdir':
                return { isDirectory: () => true, isFile: () => false };
            case '/mock/dir/subdir/temp.tmp':
                return { isDirectory: () => false, isFile: () => true, mtimeMs: now - (15 * oneDayMs), size: 50 };
            case '/mock/dir/subdir/recent.txt':
                return { isDirectory: () => false, isFile: () => true, mtimeMs: now - (1 * oneDayMs), size: 200 };
            default:
                throw new Error('File not found in mock statSync');
        }
    }),
    // Mock rationale: renameSync is used for moving files to quarantine.
    // Mocking it prevents actual file system modifications during tests.
    renameSync: jest.fn(),
    // Mock rationale: unlinkSync is used for deleting files.
    // Mocking it prevents actual file system modifications during tests.
    unlinkSync: jest.fn()
}));

// Mock rationale: path.join is deterministic, but mocking it ensures consistency
// with mocked fs paths and allows for potential future complex path logic testing.
jest.mock('path', () => ({
    ...jest.requireActual('path'), // Use actual path functions for most operations
    join: jest.fn((...args) => args.join('/')) // Simple join for mock paths
}));

describe('Nightly Digital Dust Bunny Sweeper', () => {
    beforeEach(() => {
        jest.clearAllMocks();
        // Reset path.join mock to default behavior for each test if needed, or keep simple mock
        path.join.mockImplementation(jest.requireActual('path').join);
    });

    describe('parseArgs', () => {
        it('should parse directory and default options correctly', () => {
            const args = ['node', 'src/index.js', '/test/dir'];
            const { dirToScan, options } = parseArgs(args);
            expect(dirToScan).toBe('/test/dir');
            expect(options.recursive).toBe(true);
            expect(options.action).toBe('list');
        });

        it('should parse --age option', () => {
            const args = ['node', 'src/index.js', '/test/dir', '--age', '30'];
            const { options } = parseArgs(args);
            expect(options.ageDays).toBe(30);
        });

        it('should parse --size-gt option', () => {
            const args = ['node', 'src/index.js', '/test/dir', '--size-gt', '1024'];
            const { options } = parseArgs(args);
            expect(options.sizeGtBytes).toBe(1024);
        });

        it('should parse --pattern option', () => {
            const args = ['node', 'src/index.js', '/test/dir', '--pattern', '\\.log$'];
            const { options } = parseArgs(args);
            expect(options.pattern).toEqual(/\.log$/);
        });

        it('should parse --quarantine option and set action', () => {
            fs.existsSync.mockReturnValueOnce(true); // Mock rationale: Ensure quarantine path exists for this test
            const args = ['node', 'src/index.js', '/test/dir', '--quarantine', '/q/path'];
            const { options } = parseArgs(args);
            expect(options.quarantinePath).toBe('/q/path');
            expect(options.action).toBe('quarantine');
        });

        it('should exit if quarantine path does not exist', () => {
            fs.existsSync.mockReturnValueOnce(false); // Mock rationale: Simulate non-existent quarantine path
            const mockExit = jest.spyOn(process, 'exit').mockImplementation(() => {});
            const mockError = jest.spyOn(console, 'error').mockImplementation(() => {});

            const args = ['node', 'src/index.js', '/test/dir', '--quarantine', '/mock/nonexistent'];
            parseArgs(args);

            expect(mockError).toHaveBeenCalledWith(expect.stringContaining('Quarantine path does not exist'));
            expect(mockExit).toHaveBeenCalledWith(1);

            mockExit.mockRestore();
            mockError.mockRestore();
        });

        it('should parse --delete option and set action', () => {
            const args = ['node', 'src/index.js', '/test/dir', '--delete'];
            const { options } = parseArgs(args);
            expect(options.action).toBe('delete');
        });

        it('should exit if no directory is specified', () => {
            const mockExit = jest.spyOn(process, 'exit').mockImplementation(() => {});
            const mockError = jest.spyOn(console, 'error').mockImplementation(() => {});

            const args = ['node', 'src/index.js', '--age', '10'];
            parseArgs(args);

            expect(mockError).toHaveBeenCalledWith(expect.stringContaining('No directory to scan specified'));
            expect(mockExit).toHaveBeenCalledWith(1);

            mockExit.mockRestore();
            mockError.mockRestore();
        });
    });

    describe('scanDirectory', () => {
        it('should identify files older than specified age', () => {
            const options = { ageDays: 30, recursive: true };
            const dustBunnies = scanDirectory('/mock/dir', options);
            expect(dustBunnies).toEqual(['/mock/dir/old_log.log']);
        });

        it('should identify files matching a pattern', () => {
            const options = { pattern: /\.log$/, recursive: true };
            const dustBunnies = scanDirectory('/mock/dir', options);
            expect(dustBunnies).toEqual(['/mock/dir/old_log.log']);
        });

        it('should identify files larger than specified size', () => {
            const options = { sizeGtBytes: 1024 * 1024, recursive: true }; // 1MB
            const dustBunnies = scanDirectory('/mock/dir', options);
            expect(dustBunnies).toEqual(['/mock/dir/large_file.dat']);
        });

        it('should combine multiple criteria', () => {
            const options = { ageDays: 10, pattern: /\.txt$/, recursive: true };
            const dustBunnies = scanDirectory('/mock/dir', options);
            // file1.txt is 5 days old, matches .txt, but not older than 10 days
            // recent.txt is 1 day old, matches .txt, but not older than 10 days
            expect(dustBunnies).toEqual([]);

            const options2 = { ageDays: 30, pattern: /\.log$/, recursive: true };
            const dustBunnies2 = scanDirectory('/mock/dir', options2);
            expect(dustBunnies2).toEqual(['/mock/dir/old_log.log']);
        });

        it('should handle non-recursive scanning', () => {
            const options = { ageDays: 30, recursive: false };
            const dustBunnies = scanDirectory('/mock/dir', options);
            expect(dustBunnies).toEqual(['/mock/dir/old_log.log']); // subdir files not included
        });

        it('should return empty array if directory does not exist', () => {
            fs.existsSync.mockReturnValueOnce(false); // Mock rationale: Simulate non-existent directory
            const mockWarn = jest.spyOn(console, 'warn').mockImplementation(() => {});
            const dustBunnies = scanDirectory('/mock/nonexistent', {});
            expect(dustBunnies).toEqual([]);
            expect(mockWarn).toHaveBeenCalledWith(expect.stringContaining('Directory not found'));
            mockWarn.mockRestore();
        });
    });

    describe('processDustBunnies', () => {
        let mockLog;
        beforeEach(() => {
            mockLog = jest.spyOn(console, 'log').mockImplementation(() => {});
            jest.spyOn(console, 'error').mockImplementation(() => {}); // Suppress error logs for cleaner test output
        });

        afterEach(() => {
            mockLog.mockRestore();
            jest.restoreAllMocks();
        });

        it('should list files correctly', () => {
            const files = ['/mock/dir/file1.txt', '/mock/dir/file2.log'];
            processDustBunnies(files, 'list');
            expect(mockLog).toHaveBeenCalledWith(expect.stringContaining('Found 2 digital dust bunnies:'));
            expect(mockLog).toHaveBeenCalledWith(expect.stringContaining('  - /mock/dir/file1.txt'));
            expect(mockLog).toHaveBeenCalledWith(expect.stringContaining('  - /mock/dir/file2.log'));
        });

        it('should move files to quarantine', () => {
            const files = ['/mock/dir/file1.txt'];
            const quarantinePath = '/mock/quarantine';
            processDustBunnies(files, 'quarantine', quarantinePath);
            expect(fs.renameSync).toHaveBeenCalledWith('/mock/dir/file1.txt', '/mock/quarantine/file1.txt');
            expect(mockLog).toHaveBeenCalledWith(expect.stringContaining("Moved '/mock/dir/file1.txt' to '/mock/quarantine/file1.txt'"));
        });

        it('should delete files', () => {
            const files = ['/mock/dir/file1.txt'];
            processDustBunnies(files, 'delete');
            expect(fs.unlinkSync).toHaveBeenCalledWith('/mock/dir/file1.txt');
            expect(mockLog).toHaveBeenCalledWith(expect.stringContaining("Deleted '/mock/dir/file1.txt'"));
        });

        it('should report no dust bunnies found', () => {
            processDustBunnies([], 'list');
            expect(mockLog).toHaveBeenCalledWith('No digital dust bunnies found. Your system is sparkling clean!');
        });

        it('should handle renameSync errors gracefully', () => {
            fs.renameSync.mockImplementationOnce(() => { throw new Error('Permission denied'); }); // Mock rationale: Simulate a file system error
            const files = ['/mock/dir/file1.txt'];
            const quarantinePath = '/mock/quarantine';
            processDustBunnies(files, 'quarantine', quarantinePath);
            expect(console.error).toHaveBeenCalledWith(expect.stringContaining("Failed to move '/mock/dir/file1.txt': Permission denied"));
        });

        it('should handle unlinkSync errors gracefully', () => {
            fs.unlinkSync.mockImplementationOnce(() => { throw new Error('File in use'); }); // Mock rationale: Simulate a file system error
            const files = ['/mock/dir/file1.txt'];
            processDustBunnies(files, 'delete');
            expect(console.error).toHaveBeenCalledWith(expect.stringContaining("Failed to delete '/mock/dir/file1.txt': File in use"));
        });
    });
});
