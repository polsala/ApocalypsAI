const { findDustBunnies, getFileAgeInDays, runCLI } = require('../src/index');
const fs = require('fs');
const path = require('path');

// Mock rationale: We need to control file system interactions to ensure tests are
// deterministic, offline, and don't rely on actual file system state.
// This allows us to simulate various directory structures and file ages.
jest.mock('fs', () => ({
    readdirSync: jest.fn(),
    statSync: jest.fn(),
    existsSync: jest.fn(),
}));

jest.mock('path', () => ({
    join: jest.fn((...args) => args.join('/')), // Simple join for mock paths
}));

describe('Digital Dust Bunny Sweeper', () => {
    const MOCK_NOW = new Date('2023-10-27T10:00:00.000Z').getTime(); // Consistent "now" for tests

    let consoleErrorSpy;
    let consoleLogSpy;

    beforeAll(() => {
        // Mock Date.now() to ensure consistent age calculations
        const mockDate = new Date(MOCK_NOW);
        jest.spyOn(global.Date, 'now').mockReturnValue(mockDate.getTime());
    });

    afterAll(() => {
        jest.restoreAllMocks(); // Restore original Date.now()
    });

    beforeEach(() => {
        fs.readdirSync.mockClear();
        fs.statSync.mockClear();
        fs.existsSync.mockClear();
        path.join.mockClear();
        consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
        consoleLogSpy = jest.spyOn(console, 'log').mockImplementation(() => {});
    });

    afterEach(() => {
        consoleErrorSpy.mockRestore();
        consoleLogSpy.mockRestore();
    });

    // Helper to create a mock stat object
    const mockStats = (mtimeMs, isDirectory = false) => ({
        mtimeMs: mtimeMs,
        isDirectory: () => isDirectory,
        isFile: () => !isDirectory,
    });

    test('getFileAgeInDays calculates age correctly', () => {
        const fileTime = new Date('2023-10-26T10:00:00.000Z').getTime(); // 1 day ago
        fs.statSync.mockReturnValue(mockStats(fileTime));
        const age = getFileAgeInDays('/mock/file.txt');
        expect(age).toBeCloseTo(1);

        const fileTimeOld = new Date('2023-09-27T10:00:00.000Z').getTime(); // 30 days ago
        fs.statSync.mockReturnValue(mockStats(fileTimeOld));
        const ageOld = getFileAgeInDays('/mock/old_file.txt');
        expect(ageOld).toBeCloseTo(30);
    });

    test('findDustBunnies finds no files if directory is empty', () => {
        fs.readdirSync.mockReturnValue([]);
        fs.existsSync.mockReturnValue(true);

        const bunnies = findDustBunnies('/empty/dir', 10);
        expect(bunnies).toEqual([]);
        expect(fs.readdirSync).toHaveBeenCalledWith('/empty/dir', { withFileTypes: true });
    });

    test('findDustBunnies finds no dust bunnies if all files are new', () => {
        const newFileTime = MOCK_NOW - (0.5 * 24 * 60 * 60 * 1000); // 0.5 days ago
        fs.readdirSync.mockReturnValue([
            { name: 'new_file.txt', isDirectory: () => false, isFile: () => true },
        ]);
        fs.statSync.mockReturnValue(mockStats(newFileTime));
        fs.existsSync.mockReturnValue(true);
        path.join.mockImplementation((dir, file) => `${dir}/${file}`);

        const bunnies = findDustBunnies('/test/dir', 1); // minAgeDays = 1
        expect(bunnies).toEqual([]);
    });

    test('findDustBunnies finds dust bunnies correctly', () => {
        const oldFileTime = MOCK_NOW - (15 * 24 * 60 * 60 * 1000); // 15 days ago
        const newerFileTime = MOCK_NOW - (5 * 24 * 60 * 60 * 1000); // 5 days ago

        fs.readdirSync.mockImplementation((dirPath) => {
            if (dirPath === '/test/dir') {
                return [
                    { name: 'old_file.txt', isDirectory: () => false, isFile: () => true },
                    { name: 'newer_file.txt', isDirectory: () => false, isFile: () => true },
                    { name: 'subdir', isDirectory: () => true, isFile: () => false },
                ];
            } else if (dirPath === '/test/dir/subdir') {
                return [
                    { name: 'very_old.log', isDirectory: () => false, isFile: () => true },
                ];
            }
            return [];
        });

        fs.statSync.mockImplementation((filePath) => {
            if (filePath === '/test/dir/old_file.txt') return mockStats(oldFileTime);
            if (filePath === '/test/dir/newer_file.txt') return mockStats(newerFileTime);
            if (filePath === '/test/dir/subdir') return mockStats(MOCK_NOW, true); // Directory itself
            if (filePath === '/test/dir/subdir/very_old.log') return mockStats(oldFileTime - (10 * 24 * 60 * 60 * 1000)); // 25 days ago
            return mockStats(MOCK_NOW); // Default for unexpected paths
        });
        fs.existsSync.mockReturnValue(true);
        path.join.mockImplementation((dir, file) => `${dir}/${file}`);

        const bunnies = findDustBunnies('/test/dir', 10); // minAgeDays = 10

        expect(bunnies.length).toBe(2);
        expect(bunnies).toContainEqual(expect.objectContaining({ path: '/test/dir/old_file.txt', age: expect.closeTo(15) }));
        expect(bunnies).toContainEqual(expect.objectContaining({ path: '/test/dir/subdir/very_old.log', age: expect.closeTo(25) }));
        expect(bunnies).not.toContainEqual(expect.objectContaining({ path: '/test/dir/newer_file.txt' })); // Should be excluded
    });

    test('findDustBunnies handles file system errors gracefully when reading directory', () => {
        fs.readdirSync.mockImplementation((dirPath) => {
            if (dirPath === '/test/dir') {
                throw new Error('Permission denied for directory');
            }
            return [];
        });
        fs.existsSync.mockReturnValue(true);

        const bunnies = findDustBunnies('/test/dir', 10);
        expect(bunnies).toEqual([]);
        // No console.warn in the actual code, so no expectation for it.
    });

    test('findDustBunnies handles file system errors gracefully when stating files', () => {
        fs.readdirSync.mockReturnValue([
            { name: 'accessible.txt', isDirectory: () => false, isFile: () => true },
            { name: 'unreadable.txt', isDirectory: () => false, isFile: () => true },
        ]);
        fs.statSync.mockImplementation((filePath) => {
            if (filePath === '/test/dir/accessible.txt') {
                return mockStats(MOCK_NOW - (20 * 24 * 60 * 60 * 1000)); // 20 days ago
            }
            if (filePath === '/test/dir/unreadable.txt') {
                throw new Error('Permission denied'); // Simulate error
            }
            return mockStats(MOCK_NOW);
        });
        fs.existsSync.mockReturnValue(true);
        path.join.mockImplementation((dir, file) => `${dir}/${file}`);

        const bunnies = findDustBunnies('/test/dir', 10); // minAgeDays = 10
        expect(bunnies.length).toBe(1);
        expect(bunnies).toContainEqual(expect.objectContaining({ path: '/test/dir/accessible.txt', age: expect.closeTo(20) }));
    });

    describe('runCLI', () => {
        test('exits with error for missing arguments', () => {
            const exitCode = runCLI(['node', 'src/index.js', '/some/path']);
            expect(consoleErrorSpy).toHaveBeenCalledWith('Usage: node src/index.js <directory_path> <age_in_days>');
            expect(exitCode).toBe(1);
        });

        test('exits with error for invalid age (not a number)', () => {
            const exitCode = runCLI(['node', 'src/index.js', '/some/path', 'not-a-number']);
            expect(consoleErrorSpy).toHaveBeenCalledWith('Error: <age_in_days> must be a non-negative number.');
            expect(exitCode).toBe(1);
        });

        test('exits with error for invalid age (negative number)', () => {
            const exitCode = runCLI(['node', 'src/index.js', '/some/path', '-5']);
            expect(consoleErrorSpy).toHaveBeenCalledWith('Error: <age_in_days> must be a non-negative number.');
            expect(exitCode).toBe(1);
        });

        test('exits with error for non-existent directory', () => {
            fs.existsSync.mockReturnValue(false);
            const exitCode = runCLI(['node', 'src/index.js', '/nonexistent/path', '10']);
            expect(consoleErrorSpy).toHaveBeenCalledWith('Error: Directory not found: /nonexistent/path');
            expect(exitCode).toBe(1);
        });

        test('reports no dust bunnies found', () => {
            fs.existsSync.mockReturnValue(true);
            fs.readdirSync.mockReturnValue([]);
            const exitCode = runCLI(['node', 'src/index.js', '/empty/dir', '10']);
            expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining('No dust bunnies found.'));
            expect(exitCode).toBe(0);
        });

        test('reports dust bunnies found', () => {
            const oldFileTime = MOCK_NOW - (15 * 24 * 60 * 60 * 1000); // 15 days ago
            fs.existsSync.mockReturnValue(true);
            fs.readdirSync.mockReturnValue([
                { name: 'old_file.txt', isDirectory: () => false, isFile: () => true },
            ]);
            fs.statSync.mockReturnValue(mockStats(oldFileTime));
            path.join.mockImplementation((dir, file) => `${dir}/${file}`);

            const exitCode = runCLI(['node', 'src/index.js', '/test/dir', '10']);
            expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining('Found 1 digital dust bunnies:'));
            expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining('  - /test/dir/old_file.txt (forgotten for 15.00 days)'));
            expect(exitCode).toBe(0);
        });
    });
});
