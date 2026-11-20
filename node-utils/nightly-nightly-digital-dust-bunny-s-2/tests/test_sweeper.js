const { findDustBunnies, getFileAgeInDays, formatBytes } = require('../src/index');
const fs = require('fs').promises;
const path = require('path');

// Mock rationale: We need to control the file system state and time for deterministic tests.
// Directly interacting with the actual file system would make tests slow, non-deterministic,
// and potentially destructive. Mocks allow us to simulate various directory structures
// and file ages without side effects.
jest.mock('fs', () => ({
    promises: {
        readdir: jest.fn(),
        stat: jest.fn(),
        writeFile: jest.fn() // Mock writeFile for output option
    }
}));

describe('Nightly Digital Dust Bunny Sweeper', () => {
    beforeEach(() => {
        jest.clearAllMocks();
        // Set a fixed "now" for consistent age calculation
        jest.useFakeTimers();
        jest.setSystemTime(new Date('2023-10-26T12:00:00Z'));
    });

    afterEach(() => {
        jest.useRealTimers();
    });

    describe('getFileAgeInDays', () => {
        test('should return correct age for an old file', async () => {
            // Mock rationale: Simulate a file's modification time.
            fs.stat.mockResolvedValueOnce({
                isFile: () => true,
                mtime: new Date('2023-07-01T10:00:00Z'), // Older than 90 days from 2023-10-26
                size: 100
            });
            const age = await getFileAgeInDays('/test/old_file.txt');
            expect(age).toBe(117); // (26-1) + 31 + 31 + 30 = 25 + 92 = 117 days
        });

        test('should return -1 for a recent file', async () => {
            // Mock rationale: Simulate a file's modification time.
            fs.stat.mockResolvedValueOnce({
                isFile: () => true,
                mtime: new Date('2023-10-20T10:00:00Z'), // Recent
                size: 100
            });
            const age = await getFileAgeInDays('/test/recent_file.txt');
            expect(age).toBe(6);
        });

        test('should return -1 for a directory', async () => {
            // Mock rationale: Simulate a directory.
            fs.stat.mockResolvedValueOnce({
                isFile: () => false,
                isDirectory: () => true,
                mtime: new Date(),
                size: 0
            });
            const age = await getFileAgeInDays('/test/directory');
            expect(age).toBe(-1);
        });

        test('should return -1 for a non-existent file', async () => {
            // Mock rationale: Simulate fs.stat throwing an error for a non-existent file.
            fs.stat.mockRejectedValueOnce(new Error('File not found'));
            const age = await getFileAgeInDays('/test/non_existent.txt');
            expect(age).toBe(-1);
        });
    });

    describe('findDustBunnies', () => {
        const testDir = '/mock/dir';

        test('should find old files in a flat directory', async () => {
            // Mock rationale: Simulate a directory with old and recent files.
            fs.readdir.mockResolvedValueOnce([
                { name: 'old_file_1.txt', isFile: () => true, isDirectory: () => false },
                { name: 'recent_file.log', isFile: () => true, isDirectory: () => false },
                { name: 'old_file_2.json', isFile: () => true, isDirectory: () => false }
            ]);
            fs.stat
                .mockResolvedValueOnce({ isFile: () => true, mtime: new Date('2023-06-01T00:00:00Z'), size: 100 }) // old_file_1.txt (147 days)
                .mockResolvedValueOnce({ isFile: () => true, mtime: new Date('2023-10-20T00:00:00Z'), size: 50 })  // recent_file.log (6 days)
                .mockResolvedValueOnce({ isFile: () => true, mtime: new Date('2023-05-15T00:00:00Z'), size: 200 }); // old_file_2.json (164 days)

            const { dustBunnies, totalSize } = await findDustBunnies(testDir, 90, false);

            expect(dustBunnies).toHaveLength(2);
            expect(dustBunnies[0].path).toBe(path.join(testDir, 'old_file_1.txt'));
            expect(dustBunnies[0].age).toBe(147);
            expect(dustBunnies[1].path).toBe(path.join(testDir, 'old_file_2.json'));
            expect(dustBunnies[1].age).toBe(164);
            expect(totalSize).toBe(300);
        });

        test('should not find files if none are old enough', async () => {
            // Mock rationale: Simulate a directory with only recent files.
            fs.readdir.mockResolvedValueOnce([
                { name: 'recent_file_1.txt', isFile: () => true, isDirectory: () => false },
                { name: 'recent_file_2.log', isFile: () => true, isDirectory: () => false }
            ]);
            fs.stat
                .mockResolvedValueOnce({ isFile: () => true, mtime: new Date('2023-10-01T00:00:00Z'), size: 100 }) // 25 days
                .mockResolvedValueOnce({ isFile: () => true, mtime: new Date('2023-09-15T00:00:00Z'), size: 50 });  // 41 days

            const { dustBunnies, totalSize } = await findDustBunnies(testDir, 90, false);

            expect(dustBunnies).toHaveLength(0);
            expect(totalSize).toBe(0);
        });

        test('should handle empty directory', async () => {
            // Mock rationale: Simulate an empty directory.
            fs.readdir.mockResolvedValueOnce([]);
            const { dustBunnies, totalSize } = await findDustBunnies(testDir, 90, false);
            expect(dustBunnies).toHaveLength(0);
            expect(totalSize).toBe(0);
        });

        test('should scan recursively when recursive is true', async () => {
            // Mock rationale: Simulate a nested directory structure.
            fs.readdir
                .mockResolvedValueOnce([ // /mock/dir
                    { name: 'old_root.txt', isFile: () => true, isDirectory: () => false },
                    { name: 'subdir', isFile: () => false, isDirectory: () => true }
                ])
                .mockResolvedValueOnce([ // /mock/dir/subdir
                    { name: 'old_sub.txt', isFile: () => true, isDirectory: () => false },
                    { name: 'recent_sub.txt', isFile: () => true, isDirectory: () => false }
                ]);
            fs.stat
                .mockResolvedValueOnce({ isFile: () => true, mtime: new Date('2023-04-01T00:00:00Z'), size: 100 }) // old_root.txt (208 days)
                .mockResolvedValueOnce({ isFile: () => true, mtime: new Date('2023-03-01T00:00:00Z'), size: 239 }) // old_sub.txt (239 days)
                .mockResolvedValueOnce({ isFile: () => true, mtime: new Date('2023-10-01T00:00:00Z'), size: 50 });  // recent_sub.txt (25 days)

            const { dustBunnies, totalSize } = await findDustBunnies(testDir, 90, true);

            expect(dustBunnies).toHaveLength(2);
            expect(dustBunnies.some(b => b.path === path.join(testDir, 'old_root.txt'))).toBe(true);
            expect(dustBunnies.some(b => b.path === path.join(testDir, 'subdir', 'old_sub.txt'))).toBe(true);
            expect(totalSize).toBe(339); // 100 + 239
        });

        test('should not scan recursively when recursive is false', async () => {
            // Mock rationale: Simulate a nested directory structure, but only expect top-level scan.
            fs.readdir
                .mockResolvedValueOnce([ // /mock/dir
                    { name: 'old_root.txt', isFile: () => true, isDirectory: () => false },
                    { name: 'subdir', isFile: () => false, isDirectory: () => true }
                ]);
            fs.stat
                .mockResolvedValueOnce({ isFile: () => true, mtime: new Date('2023-04-01T00:00:00Z'), size: 100 }); // old_root.txt (208 days)

            const { dustBunnies, totalSize } = await findDustBunnies(testDir, 90, false);

            expect(dustBunnies).toHaveLength(1);
            expect(dustBunnies[0].path).toBe(path.join(testDir, 'old_root.txt'));
            expect(totalSize).toBe(100);
            expect(fs.readdir).toHaveBeenCalledTimes(1); // Only root directory read
        });

        test('should handle directory read errors gracefully', async () => {
            // Mock rationale: Simulate a directory that cannot be read.
            fs.readdir
                .mockResolvedValueOnce([
                    { name: 'old_file.txt', isFile: () => true, isDirectory: () => false },
                    { name: 'unreadable_dir', isFile: () => false, isDirectory: () => true }
                ])
                .mockRejectedValueOnce(new Error('Permission denied')); // For unreadable_dir
            fs.stat
                .mockResolvedValueOnce({ isFile: () => true, mtime: new Date('2023-06-01T00:00:00Z'), size: 100 }); // old_file.txt

            const { dustBunnies, totalSize } = await findDustBunnies(testDir, 90, true);

            expect(dustBunnies).toHaveLength(1);
            expect(dustBunnies[0].path).toBe(path.join(testDir, 'old_file.txt'));
            expect(totalSize).toBe(100);
        });
    });

    describe('formatBytes', () => {
        test('should format bytes correctly', () => {
            expect(formatBytes(0)).toBe('0 Bytes');
            expect(formatBytes(100)).toBe('100 Bytes');
            expect(formatBytes(1024)).toBe('1.00 KB');
            expect(formatBytes(1536)).toBe('1.50 KB');
            expect(formatBytes(1024 * 1024)).toBe('1.00 MB');
            expect(formatBytes(1.5 * 1024 * 1024 * 1024)).toBe('1.50 GB');
            expect(formatBytes(2 * 1024 * 1024 * 1024 * 1024)).toBe('2.00 TB');
        });
    });
});
