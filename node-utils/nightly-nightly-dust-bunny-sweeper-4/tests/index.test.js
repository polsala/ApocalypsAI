const { sweepDigitalDustBunnies } = require('../src/index');
const fs = require('fs').promises;
const path = require('path');

// Mock rationale: We need to simulate file system operations without actually touching the disk.
// This ensures tests are deterministic, fast, and don't leave artifacts.
jest.mock('fs', () => ({
    promises: {
        readdir: jest.fn(),
        stat: jest.fn(),
        rename: jest.fn(),
        mkdir: jest.fn(),
        rmdir: jest.fn(),
    },
}));

describe('sweepDigitalDustBunnies', () => {
    const TARGET_DIR = '/mock/target';
    const SANCTUARY_DIR = '/mock/sanctuary';
    const AGE_THRESHOLD_DAYS = 30;
    const THRESHOLD_MS = AGE_THRESHOLD_DAYS * 24 * 60 * 60 * 1000;
    const NOW = Date.now();

    beforeEach(() => {
        jest.clearAllMocks();
        // Default mocks for common operations
        fs.promises.mkdir.mockResolvedValue(undefined);
        fs.promises.rename.mockResolvedValue(undefined);
        fs.promises.rmdir.mockResolvedValue(undefined);
    });

    test('should sweep old files into the sanctuary and report correctly', async () => {
        // Mock rationale: Simulate a directory with old and new files.
        fs.promises.readdir.mockImplementation(async (dirPath) => {
            if (dirPath === TARGET_DIR) {
                return [
                    { name: 'old_file.txt', isDirectory: () => false, isFile: () => true },
                    { name: 'new_file.txt', isDirectory: () => false, isFile: () => true },
                    { name: 'subdir', isDirectory: () => true, isFile: () => false },
                ];
            }
            if (dirPath === path.join(TARGET_DIR, 'subdir')) {
                return [
                    { name: 'another_old_file.log', isDirectory: () => false, isFile: () => true },
                ];
            }
            return [];
        });

        // Mock rationale: Simulate file stats for old and new files.
        fs.promises.stat.mockImplementation(async (filePath) => {
            if (filePath === path.join(TARGET_DIR, 'old_file.txt')) {
                return { mtimeMs: NOW - THRESHOLD_MS - 1000, size: 100 }; // Older than threshold
            }
            if (filePath === path.join(TARGET_DIR, 'new_file.txt')) {
                return { mtimeMs: NOW - THRESHOLD_MS + 1000, size: 50 }; // Newer than threshold
            }
            if (filePath === path.join(TARGET_DIR, 'subdir', 'another_old_file.log')) {
                return { mtimeMs: NOW - THRESHOLD_MS - 5000, size: 200 }; // Older than threshold
            }
            return { mtimeMs: NOW, size: 0 }; // Default for directories or other files
        });

        const { sweptCount, sweptSize } = await sweepDigitalDustBunnies(TARGET_DIR, SANCTUARY_DIR, AGE_THRESHOLD_DAYS);

        expect(sweptCount).toBe(2);
        expect(sweptSize).toBe(300); // 100 + 200

        expect(fs.promises.mkdir).toHaveBeenCalledWith(SANCTUARY_DIR, { recursive: true });
        expect(fs.promises.rename).toHaveBeenCalledWith(
            path.join(TARGET_DIR, 'old_file.txt'),
            path.join(SANCTUARY_DIR, 'old_file.txt')
        );
        expect(fs.promises.rename).toHaveBeenCalledWith(
            path.join(TARGET_DIR, 'subdir', 'another_old_file.log'),
            path.join(SANCTUARY_DIR, 'another_old_file.log')
        );
        expect(fs.promises.rename).not.toHaveBeenCalledWith(
            path.join(TARGET_DIR, 'new_file.txt'),
            expect.any(String)
        );
    });

    test('should remove empty directories after sweeping', async () => {
        // Mock rationale: Simulate a directory that becomes empty after its only file is swept.
        fs.promises.readdir.mockImplementation(async (dirPath) => {
            if (dirPath === TARGET_DIR) {
                return [{ name: 'empty_subdir', isDirectory: () => true, isFile: () => false }];
            }
            if (dirPath === path.join(TARGET_DIR, 'empty_subdir')) {
                // First call: contains a file
                if (fs.promises.rename.mock.calls.length === 0) {
                    return [{ name: 'file_to_sweep.tmp', isDirectory: () => false, isFile: () => true }];
                }
                // Second call (during rmdir check): is empty
                return [];
            }
            return [];
        });

        fs.promises.stat.mockImplementation(async (filePath) => {
            if (filePath === path.join(TARGET_DIR, 'empty_subdir', 'file_to_sweep.tmp')) {
                return { mtimeMs: NOW - THRESHOLD_MS - 1000, size: 10 };
            }
            return { mtimeMs: NOW, size: 0 };
        });

        await sweepDigitalDustBunnies(TARGET_DIR, SANCTUARY_DIR, AGE_THRESHOLD_DAYS);

        expect(fs.promises.rename).toHaveBeenCalledWith(
            path.join(TARGET_DIR, 'empty_subdir', 'file_to_sweep.tmp'),
            path.join(SANCTUARY_DIR, 'file_to_sweep.tmp')
        );
        expect(fs.promises.rmdir).toHaveBeenCalledWith(path.join(TARGET_DIR, 'empty_subdir'));
    });

    test('should not sweep new files', async () => {
        // Mock rationale: Simulate a directory containing only new files.
        fs.promises.readdir.mockResolvedValue([
            { name: 'recent_doc.pdf', isDirectory: () => false, isFile: () => true },
        ]);
        fs.promises.stat.mockResolvedValue({ mtimeMs: NOW - THRESHOLD_MS + 1000, size: 1024 }); // Newer

        const { sweptCount, sweptSize } = await sweepDigitalDustBunnies(TARGET_DIR, SANCTUARY_DIR, AGE_THRESHOLD_DAYS);

        expect(sweptCount).toBe(0);
        expect(sweptSize).toBe(0);
        expect(fs.promises.rename).not.toHaveBeenCalled();
    });

    test('should handle non-existent target directory gracefully', async () => {
        // Mock rationale: Simulate fs.readdir throwing ENOENT for the target directory.
        fs.promises.readdir.mockImplementation(async (dirPath) => {
            if (dirPath === TARGET_DIR) {
                const error = new Error('No such file or directory');
                error.code = 'ENOENT';
                throw error;
            }
            return [];
        });

        const consoleWarnSpy = jest.spyOn(console, 'warn').mockImplementation(() => {});

        const { sweptCount, sweptSize } = await sweepDigitalDustBunnies(TARGET_DIR, SANCTUARY_DIR, AGE_THRESHOLD_DAYS);

        expect(sweptCount).toBe(0);
        expect(sweptSize).toBe(0);
        expect(consoleWarnSpy).toHaveBeenCalledWith(expect.stringContaining('Target directory not found'));
        expect(fs.promises.mkdir).toHaveBeenCalledWith(SANCTUARY_DIR, { recursive: true }); // Sanctuary should still be ensured
        expect(fs.promises.rename).not.toHaveBeenCalled();

        consoleWarnSpy.mockRestore();
    });

    test('should handle file system errors during rename', async () => {
        // Mock rationale: Simulate a file that exists but rename fails (e.g., permissions).
        fs.promises.readdir.mockResolvedValue([
            { name: 'problem_file.txt', isDirectory: () => false, isFile: () => true },
        ]);
        fs.promises.stat.mockResolvedValue({ mtimeMs: NOW - THRESHOLD_MS - 1000, size: 100 });
        fs.promises.rename.mockRejectedValue(new Error('Permission denied'));

        const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});

        const { sweptCount, sweptSize } = await sweepDigitalDustBunnies(TARGET_DIR, SANCTUARY_DIR, AGE_THRESHOLD_DAYS);

        expect(sweptCount).toBe(0); // File not swept due to error
        expect(sweptSize).toBe(0);
        expect(consoleErrorSpy).toHaveBeenCalledWith(expect.stringContaining('Failed to sweep'));
        expect(fs.promises.rename).toHaveBeenCalledTimes(1);

        consoleErrorSpy.mockRestore();
    });

    test('should handle file system errors during rmdir', async () => {
        // Mock rationale: Simulate a directory that becomes empty but rmdir fails.
        fs.promises.readdir.mockImplementation(async (dirPath) => {
            if (dirPath === TARGET_DIR) {
                return [{ name: 'empty_subdir', isDirectory: () => true, isFile: () => false }];
            }
            if (dirPath === path.join(TARGET_DIR, 'empty_subdir')) {
                if (fs.promises.rename.mock.calls.length === 0) {
                    return [{ name: 'file_to_sweep.tmp', isDirectory: () => false, isFile: () => true }];
                }
                return [];
            }
            return [];
        });

        fs.promises.stat.mockImplementation(async (filePath) => {
            if (filePath === path.join(TARGET_DIR, 'empty_subdir', 'file_to_sweep.tmp')) {
                return { mtimeMs: NOW - THRESHOLD_MS - 1000, size: 10 };
            }
            return { mtimeMs: NOW, size: 0 };
        });

        fs.promises.rmdir.mockRejectedValueOnce(new Error('Directory not empty or permission denied'));

        const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});

        await sweepDigitalDustBunnies(TARGET_DIR, SANCTUARY_DIR, AGE_THRESHOLD_DAYS);

        expect(fs.promises.rename).toHaveBeenCalledTimes(1);
        expect(fs.promises.rmdir).toHaveBeenCalledWith(path.join(TARGET_DIR, 'empty_subdir'));
        expect(consoleErrorSpy).toHaveBeenCalledWith(expect.stringContaining('Failed to remove empty directory'));

        consoleErrorSpy.mockRestore();
    });

    test('should not remove non-empty directories', async () => {
        // Mock rationale: Simulate a directory that still contains files after sweeping.
        fs.promises.readdir.mockImplementation(async (dirPath) => {
            if (dirPath === TARGET_DIR) {
                return [{ name: 'mixed_subdir', isDirectory: () => true, isFile: () => false }];
            }
            if (dirPath === path.join(TARGET_DIR, 'mixed_subdir')) {
                // Contains one old file (swept) and one new file (remains)
                if (fs.promises.rename.mock.calls.length === 0) {
                    return [
                        { name: 'old_file.txt', isDirectory: () => false, isFile: () => true },
                        { name: 'new_file.txt', isDirectory: () => false, isFile: () => true },
                    ];
                }
                // After sweeping, only new_file.txt remains
                return [{ name: 'new_file.txt', isDirectory: () => false, isFile: () => true }];
            }
            return [];
        });

        fs.promises.stat.mockImplementation(async (filePath) => {
            if (filePath === path.join(TARGET_DIR, 'mixed_subdir', 'old_file.txt')) {
                return { mtimeMs: NOW - THRESHOLD_MS - 1000, size: 100 };
            }
            if (filePath === path.join(TARGET_DIR, 'mixed_subdir', 'new_file.txt')) {
                return { mtimeMs: NOW - THRESHOLD_MS + 1000, size: 50 };
            }
            return { mtimeMs: NOW, size: 0 };
        });

        await sweepDigitalDustBunnies(TARGET_DIR, SANCTUARY_DIR, AGE_THRESHOLD_DAYS);

        expect(fs.promises.rename).toHaveBeenCalledWith(
            path.join(TARGET_DIR, 'mixed_subdir', 'old_file.txt'),
            path.join(SANCTUARY_DIR, 'old_file.txt')
        );
        expect(fs.promises.rmdir).not.toHaveBeenCalledWith(path.join(TARGET_DIR, 'mixed_subdir'));
    });
});
