const { findDustBunnies, deleteDustBunnies, defaultPatterns } = require('../src/sweeper');
const fs = require('fs');
const path = require('path');

// Mock rationale: fs operations are side-effecting and interact with the actual file system.
// To ensure deterministic and offline tests, we mock fs methods to simulate file system interactions
// without touching real files, allowing us to control the test environment completely.
jest.mock('fs', () => ({
    existsSync: jest.fn(),
    readdirSync: jest.fn(),
    statSync: jest.fn(),
    rmSync: jest.fn(),
    unlinkSync: jest.fn(),
}));

describe('findDustBunnies', () => {
    beforeEach(() => {
        jest.clearAllMocks();
    });

    test('should find node_modules and dist directories', () => {
        // Mock rationale: Simulate a directory structure for testing `findDustBunnies`.
        // This allows us to define specific files and directories that should or should not be found.
        fs.existsSync.mockReturnValue(true);
        fs.readdirSync.mockImplementation((dirPath) => {
            if (dirPath === '/mock/project') {
                return [
                    { name: 'src', isDirectory: () => true, isFile: () => false, isSymbolicLink: () => false },
                    { name: 'node_modules', isDirectory: () => true, isFile: () => false, isSymbolicLink: () => false },
                    { name: 'dist', isDirectory: () => true, isFile: () => false, isSymbolicLink: () => false },
                    { name: 'package.json', isDirectory: () => false, isFile: () => true, isSymbolicLink: () => false }
                ];
            }
            if (dirPath === '/mock/project/src') {
                return [
                    { name: 'index.js', isDirectory: () => false, isFile: () => true, isSymbolicLink: () => false }
                ];
            }
            return [];
        });
        fs.statSync.mockImplementation((filePath) => {
            if (filePath.includes('node_modules') || filePath.includes('dist')) {
                return { isDirectory: () => true, isFile: () => false };
            }
            return { isDirectory: () => false, isFile: () => true };
        });

        const found = findDustBunnies('/mock/project', ['node_modules', 'dist']);
        expect(found).toEqual([
            '/mock/project/node_modules',
            '/mock/project/dist'
        ]);
    });

    test('should find .log files and .DS_Store', () => {
        // Mock rationale: Simulate a directory structure with specific file types for testing `findDustBunnies`.
        fs.existsSync.mockReturnValue(true);
        fs.readdirSync.mockImplementation((dirPath) => {
            if (dirPath === '/mock/project') {
                return [
                    { name: 'app.js', isDirectory: () => false, isFile: () => true, isSymbolicLink: () => false },
                    { name: 'error.log', isDirectory: () => false, isFile: () => true, isSymbolicLink: () => false },
                    { name: '.DS_Store', isDirectory: () => false, isFile: () => true, isSymbolicLink: () => false },
                    { name: 'temp', isDirectory: () => true, isFile: () => false, isSymbolicLink: () => false }
                ];
            }
            if (dirPath === '/mock/project/temp') {
                return [
                    { name: 'another.log', isDirectory: () => false, isFile: () => true, isSymbolicLink: () => false }
                ];
            }
            return [];
        });
        fs.statSync.mockImplementation((filePath) => {
            if (filePath.endsWith('.log') || filePath.endsWith('.DS_Store')) {
                return { isDirectory: () => false, isFile: () => true };
            }
            if (filePath.includes('temp')) {
                return { isDirectory: () => true, isFile: () => false };
            }
            return { isDirectory: () => false, isFile: () => true };
        });

        const found = findDustBunnies('/mock/project', ['.DS_Store', '*.log']);
        expect(found).toEqual([
            '/mock/project/error.log',
            '/mock/project/.DS_Store',
            '/mock/project/temp/another.log'
        ]);
    });

    test('should handle non-existent path gracefully', () => {
        // Mock rationale: Test edge case where the starting path does not exist.
        fs.existsSync.mockReturnValue(false);
        const found = findDustBunnies('/non/existent/path');
        expect(found).toEqual([]);
        expect(fs.readdirSync).not.toHaveBeenCalled();
    });

    test('should not scan into matched directories', () => {
        // Mock rationale: Ensure optimization where matched directories are not traversed.
        fs.existsSync.mockReturnValue(true);
        fs.readdirSync.mockImplementation((dirPath) => {
            if (dirPath === '/mock/project') {
                return [
                    { name: 'node_modules', isDirectory: () => true, isFile: () => false, isSymbolicLink: () => false }
                ];
            }
            // If node_modules is matched, readdirSync should not be called for /mock/project/node_modules
            return [];
        });
        fs.statSync.mockReturnValue({ isDirectory: () => true, isFile: () => false });

        const found = findDustBunnies('/mock/project', ['node_modules']);
        expect(found).toEqual(['/mock/project/node_modules']);
        expect(fs.readdirSync).toHaveBeenCalledTimes(1); // Only for /mock/project
        expect(fs.readdirSync).toHaveBeenCalledWith('/mock/project', expect.any(Object));
    });

    test('should use default patterns if none provided', () => {
        // Mock rationale: Verify that the function correctly falls back to default patterns.
        fs.existsSync.mockReturnValue(true);
        fs.readdirSync.mockImplementation((dirPath) => {
            if (dirPath === '/mock/project') {
                return [
                    { name: 'node_modules', isDirectory: () => true, isFile: () => false, isSymbolicLink: () => false },
                    { name: 'src', isDirectory: () => true, isFile: () => false, isSymbolicLink: () => false }
                ];
            }
            return [];
        });
        fs.statSync.mockReturnValue({ isDirectory: () => true, isFile: () => false });

        const found = findDustBunnies('/mock/project');
        expect(found).toContain('/mock/project/node_modules');
        // Check that it doesn't contain 'src' as it's not a default pattern
        expect(found).not.toContain('/mock/project/src');
    });

    test('should ignore symbolic links', () => {
        // Mock rationale: Ensure symbolic links are skipped to prevent issues like infinite loops.
        fs.existsSync.mockReturnValue(true);
        fs.readdirSync.mockImplementation((dirPath) => {
            if (dirPath === '/mock/project') {
                return [
                    { name: 'symlink_dir', isDirectory: () => true, isFile: () => false, isSymbolicLink: () => true },
                    { name: 'real_dir', isDirectory: () => true, isFile: () => false, isSymbolicLink: () => false }
                ];
            }
            if (dirPath === '/mock/project/real_dir') {
                return [
                    { name: 'node_modules', isDirectory: () => true, isFile: () => false, isSymbolicLink: () => false }
                ];
            }
            return [];
        });
        fs.statSync.mockReturnValue({ isDirectory: () => true, isFile: () => false });

        const found = findDustBunnies('/mock/project', ['node_modules']);
        expect(found).toEqual(['/mock/project/real_dir/node_modules']);
        expect(found).not.toContain('/mock/project/symlink_dir');
    });
});

describe('deleteDustBunnies', () => {
    beforeEach(() => {
        jest.clearAllMocks();
    });

    test('should delete specified files and directories', () => {
        // Mock rationale: Simulate successful deletion of various file system entries.
        fs.statSync.mockImplementation((filePath) => {
            if (filePath.endsWith('.log')) {
                return { isDirectory: () => false, isFile: () => true };
            }
            return { isDirectory: () => true, isFile: () => false };
        });
        fs.rmSync.mockReturnValue(undefined);
        fs.unlinkSync.mockReturnValue(undefined);

        const pathsToDelete = [
            '/mock/project/node_modules',
            '/mock/project/error.log',
            '/mock/project/dist'
        ];
        const result = deleteDustBunnies(pathsToDelete);

        expect(result.deletedCount).toBe(3);
        expect(result.errorCount).toBe(0);
        expect(result.errors).toEqual([]);
        expect(fs.rmSync).toHaveBeenCalledWith('/mock/project/node_modules', { recursive: true, force: true });
        expect(fs.unlinkSync).toHaveBeenCalledWith('/mock/project/error.log');
        expect(fs.rmSync).toHaveBeenCalledWith('/mock/project/dist', { recursive: true, force: true });
    });

    test('should handle deletion errors gracefully', () => {
        // Mock rationale: Simulate a scenario where some deletions fail.
        fs.statSync.mockImplementation((filePath) => {
            if (filePath.endsWith('fail.log')) {
                return { isDirectory: () => false, isFile: () => true };
            }
            return { isDirectory: () => true, isFile: () => false };
        });
        fs.rmSync.mockImplementation((filePath) => {
            if (filePath === '/mock/project/fail_dir') {
                throw new Error('Permission denied');
            }
            return undefined;
        });
        fs.unlinkSync.mockImplementation((filePath) => {
            if (filePath === '/mock/project/fail.log') {
                throw new Error('File in use');
            }
            return undefined;
        });

        const pathsToDelete = [
            '/mock/project/success_dir',
            '/mock/project/fail_dir',
            '/mock/project/success.log',
            '/mock/project/fail.log'
        ];
        const result = deleteDustBunnies(pathsToDelete);

        expect(result.deletedCount).toBe(2);
        expect(result.errorCount).toBe(2);
        expect(result.errors).toEqual([
            { path: '/mock/project/fail_dir', error: 'Permission denied' },
            { path: '/mock/project/fail.log', error: 'File in use' }
        ]);
        expect(fs.rmSync).toHaveBeenCalledWith('/mock/project/success_dir', { recursive: true, force: true });
        expect(fs.rmSync).toHaveBeenCalledWith('/mock/project/fail_dir', { recursive: true, force: true });
        expect(fs.unlinkSync).toHaveBeenCalledWith('/mock/project/success.log');
        expect(fs.unlinkSync).toHaveBeenCalledWith('/mock/project/fail.log');
    });

    test('should return 0 deleted and 0 errors for empty list', () => {
        // Mock rationale: Test the function's behavior with an empty input array.
        const result = deleteDustBunnies([]);
        expect(result.deletedCount).toBe(0);
        expect(result.errorCount).toBe(0);
        expect(result.errors).toEqual([]);
        expect(fs.rmSync).not.toHaveBeenCalled();
        expect(fs.unlinkSync).not.toHaveBeenCalled();
    });
});
