const { findStaleFiles } = require('../src/index');
const fs = require('fs').promises;
const path = require('path');

// Mock rationale: We need to control the file system state and timestamps
// to ensure deterministic tests without actually touching the disk.
jest.mock('fs', () => ({
    promises: {
        readdir: jest.fn(),
        stat: jest.fn(),
    },
}));

describe('Nightly Digital Dust Sweeper', () => {
    const MOCK_CURRENT_TIMESTAMP = new Date('2023-10-26T12:00:00Z').getTime(); // Fixed current time for tests
    const THIRTY_DAYS_MS = 30 * 24 * 60 * 60 * 1000;

    beforeEach(() => {
        jest.clearAllMocks();
        // Mock Date.now() for consistent time calculations
        const mockDate = new Date(MOCK_CURRENT_TIMESTAMP);
        jest.spyOn(global, 'Date').mockImplementation(() => mockDate);
    });

    afterAll(() => {
        jest.restoreAllMocks();
    });

    test('should find stale files older than the specified days', async () => {
        // Mock rationale: Simulate a directory with files of different modification times.
        fs.readdir.mockImplementation(async (dirPath, options) => {
            if (dirPath === '/mock/project') {
                return [
                    { name: 'old_file.txt', isFile: () => true, isDirectory: () => false },
                    { name: 'recent_file.js', isFile: () => true, isDirectory: () => false },
                    { name: 'sub_dir', isFile: () => false, isDirectory: () => true },
                ];
            } else if (dirPath === '/mock/project/sub_dir') {
                return [
                    { name: 'very_old.log', isFile: () => true, isDirectory: () => false },
                ];
            }
            return [];
        });

        fs.stat.mockImplementation(async (filePath) => {
            if (filePath === '/mock/project/old_file.txt') {
                // Modified 31 days ago (stale)
                return { isFile: () => true, isDirectory: () => false, mtimeMs: MOCK_CURRENT_TIMESTAMP - (THIRTY_DAYS_MS + 1000) };
            } else if (filePath === '/mock/project/recent_file.js') {
                // Modified 10 days ago (not stale)
                return { isFile: () => true, isDirectory: () => false, mtimeMs: MOCK_CURRENT_TIMESTAMP - (10 * 24 * 60 * 60 * 1000) };
            } else if (filePath === '/mock/project/sub_dir') {
                return { isFile: () => false, isDirectory: () => true, mtimeMs: MOCK_CURRENT_TIMESTAMP - (5 * 24 * 60 * 60 * 1000) };
            } else if (filePath === '/mock/project/sub_dir/very_old.log') {
                // Modified 60 days ago (stale)
                return { isFile: () => true, isDirectory: () => false, mtimeMs: MOCK_CURRENT_TIMESTAMP - (60 * 24 * 60 * 60 * 1000) };
            }
            return { isFile: () => false, isDirectory: () => false, mtimeMs: MOCK_CURRENT_TIMESTAMP }; // Default for unknown
        });

        const staleFiles = await findStaleFiles('/mock/project', 30, MOCK_CURRENT_TIMESTAMP);
        expect(staleFiles).toEqual([
            '/mock/project/old_file.txt',
            '/mock/project/sub_dir/very_old.log',
        ]);
    });

    test('should return an empty array if no stale files are found', async () => {
        // Mock rationale: Simulate a directory where all files are recent.
        fs.readdir.mockImplementation(async (dirPath, options) => {
            if (dirPath === '/mock/project') {
                return [
                    { name: 'recent_file1.txt', isFile: () => true, isDirectory: () => false },
                    { name: 'recent_file2.js', isFile: () => true, isDirectory: () => false },
                ];
            }
            return [];
        });

        fs.stat.mockImplementation(async (filePath) => {
            if (filePath === '/mock/project/recent_file1.txt') {
                return { isFile: () => true, isDirectory: () => false, mtimeMs: MOCK_CURRENT_TIMESTAMP - (5 * 24 * 60 * 60 * 1000) };
            } else if (filePath === '/mock/project/recent_file2.js') {
                return { isFile: () => true, isDirectory: () => false, mtimeMs: MOCK_CURRENT_TIMESTAMP - (15 * 24 * 60 * 60 * 1000) };
            }
            return { isFile: () => false, isDirectory: () => false, mtimeMs: MOCK_CURRENT_TIMESTAMP };
        });

        const staleFiles = await findStaleFiles('/mock/project', 30, MOCK_CURRENT_TIMESTAMP);
        expect(staleFiles).toEqual([]);
    });

    test('should handle empty directories gracefully', async () => {
        // Mock rationale: Simulate an empty directory.
        fs.readdir.mockResolvedValue([]);
        fs.stat.mockResolvedValue({ isFile: () => false, isDirectory: () => false, mtimeMs: MOCK_CURRENT_TIMESTAMP });

        const staleFiles = await findStaleFiles('/mock/empty', 30, MOCK_CURRENT_TIMESTAMP);
        expect(staleFiles).toEqual([]);
    });

    test('should handle errors when reading directories', async () => {
        // Mock rationale: Simulate a permission error when reading a directory.
        fs.readdir.mockImplementation(async (dirPath) => {
            if (dirPath === '/mock/unreadable') {
                throw new Error('Permission denied');
            }
            return [];
        });
        fs.stat.mockResolvedValue({ isFile: () => false, isDirectory: () => false, mtimeMs: MOCK_CURRENT_TIMESTAMP });

        const staleFiles = await findStaleFiles('/mock/unreadable', 30, MOCK_CURRENT_TIMESTAMP);
        expect(staleFiles).toEqual([]); // Should not throw, just return empty
    });

    test('should handle errors when stating files', async () => {
        // Mock rationale: Simulate a broken symlink or other stat error.
        fs.readdir.mockImplementation(async (dirPath) => {
            if (dirPath === '/mock/broken') {
                return [{ name: 'broken_link.txt', isFile: () => true, isDirectory: () => false }];
            }
            return [];
        });
        fs.stat.mockImplementation(async (filePath) => {
            if (filePath === '/mock/broken/broken_link.txt') {
                throw new Error('No such file or directory');
            }
            return { isFile: () => false, isDirectory: () => false, mtimeMs: MOCK_CURRENT_TIMESTAMP };
        });

        const staleFiles = await findStaleFiles('/mock/broken', 30, MOCK_CURRENT_TIMESTAMP);
        expect(staleFiles).toEqual([]); // Should not throw, just return empty
    });
});
