const { findDustBunnies } = require('../src/index');
const fs = require('fs').promises;
const path = require('path');

// Mock rationale: We need to simulate file system operations without actually touching the disk
// to ensure deterministic and offline tests. This prevents tests from creating/deleting real files
// and ensures consistent results regardless of the host system's file state.
jest.mock('fs', () => ({
    promises: {
        readdir: jest.fn(),
        stat: jest.fn(),
        rmdir: jest.fn(),
        unlink: jest.fn(),
    },
}));

describe('findDustBunnies', () => {
    const mockRoot = '/mock/path';
    const now = Date.now();
    const thirtyDaysAgo = new Date(now - (30 * 24 * 60 * 60 * 1000));
    const sixtyDaysAgo = new Date(now - (60 * 24 * 60 * 60 * 1000));

    beforeEach(() => {
        jest.clearAllMocks();
        // Default mock for stat to return a directory for the root path
        fs.promises.stat.mockImplementation((p) => {
            if (p === mockRoot) {
                return Promise.resolve({ isDirectory: () => true, mtime: new Date() });
            }
            // Default for other paths, assume they are files unless explicitly mocked otherwise
            return Promise.resolve({ isDirectory: () => false, mtime: new Date() });
        });
    });

    test('should report empty directories', async () => {
        // Mock rationale: Simulate a directory structure where 'emptyDir' is found to be empty
        // after recursive scanning.
        fs.promises.readdir
            .mockResolvedValueOnce([{ name: 'emptyDir', isDirectory: () => true }]) // mockRoot content
            .mockResolvedValueOnce([]); // emptyDir content

        const result = await findDustBunnies(mockRoot, {});
        expect(result.emptyDirs).toEqual([path.join(mockRoot, 'emptyDir')]);
        expect(result.oldFiles).toEqual([]);
        expect(fs.promises.rmdir).not.toHaveBeenCalled(); // Dry run, no deletion
    });

    test('should report old files', async () => {
        // Mock rationale: Simulate a directory containing two files, one older than the threshold
        // and one newer, to test age-based filtering.
        fs.promises.readdir
            .mockResolvedValueOnce([
                { name: 'oldFile.txt', isDirectory: () => false },
                { name: 'newFile.txt', isDirectory: () => false },
            ]);

        fs.promises.stat
            .mockImplementation((p) => {
                if (p === mockRoot) return Promise.resolve({ isDirectory: () => true, mtime: new Date() });
                if (p === path.join(mockRoot, 'oldFile.txt')) {
                    return Promise.resolve({ isDirectory: () => false, mtime: sixtyDaysAgo });
                }
                if (p === path.join(mockRoot, 'newFile.txt')) {
                    return Promise.resolve({ isDirectory: () => false, mtime: thirtyDaysAgo });
                }
                return Promise.reject(new Error('File not found')); // Fallback for unexpected paths
            });

        const result = await findDustBunnies(mockRoot, { maxAgeDays: 45 }); // Files older than 45 days
        expect(result.emptyDirs).toEqual([]);
        expect(result.oldFiles).toEqual([path.join(mockRoot, 'oldFile.txt')]);
        expect(fs.promises.unlink).not.toHaveBeenCalled(); // Dry run, no deletion
    });

    test('should sweep empty directories when --sweep is true', async () => {
        // Mock rationale: Simulate an empty directory and verify that fs.promises.rmdir is called
        // when the sweep option is enabled.
        fs.promises.readdir
            .mockResolvedValueOnce([{ name: 'emptyDir', isDirectory: () => true }])
            .mockResolvedValueOnce([]);

        const result = await findDustBunnies(mockRoot, { sweep: true });
        expect(result.emptyDirs).toEqual([path.join(mockRoot, 'emptyDir')]);
        expect(fs.promises.rmdir).toHaveBeenCalledWith(path.join(mockRoot, 'emptyDir'));
    });

    test('should sweep old files when --sweep is true', async () => {
        // Mock rationale: Simulate an old file and verify that fs.promises.unlink is called
        // when the sweep option is enabled.
        fs.promises.readdir
            .mockResolvedValueOnce([{ name: 'oldFile.txt', isDirectory: () => false }]);

        fs.promises.stat
            .mockImplementation((p) => {
                if (p === mockRoot) return Promise.resolve({ isDirectory: () => true, mtime: new Date() });
                if (p === path.join(mockRoot, 'oldFile.txt')) {
                    return Promise.resolve({ isDirectory: () => false, mtime: sixtyDaysAgo });
                }
                return Promise.reject(new Error('File not found'));
            });

        const result = await findDustBunnies(mockRoot, { sweep: true, maxAgeDays: 45 });
        expect(result.oldFiles).toEqual([path.join(mockRoot, 'oldFile.txt')]);
        expect(fs.promises.unlink).toHaveBeenCalledWith(path.join(mockRoot, 'oldFile.txt'));
    });

    test('should handle non-existent target path gracefully', async () => {
        // Mock rationale: Simulate fs.stat throwing an 'ENOENT' error for the initial target path,
        // indicating it does not exist. The utility should report an error and return empty results.
        fs.promises.stat.mockImplementation((p) => {
            if (p === mockRoot) {
                const error = new Error('No such file or directory');
                error.code = 'ENOENT';
                return Promise.reject(error);
            }
            return Promise.resolve({ isDirectory: () => false, mtime: new Date() });
        });
        const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});

        const result = await findDustBunnies(mockRoot, {});
        expect(result.emptyDirs).toEqual([]);
        expect(result.oldFiles).toEqual([]);
        expect(consoleErrorSpy).toHaveBeenCalledWith(expect.stringContaining(`Target path "${mockRoot}" is not a valid directory.`));
        consoleErrorSpy.mockRestore();
    });

    test('should handle errors during readdir gracefully', async () => {
        // Mock rationale: Simulate fs.readdir throwing an error (e.g., permission denied) for a subdirectory.
        // The utility should log a warning and continue processing other accessible paths.
        fs.promises.readdir
            .mockResolvedValueOnce([{ name: 'subDir', isDirectory: () => true }]) // mockRoot content
            .mockRejectedValueOnce(new Error('Permission denied')); // Error for subDir

        const consoleWarnSpy = jest.spyOn(console, 'warn').mockImplementation(() => {});

        const result = await findDustBunnies(mockRoot, {});
        expect(result.emptyDirs).toEqual([]);
        expect(result.oldFiles).toEqual([]);
        expect(consoleWarnSpy).toHaveBeenCalledWith(expect.stringContaining('Cannot access'));
        consoleWarnSpy.mockRestore();
    });

    test('should not delete files/dirs if sweep is false', async () => {
        // Mock rationale: Ensure that even if empty directories or old files are identified,
        // no deletion functions (rmdir, unlink) are called when the sweep option is false (dry run).
        fs.promises.readdir
            .mockResolvedValueOnce([
                { name: 'emptyDir', isDirectory: () => true },
                { name: 'oldFile.txt', isDirectory: () => false },
            ])
            .mockResolvedValueOnce([]); // for emptyDir

        fs.promises.stat
            .mockImplementation((p) => {
                if (p === mockRoot) return Promise.resolve({ isDirectory: () => true, mtime: new Date() });
                if (p === path.join(mockRoot, 'oldFile.txt')) {
                    return Promise.resolve({ isDirectory: () => false, mtime: sixtyDaysAgo });
                }
                return Promise.reject(new Error('File not found'));
            });

        await findDustBunnies(mockRoot, { maxAgeDays: 45, sweep: false });
        expect(fs.promises.rmdir).not.toHaveBeenCalled();
        expect(fs.promises.unlink).not.toHaveBeenCalled();
    });
});
