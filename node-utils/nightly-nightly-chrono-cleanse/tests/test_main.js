const fs = require('fs');
const path = require('path');
const { processFiles, parseDurationToMs } = require('../src/main');

// Mock rationale: To prevent actual file system modifications during tests and ensure determinism.
// We control what files exist, their modification times, and the outcomes of operations like moving or deleting.
jest.mock('fs', () => ({
    existsSync: jest.fn(),
    readdirSync: jest.fn(),
    statSync: jest.fn(),
    mkdirSync: jest.fn(),
    renameSync: jest.fn(),
    unlinkSync: jest.fn(),
}));

// Mock rationale: To capture and assert the output of the CLI tool without polluting the test runner's console.
const mockConsoleLog = jest.spyOn(console, 'log').mockImplementation(() => {});
const mockConsoleError = jest.spyOn(console, 'error').mockImplementation(() => {});
const mockConsoleWarn = jest.spyOn(console, 'warn').mockImplementation(() => {});

describe('parseDurationToMs', () => {
    test('should parse days correctly', () => {
        expect(parseDurationToMs('7d')).toBe(7 * 24 * 60 * 60 * 1000);
    });

    test('should parse hours correctly', () => {
        expect(parseDurationToMs('24h')).toBe(24 * 60 * 60 * 1000);
    });

    test('should parse minutes correctly', () => {
        expect(parseDurationToMs('30m')).toBe(30 * 60 * 1000);
    });

    test('should parse seconds correctly', () => {
        expect(parseDurationToMs('60s')).toBe(60 * 1000);
    });

    test('should throw error for invalid format', () => {
        expect(() => parseDurationToMs('7x')).toThrow('Invalid age duration format.');
        expect(() => parseDurationToMs('d')).toThrow('Invalid age duration format.');
        expect(() => parseDurationToMs('7')).toThrow('Invalid age duration format.');
    });
});

describe('processFiles', () => {
    const TEST_DIR = '/test/dir';
    const ARCHIVE_DIR = '/test/archive';
    const NOW = Date.now();
    const ONE_DAY_MS = 24 * 60 * 60 * 1000;

    beforeEach(() => {
        jest.clearAllMocks();
        fs.existsSync.mockReturnValue(true); // Default: directories exist
        fs.readdirSync.mockReturnValue([]); // Default: no files
        fs.statSync.mockImplementation((filePath) => {
            // Default stat for files, can be overridden per test
            return {
                isFile: () => true,
                mtimeMs: NOW - (2 * ONE_DAY_MS) // Default: 2 days old
            };
        });
    });

    afterAll(() => {
        mockConsoleLog.mockRestore();
        mockConsoleError.mockRestore();
        mockConsoleWarn.mockRestore();
    });

    // Helper to simulate file stats
    const mockFileStat = (mtimeMs) => ({
        isFile: () => true,
        mtimeMs: mtimeMs,
    });

    test('should log error if directory does not exist', async () => {
        fs.existsSync.mockReturnValueOnce(false); // Only for the test directory
        await processFiles(TEST_DIR, ONE_DAY_MS, 'list', null, false);
        expect(mockConsoleError).toHaveBeenCalledWith(`Error: Directory not found: ${TEST_DIR}`);
    });

    test('should list old files', async () => {
        fs.readdirSync.mockReturnValue(['old_file.txt', 'new_file.txt']);
        fs.statSync.mockImplementation((filePath) => {
            if (filePath === path.join(TEST_DIR, 'old_file.txt')) {
                return mockFileStat(NOW - (2 * ONE_DAY_MS)); // 2 days old
            }
            if (filePath === path.join(TEST_DIR, 'new_file.txt')) {
                return mockFileStat(NOW - (0.5 * ONE_DAY_MS)); // 0.5 days old
            }
            return mockFileStat(NOW); // Default for others
        });

        await processFiles(TEST_DIR, ONE_DAY_MS, 'list', null, false);

        expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Initiating Chrono-Cleanse Protocol'));
        expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining(`  [ECHO] ${path.join(TEST_DIR, 'old_file.txt')}`));
        expect(mockConsoleLog).not.toHaveBeenCalledWith(expect.stringContaining(`  [ECHO] ${path.join(TEST_DIR, 'new_file.txt')}`));
        expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Total files identified: 1.'));
    });

    test('should archive old files', async () => {
        fs.readdirSync.mockReturnValue(['old_file.txt', 'new_file.txt']);
        fs.statSync.mockImplementation((filePath) => {
            if (filePath === path.join(TEST_DIR, 'old_file.txt')) {
                return mockFileStat(NOW - (2 * ONE_DAY_MS)); // 2 days old
            }
            if (filePath === path.join(TEST_DIR, 'new_file.txt')) {
                return mockFileStat(NOW - (0.5 * ONE_DAY_MS)); // 0.5 days old
            }
            return mockFileStat(NOW);
        });
        fs.mkdirSync.mockClear(); // Clear any default calls from beforeEach
        fs.renameSync.mockClear();

        await processFiles(TEST_DIR, ONE_DAY_MS, 'archive', ARCHIVE_DIR, false);

        expect(fs.mkdirSync).toHaveBeenCalledWith(ARCHIVE_DIR, { recursive: true });
        expect(fs.renameSync).toHaveBeenCalledWith(
            path.join(TEST_DIR, 'old_file.txt'),
            path.join(ARCHIVE_DIR, 'old_file.txt')
        );
        expect(fs.renameSync).not.toHaveBeenCalledWith(
            path.join(TEST_DIR, 'new_file.txt'),
            expect.any(String)
        );
        expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Total files processed: 1.'));
    });

    test('should delete old files', async () => {
        fs.readdirSync.mockReturnValue(['old_file.txt', 'new_file.txt']);
        fs.statSync.mockImplementation((filePath) => {
            if (filePath === path.join(TEST_DIR, 'old_file.txt')) {
                return mockFileStat(NOW - (2 * ONE_DAY_MS)); // 2 days old
            }
            if (filePath === path.join(TEST_DIR, 'new_file.txt')) {
                return mockFileStat(NOW - (0.5 * ONE_DAY_MS)); // 0.5 days old
            }
            return mockFileStat(NOW);
        });
        fs.unlinkSync.mockClear();

        await processFiles(TEST_DIR, ONE_DAY_MS, 'delete', null, false);

        expect(fs.unlinkSync).toHaveBeenCalledWith(path.join(TEST_DIR, 'old_file.txt'));
        expect(fs.unlinkSync).not.toHaveBeenCalledWith(path.join(TEST_DIR, 'new_file.txt'));
        expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Total files processed: 1.'));
    });

    test('should handle empty directory gracefully', async () => {
        fs.readdirSync.mockReturnValue([]);
        await processFiles(TEST_DIR, ONE_DAY_MS, 'list', null, false);
        expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining(`No temporal echoes found in '${TEST_DIR}' older than the specified age.`));
        expect(mockConsoleLog).not.toHaveBeenCalledWith(expect.stringContaining('Initiating Chrono-Cleanse Protocol'));
    });

    test('should handle errors during statSync in verbose mode', async () => {
        fs.readdirSync.mockReturnValue(['bad_file.txt']);
        fs.statSync.mockImplementationOnce(() => {
            throw new Error('Permission denied');
        });

        await processFiles(TEST_DIR, ONE_DAY_MS, 'list', null, true); // verbose true

        expect(mockConsoleWarn).toHaveBeenCalledWith(expect.stringContaining('Warning: Could not stat file'));
        expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining(`No temporal echoes found in '${TEST_DIR}' older than the specified age.`));
    });

    test('should require archive directory for archive command', async () => {
        await processFiles(TEST_DIR, ONE_DAY_MS, 'archive', null, false);
        expect(mockConsoleError).toHaveBeenCalledWith('Error: Archive directory (--output) is required for the archive command.');
    });

    test('should not process files if no files are old enough', async () => {
        fs.readdirSync.mockReturnValue(['new_file.txt']);
        fs.statSync.mockImplementation((filePath) => {
            return mockFileStat(NOW - (0.5 * ONE_DAY_MS)); // 0.5 days old
        });

        await processFiles(TEST_DIR, ONE_DAY_MS, 'list', null, false);
        expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining(`No temporal echoes found in '${TEST_DIR}' older than the specified age.`));
        expect(mockConsoleLog).not.toHaveBeenCalledWith(expect.stringContaining('Initiating Chrono-Cleanse Protocol'));
    });

    test('should handle archive directory creation failure', async () => {
        fs.mkdirSync.mockImplementationOnce(() => {
            throw new Error('Cannot create dir');
        });
        fs.existsSync.mockImplementation((p) => p === TEST_DIR); // Archive dir doesn't exist initially
        fs.readdirSync.mockReturnValue(['old_file.txt']);
        fs.statSync.mockReturnValue(mockFileStat(NOW - (2 * ONE_DAY_MS)));

        await processFiles(TEST_DIR, ONE_DAY_MS, 'archive', ARCHIVE_DIR, false);
        expect(mockConsoleError).toHaveBeenCalledWith(expect.stringContaining(`Error creating archive directory ${ARCHIVE_DIR}: Cannot create dir`));
        expect(fs.renameSync).not.toHaveBeenCalled();
    });

    test('should handle archive failure for a specific file', async () => {
        fs.readdirSync.mockReturnValue(['old_file.txt']);
        fs.statSync.mockReturnValue(mockFileStat(NOW - (2 * ONE_DAY_MS)));
        fs.renameSync.mockImplementationOnce(() => {
            throw new Error('Archive permission denied');
        });

        await processFiles(TEST_DIR, ONE_DAY_MS, 'archive', ARCHIVE_DIR, false);
        expect(mockConsoleError).toHaveBeenCalledWith(expect.stringContaining(`  [ERROR] Failed to archive ${path.join(TEST_DIR, 'old_file.txt')}: Archive permission denied`));
        expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Total files processed: 0.')); // Because it failed
    });

    test('should handle delete failure for a specific file', async () => {
        fs.readdirSync.mockReturnValue(['old_file.txt']);
        fs.statSync.mockReturnValue(mockFileStat(NOW - (2 * ONE_DAY_MS)));
        fs.unlinkSync.mockImplementationOnce(() => {
            throw new Error('Delete permission denied');
        });

        await processFiles(TEST_DIR, ONE_DAY_MS, 'delete', null, false);
        expect(mockConsoleError).toHaveBeenCalledWith(expect.stringContaining(`  [ERROR] Failed to delete ${path.join(TEST_DIR, 'old_file.txt')}: Delete permission denied`));
        expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Total files processed: 0.')); // Because it failed
    });
});
