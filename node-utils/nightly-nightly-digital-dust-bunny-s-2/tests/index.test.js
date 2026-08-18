const { main, parseArgs } = require('../src/index');
const fs = require('fs/promises');
const path = require('path');

// Mock fs/promises for deterministic, offline testing
// Mock rationale: Simulate directory contents, file stats, and file operations (rename, unlink, mkdir)
// without actually touching the file system, ensuring tests are fast, isolated, and repeatable.
jest.mock('fs/promises', () => ({
    readdir: jest.fn(),
    stat: jest.fn(),
    rename: jest.fn(),
    unlink: jest.fn(),
    mkdir: jest.fn(),
}));

// Mock console.log, console.error, and process.exit to capture output and prevent premature test exit
// Mock rationale: Capture CLI output for assertions and prevent tests from terminating the Node.js process.
const mockLog = jest.spyOn(console, 'log').mockImplementation(() => {});
const mockError = jest.spyOn(console, 'error').mockImplementation(() => {});
const mockExit = jest.spyOn(process, 'exit').mockImplementation(() => {});

describe('parseArgs', () => {
    const originalArgv = process.argv;

    beforeEach(() => {
        jest.clearAllMocks();
        process.argv = ['node', 'index.js']; // Reset argv for each test
    });

    afterAll(() => {
        process.argv = originalArgv;
    });

    test('should parse default arguments correctly', () => {
        const options = parseArgs(process.argv);
        expect(options.dir).toBe(process.cwd());
        expect(options.ageDays).toBe(90);
        expect(options.action).toBe('list');
        expect(options.quarantineDir).toBe(path.join(process.cwd(), '.digital_attic'));
        expect(options.force).toBe(false);
    });

    test('should parse custom arguments correctly', () => {
        process.argv = ['node', 'index.js', '--dir', '/my/path', '--age', '180', '--action', 'quarantine', '--quarantine-dir', '/my/attic', '--force'];
        const options = parseArgs(process.argv);
        expect(options.dir).toBe('/my/path');
        expect(options.ageDays).toBe(180);
        expect(options.action).toBe('quarantine');
        expect(options.quarantineDir).toBe('/my/attic');
        expect(options.force).toBe(true);
    });

    test('should throw error for invalid age', () => {
        process.argv = ['node', 'index.js', '--age', '0'];
        expect(() => parseArgs(process.argv)).toThrow('Invalid --age. Must be a positive number of days.');

        process.argv = ['node', 'index.js', '--age', 'abc'];
        expect(() => parseArgs(process.argv)).toThrow('Invalid --age. Must be a positive number of days.');
    });

    test('should throw error for invalid action', () => {
        process.argv = ['node', 'index.js', '--action', 'invalid'];
        expect(() => parseArgs(process.argv)).toThrow('Invalid --action. Must be one of: list, quarantine, delete.');
    });

    test('should throw error for delete action without --force', () => {
        process.argv = ['node', 'index.js', '--action', 'delete'];
        expect(() => parseArgs(process.argv)).toThrow('Deletion requires --force flag for safety. No digital dust bunnies will be deleted without explicit confirmation.');
    });

    test('should not throw error for delete action with --force', () => {
        process.argv = ['node', 'index.js', '--action', 'delete', '--force'];
        expect(() => parseArgs(process.argv)).not.toThrow();
    });

    test('should throw error for unknown argument', () => {
        process.argv = ['node', 'index.js', '--unknown-arg'];
        expect(() => parseArgs(process.argv)).toThrow('Unknown argument: --unknown-arg');
    });

    test('should exit and log help for --help', () => {
        process.argv = ['node', 'index.js', '--help'];
        parseArgs(process.argv);
        expect(mockLog).toHaveBeenCalledWith(expect.stringContaining('Digital Dust Bunny Sweeper - Sweep away old, unused files!'));
        expect(mockExit).toHaveBeenCalledWith(0);
    });
});

describe('main', () => {
    const originalArgv = process.argv;

    beforeEach(() => {
        jest.clearAllMocks();
        // Mock rationale: Set a fixed system time for deterministic age calculations.
        jest.useFakeTimers();
        jest.setSystemTime(new Date('2024-01-01T12:00:00Z')); // Mock current time
        process.argv = ['node', 'index.js']; // Reset argv for each test
    });

    afterEach(() => {
        jest.useRealTimers();
    });

    afterAll(() => {
        process.argv = originalArgv;
    });

    test('should list old files correctly', async () => {
        // Mock rationale: Simulate directory contents and file stats for listing.
        fs.readdir.mockResolvedValueOnce([
            { name: 'file1.txt', isFile: () => true, isDirectory: () => false },
            { name: 'subdir', isFile: () => false, isDirectory: () => true }
        ]);
        fs.stat.mockImplementation((p) => {
            if (p === '/test/dir/file1.txt') {
                return Promise.resolve({
                    isFile: () => true,
                    isDirectory: () => false,
                    mtimeMs: new Date('2023-01-01T11:00:00Z').getTime(), // Old file (365 days old)
                    size: 1024
                });
            }
            if (p === '/test/dir/subdir') {
                return Promise.resolve({
                    isFile: () => false,
                    isDirectory: () => true,
                    mtimeMs: new Date('2023-11-01T12:00:00Z').getTime(), // Newer dir
                    size: 0
                });
            }
            return Promise.reject(new Error('Not found'));
        });
        fs.readdir.mockResolvedValueOnce([]); // subdir is empty

        process.argv = ['node', 'index.js', '--dir', '/test/dir', '--age', '90', '--action', 'list'];
        await main();

        expect(mockLog).toHaveBeenCalledWith(expect.stringContaining('Found 1 digital dust bunnies'));
        expect(mockLog).toHaveBeenCalledWith(expect.stringContaining('- /test/dir/file1.txt (Size: 1024 bytes, Last Modified: 1/1/2023)'));
        expect(fs.rename).not.toHaveBeenCalled();
        expect(fs.unlink).not.toHaveBeenCalled();
        expect(mockExit).not.toHaveBeenCalled();
    });

    test('should quarantine old files', async () => {
        // Mock rationale: Simulate directory contents, file stats, and successful move operation.
        fs.readdir.mockResolvedValueOnce([
            { name: 'old_file.log', isFile: () => true, isDirectory: () => false },
            { name: 'new_file.txt', isFile: () => true, isDirectory: () => false }
        ]);
        fs.stat.mockImplementation((p) => {
            if (p === '/test/dir/old_file.log') {
                return Promise.resolve({
                    isFile: () => true,
                    isDirectory: () => false,
                    mtimeMs: new Date('2023-01-01T12:00:00Z').getTime(), // Old file
                    size: 2048
                });
            }
            if (p === '/test/dir/new_file.txt') {
                return Promise.resolve({
                    isFile: () => true,
                    isDirectory: () => false,
                    mtimeMs: new Date('2023-12-01T12:00:00Z').getTime(), // Newer file
                    size: 512
                });
            }
            return Promise.reject(new Error('Not found'));
        });
        fs.mkdir.mockResolvedValueOnce(undefined); // Quarantine dir creation
        fs.rename.mockResolvedValueOnce(undefined); // File move

        process.argv = ['node', 'index.js', '--dir', '/test/dir', '--age', '30', '--action', 'quarantine', '--quarantine-dir', '/attic'];
        await main();

        expect(mockLog).toHaveBeenCalledWith(expect.stringContaining('Found 1 digital dust bunnies'));
        expect(fs.mkdir).toHaveBeenCalledWith('/attic', { recursive: true });
        expect(fs.rename).toHaveBeenCalledWith('/test/dir/old_file.log', '/attic/old_file.log');
        expect(mockLog).toHaveBeenCalledWith(expect.stringContaining('Moved 1 dust bunny(ies) to digital attic. They\'re safe there!'));
        expect(fs.unlink).not.toHaveBeenCalled();
        expect(mockExit).not.toHaveBeenCalled();
    });

    test('should delete old files with --force', async () => {
        // Mock rationale: Simulate directory contents, file stats, and successful delete operation.
        fs.readdir.mockResolvedValueOnce([
            { name: 'temp.bak', isFile: () => true, isDirectory: () => false }
        ]);
        fs.stat.mockImplementation((p) => {
            if (p === '/test/dir/temp.bak') {
                return Promise.resolve({
                    isFile: () => true,
                    isDirectory: () => false,
                    mtimeMs: new Date('2023-01-01T12:00:00Z').getTime(), // Old file
                    size: 100
                });
            }
            return Promise.reject(new Error('Not found'));
        });
        fs.unlink.mockResolvedValueOnce(undefined); // File delete

        process.argv = ['node', 'index.js', '--dir', '/test/dir', '--age', '30', '--action', 'delete', '--force'];
        await main();

        expect(mockLog).toHaveBeenCalledWith(expect.stringContaining('Found 1 digital dust bunnies'));
        expect(fs.unlink).toHaveBeenCalledWith('/test/dir/temp.bak');
        expect(mockLog).toHaveBeenCalledWith(expect.stringContaining('Swept away 1 dust bunny(ies) forever! Your digital space is cleaner.'));
        expect(fs.rename).not.toHaveBeenCalled();
        expect(mockExit).not.toHaveBeenCalled();
    });

    test('should handle no old files found', async () => {
        // Mock rationale: Simulate an empty directory or all files being new.
        fs.readdir.mockResolvedValueOnce([
            { name: 'recent.txt', isFile: () => true, isDirectory: () => false }
        ]);
        fs.stat.mockImplementation((p) => {
            if (p === '/test/dir/recent.txt') {
                return Promise.resolve({
                    isFile: () => true,
                    isDirectory: () => false,
                    mtimeMs: new Date('2023-12-15T12:00:00Z').getTime(), // Newer file
                    size: 100
                });
            }
            return Promise.reject(new Error('Not found'));
        });

        process.argv = ['node', 'index.js', '--dir', '/test/dir', '--age', '30', '--action', 'list'];
        await main();

        expect(mockLog).toHaveBeenCalledWith(expect.stringContaining('Your digital space is sparkling! No dust bunnies found'));
        expect(fs.rename).not.toHaveBeenCalled();
        expect(fs.unlink).not.toHaveBeenCalled();
        expect(mockExit).not.toHaveBeenCalled();
    });

    test('should exit with error for invalid directory', async () => {
        // Mock rationale: Simulate fs.readdir throwing an error for an invalid directory.
        fs.readdir.mockRejectedValueOnce(new Error('ENOENT: no such file or directory, scandir \'nonexistent\''));

        process.argv = ['node', 'index.js', '--dir', 'nonexistent', '--age', '30', '--action', 'list'];
        await main();

        expect(mockError).toHaveBeenCalledWith(expect.stringContaining('Warning: Directory not found or accessible: \'nonexistent\'. Skipping.'));
        // No exit(1) for a warning, it continues if other paths exist. If it's the only path, it will just report no dust bunnies.
        expect(mockExit).not.toHaveBeenCalled();
    });

    test('should exit with error if quarantine directory cannot be created', async () => {
        // Mock rationale: Simulate a file that needs quarantining, but fs.mkdir fails.
        fs.readdir.mockResolvedValueOnce([
            { name: 'old_file.log', isFile: () => true, isDirectory: () => false }
        ]);
        fs.stat.mockImplementation((p) => {
            if (p === '/test/dir/old_file.log') {
                return Promise.resolve({
                    isFile: () => true,
                    isDirectory: () => false,
                    mtimeMs: new Date('2023-01-01T12:00:00Z').getTime(),
                    size: 100
                });
            }
            return Promise.reject(new Error('Not found'));
        });
        fs.mkdir.mockRejectedValueOnce(new Error('EACCES: permission denied, mkdir \'/attic\''));

        process.argv = ['node', 'index.js', '--dir', '/test/dir', '--age', '30', '--action', 'quarantine', '--quarantine-dir', '/attic'];
        await main();

        expect(mockError).toHaveBeenCalledWith(expect.stringContaining('Failed to quarantine files: EACCES: permission denied'));
        expect(mockExit).toHaveBeenCalledWith(1);
    });

    test('should exit with error if file cannot be deleted', async () => {
        // Mock rationale: Simulate a file that needs deleting, but fs.unlink fails.
        fs.readdir.mockResolvedValueOnce([
            { name: 'old_file.log', isFile: () => true, isDirectory: () => false }
        ]);
        fs.stat.mockImplementation((p) => {
            if (p === '/test/dir/old_file.log') {
                return Promise.resolve({
                    isFile: () => true,
                    isDirectory: () => false,
                    mtimeMs: new Date('2023-01-01T12:00:00Z').getTime(),
                    size: 100
                });
            }
            return Promise.reject(new Error('Not found'));
        });
        fs.unlink.mockRejectedValueOnce(new Error('EACCES: permission denied, unlink \'/test/dir/old_file.log\''));

        process.argv = ['node', 'index.js', '--dir', '/test/dir', '--age', '30', '--action', 'delete', '--force'];
        await main();

        expect(mockError).toHaveBeenCalledWith(expect.stringContaining('Failed to delete files: EACCES: permission denied'));
        expect(mockExit).toHaveBeenCalledWith(1);
    });

    test('should skip quarantine directory during scan', async () => {
        const testDir = '/test/dir';
        const quarantineDir = path.join(testDir, '.digital_attic');

        fs.readdir.mockResolvedValueOnce([
            { name: 'old_file.log', isFile: () => true, isDirectory: () => false },
            { name: '.digital_attic', isFile: () => false, isDirectory: () => true }
        ]);
        fs.stat.mockImplementation((p) => {
            if (p === path.join(testDir, 'old_file.log')) {
                return Promise.resolve({
                    isFile: () => true,
                    isDirectory: () => false,
                    mtimeMs: new Date('2023-01-01T12:00:00Z').getTime(), // Old file
                    size: 100
                });
            }
            if (p === quarantineDir) {
                return Promise.resolve({
                    isFile: () => false,
                    isDirectory: () => true,
                    mtimeMs: new Date('2023-12-01T12:00:00Z').getTime(),
                    size: 0
                });
            }
            return Promise.reject(new Error('Not found'));
        });
        // Mock rationale: Ensure readdir is not called for the quarantine directory itself.
        fs.readdir.mockImplementation(async (dirPath) => {
            if (dirPath === quarantineDir) {
                throw new Error('Should not read quarantine directory');
            }
            return [
                { name: 'old_file.log', isFile: () => true, isDirectory: () => false },
                { name: '.digital_attic', isFile: () => false, isDirectory: () => true }
            ];
        });

        process.argv = ['node', 'index.js', '--dir', testDir, '--age', '30', '--action', 'list', '--quarantine-dir', quarantineDir];
        await main();

        expect(mockLog).toHaveBeenCalledWith(expect.stringContaining('Found 1 digital dust bunnies'));
        expect(mockLog).toHaveBeenCalledWith(expect.stringContaining('- /test/dir/old_file.log'));
        // Verify that readdir was not called on the quarantine directory itself
        expect(fs.readdir).toHaveBeenCalledWith(testDir, { withFileTypes: true });
        // The mock readdir for the main directory will be called, but the recursive call for .digital_attic should be skipped.
        // This is implicitly tested by not throwing the 'Should not read quarantine directory' error.
        expect(mockExit).not.toHaveBeenCalled();
    });
});
