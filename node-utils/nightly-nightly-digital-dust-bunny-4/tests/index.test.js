const { findDigitalDustBunnies, parseAgeThreshold } = require('../src/index');
const { vol } = require('memfs'); // For mocking fs
const path = require('node:path');

// Mock rationale: We need to simulate file system operations (readdir, stat)
// without actually touching the disk. 'memfs' provides an in-memory file system
// that can be controlled programmatically, making tests deterministic and offline.
jest.mock('node:fs/promises', () => {
    const { fs } = require('memfs');
    return {
        readdir: fs.promises.readdir,
        stat: fs.promises.stat,
    };
});

// Mock rationale: path.resolve can be affected by the current working directory.
// For deterministic tests, we want to control the base path.
jest.mock('node:path', () => ({
    ...jest.requireActual('node:path'), // Keep original path functions
    resolve: jest.fn((p) => p), // Mock resolve to just return the path for testing
    join: jest.requireActual('node:path').join, // Keep join as it's used internally
}));


describe('parseAgeThreshold', () => {
    test('should correctly parse days', () => {
        const days = 10;
        const expectedMs = days * 24 * 60 * 60 * 1000;
        expect(parseAgeThreshold(days, 'days')).toBe(expectedMs);
    });

    test('should correctly parse months (approximate)', () => {
        const months = 2;
        const expectedMs = months * 30 * 24 * 60 * 60 * 1000;
        expect(parseAgeThreshold(months, 'months')).toBe(expectedMs);
    });

    test('should correctly parse years (approximate)', () => {
        const years = 1;
        const expectedMs = years * 365 * 24 * 60 * 60 * 1000;
        expect(parseAgeThreshold(years, 'years')).toBe(expectedMs);
    });

    test('should throw error for invalid age', () => {
        expect(() => parseAgeThreshold('abc', 'days')).toThrow('Age must be a positive number.');
        expect(() => parseAgeThreshold('-5', 'days')).toThrow('Age must be a positive number.');
        expect(() => parseAgeThreshold('0', 'days')).toThrow('Age must be a positive number.');
    });

    test('should throw error for invalid unit', () => {
        expect(() => parseAgeThreshold('10', 'weeks')).toThrow('Unit must be "days", "months", or "years".');
    });
});

describe('findDigitalDustBunnies', () => {
    const now = Date.now();
    const oneDayMs = 24 * 60 * 60 * 1000;
    const oldFileTime = now - (100 * oneDayMs); // 100 days ago
    const newFileTime = now - (10 * oneDayMs);  // 10 days ago

    beforeEach(() => {
        vol.reset(); // Clear the in-memory file system before each test
        // Reset path.resolve mock
        path.resolve.mockImplementation((p) => p);
    });

    test('should find old files in a flat directory', async () => {
        vol.fromJSON({
            '/testdir/old_file.txt': 'content',
            '/testdir/new_file.txt': 'content',
        }, '/');

        // Mock stat to return specific mtimeMs
        const mockStat = jest.fn(async (filePath) => {
            if (filePath === '/testdir/old_file.txt') {
                return { isFile: () => true, isDirectory: () => false, mtimeMs: oldFileTime };
            }
            if (filePath === '/testdir/new_file.txt') {
                return { isFile: () => true, isDirectory: () => false, mtimeMs: newFileTime };
            }
            throw new Error('File not found in mock');
        });
        require('node:fs/promises').stat.mockImplementation(mockStat);

        const threshold = 50 * oneDayMs; // Files older than 50 days
        const bunnies = await findDigitalDustBunnies('/testdir', threshold);

        expect(bunnies).toHaveLength(1);
        expect(bunnies[0].path).toBe('/testdir/old_file.txt');
        expect(bunnies[0].modified).toBe(new Date(oldFileTime).toISOString().split('T')[0]);
    });

    test('should find old files in nested directories', async () => {
        vol.fromJSON({
            '/testdir/subdir1/old_nested.log': 'log content',
            '/testdir/subdir1/new_nested.json': '{}',
            '/testdir/subdir2/another_old.bak': 'backup',
            '/testdir/new_root.js': 'console.log("hello");',
        }, '/');

        const mockStat = jest.fn(async (filePath) => {
            if (filePath.includes('old_nested.log')) {
                return { isFile: () => true, isDirectory: () => false, mtimeMs: oldFileTime };
            }
            if (filePath.includes('new_nested.json')) {
                return { isFile: () => true, isDirectory: () => false, mtimeMs: newFileTime };
            }
            if (filePath.includes('another_old.bak')) {
                return { isFile: () => true, isDirectory: () => false, mtimeMs: oldFileTime };
            }
            if (filePath.includes('new_root.js')) {
                return { isFile: () => true, isDirectory: () => false, mtimeMs: newFileTime };
            }
            // For directories, return isDirectory: true
            if (filePath === '/testdir' || filePath === '/testdir/subdir1' || filePath === '/testdir/subdir2') {
                return { isFile: () => false, isDirectory: () => true, mtimeMs: now };
            }
            throw new Error(`File not found in mock: ${filePath}`);
        });
        require('node:fs/promises').stat.mockImplementation(mockStat);

        const threshold = 50 * oneDayMs;
        const bunnies = await findDigitalDustBunnies('/testdir', threshold);

        expect(bunnies).toHaveLength(2);
        const paths = bunnies.map(b => b.path).sort();
        expect(paths).toEqual([
            '/testdir/subdir1/old_nested.log',
            '/testdir/subdir2/another_old.bak',
        ].sort());
    });

    test('should return empty array if no old files found', async () => {
        vol.fromJSON({
            '/testdir/file1.txt': 'content',
            '/testdir/file2.txt': 'content',
        }, '/');

        const mockStat = jest.fn(async (filePath) => {
            if (filePath === '/testdir/file1.txt' || filePath === '/testdir/file2.txt') {
                return { isFile: () => true, isDirectory: () => false, mtimeMs: newFileTime };
            }
            if (filePath === '/testdir') {
                return { isFile: () => false, isDirectory: () => true, mtimeMs: now };
            }
            throw new Error('File not found in mock');
        });
        require('node:fs/promises').stat.mockImplementation(mockStat);

        const threshold = 50 * oneDayMs;
        const bunnies = await findDigitalDustBunnies('/testdir', threshold);

        expect(bunnies).toHaveLength(0);
    });

    test('should handle empty directory', async () => {
        vol.fromJSON({
            '/empty_dir': null, // Represents an empty directory
        }, '/');

        const mockStat = jest.fn(async (filePath) => {
            if (filePath === '/empty_dir') {
                return { isFile: () => false, isDirectory: () => true, mtimeMs: now };
            }
            throw new Error('File not found in mock');
        });
        require('node:fs/promises').stat.mockImplementation(mockStat);

        const threshold = 50 * oneDayMs;
        const bunnies = await findDigitalDustBunnies('/empty_dir', threshold);

        expect(bunnies).toHaveLength(0);
    });

    test('should handle non-existent directory gracefully', async () => {
        // No files in memfs, so /nonexistent will not exist
        const threshold = 50 * oneDayMs;
        const bunnies = await findDigitalDustBunnies('/nonexistent', threshold);

        // Expect an empty array, as the error is caught and handled internally
        expect(bunnies).toHaveLength(0);
    });

    test('should ignore files that cannot be stat-ed (e.g., permission errors)', async () => {
        vol.fromJSON({
            '/testdir/accessible.txt': 'content',
            '/testdir/inaccessible.txt': 'content',
        }, '/');

        const mockStat = jest.fn(async (filePath) => {
            if (filePath === '/testdir/accessible.txt') {
                return { isFile: () => true, isDirectory: () => false, mtimeMs: oldFileTime };
            }
            if (filePath === '/testdir/inaccessible.txt') {
                throw new Error('EACCES: permission denied'); // Simulate permission error
            }
            if (filePath === '/testdir') {
                return { isFile: () => false, isDirectory: () => true, mtimeMs: now };
            }
            throw new Error('File not found in mock');
        });
        require('node:fs/promises').stat.mockImplementation(mockStat);

        const threshold = 50 * oneDayMs;
        const bunnies = await findDigitalDustBunnies('/testdir', threshold);

        expect(bunnies).toHaveLength(1);
        expect(bunnies[0].path).toBe('/testdir/accessible.txt');
    });
});
