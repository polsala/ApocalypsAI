const { getFileDustScore, scanDirectory, main } = require('../src/index');
const fs = require('fs').promises;
const path = require('path');

// Mock rationale: We need to control file system interactions to ensure deterministic tests
// without actually touching the disk. This allows us to simulate different file structures
// and modification/access times, which are central to the utility's logic.
jest.mock('fs', () => ({
    promises: {
        readdir: jest.fn(),
        stat: jest.fn(),
    },
}));

// Mock console.log and console.error to capture output and prevent actual logging during tests.
const mockLog = jest.spyOn(console, 'log').mockImplementation(() => {});
const mockError = jest.spyOn(console, 'error').mockImplementation(() => {});
// Mock process.exit to prevent tests from terminating the Node.js process.
const mockExit = jest.spyOn(process, 'exit').mockImplementation(() => {});

describe('Nightly Byte-Breeze Whisperer', () => {
    beforeEach(() => {
        jest.clearAllMocks();
        // Reset Date.now() for consistent dust score calculation across tests.
        // Mock rationale: The 'digital dust' score is time-dependent. Fixing Date.now()
        // ensures that calculations like 'days since modified' are always the same.
        jest.spyOn(Date, 'now').mockReturnValue(new Date('2024-01-01T00:00:00.000Z').getTime());
    });

    afterAll(() => {
        jest.restoreAllMocks();
    });

    describe('getFileDustScore', () => {
        test('should return null for non-file entries', async () => {
            fs.stat.mockResolvedValue({ isFile: () => false });
            const result = await getFileDustScore('/path/to/dir');
            expect(result).toBeNull();
        });

        test('should calculate dust score correctly for an old file', async () => {
            const fileMtime = new Date('2022-01-01T00:00:00.000Z').getTime(); // 2 years old
            const fileAtime = new Date('2022-06-01T00:00:00.000Z').getTime(); // 1.5 years old
            fs.stat.mockResolvedValue({
                isFile: () => true,
                mtimeMs: fileMtime,
                atimeMs: fileAtime,
            });

            const result = await getFileDustScore('/path/to/old_file.txt');
            expect(result).not.toBeNull();
            expect(result.filePath).toBe('/path/to/old_file.txt');
            // Date.now() is 2024-01-01. mtime is 2022-01-01. Difference is 2 years = 730 days.
            // atime is 2022-06-01. Difference is 1.5 years = 549 days (approx, due to leap year/month lengths).
            // Max of (730, 549) is 730.
            expect(result.dustScore).toBe(730);
        });

        test('should calculate dust score correctly for a recently modified file', async () => {
            const fileMtime = new Date('2023-12-20T00:00:00.000Z').getTime(); // 12 days old
            const fileAtime = new Date('2023-12-25T00:00:00.000Z').getTime(); // 7 days old
            fs.stat.mockResolvedValue({
                isFile: () => true,
                mtimeMs: fileMtime,
                atimeMs: fileAtime,
            });

            const result = await getFileDustScore('/path/to/recent_file.txt');
            expect(result).not.toBeNull();
            expect(result.dustScore).toBe(12); // Max of (12, 7) is 12
        });

        test('should return null if stat fails', async () => {
            fs.stat.mockRejectedValue(new Error('Permission denied'));
            const result = await getFileDustScore('/path/to/unreadable_file.txt');
            expect(result).toBeNull();
        });
    });

    describe('scanDirectory', () => {
        test('should return empty array for an empty directory', async () => {
            fs.readdir.mockResolvedValue([]);
            const result = await scanDirectory('/empty/dir');
            expect(result).toEqual([]);
        });

        test('should find forgotten files in a flat directory', async () => {
            fs.readdir.mockResolvedValue([
                { name: 'old_file.txt', isDirectory: () => false, isFile: () => true },
                { name: 'recent_file.txt', isDirectory: () => false, isFile: () => true },
            ]);
            // Mock stat for old_file.txt (dust > 90)
            fs.stat.mockImplementation((filePath) => {
                if (filePath.includes('old_file.txt')) {
                    return Promise.resolve({
                        isFile: () => true,
                        mtimeMs: new Date('2023-01-01T00:00:00.000Z').getTime(), // 365 days old
                        atimeMs: new Date('2023-01-01T00:00:00.000Z').getTime(),
                    });
                }
                // Mock stat for recent_file.txt (dust < 90)
                return Promise.resolve({
                    isFile: () => true,
                    mtimeMs: new Date('2023-11-01T00:00:00.000Z').getTime(), // 61 days old
                    atimeMs: new Date('2023-11-01T00:00:00.000Z').getTime(),
                });
            });

            const result = await scanDirectory('/test/dir', 90);
            expect(result.length).toBe(1);
            expect(result[0].filePath).toContain('old_file.txt');
            expect(result[0].dustScore).toBe(365);
        });

        test('should find forgotten files in nested directories', async () => {
            fs.readdir
                .mockResolvedValueOnce([
                    { name: 'subdir', isDirectory: () => true, isFile: () => false },
                    { name: 'recent_root.txt', isDirectory: () => false, isFile: () => true },
                ])
                .mockResolvedValueOnce([
                    { name: 'old_nested.txt', isDirectory: () => false, isFile: () => true },
                ]);

            fs.stat.mockImplementation((filePath) => {
                if (filePath.includes('old_nested.txt')) {
                    return Promise.resolve({
                        isFile: () => true,
                        mtimeMs: new Date('2023-01-01T00:00:00.000Z').getTime(), // 365 days old
                        atimeMs: new Date('2023-01-01T00:00:00.000Z').getTime(),
                    });
                }
                return Promise.resolve({
                    isFile: () => true,
                    mtimeMs: new Date('2023-11-01T00:00:00.000Z').getTime(), // 61 days old
                    atimeMs: new Date('2023-11-01T00:00:00.000Z').getTime(),
                });
            });

            const result = await scanDirectory('/test/root', 90);
            expect(result.length).toBe(1);
            expect(result[0].filePath).toContain(path.join('subdir', 'old_nested.txt'));
            expect(result[0].dustScore).toBe(365);
        });

        test('should handle readdir errors gracefully', async () => {
            fs.readdir.mockRejectedValue(new Error('Permission denied'));
            const result = await scanDirectory('/unreadable/dir');
            expect(result).toEqual([]);
        });
    });

    describe('main', () => {
        test('should print usage and exit if no path is provided', async () => {
            process.argv = ['node', 'index.js'];
            await main();
            expect(mockError).toHaveBeenCalledWith("Usage: node src/index.js <directory_to_scan> [minimum_dust_days (default: 90)]");
            expect(mockExit).toHaveBeenCalledWith(1);
        });

        test('should use default minDustDays if not provided or invalid', async () => {
            process.argv = ['node', 'index.js', '/test/path'];
            fs.readdir.mockResolvedValue([]); // No files found
            await main();
            expect(mockLog).toHaveBeenCalledWith(expect.stringContaining("at least 90 days of digital dust"));
            expect(mockExit).not.toHaveBeenCalled(); // Should not exit on successful scan
        });

        test('should report no forgotten files if none meet criteria', async () => {
            process.argv = ['node', 'index.js', '/test/path', '100'];
            fs.readdir.mockResolvedValue([
                { name: 'recent.txt', isDirectory: () => false, isFile: () => true },
            ]);
            fs.stat.mockResolvedValue({
                isFile: () => true,
                mtimeMs: new Date('2023-12-01T00:00:00.000Z').getTime(), // 31 days old
                atimeMs: new Date('2023-12-01T00:00:00.000Z').getTime(),
            });

            await main();
            expect(mockLog).toHaveBeenCalledWith("The Byte-Breeze finds no truly forgotten files here. All is well!");
        });

        test('should list forgotten files sorted by dust score', async () => {
            process.argv = ['node', 'index.js', '/test/path', '50'];
            fs.readdir.mockResolvedValue([
                { name: 'file_a.txt', isDirectory: () => false, isFile: () => true },
                { name: 'file_b.txt', isDirectory: () => false, isFile: () => true },
                { name: 'file_c.txt', isDirectory: () => false, isFile: () => true },
            ]);
            fs.stat.mockImplementation((filePath) => {
                if (filePath.includes('file_a.txt')) {
                    return Promise.resolve({
                        isFile: () => true,
                        mtimeMs: new Date('2023-01-01T00:00:00.000Z').getTime(), // 365 days old
                        atimeMs: new Date('2023-01-01T00:00:00.000Z').getTime(),
                    });
                } else if (filePath.includes('file_b.txt')) {
                    return Promise.resolve({
                        isFile: () => true,
                        mtimeMs: new Date('2023-06-01T00:00:00.000Z').getTime(), // 214 days old
                        atimeMs: new Date('2023-06-01T00:00:00.000Z').getTime(),
                    });
                }
                // file_c.txt (dust < 50)
                return Promise.resolve({
                    isFile: () => true,
                    mtimeMs: new Date('2023-11-15T00:00:00.000Z').getTime(), // 47 days old
                    atimeMs: new Date('2023-11-15T00:00:00.000Z').getTime(),
                });
            });

            await main();
            expect(mockLog).toHaveBeenCalledWith(expect.stringContaining("The Byte-Breeze whispers about these forgotten files:"));
            expect(mockLog).toHaveBeenCalledWith(expect.stringContaining("[Digital Dust: 365 days] /test/path/file_a.txt"));
            expect(mockLog).toHaveBeenCalledWith(expect.stringContaining("[Digital Dust: 214 days] /test/path/file_b.txt"));
            expect(mockLog).not.toHaveBeenCalledWith(expect.stringContaining("file_c.txt")); // Should not be listed as dust < 50

            // Verify order: file_a (365) should come before file_b (214)
            const logs = mockLog.mock.calls.flat();
            const fileALogIndex = logs.findIndex(log => log.includes('file_a.txt'));
            const fileBLogIndex = logs.findIndex(log => log.includes('file_b.txt'));
            expect(fileALogIndex).toBeLessThan(fileBLogIndex);
        });
    });
});
