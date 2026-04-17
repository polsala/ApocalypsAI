const { scan } = require('../src/fileScanner');
const fs = require('fs');
const path = require('path');

// Mock rationale: We need to simulate file system operations (reading directories, getting file stats)
// without actually touching the disk. This ensures tests are fast, deterministic, and isolated.
jest.mock('fs', () => ({
    existsSync: jest.fn(),
    readdirSync: jest.fn(),
    statSync: jest.fn(),
}));

describe('fileScanner', () => {
    const MOCK_ROOT = '/mock/root';
    const NOW = new Date('2023-10-26T12:00:00Z').getTime(); // Consistent "now" for testing age

    beforeEach(() => {
        jest.clearAllMocks();
        // Default mock for existsSync
        fs.existsSync.mockReturnValue(true);
    });

    test('should return an empty array for an empty directory', () => {
        fs.readdirSync.mockReturnValue([]);
        const result = scan(MOCK_ROOT, 90);
        expect(result).toEqual([]);
        expect(fs.readdirSync).toHaveBeenCalledWith(MOCK_ROOT, { withFileTypes: true });
    });

    test('should return an empty array if rootPath does not exist', () => {
        fs.existsSync.mockReturnValue(false);
        const result = scan('/non/existent/path', 90);
        expect(result).toEqual([]);
        expect(fs.existsSync).toHaveBeenCalledWith('/non/existent/path');
        expect(fs.readdirSync).not.toHaveBeenCalled(); // Should not try to read
    });

    test('should find old files and ignore recent ones', () => {
        // Mock rationale: Simulate a directory with mixed file ages.
        // Old file: modified 100 days ago (older than 90 days threshold)
        // Recent file: modified 50 days ago (newer than 90 days threshold)
        fs.readdirSync.mockReturnValue([
            { name: 'old_file.txt', isDirectory: () => false, isFile: () => true },
            { name: 'recent_file.txt', isDirectory: () => false, isFile: () => true },
        ]);

        fs.statSync.mockImplementation((filePath) => {
            if (filePath === path.join(MOCK_ROOT, 'old_file.txt')) {
                return {
                    mtime: new Date(NOW - (100 * 24 * 60 * 60 * 1000)), // 100 days old
                    isDirectory: () => false,
                    isFile: () => true
                };
            }
            if (filePath === path.join(MOCK_ROOT, 'recent_file.txt')) {
                return {
                    mtime: new Date(NOW - (50 * 24 * 60 * 60 * 1000)), // 50 days old
                    isDirectory: () => false,
                    isFile: () => true
                };
            }
            return { mtime: new Date(), isDirectory: () => false, isFile: () => true };
        });

        const result = scan(MOCK_ROOT, 90);
        expect(result).toHaveLength(1);
        expect(result[0].path).toBe(path.join(MOCK_ROOT, 'old_file.txt'));
        expect(result[0].ageDays).toBeCloseTo(100);
    });

    test('should recurse into subdirectories', () => {
        // Mock rationale: Simulate a nested directory structure.
        // Root has a directory 'subdir' and a recent file.
        // 'subdir' has an old file.
        fs.readdirSync.mockImplementation((dirPath) => {
            if (dirPath === MOCK_ROOT) {
                return [
                    { name: 'subdir', isDirectory: () => true, isFile: () => false },
                    { name: 'recent_root_file.txt', isDirectory: () => false, isFile: () => true },
                ];
            }
            if (dirPath === path.join(MOCK_ROOT, 'subdir')) {
                return [
                    { name: 'old_subdir_file.txt', isDirectory: () => false, isFile: () => true },
                ];
            }
            return [];
        });

        fs.statSync.mockImplementation((filePath) => {
            if (filePath === path.join(MOCK_ROOT, 'recent_root_file.txt')) {
                return { mtime: new Date(NOW - (10 * 24 * 60 * 60 * 1000)), isDirectory: () => false, isFile: () => true }; // 10 days old
            }
            if (filePath === path.join(MOCK_ROOT, 'subdir', 'old_subdir_file.txt')) {
                return { mtime: new Date(NOW - (120 * 24 * 60 * 60 * 1000)), isDirectory: () => false, isFile: () => true }; // 120 days old
            }
            return { mtime: new Date(), isDirectory: () => false, isFile: () => true };
        });

        const result = scan(MOCK_ROOT, 90);
        expect(result).toHaveLength(1);
        expect(result[0].path).toBe(path.join(MOCK_ROOT, 'subdir', 'old_subdir_file.txt'));
        expect(result[0].ageDays).toBeCloseTo(120);
    });

    test('should exclude files/directories matching patterns', () => {
        // Mock rationale: Test the exclusion logic.
        // 'excluded_dir' should be skipped.
        // 'excluded_file.log' should be skipped.
        // 'included_file.txt' should be found if old.
        fs.readdirSync.mockImplementation((dirPath) => {
            if (dirPath === MOCK_ROOT) {
                return [
                    { name: 'excluded_dir', isDirectory: () => true, isFile: () => false },
                    { name: 'excluded_file.log', isDirectory: () => false, isFile: () => true },
                    { name: 'included_file.txt', isDirectory: () => false, isFile: () => true },
                ];
            }
            if (dirPath === path.join(MOCK_ROOT, 'excluded_dir')) {
                return [
                    { name: 'file_inside_excluded_dir.txt', isDirectory: () => false, isFile: () => true },
                ];
            }
            return [];
        });

        fs.statSync.mockImplementation((filePath) => {
            // All files are old enough for this test
            return { mtime: new Date(NOW - (100 * 24 * 60 * 60 * 1000)), isDirectory: () => false, isFile: () => true };
        });

        const excludePatterns = ['excluded_dir', '\\.log$'];
        const result = scan(MOCK_ROOT, 90, excludePatterns);

        expect(result).toHaveLength(1);
        expect(result[0].path).toBe(path.join(MOCK_ROOT, 'included_file.txt'));
        expect(fs.readdirSync).not.toHaveBeenCalledWith(path.join(MOCK_ROOT, 'excluded_dir'), expect.any(Object)); // Excluded dir not traversed
    });

    test('should handle errors during directory read gracefully', () => {
        // Mock rationale: Simulate a permission error when reading a directory.
        // The scanner should continue and not crash.
        fs.readdirSync.mockImplementation((dirPath) => {
            if (dirPath === MOCK_ROOT) {
                return [
                    { name: 'problem_dir', isDirectory: () => true, isFile: () => false },
                    { name: 'good_file.txt', isDirectory: () => false, isFile: () => true },
                ];
            }
            if (dirPath === path.join(MOCK_ROOT, 'problem_dir')) {
                throw new Error('Permission denied'); // Simulate error
            }
            return [];
        });

        fs.statSync.mockImplementation((filePath) => {
            if (filePath === path.join(MOCK_ROOT, 'good_file.txt')) {
                return { mtime: new Date(NOW - (100 * 24 * 60 * 60 * 1000)), isDirectory: () => false, isFile: () => true };
            }
            return { mtime: new Date(), isDirectory: () => false, isFile: () => true };
        });

        const result = scan(MOCK_ROOT, 90);
        expect(result).toHaveLength(1);
        expect(result[0].path).toBe(path.join(MOCK_ROOT, 'good_file.txt'));
    });
});
