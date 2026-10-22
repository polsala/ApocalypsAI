const { findDigitalEchoes, archiveEcho, isFileOld, getFileStats } = require('../src/index');
const fs = require('fs').promises;
const path = require('path');

// Mock rationale: We need to simulate file system interactions (reading directories, getting file stats, moving files)
// without actually touching the disk. This ensures tests are deterministic, fast, and don't leave artifacts.
jest.mock('fs', () => ({
    promises: {
        readdir: jest.fn(),
        stat: jest.fn(),
        mkdir: jest.fn(),
        rename: jest.fn()
    }
}));

describe('Nightly Digital Echo Purifier', () => {
    beforeEach(() => {
        jest.clearAllMocks();
    });

    describe('getFileStats', () => {
        test('should return stats for an existing file', async () => {
            const mockStats = { isFile: () => true, mtime: new Date() };
            fs.stat.mockResolvedValue(mockStats);
            const stats = await getFileStats('/test/file.txt');
            expect(stats).toBe(mockStats);
            expect(fs.stat).toHaveBeenCalledWith('/test/file.txt');
        });

        test('should return null and log warning for a non-existent file', async () => {
            fs.stat.mockRejectedValue(new Error('File not found'));
            const consoleWarnSpy = jest.spyOn(console, 'warn').mockImplementation(() => {});
            const stats = await getFileStats('/test/nonexistent.txt');
            expect(stats).toBeNull();
            expect(consoleWarnSpy).toHaveBeenCalledWith(expect.stringContaining('Could not get stats for /test/nonexistent.txt'));
            consoleWarnSpy.mockRestore();
        });
    });

    describe('isFileOld', () => {
        const now = new Date();
        const oldDate = new Date(now.getTime() - (91 * 24 * 60 * 60 * 1000)); // 91 days ago
        const recentDate = new Date(now.getTime() - (10 * 24 * 60 * 60 * 1000)); // 10 days ago

        test('should return true for a file older than threshold', () => {
            const mockStats = { isFile: () => true, mtime: oldDate };
            expect(isFileOld(mockStats, 90)).toBe(true);
        });

        test('should return false for a file newer than threshold', () => {
            const mockStats = { isFile: () => true, mtime: recentDate };
            expect(isFileOld(mockStats, 90)).toBe(false);
        });

        test('should return false for a directory', () => {
            const mockStats = { isFile: () => false, mtime: oldDate };
            expect(isFileOld(mockStats, 90)).toBe(false);
        });

        test('should return false if stats are null', () => {
            expect(isFileOld(null, 90)).toBe(false);
        });
    });

    describe('findDigitalEchoes', () => {
        const mockDir = '/test/project';
        const now = new Date();
        const oldFileMtime = new Date(now.getTime() - (100 * 24 * 60 * 60 * 1000)); // 100 days ago
        const recentFileMtime = new Date(now.getTime() - (10 * 24 * 60 * 60 * 1000)); // 10 days ago

        test('should find old files in a single directory', async () => {
            fs.readdir.mockResolvedValueOnce([
                { name: 'old_file.txt', isDirectory: () => false, isFile: () => true },
                { name: 'recent_file.js', isDirectory: () => false, isFile: () => true },
                { name: 'subdir', isDirectory: () => true, isFile: () => false }
            ]);
            fs.stat.mockImplementation((filePath) => {
                if (filePath === path.join(mockDir, 'old_file.txt')) {
                    return Promise.resolve({ isFile: () => true, mtime: oldFileMtime });
                }
                if (filePath === path.join(mockDir, 'recent_file.js')) {
                    return Promise.resolve({ isFile: () => true, mtime: recentFileMtime });
                }
                return Promise.resolve({ isFile: () => false, isDirectory: () => true }); // for subdir
            });
            fs.readdir.mockResolvedValueOnce([]); // for subdir

            const echoes = await findDigitalEchoes(mockDir, 90);
            expect(echoes).toEqual([path.join(mockDir, 'old_file.txt')]);
            expect(fs.readdir).toHaveBeenCalledWith(mockDir, { withFileTypes: true });
            expect(fs.stat).toHaveBeenCalledTimes(3); // old_file, recent_file, subdir
        });

        test('should find old files recursively', async () => {
            const subDir = path.join(mockDir, 'subdir');
            fs.readdir
                .mockResolvedValueOnce([ // For mockDir
                    { name: 'old_file.txt', isDirectory: () => false, isFile: () => true },
                    { name: 'subdir', isDirectory: () => true, isFile: () => false }
                ])
                .mockResolvedValueOnce([ // For subdir
                    { name: 'another_old.log', isDirectory: () => false, isFile: () => true },
                    { name: 'recent_config.json', isDirectory: () => false, isFile: () => true }
                ]);

            fs.stat.mockImplementation((filePath) => {
                if (filePath === path.join(mockDir, 'old_file.txt')) {
                    return Promise.resolve({ isFile: () => true, mtime: oldFileMtime });
                }
                if (filePath === path.join(mockDir, 'subdir')) {
                    return Promise.resolve({ isFile: () => false, isDirectory: () => true });
                }
                if (filePath === path.join(subDir, 'another_old.log')) {
                    return Promise.resolve({ isFile: () => true, mtime: oldFileMtime });
                }
                if (filePath === path.join(subDir, 'recent_config.json')) {
                    return Promise.resolve({ isFile: () => true, mtime: recentFileMtime });
                }
                return Promise.resolve({ isFile: () => false, isDirectory: () => true });
            });

            const echoes = await findDigitalEchoes(mockDir, 90);
            expect(echoes).toEqual([
                path.join(mockDir, 'old_file.txt'),
                path.join(subDir, 'another_old.log')
            ]);
            expect(fs.readdir).toHaveBeenCalledTimes(2);
            expect(fs.stat).toHaveBeenCalledTimes(4);
        });

        test('should handle empty directory', async () => {
            fs.readdir.mockResolvedValueOnce([]);
            const echoes = await findDigitalEchoes(mockDir, 90);
            expect(echoes).toEqual([]);
            expect(fs.readdir).toHaveBeenCalledWith(mockDir, { withFileTypes: true });
        });

        test('should handle directory read error', async () => {
            fs.readdir.mockRejectedValueOnce(new Error('Permission denied'));
            const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
            const echoes = await findDigitalEchoes(mockDir, 90);
            expect(echoes).toEqual([]);
            expect(consoleErrorSpy).toHaveBeenCalledWith(expect.stringContaining('Error scanning directory'));
            consoleErrorSpy.mockRestore();
        });
    });

    describe('archiveEcho', () => {
        const mockFilePath = '/test/project/old_file.txt';
        const mockArchiveDir = '/test/_digital_echoes_archive';
        const mockBaseDir = '/test/project'; // The base directory passed to archiveEcho
        const mockDestPath = path.join(mockArchiveDir, 'old_file.txt'); // Relative to mockBaseDir

        test('should successfully archive a file', async () => {
            fs.mkdir.mockResolvedValue(undefined);
            fs.rename.mockResolvedValue(undefined);

            const success = await archiveEcho(mockFilePath, mockArchiveDir, mockBaseDir);
            expect(success).toBe(true);
            expect(fs.mkdir).toHaveBeenCalledWith(path.dirname(mockDestPath), { recursive: true });
            expect(fs.rename).toHaveBeenCalledWith(mockFilePath, mockDestPath);
        });

        test('should return false and log error if archiving fails', async () => {
            fs.mkdir.mockResolvedValue(undefined);
            fs.rename.mockRejectedValue(new Error('Permission denied'));
            const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});

            const success = await archiveEcho(mockFilePath, mockArchiveDir, mockBaseDir);
            expect(success).toBe(false);
            expect(consoleErrorSpy).toHaveBeenCalledWith(expect.stringContaining('Failed to archive'));
            consoleErrorSpy.mockRestore();
        });
    });
});
