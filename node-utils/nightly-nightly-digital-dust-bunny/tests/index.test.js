const { findDustBunnies, sweepDustBunnies } = require('../src/index');
const fs = require('fs').promises;
const path = require('path');
const prompts = require('prompts');

// Mock rationale: We need to simulate file system operations (reading directories,
// getting file stats, deleting files) without actually interacting with the real
// file system. This ensures tests are deterministic, fast, and don't cause
// side effects on the user's machine.
jest.mock('fs', () => ({
    promises: {
        readdir: jest.fn(),
        stat: jest.fn(),
        unlink: jest.fn(),
    }
}));

// Mock rationale: We need to control the interactive prompts for testing
// different user responses (e.g., confirming deletion or cancelling).
jest.mock('prompts', () => jest.fn());

describe('Nightly Digital Dust Bunny Sweeper', () => {
    const MOCK_DIR = '/mock/test/dir';
    const NOW_MS = Date.now();
    const ONE_DAY_MS = 24 * 60 * 60 * 1000;

    beforeEach(() => {
        jest.clearAllMocks();
        // Mock path.join to simply concatenate for easier testing with mock paths
        jest.spyOn(path, 'join').mockImplementation((...args) => args.join('/'));
    });

    afterEach(() => {
        jest.restoreAllMocks();
    });

    describe('findDustBunnies', () => {
        test('should find no dust bunnies if directory is empty', async () => {
            fs.readdir.mockResolvedValueOnce([]); // Empty directory
            const bunnies = await findDustBunnies(MOCK_DIR, 30);
            expect(bunnies).toEqual([]);
            expect(fs.readdir).toHaveBeenCalledWith(MOCK_DIR, { withFileTypes: true });
        });

        test('should find files older than the specified age', async () => {
            const oldFile1Path = `${MOCK_DIR}/old_file_1.txt`;
            const oldFile2Path = `${MOCK_DIR}/subdir/old_file_2.log`;
            const newFilePath = `${MOCK_DIR}/new_file.js`;

            fs.readdir
                .mockResolvedValueOnce([ // MOCK_DIR contents
                    { name: 'old_file_1.txt', isDirectory: () => false, isFile: () => true },
                    { name: 'new_file.js', isDirectory: () => false, isFile: () => true },
                    { name: 'subdir', isDirectory: () => true, isFile: () => false }
                ])
                .mockResolvedValueOnce([ // MOCK_DIR/subdir contents
                    { name: 'old_file_2.log', isDirectory: () => false, isFile: () => true }
                ]);

            fs.stat
                .mockImplementation(async (filePath) => {
                    if (filePath === oldFile1Path) {
                        return { mtimeMs: NOW_MS - (31 * ONE_DAY_MS) }; // 31 days old
                    }
                    if (filePath === oldFile2Path) {
                        return { mtimeMs: NOW_MS - (40 * ONE_DAY_MS) }; // 40 days old
                    }
                    if (filePath === newFilePath) {
                        return { mtimeMs: NOW_MS - (10 * ONE_DAY_MS) }; // 10 days old
                    }
                    throw new Error('File not found in mock');
                });

            const bunnies = await findDustBunnies(MOCK_DIR, 30); // Threshold: 30 days
            expect(bunnies.length).toBe(2);
            expect(bunnies.some(b => b.path === oldFile1Path)).toBe(true);
            expect(bunnies.some(b => b.path === oldFile2Path)).toBe(true);
            expect(bunnies.some(b => b.path === newFilePath)).toBe(false); // Should not be included
        });

        test('should ignore specified directories like node_modules', async () => {
            const oldFilePath = `${MOCK_DIR}/node_modules/old_dep.js`;
            fs.readdir
                .mockResolvedValueOnce([
                    { name: 'node_modules', isDirectory: () => true, isFile: () => false }
                ])
                .mockResolvedValueOnce([ // Contents of node_modules
                    { name: 'old_dep.js', isDirectory: () => false, isFile: () => true }
                ]);
            fs.stat.mockResolvedValue({ mtimeMs: NOW_MS - (100 * ONE_DAY_MS) }); // Very old

            const bunnies = await findDustBunnies(MOCK_DIR, 30);
            expect(bunnies).toEqual([]); // node_modules should be skipped
            expect(fs.stat).not.toHaveBeenCalledWith(oldFilePath);
        });

        test('should handle errors during readdir gracefully', async () => {
            fs.readdir.mockRejectedValueOnce(new Error('Permission denied'));
            const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
            const bunnies = await findDustBunnies(MOCK_DIR, 30);
            expect(bunnies).toEqual([]);
            expect(consoleErrorSpy).toHaveBeenCalledWith(expect.stringContaining('Error reading directory'));
            consoleErrorSpy.mockRestore();
        });

        test('should handle errors during stat gracefully', async () => {
            const fileWithErrorPath = `${MOCK_DIR}/error_file.txt`;
            fs.readdir.mockResolvedValueOnce([
                { name: 'error_file.txt', isDirectory: () => false, isFile: () => true }
            ]);
            fs.stat.mockRejectedValueOnce(new Error('File not found'));
            const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
            const bunnies = await findDustBunnies(MOCK_DIR, 30);
            expect(bunnies).toEqual([]);
            expect(consoleErrorSpy).toHaveBeenCalledWith(expect.stringContaining('Error getting stats for file'));
            consoleErrorSpy.mockRestore();
        });
    });

    describe('sweepDustBunnies', () => {
        const mockDustBunnies = [
            { path: `${MOCK_DIR}/bunny1.txt`, mtime: 'mock_date_1' },
            { path: `${MOCK_DIR}/bunny2.log`, mtime: 'mock_date_2' }
        ];

        test('should not delete files in dry run mode', async () => {
            const consoleLogSpy = jest.spyOn(console, 'log').mockImplementation(() => {});
            await sweepDustBunnies(mockDustBunnies, true, false);
            expect(fs.unlink).not.toHaveBeenCalled();
            expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining('This was a dry run. No files were deleted.'));
            consoleLogSpy.mockRestore();
        });

        test('should delete files if user confirms', async () => {
            prompts.mockResolvedValueOnce({ value: true }); // User confirms
            const consoleLogSpy = jest.spyOn(console, 'log').mockImplementation(() => {});
            await sweepDustBunnies(mockDustBunnies, false, false);
            expect(fs.unlink).toHaveBeenCalledTimes(mockDustBunnies.length);
            expect(fs.unlink).toHaveBeenCalledWith(mockDustBunnies[0].path);
            expect(fs.unlink).toHaveBeenCalledWith(mockDustBunnies[1].path);
            expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining('Digital dust bunnies swept!'));
            consoleLogSpy.mockRestore();
        });

        test('should not delete files if user cancels', async () => {
            prompts.mockResolvedValueOnce({ value: false }); // User cancels
            const consoleLogSpy = jest.spyOn(console, 'log').mockImplementation(() => {});
            await sweepDustBunnies(mockDustBunnies, false, false);
            expect(fs.unlink).not.toHaveBeenCalled();
            expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining('Sweeping cancelled.'));
            consoleLogSpy.mockRestore();
        });

        test('should delete files automatically if autoYes is true', async () => {
            const consoleLogSpy = jest.spyOn(console, 'log').mockImplementation(() => {});
            await sweepDustBunnies(mockDustBunnies, false, true);
            expect(prompts).not.toHaveBeenCalled(); // No prompt
            expect(fs.unlink).toHaveBeenCalledTimes(mockDustBunnies.length);
            expect(fs.unlink).toHaveBeenCalledWith(mockDustBunnies[0].path);
            expect(fs.unlink).toHaveBeenCalledWith(mockDustBunnies[1].path);
            expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining('Digital dust bunnies swept!'));
            consoleLogSpy.mockRestore();
        });

        test('should handle unlink errors gracefully', async () => {
            prompts.mockResolvedValueOnce({ value: true });
            fs.unlink
                .mockRejectedValueOnce(new Error('Permission denied')) // First file fails
                .mockResolvedValueOnce(); // Second file succeeds

            const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
            const consoleLogSpy = jest.spyOn(console, 'log').mockImplementation(() => {});

            await sweepDustBunnies(mockDustBunnies, false, false);

            expect(fs.unlink).toHaveBeenCalledTimes(mockDustBunnies.length);
            expect(consoleErrorSpy).toHaveBeenCalledWith(expect.stringContaining(`Failed to sweep ${mockDustBunnies[0].path}`));
            expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining(`Swept: ${mockDustBunnies[1].path}`));
            consoleErrorSpy.mockRestore();
            consoleLogSpy.mockRestore();
        });

        test('should log message if no dust bunnies are found', async () => {
            const consoleLogSpy = jest.spyOn(console, 'log').mockImplementation(() => {});
            await sweepDustBunnies([], false, false);
            expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining('No digital dust bunnies found.'));
            expect(prompts).not.toHaveBeenCalled();
            expect(fs.unlink).not.toHaveBeenCalled();
            consoleLogSpy.mockRestore();
        });
    });
});
