const { sweepDigitalDustBunnies } = require('../src/index');
const path = require('path');

// Mock rationale: We don't want to actually touch the file system during tests.
// Mocking fs.promises allows us to simulate file system operations deterministically
// and control the outcomes (e.g., file existence, modification times, permissions).
const mockReaddir = jest.fn();
const mockStat = jest.fn();
const mockMkdir = jest.fn();
const mockRename = jest.fn();

jest.mock('fs/promises', () => ({
    readdir: mockReaddir,
    stat: mockStat,
    mkdir: mockMkdir,
    rename: mockRename,
}));

// Mock console.log/error/warn to capture output and prevent clutter during tests.
const mockConsoleLog = jest.spyOn(console, 'log').mockImplementation(() => {});
const mockConsoleError = jest.spyOn(console, 'error').mockImplementation(() => {});
const mockConsoleWarn = jest.spyOn(console, 'warn').mockImplementation(() => {});

describe('sweepDigitalDustBunnies', () => {
    const testPath = '/test/dir';
    const quarantineDirName = '.digital_compost_bin';
    const quarantinePath = path.join(testPath, quarantineDirName);
    const now = Date.now();
    const oldFileTime = now - (91 * 24 * 60 * 60 * 1000); // 91 days ago, older than 90-day threshold
    const newFileTime = now - (10 * 24 * 60 * 60 * 1000); // 10 days ago, newer than 90-day threshold

    beforeEach(() => {
        jest.clearAllMocks();
        mockConsoleLog.mockClear();
        mockConsoleError.mockClear();
        mockConsoleWarn.mockClear();
    });

    test('should identify and move old files in non-dry-run mode', async () => {
        mockReaddir.mockResolvedValueOnce([
            { name: 'old_file.txt', isDirectory: () => false },
            { name: 'new_file.txt', isDirectory: () => false },
            { name: 'some_dir', isDirectory: () => true }, // Should be skipped
        ]);
        mockStat
            .mockResolvedValueOnce({ mtimeMs: oldFileTime }) // old_file.txt
            .mockResolvedValueOnce({ mtimeMs: newFileTime }); // new_file.txt
        mockMkdir.mockResolvedValueOnce();
        mockRename.mockResolvedValueOnce();

        await sweepDigitalDustBunnies(testPath, 90, false, quarantineDirName);

        expect(mockMkdir).toHaveBeenCalledWith(quarantinePath, { recursive: true });
        expect(mockReaddir).toHaveBeenCalledWith(testPath, { withFileTypes: true });
        expect(mockStat).toHaveBeenCalledWith(path.join(testPath, 'old_file.txt'));
        expect(mockStat).toHaveBeenCalledWith(path.join(testPath, 'new_file.txt'));
        expect(mockRename).toHaveBeenCalledWith(
            path.join(testPath, 'old_file.txt'),
            path.join(quarantinePath, 'old_file.txt')
        );
        expect(mockRename).not.toHaveBeenCalledWith(
            path.join(testPath, 'new_file.txt'),
            expect.any(String)
        );
        expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Successfully swept 1 digital dust bunnies.'));
        expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('- old_file.txt'));
    });

    test('should identify old files but not move them in dry-run mode', async () => {
        mockReaddir.mockResolvedValueOnce([
            { name: 'old_file_dry.txt', isDirectory: () => false },
        ]);
        mockStat.mockResolvedValueOnce({ mtimeMs: oldFileTime });
        mockMkdir.mockResolvedValueOnce();
        mockRename.mockResolvedValueOnce(); // Should not be called

        await sweepDigitalDustBunnies(testPath, 90, true, quarantineDirName);

        expect(mockMkdir).toHaveBeenCalledWith(quarantinePath, { recursive: true });
        expect(mockReaddir).toHaveBeenCalledWith(testPath, { withFileTypes: true });
        expect(mockStat).toHaveBeenCalledWith(path.join(testPath, 'old_file_dry.txt'));
        expect(mockRename).not.toHaveBeenCalled();
        expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('DRY RUN mode: No files will be moved or deleted.'));
        expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Successfully swept 1 digital dust bunnies.'));
        expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('These files *would have been* moved (dry run):'));
    });

    test('should report no dust bunnies if no old files are found', async () => {
        mockReaddir.mockResolvedValueOnce([
            { name: 'new_file_1.txt', isDirectory: () => false },
            { name: 'new_file_2.txt', isDirectory: () => false },
        ]);
        mockStat
            .mockResolvedValueOnce({ mtimeMs: newFileTime })
            .mockResolvedValueOnce({ mtimeMs: newFileTime });
        mockMkdir.mockResolvedValueOnce();

        await sweepDigitalDustBunnies(testPath, 90, false, quarantineDirName);

        expect(mockRename).not.toHaveBeenCalled();
        expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('No digital dust bunnies found. Your digital space is sparkling clean!'));
    });

    test('should handle errors during readdir', async () => {
        mockReaddir.mockRejectedValueOnce(new Error('Permission denied'));
        mockMkdir.mockResolvedValueOnce();

        await sweepDigitalDustBunnies(testPath, 90, false, quarantineDirName);

        expect(mockConsoleError).toHaveBeenCalledWith(expect.stringContaining('Error during sweep: Permission denied'));
        expect(mockRename).not.toHaveBeenCalled();
        expect(mockConsoleLog).not.toHaveBeenCalledWith(expect.stringContaining('Successfully swept'));
    });

    test('should handle errors during stat', async () => {
        mockReaddir.mockResolvedValueOnce([
            { name: 'unreadable_file.txt', isDirectory: () => false },
        ]);
        mockStat.mockRejectedValueOnce(new Error('File not found'));
        mockMkdir.mockResolvedValueOnce();

        await sweepDigitalDustBunnies(testPath, 90, false, quarantineDirName);

        expect(mockConsoleWarn).toHaveBeenCalledWith(expect.stringContaining('Could not stat file unreadable_file.txt: File not found'));
        expect(mockRename).not.toHaveBeenCalled();
        expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('No digital dust bunnies found. Your digital space is sparkling clean!')); // Because no files were successfully processed as old
    });

    test('should handle errors during mkdir for quarantine directory', async () => {
        mockMkdir.mockRejectedValueOnce(new Error('Cannot create dir'));
        
        await sweepDigitalDustBunnies(testPath, 90, false, quarantineDirName);

        expect(mockConsoleError).toHaveBeenCalledWith(expect.stringContaining('Error creating quarantine directory: Cannot create dir'));
        expect(mockReaddir).not.toHaveBeenCalled(); // Should exit early if mkdir fails
        expect(mockRename).not.toHaveBeenCalled();
    });

    test('should handle errors during rename', async () => {
        mockReaddir.mockResolvedValueOnce([
            { name: 'old_file_rename_fail.txt', isDirectory: () => false },
        ]);
        mockStat.mockResolvedValueOnce({ mtimeMs: oldFileTime });
        mockMkdir.mockResolvedValueOnce();
        mockRename.mockRejectedValueOnce(new Error('Permission denied to move'));

        await sweepDigitalDustBunnies(testPath, 90, false, quarantineDirName);

        expect(mockRename).toHaveBeenCalled();
        expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Successfully swept 0 digital dust bunnies.')); // Because the move failed
        expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('No digital dust bunnies found. Your digital space is sparkling clean!'));
    });
});
