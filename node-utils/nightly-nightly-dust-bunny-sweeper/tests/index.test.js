const fs = require('fs');
const path = require('path');
const { main } = require('../src/index');

// Mock fs module
jest.mock('fs', () => ({
    readdirSync: jest.fn(),
    statSync: jest.fn(),
    unlinkSync: jest.fn(),
    existsSync: jest.fn(),
}));

// Mock console.log and console.error
const mockLog = jest.spyOn(console, 'log').mockImplementation(() => {});
const mockError = jest.spyOn(console, 'error').mockImplementation(() => {});

describe('Nightly Digital Dust Bunny Sweeper', () => {
    beforeEach(() => {
        mockLog.mockClear();
        mockError.mockClear();
        fs.readdirSync.mockClear();
        fs.statSync.mockClear();
        fs.unlinkSync.mockClear();
        fs.existsSync.mockClear();
        // Reset process.argv for each test
        process.argv = ['node', 'src/index.js'];
    });

    // Helper to set up mock file system
    const setupMockFs = (structure, now = Date.now()) => {
        const mockStats = {};
        const existingPaths = new Set();

        const createStats = (type, mtimeMs) => ({
            isDirectory: () => type === 'directory',
            isFile: () => type === 'file',
            mtimeMs: mtimeMs,
        });

        const populate = (currentPath, currentStructure) => {
            existingPaths.add(currentPath);
            fs.readdirSync.mockImplementation((p) => {
                if (p === currentPath) {
                    return Object.keys(currentStructure);
                }
                return []; // Default for paths not explicitly defined
            });

            for (const name in currentStructure) {
                const fullPath = path.join(currentPath, name);
                existingPaths.add(fullPath);
                const item = currentStructure[name];

                if (typeof item === 'object' && item !== null && !Array.isArray(item)) { // It's a directory
                    mockStats[fullPath] = createStats('directory', now); // Directories don't age for this tool, their mtimeMs doesn't matter for this logic
                    populate(fullPath, item);
                } else { // It's a file
                    mockStats[fullPath] = createStats('file', now - item); // item is age in ms
                }
            }
        };

        populate('/test-dir', structure); // Always populate a base directory for tests

        fs.statSync.mockImplementation((p) => {
            if (mockStats[p]) {
                return mockStats[p];
            }
            // If statSync is called for a path not in mockStats, it's an error in real fs
            throw new Error(`ENOENT: no such file or directory, stat '${p}'`);
        });

        fs.existsSync.mockImplementation((p) => existingPaths.has(p));
    };

    test('should report no dust bunnies if all files are recent', () => {
        process.argv.push('/test-dir', '30'); // 30 days threshold
        setupMockFs({
            'recent_file.txt': 1000 * 60 * 60 * 24 * 10, // 10 days old
            'another_recent.log': 1000 * 60 * 60 * 24 * 5, // 5 days old
        });

        main();

        expect(mockLog).toHaveBeenCalledWith('No digital dust bunnies found older than 30 days in /test-dir.');
        expect(fs.unlinkSync).not.toHaveBeenCalled();
    });

    test('should report dust bunnies without cleaning if --clean is not provided', () => {
        process.argv.push('/test-dir', '10'); // 10 days threshold
        setupMockFs({
            'old_file.txt': 1000 * 60 * 60 * 24 * 15, // 15 days old
            'recent_file.txt': 1000 * 60 * 60 * 24 * 5, // 5 days old
            'subdir': {
                'very_old.log': 1000 * 60 * 60 * 24 * 20, // 20 days old
            },
        });

        main();

        expect(mockLog).toHaveBeenCalledWith('Found 2 digital dust bunnies older than 10 days:');
        expect(mockLog).toHaveBeenCalledWith('- /test-dir/old_file.txt');
        expect(mockLog).toHaveBeenCalledWith('- /test-dir/subdir/very_old.log');
        expect(mockLog).toHaveBeenCalledWith('Run with --clean to sweep them away.');
        expect(fs.unlinkSync).not.toHaveBeenCalled();
    });

    test('should clean dust bunnies if --clean is provided', () => {
        process.argv.push('/test-dir', '10', '--clean'); // 10 days threshold, clean
        setupMockFs({
            'old_file.txt': 1000 * 60 * 60 * 24 * 15, // 15 days old
            'recent_file.txt': 1000 * 60 * 60 * 24 * 5, // 5 days old
            'subdir': {
                'very_old.log': 1000 * 60 * 60 * 24 * 20, // 20 days old
            },
        });

        main();

        expect(mockLog).toHaveBeenCalledWith('Found 2 digital dust bunnies older than 10 days:');
        expect(mockLog).toHaveBeenCalledWith('- /test-dir/old_file.txt');
        expect(mockLog).toHaveBeenCalledWith('- /test-dir/subdir/very_old.log');
        expect(mockLog).toHaveBeenCalledWith('Swept them away!');
        expect(fs.unlinkSync).toHaveBeenCalledTimes(2);
        expect(fs.unlinkSync).toHaveBeenCalledWith('/test-dir/old_file.txt');
        expect(fs.unlinkSync).toHaveBeenCalledWith('/test-dir/subdir/very_old.log');
    });

    test('should handle non-existent directory path gracefully', () => {
        process.argv.push('/non-existent-dir', '30');
        fs.existsSync.mockReturnValue(false); // # Mock rationale: `fs.existsSync` is mocked to simulate a directory not existing, allowing testing of error handling for invalid paths.

        main();

        expect(mockError).toHaveBeenCalledWith('Error sweeping directory: Directory not found: /non-existent-dir');
        expect(mockLog).not.toHaveBeenCalledWith(expect.stringContaining('dust bunnies'));
        expect(fs.readdirSync).not.toHaveBeenCalled(); // Should not try to read a non-existent dir
    });

    test('should show usage if arguments are missing', () => {
        process.argv.push('/test-dir'); // Missing age
        main();
        expect(mockLog).toHaveBeenCalledWith('Usage: node src/index.js <directory> <age_in_days> [--clean]');
        expect(mockError).not.toHaveBeenCalled();

        mockLog.mockClear();
        process.argv = ['node', 'src/index.js']; // No args
        main();
        expect(mockLog).toHaveBeenCalledWith('Usage: node src/index.js <directory> <age_in_days> [--clean]');
        expect(mockError).not.toHaveBeenCalled();
    });
});
