const { getFilesWithDecay, generateCuratorReport, main } = require('../src/index');
const fs = require('fs').promises;

// Mock rationale: fs.promises.readdir is mocked to simulate directory contents
// without actual file system access, ensuring tests are fast and isolated.
// fs.promises.stat is mocked to provide controlled mtimeMs values for files,
// allowing precise testing of age calculation and categorization logic.
jest.mock('fs', () => ({
    promises: {
        readdir: jest.fn(),
        stat: jest.fn(),
    },
    constants: {
        F_OK: 0 // Mock for fs.access if needed, though not used here
    }
}));

// Mock rationale: console.log and console.error are mocked to capture output
// and prevent it from polluting test results, allowing assertions on the output.
const mockConsoleLog = jest.spyOn(console, 'log').mockImplementation(() => {});
const mockConsoleError = jest.spyOn(console, 'error').mockImplementation(() => {});
// Mock rationale: process.exit is mocked to prevent actual process termination
// during tests, allowing assertions on exit codes and error handling.
const mockProcessExit = jest.spyOn(process, 'exit').mockImplementation(() => {});

describe('Temporal File Curator', () => {
    const MOCK_NOW = new Date('2024-01-15T12:00:00Z').getTime(); // Fixed current time for deterministic tests

    beforeEach(() => {
        jest.clearAllMocks();
        // Mock rationale: Date.now() is mocked to fix the "current time" for age calculations,
        // making tests deterministic regardless of when they are run.
        jest.spyOn(Date, 'now').mockReturnValue(MOCK_NOW);
    });

    afterAll(() => {
        jest.restoreAllMocks();
    });

    describe('getFilesWithDecay', () => {
        test('should return empty array for an empty directory', async () => {
            fs.promises.readdir.mockResolvedValue([]);
            const files = await getFilesWithDecay('/test/dir');
            expect(files).toEqual([]);
            expect(fs.promises.readdir).toHaveBeenCalledWith('/test/dir', { withFileTypes: true });
        });

        test('should return files with correct decay info for mixed files', async () => {
            const mockEntries = [
                { name: 'recent.txt', isFile: () => true },
                { name: 'old.log', isFile: () => true },
                { name: 'ancient.data', isFile: () => true },
                { name: 'subdir', isFile: () => false, isDirectory: () => true },
            ];
            fs.promises.readdir.mockResolvedValue(mockEntries);

            fs.promises.stat.mockImplementation((filePath) => {
                if (filePath.includes('recent.txt')) {
                    return Promise.resolve({ mtimeMs: MOCK_NOW - (10 * 24 * 60 * 60 * 1000) }); // 10 days old
                }
                if (filePath.includes('old.log')) {
                    return Promise.resolve({ mtimeMs: MOCK_NOW - (100 * 24 * 60 * 60 * 1000) }); // 100 days old
                }
                if (filePath.includes('ancient.data')) {
                    return Promise.resolve({ mtimeMs: MOCK_NOW - (250 * 24 * 60 * 60 * 1000) }); // 250 days old
                }
                return Promise.reject(new Error('File not found'));
            });

            const files = await getFilesWithDecay('/test/dir', MOCK_NOW);

            expect(files.length).toBe(3);
            expect(files[0].name).toBe('recent.txt');
            expect(files[0].ageInDays).toBeCloseTo(10);
            expect(files[1].name).toBe('old.log');
            expect(files[1].ageInDays).toBeCloseTo(100);
            expect(files[2].name).toBe('ancient.data');
            expect(files[2].ageInDays).toBeCloseTo(250);
        });

        test('should throw error if directory does not exist', async () => {
            fs.promises.readdir.mockRejectedValue(Object.assign(new Error('ENOENT'), { code: 'ENOENT' }));
            await expect(getFilesWithDecay('/nonexistent/dir')).rejects.toThrow('Directory not found: /nonexistent/dir');
        });

        test('should handle stat errors gracefully with a warning', async () => {
            const mockEntries = [
                { name: 'valid.txt', isFile: () => true },
                { name: 'invalid.txt', isFile: () => true },
            ];
            fs.promises.readdir.mockResolvedValue(mockEntries);

            fs.promises.stat.mockImplementation((filePath) => {
                if (filePath.includes('valid.txt')) {
                    return Promise.resolve({ mtimeMs: MOCK_NOW - (10 * 24 * 60 * 60 * 1000) });
                }
                return Promise.reject(new Error('Permission denied'));
            });

            const files = await getFilesWithDecay('/test/dir', MOCK_NOW);
            expect(files.length).toBe(1);
            expect(files[0].name).toBe('valid.txt');
            expect(console.warn).toHaveBeenCalledWith(expect.stringContaining('Warning: Could not stat file'));
        });
    });

    describe('generateCuratorReport', () => {
        const threshold = 90; // 90 days

        test('should generate a report for no files', () => {
            const report = generateCuratorReport([], threshold);
            expect(report).toContain('No files found in the specified directory.');
            expect(report).toContain(`Scanning for files older than ${threshold} days.`);
        });

        test('should categorize files correctly into fresh, moderate, and deep decay', () => {
            const files = [
                { name: 'fresh.txt', path: '/dir/fresh.txt', mtime: '2024-01-05', ageInDays: 10 }, // < 90 days
                { name: 'moderate.log', path: '/dir/moderate.log', mtime: '2023-09-01', ageInDays: 136 }, // > 90, < 180 days
                { name: 'deep.data', path: '/dir/deep.data', mtime: '2023-04-01', ageInDays: 289 }, // > 180 days
            ];
            const report = generateCuratorReport(files, threshold);

            expect(report).toContain('Freshly Manifested Artifacts (Within 90 days):');
            expect(report).toContain('- fresh.txt');
            expect(report).toContain('Moderately Decayed Artifacts (Older than 90 days, but less than 180 days):');
            expect(report).toContain('- moderate.log');
            expect(report).toContain('Deeply Decayed Artifacts (Older than 180 days):');
            expect(report).toContain('- deep.data');
            expect(report).toContain('Total files scanned: 3');
            expect(report).toContain('Total decayed files: 2');
        });

        test('should handle only fresh files', () => {
            const files = [
                { name: 'fresh1.txt', path: '/dir/fresh1.txt', mtime: '2024-01-05', ageInDays: 10 },
                { name: 'fresh2.log', path: '/dir/fresh2.log', mtime: '2023-11-01', ageInDays: 75 },
            ];
            const report = generateCuratorReport(files, threshold);
            expect(report).toContain('Freshly Manifested Artifacts (Within 90 days):');
            expect(report).toContain('- fresh1.txt');
            expect(report).toContain('- fresh2.log');
            expect(report).not.toContain('Moderately Decayed Artifacts');
            expect(report).not.toContain('Deeply Decayed Artifacts');
            expect(report).toContain('Total files scanned: 2');
            expect(report).toContain('Total decayed files: 0');
        });

        test('should handle only deeply decayed files', () => {
            const files = [
                { name: 'ancient1.txt', path: '/dir/ancient1.txt', mtime: '2023-01-01', ageInDays: 379 },
                { name: 'ancient2.log', path: '/dir/ancient2.log', mtime: '2022-01-01', ageInDays: 744 },
            ];
            const report = generateCuratorReport(files, threshold);
            expect(report).not.toContain('Freshly Manifested Artifacts');
            expect(report).not.toContain('Moderately Decayed Artifacts');
            expect(report).toContain('Deeply Decayed Artifacts (Older than 180 days):');
            expect(report).toContain('- ancient1.txt');
            expect(report).toContain('- ancient2.log');
            expect(report).toContain('Total files scanned: 2');
            expect(report).toContain('Total decayed files: 2');
        });
    });

    describe('main', () => {
        let originalArgv;

        beforeEach(() => {
            originalArgv = process.argv;
            fs.promises.readdir.mockResolvedValue([]); // Default to empty dir
        });

        afterEach(() => {
            process.argv = originalArgv;
        });

        test('should exit with error if no arguments are provided', async () => {
            process.argv = ['node', 'src/index.js'];
            await main();
            expect(mockConsoleError).toHaveBeenCalledWith('Usage: node src/index.js <directory_path> <age_threshold_in_days>');
            expect(mockProcessExit).toHaveBeenCalledWith(1);
        });

        test('should exit with error if invalid threshold is provided', async () => {
            process.argv = ['node', 'src/index.js', '/test/dir', 'abc'];
            await main();
            expect(mockConsoleError).toHaveBeenCalledWith('Usage: node src/index.js <directory_path> <age_threshold_in_days>');
            expect(mockProcessExit).toHaveBeenCalledWith(1);
        });

        test('should print report for valid arguments', async () => {
            process.argv = ['node', 'src/index.js', '/test/dir', '90'];
            const mockEntries = [
                { name: 'old.log', isFile: () => true },
            ];
            fs.promises.readdir.mockResolvedValue(mockEntries);
            fs.promises.stat.mockResolvedValue({ mtimeMs: MOCK_NOW - (100 * 24 * 60 * 60 * 1000) }); // 100 days old

            await main();
            expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Moderately Decayed Artifacts'));
            expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('- old.log'));
            expect(mockProcessExit).not.toHaveBeenCalled();
        });

        test('should print error if getFilesWithDecay throws an error', async () => {
            process.argv = ['node', 'src/index.js', '/nonexistent/dir', '90'];
            fs.promises.readdir.mockRejectedValue(Object.assign(new Error('ENOENT'), { code: 'ENOENT' }));

            await main();
            expect(mockConsoleError).toHaveBeenCalledWith('Error: Directory not found: /nonexistent/dir');
            expect(mockProcessExit).toHaveBeenCalledWith(1);
        });
    });
});
