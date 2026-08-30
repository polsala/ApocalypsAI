const assert = require('assert');
const path = require('path');
const { findOldFiles, formatBytes, main } = require('../src/index');
const fs = require('fs'); // We will mock this

// Mock rationale: We need to simulate file system operations without actually creating/deleting files
// on the disk. This ensures tests are deterministic, fast, and don't have side effects.
jest.mock('fs', () => ({
    readdirSync: jest.fn(),
    statSync: jest.fn(),
}));

describe('Digital Dust Bunny Sweeper', () => {

    beforeEach(() => {
        // Reset mocks before each test
        fs.readdirSync.mockReset();
        fs.statSync.mockReset();
    });

    describe('formatBytes', () => {
        test('should format bytes correctly', () => {
            assert.strictEqual(formatBytes(0), '0 Bytes');
            assert.strictEqual(formatBytes(1023), '1023 Bytes');
            assert.strictEqual(formatBytes(1024), '1 KB');
            assert.strictEqual(formatBytes(1536), '1.5 KB');
            assert.strictEqual(formatBytes(1024 * 1024), '1 MB');
            assert.strictEqual(formatBytes(1024 * 1024 * 1024), '1 GB');
            assert.strictEqual(formatBytes(1024 * 1024 * 1024 * 1024), '1 TB');
            assert.strictEqual(formatBytes(1234567890), '1.15 GB');
        });
    });

    describe('findOldFiles', () => {
        const mockNow = new Date('2024-01-01T12:00:00.000Z'); // Consistent "now" for testing age

        // Mock rationale: We need to control the current time for age calculations to be deterministic.
        // This ensures that `new Date()` inside `findOldFiles` returns a predictable value.
        const RealDate = Date;
        global.Date = jest.fn(() => mockNow);
        global.Date.now = jest.fn(() => mockNow.getTime());
        global.Date.prototype = RealDate.prototype;
        global.Date.parse = RealDate.parse;
        global.Date.UTC = RealDate.UTC;

        test('should find no files in an empty directory', () => {
            fs.readdirSync.mockReturnValue([]);
            const result = findOldFiles('/test/empty', 90);
            assert.deepStrictEqual(result, []);
        });

        test('should find no old files if all are recent', () => {
            const recentDate = new Date(mockNow.getTime() - (30 * 24 * 60 * 60 * 1000)); // 30 days ago
            fs.readdirSync.mockReturnValue([
                { name: 'recent_file.txt', isDirectory: () => false, isFile: () => true },
            ]);
            fs.statSync.mockReturnValue({ mtime: recentDate, size: 100 });

            const result = findOldFiles('/test/recent', 90);
            assert.deepStrictEqual(result, []);
        });

        test('should find old files correctly', () => {
            const oldDate = new Date(mockNow.getTime() - (100 * 24 * 60 * 60 * 1000)); // 100 days ago
            fs.readdirSync.mockReturnValue([
                { name: 'old_file.txt', isDirectory: () => false, isFile: () => true },
            ]);
            fs.statSync.mockReturnValue({ mtime: oldDate, size: 200 });

            const result = findOldFiles('/test/old', 90);
            assert.strictEqual(result.length, 1);
            assert.strictEqual(result[0].path, path.join('/test/old', 'old_file.txt'));
            assert.deepStrictEqual(result[0].mtime, oldDate);
            assert.strictEqual(result[0].size, 200);
        });

        test('should handle nested directories and find old files', () => {
            const oldDate = new Date(mockNow.getTime() - (100 * 24 * 60 * 60 * 1000)); // 100 days ago
            const recentDate = new Date(mockNow.getTime() - (30 * 24 * 60 * 60 * 1000)); // 30 days ago

            fs.readdirSync
                .mockImplementation((p) => {
                    if (p === '/test/nested') {
                        return [
                            { name: 'subdir', isDirectory: () => true, isFile: () => false },
                            { name: 'recent_root.txt', isDirectory: () => false, isFile: () => true },
                        ];
                    }
                    if (p === path.join('/test/nested', 'subdir')) {
                        return [
                            { name: 'old_nested.txt', isDirectory: () => false, isFile: () => true },
                            { name: 'recent_nested.txt', isDirectory: () => false, isFile: () => true },
                        ];
                    }
                    return [];
                });

            fs.statSync
                .mockImplementation((p) => {
                    if (p === path.join('/test/nested', 'subdir')) {
                        return { mtime: recentDate, size: 0 }; // Directory stat, not relevant for age
                    }
                    if (p === path.join('/test/nested', 'recent_root.txt')) {
                        return { mtime: recentDate, size: 100 };
                    }
                    if (p === path.join('/test/nested', 'subdir', 'old_nested.txt')) {
                        return { mtime: oldDate, size: 200 };
                    }
                    if (p === path.join('/test/nested', 'subdir', 'recent_nested.txt')) {
                        return { mtime: recentDate, size: 50 };
                    }
                    return { mtime: recentDate, size: 0 }; // Default for other paths
                });

            const result = findOldFiles('/test/nested', 90);
            assert.strictEqual(result.length, 1);
            assert.strictEqual(result[0].path, path.join('/test/nested', 'subdir', 'old_nested.txt'));
        });

        test('should handle permission errors gracefully for directories', () => {
            fs.readdirSync.mockImplementation((p) => {
                if (p === '/test/permissions') {
                    throw new Error('EACCES: permission denied');
                }
                return [];
            });
            // Mock rationale: We need to capture console warnings without them polluting test output.
            const consoleWarnSpy = jest.spyOn(console, 'warn').mockImplementation(() => {});

            const result = findOldFiles('/test/permissions', 90);
            assert.deepStrictEqual(result, []);
            assert.ok(consoleWarnSpy.mock.calledWith(expect.stringContaining('Could not read directory')));
            consoleWarnSpy.mockRestore();
        });

        test('should handle permission errors gracefully for files', () => {
            const oldDate = new Date(mockNow.getTime() - (100 * 24 * 60 * 60 * 1000)); // 100 days ago
            fs.readdirSync.mockReturnValue([
                { name: 'unreadable_file.txt', isDirectory: () => false, isFile: () => true },
            ]);
            fs.statSync.mockImplementation((p) => {
                if (p === path.join('/test/unreadable', 'unreadable_file.txt')) {
                    throw new Error('EACCES: permission denied');
                }
                return { mtime: oldDate, size: 100 }; // Fallback for other files if any
            });

            const result = findOldFiles('/test/unreadable', 90);
            assert.deepStrictEqual(result, []);
            // No console.warn for stat errors, as they are silently skipped.
        });
    });

    describe('main', () => {
        let consoleLogSpy;
        let consoleErrorSpy;
        let processExitSpy;

        beforeEach(() => {
            consoleLogSpy = jest.spyOn(console, 'log').mockImplementation(() => {});
            consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
            processExitSpy = jest.spyOn(process, 'exit').mockImplementation(() => {});

            // Reset mocks for fs functions for main tests
            fs.readdirSync.mockReset();
            fs.statSync.mockReset();
        });

        afterEach(() => {
            consoleLogSpy.mockRestore();
            consoleErrorSpy.mockRestore();
            processExitSpy.mockRestore();
        });

        test('should exit with error if no directory path is provided', () => {
            process.argv = ['node', 'src/index.js']; // No arguments
            main();
            assert.ok(consoleErrorSpy.mock.calledWith('Usage: node src/index.js <directory_path> [days_old]'));
            assert.ok(processExitSpy.mock.calledWith(1));
        });

        test('should report no dust bunnies found', () => {
            process.argv = ['node', 'src/index.js', '/test/clean'];
            fs.readdirSync.mockReturnValue([]); // Empty directory
            main();
            assert.ok(consoleLogSpy.mock.calledWith(expect.stringContaining('No digital dust bunnies found!')));
            assert.strictEqual(processExitSpy.mock.calls.length, 0); // Should not exit
        });

        test('should report found dust bunnies', () => {
            process.argv = ['node', 'src/index.js', '/test/dusty', '10']; // Threshold 10 days
            const mockNow = new Date('2024-01-01T12:00:00.000Z');
            const oldDate = new Date(mockNow.getTime() - (15 * 24 * 60 * 60 * 1000)); // 15 days ago

            // Mock rationale: We need to control the current time for age calculations to be deterministic.
            // This ensures that `new Date()` inside `findOldFiles` returns a predictable value.
            const RealDate = Date;
            global.Date = jest.fn(() => mockNow);
            global.Date.now = jest.fn(() => mockNow.getTime());
            global.Date.prototype = RealDate.prototype;
            global.Date.parse = RealDate.parse;
            global.Date.UTC = RealDate.UTC;

            fs.readdirSync.mockReturnValue([
                { name: 'very_old.txt', isDirectory: () => false, isFile: () => true },
            ]);
            fs.statSync.mockReturnValue({ mtime: oldDate, size: 5000 });

            main();
            assert.ok(consoleLogSpy.mock.calledWith(expect.stringContaining('Sweeping for digital dust bunnies')));
            assert.ok(consoleLogSpy.mock.calledWith(expect.stringContaining('Found 1 digital dust bunnies:')));
            assert.ok(consoleLogSpy.mock.calledWith(expect.stringContaining('very_old.txt (Modified: 2023-12-17, Size: 4.88 KB) - 15 days old!')));
            assert.ok(consoleLogSpy.mock.calledWith(expect.stringContaining('Time to consider a digital spring cleaning!')));
            assert.strictEqual(processExitSpy.mock.calls.length, 0); // Should not exit
        });
    });
});
