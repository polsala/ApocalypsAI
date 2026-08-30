const { getDustBunnies } = require('../src/index');
const fs = require('fs').promises; // Import actual fs for mocking
const path = require('path');

// Mock rationale: We need to simulate file system interactions (readdir, stat)
// without actually touching the disk, ensuring deterministic and offline tests.
jest.mock('fs', () => ({
    promises: {
        readdir: jest.fn(),
        stat: jest.fn(),
    },
}));

describe('getDustBunnies', () => {
    // Mock rationale: We need to ensure that the "current date" used for comparison
    // is fixed and predictable across test runs, making tests deterministic.
    const mockNow = new Date('2023-10-26T12:00:00Z');
    const originalDate = global.Date;

    beforeAll(() => {
        // Temporarily replace the global Date constructor
        global.Date = jest.fn((dateString) => {
            if (dateString) {
                return new originalDate(dateString); // Allow creating specific dates
            }
            return mockNow; // Default to our mockNow when called without arguments
        });
        // Also mock Date.now() for consistency
        global.Date.now = jest.fn(() => mockNow.getTime());
    });

    afterAll(() => {
        global.Date = originalDate; // Restore original Date object
    });

    beforeEach(() => {
        fs.readdir.mockReset();
        fs.stat.mockReset();
    });

    test('should find no dust bunnies in an empty directory', async () => {
        fs.readdir.mockResolvedValueOnce([]); // Mock rationale: Simulate an empty directory.
        const bunnies = await getDustBunnies('/test/empty', 90);
        expect(bunnies).toEqual([]);
        expect(fs.readdir).toHaveBeenCalledWith('/test/empty', { withFileTypes: true });
    });

    test('should find no dust bunnies if all files are recent', async () => {
        const recentDate = new Date(mockNow);
        recentDate.setDate(mockNow.getDate() - 10); // 10 days ago, well within 90 days threshold

        fs.readdir.mockResolvedValueOnce([ // Mock rationale: Simulate a directory with one recent file.
            { name: 'recent_file.txt', isFile: () => true, isDirectory: () => false }
        ]);
        fs.stat.mockResolvedValueOnce({ // Mock rationale: Provide stat data for the recent file.
            isFile: () => true,
            isDirectory: () => false,
            mtime: recentDate
        });

        const bunnies = await getDustBunnies('/test/recent', 90);
        expect(bunnies).toEqual([]);
        expect(fs.readdir).toHaveBeenCalledWith('/test/recent', { withFileTypes: true });
        expect(fs.stat).toHaveBeenCalledWith('/test/recent/recent_file.txt');
    });

    test('should find dust bunnies if files are older than threshold', async () => {
        const oldDate = new Date(mockNow);
        oldDate.setDate(mockNow.getDate() - 100); // 100 days ago, older than 90 days threshold

        fs.readdir.mockResolvedValueOnce([ // Mock rationale: Simulate a directory with one old file.
            { name: 'old_file.log', isFile: () => true, isDirectory: () => false }
        ]);
        fs.stat.mockResolvedValueOnce({ // Mock rationale: Provide stat data for the old file.
            isFile: () => true,
            isDirectory: () => false,
            mtime: oldDate
        });

        const bunnies = await getDustBunnies('/test/old', 90);
        expect(bunnies).toEqual([
            { path: '/test/old/old_file.log', modified: '2023-07-18' } // 2023-10-26 - 100 days = 2023-07-18
        ]);
    });

    test('should handle nested directories and find dust bunnies', async () => {
        const oldDate = new Date(mockNow);
        oldDate.setDate(mockNow.getDate() - 100); // 100 days ago

        const recentDate = new Date(mockNow);
        recentDate.setDate(mockNow.getDate() - 10); // 10 days ago

        fs.readdir
            .mockResolvedValueOnce([ // Mock rationale: Simulate root directory with a file and a subdirectory.
                { name: 'recent_root.js', isFile: () => true, isDirectory: () => false },
                { name: 'sub_dir', isFile: () => false, isDirectory: () => true }
            ])
            .mockResolvedValueOnce([ // Mock rationale: Simulate subdirectory with an old file.
                { name: 'old_nested.css', isFile: () => true, isDirectory: () => false }
            ]);

        fs.stat
            .mockResolvedValueOnce({ // Mock rationale: Stat for recent_root.js
                isFile: () => true,
                isDirectory: () => false,
                mtime: recentDate
            })
            .mockResolvedValueOnce({ // Mock rationale: Stat for sub_dir
                isFile: () => false,
                isDirectory: () => true,
                mtime: recentDate // mtime for directory doesn't matter for dust bunnies detection
            })
            .mockResolvedValueOnce({ // Mock rationale: Stat for old_nested.css
                isFile: () => true,
                isDirectory: () => false,
                mtime: oldDate
            });

        const bunnies = await getDustBunnies('/test/nested', 90);
        expect(bunnies).toEqual([
            { path: '/test/nested/sub_dir/old_nested.css', modified: '2023-07-18' }
        ]);
        expect(fs.readdir).toHaveBeenCalledTimes(2);
        expect(fs.stat).toHaveBeenCalledTimes(3);
    });

    test('should handle errors when reading directory', async () => {
        fs.readdir.mockRejectedValueOnce(new Error('Permission denied')); // Mock rationale: Simulate a directory that cannot be read.
        // We expect an error to be logged, but the function should not crash and return an empty array if no other files are found.
        const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {}); // Mock rationale: Suppress console.error output during test.
        const bunnies = await getDustBunnies('/test/unreadable', 90);
        expect(bunnies).toEqual([]);
        expect(consoleErrorSpy).toHaveBeenCalledWith(
            expect.stringContaining('ApocalypsAI Sentry: Cannot access path "/test/unreadable". Skipping. Error: Permission denied')
        );
        consoleErrorSpy.mockRestore();
    });

    test('should handle errors when stating a file', async () => {
        fs.readdir.mockResolvedValueOnce([ // Mock rationale: Simulate a directory with one file that causes stat error.
            { name: 'problem_file.txt', isFile: () => true, isDirectory: () => false }
        ]);
        fs.stat.mockRejectedValueOnce(new Error('File not found')); // Mock rationale: Simulate stat failing for a file.

        const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {}); // Mock rationale: Suppress console.error output during test.
        const bunnies = await getDustBunnies('/test/stat_error', 90);
        expect(bunnies).toEqual([]); // No bunnies should be found if stat fails
        expect(consoleErrorSpy).toHaveBeenCalledWith(
            expect.stringContaining('ApocalypsAI Sentry: Cannot stat "/test/stat_error/problem_file.txt". Skipping. Error: File not found')
        );
        consoleErrorSpy.mockRestore();
    });
});
