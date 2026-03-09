const { getFileAgeInDays, findDustBunnies, archiveFile, main } = require('../src/index');
const fs = require('fs');
const path = require('path');

// Mock rationale: We need to control the file system state and timestamps for deterministic testing.
// Directly interacting with the actual file system would make tests non-deterministic and slow.
jest.mock('fs', () => ({
    existsSync: jest.fn(),
    statSync: jest.fn(),
    readdirSync: jest.fn(),
    mkdirSync: jest.fn(),
    renameSync: jest.fn(),
}));

// Mock rationale: We need to control the current date for deterministic age calculations.
// Using the real Date would make tests non-deterministic.
const MOCK_CURRENT_DATE = new Date('2023-10-26T10:00:00Z');
const realDate = Date;
global.Date = jest.fn(() => MOCK_CURRENT_DATE);
global.Date.now = jest.fn(() => MOCK_CURRENT_DATE.getTime());
global.Date.prototype.getTime = jest.fn(() => MOCK_CURRENT_DATE.getTime());
Object.assign(global.Date, realDate); // Copy static methods like parse, UTC

describe('Nightly Digital Dust Bunny Collector', () => {
    beforeEach(() => {
        jest.clearAllMocks();
        console.log = jest.fn(); // Mock console.log to prevent test output pollution
        console.warn = jest.fn();
        console.error = jest.fn();
        // Mock rationale: Prevent actual process exit during tests, allowing assertions on error conditions.
        process.exit = jest.fn((code) => { throw new Error(`Process exited with code ${code}`); });
    });

    afterAll(() => {
        global.Date = realDate; // Restore original Date object
    });

    describe('getFileAgeInDays', () => {
        test('should correctly calculate age for an old file', () => {
            const filePath = '/test/old_file.txt';
            const mtime = new Date('2023-07-01T00:00:00Z'); // July 1st
            fs.statSync.mockReturnValue({ mtime: mtime, isFile: () => true });
            fs.existsSync.mockReturnValue(true); // Mock rationale: Ensure statSync is called

            const age = getFileAgeInDays(filePath);
            // MOCK_CURRENT_DATE is Oct 26. July 1 to Oct 26 is 117 days.
            expect(age).toBe(117);
        });

        test('should correctly calculate age for a recent file', () => {
            const filePath = '/test/recent_file.txt';
            const mtime = new Date('2023-10-20T00:00:00Z'); // Oct 20th
            fs.statSync.mockReturnValue({ mtime: mtime, isFile: () => true });
            fs.existsSync.mockReturnValue(true);

            const age = getFileAgeInDays(filePath);
            // MOCK_CURRENT_DATE is Oct 26. Oct 20 to Oct 26 is 6 days.
            expect(age).toBe(6);
        });

        test('should return -1 if file stats cannot be retrieved', () => {
            const filePath = '/test/non_existent.txt';
            fs.statSync.mockImplementation(() => { throw new Error('File not found'); });
            fs.existsSync.mockReturnValue(false); // Mock rationale: Simulate file not existing

            const age = getFileAgeInDays(filePath);
            expect(age).toBe(-1);
            expect(console.error).toHaveBeenCalledWith(expect.stringContaining('Error getting stats for /test/non_existent.txt: File not found'));
        });
    });

    describe('findDustBunnies', () => {
        const mockStats = (isDirectory, mtime) => ({
            isDirectory: () => isDirectory,
            isFile: () => !isDirectory,
            mtime: mtime || MOCK_CURRENT_DATE,
        });

        test('should find old files in a flat directory', () => {
            const dirPath = '/test_dir';
            fs.existsSync.mockReturnValue(true);
            fs.statSync.mockImplementation((p) => {
                if (p === dirPath) return mockStats(true);
                if (p === path.join(dirPath, 'old_file.txt')) return mockStats(false, new Date('2023-07-01T00:00:00Z')); // 117 days old
                if (p === path.join(dirPath, 'recent_file.txt')) return mockStats(false, new Date('2023-10-20T00:00:00Z')); // 6 days old
                return mockStats(false);
            });
            fs.readdirSync.mockReturnValue(['old_file.txt', 'recent_file.txt']);

            const dustBunnies = findDustBunnies(dirPath, 90);
            expect(dustBunnies).toEqual([{ path: path.join(dirPath, 'old_file.txt'), age: 117 }]);
        });

        test('should find old files in nested directories', () => {
            const dirPath = '/test_dir';
            const subDirPath = path.join(dirPath, 'sub_dir');
            fs.existsSync.mockReturnValue(true);
            fs.statSync.mockImplementation((p) => {
                if (p === dirPath) return mockStats(true);
                if (p === subDirPath) return mockStats(true);
                if (p === path.join(dirPath, 'old_file1.txt')) return mockStats(false, new Date('2023-07-01T00:00:00Z'));
                if (p === path.join(subDirPath, 'old_file2.txt')) return mockStats(false, new Date('2023-06-01T00:00:00Z')); // 147 days old
                if (p === path.join(subDirPath, 'recent_file.txt')) return mockStats(false, new Date('2023-10-20T00:00:00Z'));
                return mockStats(false);
            });
            fs.readdirSync.mockImplementation((p) => {
                if (p === dirPath) return ['old_file1.txt', 'sub_dir'];
                if (p === subDirPath) return ['old_file2.txt', 'recent_file.txt'];
                return [];
            });

            const dustBunnies = findDustBunnies(dirPath, 90);
            expect(dustBunnies).toEqual([
                { path: path.join(dirPath, 'old_file1.txt'), age: 117 },
                { path: path.join(subDirPath, 'old_file2.txt'), age: 147 },
            ]);
        });

        test('should return empty array if no dust bunnies found', () => {
            const dirPath = '/test_dir';
            fs.existsSync.mockReturnValue(true);
            fs.statSync.mockImplementation((p) => {
                if (p === dirPath) return mockStats(true);
                if (p === path.join(dirPath, 'recent_file.txt')) return mockStats(false, new Date('2023-10-20T00:00:00Z'));
                return mockStats(false);
            });
            fs.readdirSync.mockReturnValue(['recent_file.txt']);

            const dustBunnies = findDustBunnies(dirPath, 90);
            expect(dustBunnies).toEqual([]);
        });

        test('should handle non-existent directory gracefully', () => {
            const dirPath = '/non_existent';
            fs.existsSync.mockReturnValue(false);

            const dustBunnies = findDustBunnies(dirPath, 90);
            expect(dustBunnies).toEqual([]);
            expect(console.warn).toHaveBeenCalledWith(`Directory not found: ${dirPath}`);
        });

        test('should skip .dust-bunnies-archive directory', () => {
            const dirPath = '/test_dir';
            const archivePath = path.join(dirPath, '.dust-bunnies-archive');
            fs.existsSync.mockReturnValue(true);
            fs.statSync.mockImplementation((p) => {
                if (p === dirPath) return mockStats(true);
                if (p === archivePath) return mockStats(true); // Archive dir
                if (p === path.join(archivePath, 'archived_file.txt')) return mockStats(false, new Date('2023-01-01T00:00:00Z')); // Very old
                return mockStats(false);
            });
            fs.readdirSync.mockImplementation((p) => {
                if (p === dirPath) return ['.dust-bunnies-archive'];
                if (p === archivePath) return ['archived_file.txt'];
                return [];
            });

            const dustBunnies = findDustBunnies(dirPath, 90);
            expect(dustBunnies).toEqual([]); // Should not find files inside the archive
        });
    });

    describe('archiveFile', () => {
        const filePath = '/test_dir/file_to_archive.txt';
        const baseDir = '/test_dir';
        const archiveDir = path.join(baseDir, '.dust-bunnies-archive');
        const newPath = path.join(archiveDir, 'file_to_archive.txt');

        test('should archive a file successfully', () => {
            fs.existsSync.mockReturnValueOnce(false).mockReturnValue(true); // archiveDir doesn't exist initially, then exists
            fs.mkdirSync.mockReturnValue(undefined);
            fs.renameSync.mockReturnValue(undefined);

            const result = archiveFile(filePath, baseDir);
            expect(fs.mkdirSync).toHaveBeenCalledWith(archiveDir, { recursive: true });
            expect(fs.renameSync).toHaveBeenCalledWith(filePath, newPath);
            expect(console.log).toHaveBeenCalledWith(`Archived: ${filePath} -> ${newPath}`);
            expect(result).toBe(true);
        });

        test('should not create archive directory if it already exists', () => {
            fs.existsSync.mockReturnValue(true); // archiveDir already exists
            fs.mkdirSync.mockReturnValue(undefined);
            fs.renameSync.mockReturnValue(undefined);

            archiveFile(filePath, baseDir);
            expect(fs.mkdirSync).not.toHaveBeenCalled();
            expect(fs.renameSync).toHaveBeenCalledWith(filePath, newPath);
        });

        test('should log error if archiving fails', () => {
            fs.existsSync.mockReturnValue(true);
            fs.renameSync.mockImplementation(() => { throw new Error('Permission denied'); });

            const result = archiveFile(filePath, baseDir);
            expect(console.error).toHaveBeenCalledWith(expect.stringContaining(`Error archiving ${filePath}: Permission denied`));
            expect(result).toBe(false);
        });
    });

    describe('main', () => {
        test('should list dust bunnies when action is "list"', () => {
            const dirPath = '/app';
            const oldFile = path.join(dirPath, 'old.txt');
            const recentFile = path.join(dirPath, 'recent.txt');

            fs.existsSync.mockReturnValue(true);
            fs.statSync.mockImplementation((p) => {
                if (p === dirPath) return { isDirectory: () => true, isFile: () => false };
                if (p === oldFile) return { isDirectory: () => false, isFile: () => true, mtime: new Date('2023-07-01T00:00:00Z') };
                if (p === recentFile) return { isDirectory: () => false, isFile: () => true, mtime: new Date('2023-10-20T00:00:00Z') };
                return { isDirectory: () => false, isFile: () => true, mtime: MOCK_CURRENT_DATE };
            });
            fs.readdirSync.mockReturnValue(['old.txt', 'recent.txt']);

            main(['--path', dirPath, '--age', '90', '--action', 'list']);

            expect(console.log).toHaveBeenCalledWith(expect.stringContaining(`Scanning '${dirPath}' for digital dust bunnies older than 90 days...`));
            expect(console.log).toHaveBeenCalledWith(expect.stringContaining('Found 1 digital dust bunnies:'));
            expect(console.log).toHaveBeenCalledWith(expect.stringContaining(`- ${oldFile} (age: 117 days)`));
            expect(fs.renameSync).not.toHaveBeenCalled(); // Should not archive
        });

        test('should archive dust bunnies when action is "archive"', () => {
            const dirPath = '/app';
            const oldFile = path.join(dirPath, 'old.txt');
            const archiveDir = path.join(dirPath, '.dust-bunnies-archive');
            const archivedFilePath = path.join(archiveDir, 'old.txt');

            fs.existsSync.mockReturnValue(true); // For dirPath and for archiveDir existence check
            fs.statSync.mockImplementation((p) => {
                if (p === dirPath) return { isDirectory: () => true, isFile: () => false };
                if (p === oldFile) return { isDirectory: () => false, isFile: () => true, mtime: new Date('2023-07-01T00:00:00Z') };
                return { isDirectory: () => false, isFile: () => true, mtime: MOCK_CURRENT_DATE };
            });
            fs.readdirSync.mockReturnValue(['old.txt']);
            fs.mkdirSync.mockReturnValue(undefined);
            fs.renameSync.mockReturnValue(undefined);

            main(['--path', dirPath, '--age', '90', '--action', 'archive']);

            expect(console.log).toHaveBeenCalledWith(expect.stringContaining('Archiving found dust bunnies...'));
            expect(fs.mkdirSync).toHaveBeenCalledWith(archiveDir, { recursive: true });
            expect(fs.renameSync).toHaveBeenCalledWith(oldFile, archivedFilePath);
            expect(console.log).toHaveBeenCalledWith(expect.stringContaining(`Archived: ${oldFile} -> ${archivedFilePath}`));
            expect(console.log).toHaveBeenCalledWith('Archiving complete.');
        });

        test('should print message when no dust bunnies are found', () => {
            const dirPath = '/app';
            fs.existsSync.mockReturnValue(true);
            fs.statSync.mockImplementation((p) => {
                if (p === dirPath) return { isDirectory: () => true, isFile: () => false };
                return { isDirectory: () => false, isFile: () => true, mtime: MOCK_CURRENT_DATE };
            });
            fs.readdirSync.mockReturnValue(['recent.txt']);

            main(['--path', dirPath, '--age', '90']); // Default action is list

            expect(console.log).toHaveBeenCalledWith(expect.stringContaining('No digital dust bunnies found! Your directories are sparkling clean.'));
            expect(fs.renameSync).not.toHaveBeenCalled();
        });

        test('should exit with error for invalid age', () => {
            expect(() => main(['--age', 'invalid'])).toThrow('Process exited with code 1');
            expect(console.error).toHaveBeenCalledWith('Error: --age must be a positive number.');
        });

        test('should exit with error for negative age', () => {
            expect(() => main(['--age', '-5'])).toThrow('Process exited with code 1');
            expect(console.error).toHaveBeenCalledWith('Error: --age must be a positive number.');
        });

        test('should exit with error for invalid action', () => {
            expect(() => main(['--action', 'delete'])).toThrow('Process exited with code 1');
            expect(console.error).toHaveBeenCalledWith('Error: --action must be "list" or "archive".');
        });
    });
});
