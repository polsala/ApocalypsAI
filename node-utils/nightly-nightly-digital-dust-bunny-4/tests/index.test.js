const { findDustBunnies, compostDustBunnies } = require('../src/index');
const fs = require('fs').promises;
const path = require('path');

// Mock rationale: We need to simulate file system operations (reading directories, getting file stats, moving files)
// without actually touching the disk. This ensures tests are fast, deterministic, and don't leave artifacts.
jest.mock('fs', () => ({
    promises: {
        readdir: jest.fn(),
        stat: jest.fn(),
        rename: jest.fn(),
        mkdir: jest.fn(),
    }
}));

describe('Nightly Digital Dust Bunny Sweeper', () => {
    const mockNow = new Date('2023-10-26T10:00:00Z').getTime(); // Consistent "now" for testing age
    const oldFileMtime = new Date('2023-07-01T00:00:00Z').getTime(); // Older than 90 days
    const recentFileMtime = new Date('2023-10-01T00:00:00Z').getTime(); // Newer than 90 days

    let consoleLogSpy, consoleErrorSpy, consoleWarnSpy;

    beforeAll(() => {
        // Mock Date.now() to ensure consistent age calculations
        jest.spyOn(Date, 'now').mockReturnValue(mockNow);
    });

    beforeEach(() => {
        // Spy on console methods to prevent actual logging during tests and check calls
        consoleLogSpy = jest.spyOn(console, 'log').mockImplementation(() => {});
        consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
        consoleWarnSpy = jest.spyOn(console, 'warn').mockImplementation(() => {});
    });

    afterEach(() => {
        jest.clearAllMocks();
        consoleLogSpy.mockRestore();
        consoleErrorSpy.mockRestore();
        consoleWarnSpy.mockRestore();
    });

    afterAll(() => {
        jest.restoreAllMocks(); // Restore Date.now()
    });

    describe('findDustBunnies', () => {
        it('should find old files and directories based on age threshold', async () => {
            fs.readdir.mockImplementation(async (dirPath) => {
                if (dirPath === '/test/project') {
                    return [
                        { name: 'old_file.txt', isDirectory: () => false },
                        { name: 'recent_file.txt', isDirectory: () => false },
                        { name: 'old_dir', isDirectory: () => true },
                        { name: 'node_modules', isDirectory: () => true }, // Should be excluded from recursion
                    ];
                }
                if (dirPath === '/test/project/old_dir') {
                    return [
                        { name: 'nested_old.log', isDirectory: () => false },
                    ];
                }
                return [];
            });

            fs.stat.mockImplementation(async (filePath) => {
                if (filePath.includes('old_file.txt') || filePath.includes('old_dir') || filePath.includes('nested_old.log')) {
                    return { mtimeMs: oldFileMtime, isDirectory: () => filePath.includes('old_dir') };
                }
                if (filePath.includes('recent_file.txt')) {
                    return { mtimeMs: recentFileMtime, isDirectory: () => false };
                }
                if (filePath.includes('node_modules')) {
                    return { mtimeMs: recentFileMtime, isDirectory: () => true };
                }
                throw new Error('File not found');
            });

            const dustBunnies = await findDustBunnies('/test/project', 90, ['node_modules']);

            expect(dustBunnies).toHaveLength(3);
            expect(dustBunnies).toEqual(expect.arrayContaining([
                expect.objectContaining({ path: '/test/project/old_file.txt', type: 'file' }),
                expect.objectContaining({ path: '/test/project/old_dir', type: 'directory' }),
                expect.objectContaining({ path: '/test/project/old_dir/nested_old.log', type: 'file' }),
            ]));
            expect(dustBunnies.every(b => b.ageDays >= 90)).toBe(true);
            expect(fs.readdir).toHaveBeenCalledWith('/test/project', { withFileTypes: true });
            expect(fs.readdir).toHaveBeenCalledWith('/test/project/old_dir', { withFileTypes: true });
            expect(fs.readdir).not.toHaveBeenCalledWith('/test/project/node_modules', expect.any(Object)); // Should not recurse into excluded dir
        });

        it('should return an empty array if no dust bunnies are found', async () => {
            fs.readdir.mockResolvedValueOnce([
                { name: 'recent_file.txt', isDirectory: () => false },
                { name: 'recent_dir', isDirectory: () => true },
            ]);
            fs.stat.mockResolvedValue({ mtimeMs: recentFileMtime, isDirectory: () => false });

            const dustBunnies = await findDustBunnies('/test/project', 90);
            expect(dustBunnies).toHaveLength(0);
        });

        it('should handle errors during file stat gracefully', async () => {
            fs.readdir.mockResolvedValueOnce([
                { name: 'valid_file.txt', isDirectory: () => false },
                { name: 'invalid_file.txt', isDirectory: () => false },
            ]);
            fs.stat.mockImplementation(async (filePath) => {
                if (filePath.includes('valid_file.txt')) {
                    return { mtimeMs: oldFileMtime, isDirectory: () => false };
                }
                throw new Error('Permission denied');
            });

            const dustBunnies = await findDustBunnies('/test/project', 90);
            expect(dustBunnies).toHaveLength(1);
            expect(dustBunnies[0].path).toBe('/test/project/valid_file.txt');
            expect(consoleWarnSpy).toHaveBeenCalledWith(expect.stringContaining('Could not stat /test/project/invalid_file.txt'));
        });

        it('should handle errors during directory read gracefully', async () => {
            fs.readdir.mockImplementation(async (dirPath) => {
                if (dirPath === '/test/project') {
                    return [
                        { name: 'subdir', isDirectory: () => true }
                    ];
                }
                if (dirPath === '/test/project/subdir') {
                    throw new Error('Cannot access directory');
                }
                return [];
            });
            fs.stat.mockResolvedValue({ mtimeMs: oldFileMtime, isDirectory: () => true }); // For /test/project/subdir

            const dustBunnies = await findDustBunnies('/test/project', 90);
            expect(dustBunnies).toHaveLength(1); // Only the subdir itself, as its contents couldn't be read
            expect(dustBunnies[0].path).toBe('/test/project/subdir');
            expect(consoleWarnSpy).toHaveBeenCalledWith(expect.stringContaining('Could not read directory /test/project/subdir'));
        });
    });

    describe('compostDustBunnies', () => {
        it('should move all dust bunnies to the compost path', async () => {
            const bunnies = [
                { path: '/test/project/old_file.txt', type: 'file', ageDays: 100 },
                { path: '/test/project/old_dir', type: 'directory', ageDays: 120 },
            ];
            const compostPath = '/digital_compost';

            await compostDustBunnies(bunnies, compostPath);

            expect(fs.mkdir).toHaveBeenCalledWith(compostPath, { recursive: true });
            expect(fs.rename).toHaveBeenCalledTimes(2);
            expect(fs.rename).toHaveBeenCalledWith('/test/project/old_file.txt', '/digital_compost/old_file.txt');
            expect(fs.rename).toHaveBeenCalledWith('/test/project/old_dir', '/digital_compost/old_dir');
            expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining('Composting 2 digital dust bunnies'));
            expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining('Moved: /test/project/old_file.txt -> /digital_compost/old_file.txt'));
        });

        it('should log a message if no dust bunnies to compost', async () => {
            await compostDustBunnies([], '/digital_compost');
            expect(fs.mkdir).not.toHaveBeenCalled();
            expect(fs.rename).not.toHaveBeenCalled();
            expect(consoleLogSpy).toHaveBeenCalledWith("No dust bunnies to compost. Your digital space is sparkling!");
        });

        it('should handle errors during composting gracefully', async () => {
            const bunnies = [
                { path: '/test/project/old_file.txt', type: 'file', ageDays: 100 },
                { path: '/test/project/unmovable_dir', type: 'directory', ageDays: 120 },
            ];
            const compostPath = '/digital_compost';

            fs.rename.mockImplementation(async (src, dest) => {
                if (src.includes('unmovable_dir')) {
                    throw new Error('Permission denied');
                }
                // For the first file, resolve successfully
            });

            await compostDustBunnies(bunnies, compostPath);

            expect(fs.mkdir).toHaveBeenCalledWith(compostPath, { recursive: true });
            expect(fs.rename).toHaveBeenCalledTimes(2);
            expect(fs.rename).toHaveBeenCalledWith('/test/project/old_file.txt', '/digital_compost/old_file.txt');
            expect(fs.rename).toHaveBeenCalledWith('/test/project/unmovable_dir', '/digital_compost/unmovable_dir');
            expect(consoleErrorSpy).toHaveBeenCalledWith(expect.stringContaining('Failed to compost /test/project/unmovable_dir'));
        });
    });
});
