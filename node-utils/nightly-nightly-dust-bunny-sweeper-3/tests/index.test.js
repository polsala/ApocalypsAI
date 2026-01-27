const { sweepDustBunnies, classifyDustiness } = require('../src/index');
const fs = require('fs').promises;
const path = require('path');

// Mock rationale: We need to simulate a file system with specific modification times
// to deterministically test the dust bunny classification and sweeping logic
// without touching the actual file system or relying on real-time file changes.
jest.mock('fs', () => {
    const originalFs = jest.requireActual('fs');
    return {
        ...originalFs,
        promises: {
            ...originalFs.promises,
            readdir: jest.fn(),
            stat: jest.fn(),
        },
    };
});

describe('classifyDustiness', () => {
    const now = Date.now();
    const thresholdDays = 90; // 90 days for 'Very Dusty'
    const dayInMs = 1000 * 60 * 60 * 24;

    test('should classify fresh files as "Fresh"', () => {
        const mtimeMs = now - (thresholdDays / 3) * dayInMs; // 30 days old
        expect(classifyDustiness(mtimeMs, thresholdDays)).toBe('Fresh (not dusty)');
    });

    test('should classify mildly dusty files', () => {
        const mtimeMs = now - (thresholdDays / 2 + 1) * dayInMs; // 46 days old
        expect(classifyDustiness(mtimeMs, thresholdDays)).toBe('Mildly Dusty');
    });

    test('should classify very dusty files', () => {
        const mtimeMs = now - (thresholdDays + 1) * dayInMs; // 91 days old
        expect(classifyDustiness(mtimeMs, thresholdDays)).toBe('Very Dusty');
    });

    test('should classify ancient relic files', () => {
        const mtimeMs = now - (thresholdDays * 3 + 1) * dayInMs; // 271 days old
        expect(classifyDustiness(mtimeMs, thresholdDays)).toBe('Ancient Relic (very dusty)');
    });
});

describe('sweepDustBunnies', () => {
    const mockFs = fs; // Use the mocked fs.promises
    const baseDir = '/mock/project';
    const now = Date.now();
    const dayInMs = 1000 * 60 * 60 * 24;

    beforeEach(() => {
        mockFs.readdir.mockClear();
        mockFs.stat.mockClear();
    });

    test('should find no dust bunnies in a fresh directory', async () => {
        // Mock a directory with only fresh files
        mockFs.readdir.mockImplementation(async (dirPath) => {
            if (dirPath === baseDir) {
                return [
                    { name: 'file1.txt', isFile: () => true, isDirectory: () => false },
                    { name: 'subdir', isFile: () => false, isDirectory: () => true },
                ];
            }
            if (dirPath === path.join(baseDir, 'subdir')) {
                return [
                    { name: 'file2.js', isFile: () => true, isDirectory: () => false },
                ];
            }
            return [];
        });

        mockFs.stat.mockImplementation(async (filePath) => {
            // All files are 10 days old (fresh)
            return { mtimeMs: now - 10 * dayInMs, isFile: () => true, isDirectory: () => false };
        });

        const bunnies = await sweepDustBunnies(baseDir, 90);
        expect(bunnies).toEqual([]);
        expect(mockFs.readdir).toHaveBeenCalledTimes(2); // baseDir and subdir
        expect(mockFs.stat).toHaveBeenCalledTimes(2); // file1.txt and file2.js
    });

    test('should find dust bunnies and classify them correctly', async () => {
        // Mock a directory with various aged files
        mockFs.readdir.mockImplementation(async (dirPath) => {
            if (dirPath === baseDir) {
                return [
                    { name: 'fresh.txt', isFile: () => true, isDirectory: () => false },
                    { name: 'mildly.md', isFile: () => true, isDirectory: () => false },
                    { name: 'very.js', isFile: () => true, isDirectory: () => false },
                    { name: 'ancient.log', isFile: () => true, isDirectory: () => false },
                    { name: 'nested', isFile: () => false, isDirectory: () => true },
                ];
            }
            if (dirPath === path.join(baseDir, 'nested')) {
                return [
                    { name: 'nested_very.json', isFile: () => true, isDirectory: () => false },
                ];
            }
            return [];
        });

        mockFs.stat.mockImplementation(async (filePath) => {
            if (filePath === path.join(baseDir, 'fresh.txt')) {
                return { mtimeMs: now - 10 * dayInMs, isFile: () => true, isDirectory: () => false }; // 10 days old
            }
            if (filePath === path.join(baseDir, 'mildly.md')) {
                return { mtimeMs: now - 50 * dayInMs, isFile: () => true, isDirectory: () => false }; // 50 days old
            }
            if (filePath === path.join(baseDir, 'very.js')) {
                return { mtimeMs: now - 100 * dayInMs, isFile: () => true, isDirectory: () => false }; // 100 days old
            }
            if (filePath === path.join(baseDir, 'ancient.log')) {
                return { mtimeMs: now - 300 * dayInMs, isFile: () => true, isDirectory: () => false }; // 300 days old
            }
            if (filePath === path.join(baseDir, 'nested', 'nested_very.json')) {
                return { mtimeMs: now - 120 * dayInMs, isFile: () => true, isDirectory: () => false }; // 120 days old
            }
            return { mtimeMs: now, isFile: () => true, isDirectory: () => false }; // Default for others
        });

        const threshold = 90;
        const bunnies = await sweepDustBunnies(baseDir, threshold);

        expect(bunnies.length).toBe(4);
        expect(bunnies).toEqual(expect.arrayContaining([
            expect.objectContaining({
                path: path.join(baseDir, 'mildly.md'),
                dustiness: 'Mildly Dusty'
            }),
            expect.objectContaining({
                path: path.join(baseDir, 'very.js'),
                dustiness: 'Very Dusty'
            }),
            expect.objectContaining({
                path: path.join(baseDir, 'ancient.log'),
                dustiness: 'Ancient Relic (very dusty)'
            }),
            expect.objectContaining({
                path: path.join(baseDir, 'nested', 'nested_very.json'),
                dustiness: 'Very Dusty'
            }),
        ]));
        expect(bunnies.some(b => b.path.includes('fresh.txt'))).toBeFalsy();
    });

    test('should handle inaccessible directories gracefully', async () => {
        mockFs.readdir.mockImplementation(async (dirPath) => {
            if (dirPath === baseDir) {
                return [
                    { name: 'accessible_file.txt', isFile: () => true, isDirectory: () => false },
                    { name: 'inaccessible_dir', isFile: () => false, isDirectory: () => true },
                ];
            }
            if (dirPath === path.join(baseDir, 'inaccessible_dir')) {
                throw new Error('Permission denied'); // Simulate inaccessible directory
            }
            return [];
        });

        mockFs.stat.mockImplementation(async (filePath) => {
            return { mtimeMs: now - 100 * dayInMs, isFile: () => true, isDirectory: () => false }; // Dusty file
        });

        const consoleWarnSpy = jest.spyOn(console, 'warn').mockImplementation(() => {});

        const bunnies = await sweepDustBunnies(baseDir, 90);
        expect(bunnies.length).toBe(1);
        expect(bunnies[0].path).toBe(path.join(baseDir, 'accessible_file.txt'));
        expect(consoleWarnSpy).toHaveBeenCalledWith(expect.stringContaining('Warning: Could not read directory'));
        consoleWarnSpy.mockRestore();
    });

    test('should handle inaccessible files gracefully', async () => {
        mockFs.readdir.mockImplementation(async (dirPath) => {
            if (dirPath === baseDir) {
                return [
                    { name: 'accessible_file.txt', isFile: () => true, isDirectory: () => false },
                    { name: 'inaccessible_file.txt', isFile: () => true, isDirectory: () => false },
                ];
            }
            return [];
        });

        mockFs.stat.mockImplementation(async (filePath) => {
            if (filePath === path.join(baseDir, 'accessible_file.txt')) {
                return { mtimeMs: now - 100 * dayInMs, isFile: () => true, isDirectory: () => false };
            }
            if (filePath === path.join(baseDir, 'inaccessible_file.txt')) {
                throw new Error('Permission denied'); // Simulate inaccessible file
            }
            return null; // Should return null for inaccessible files
        });

        const bunnies = await sweepDustBunnies(baseDir, 90);
        expect(bunnies.length).toBe(1);
        expect(bunnies[0].path).toBe(path.join(baseDir, 'accessible_file.txt'));
    });
});
