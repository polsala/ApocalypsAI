const fs = require('fs');
const path = require('path');
const { sweepDirectory } = require('../src/sweeper'); // Assuming sweepDirectory is exported for testing

// Mock fs module
jest.mock('fs', () => ({
    // Mock rationale: To simulate file system existence checks without touching actual disk.
    existsSync: jest.fn(),
    // Mock rationale: To simulate directory listing without touching actual disk.
    readdirSync: jest.fn(),
    // Mock rationale: To simulate file stat retrieval (e.g., mtimeMs) without touching actual disk.
    statSync: jest.fn(),
    // Mock rationale: To simulate directory creation without touching actual disk.
    mkdirSync: jest.fn(),
    // Mock rationale: To simulate file moving/renaming without touching actual disk.
    renameSync: jest.fn(),
}));

// Helper to create mock Dirent objects
const createDirent = (name, isDirectory = false) => ({
    name,
    isDirectory: () => isDirectory,
    isFile: () => !isDirectory,
});

describe('sweepDirectory', () => {
    const mockRootPath = '/mock/test/dir';
    const mockArchiveDir = '/mock/archive';
    const defaultArchiveDir = path.join(mockRootPath, '.dustbunnies');
    const now = Date.now();

    beforeEach(() => {
        // Reset mocks before each test
        fs.existsSync.mockReset();
        fs.readdirSync.mockReset();
        fs.statSync.mockReset();
        fs.mkdirSync.mockReset();
        fs.renameSync.mockReset();

        // Default mock for existsSync: rootPath and archiveDir exist
        fs.existsSync.mockImplementation((p) => p === mockRootPath || p === mockArchiveDir || p === defaultArchiveDir);
    });

    test('should not sweep any files in dry-run mode', () => {
        fs.readdirSync.mockReturnValueOnce([
            createDirent('old_file.txt'),
            createDirent('new_file.txt'),
        ]);
        fs.statSync.mockImplementation((filePath) => {
            if (filePath.includes('old_file.txt')) {
                return { mtimeMs: now - (60 * 24 * 60 * 60 * 1000) }; // 60 days old
            } else if (filePath.includes('new_file.txt')) {
                return { mtimeMs: now - (1 * 24 * 60 * 60 * 1000) }; // 1 day old
            }
            return { mtimeMs: now };
        });

        const results = sweepDirectory(mockRootPath, 30, [], true, mockArchiveDir);

        expect(results.sweptFiles).toEqual([path.join(mockRootPath, 'old_file.txt')]);
        expect(results.skippedFiles).toEqual([path.join(mockRootPath, 'new_file.txt')]);
        expect(fs.renameSync).not.toHaveBeenCalled(); // No actual move in dry run
        expect(fs.mkdirSync).not.toHaveBeenCalled(); // No actual dir creation in dry run
    });

    test('should sweep old files into the specified archive directory', () => {
        fs.readdirSync.mockReturnValueOnce([
            createDirent('old_log.log'),
            createDirent('recent_doc.txt'),
            createDirent('another_old.bak'),
        ]);
        fs.statSync.mockImplementation((filePath) => {
            if (filePath.includes('old_log.log')) {
                return { mtimeMs: now - (40 * 24 * 60 * 60 * 1000) }; // 40 days old
            } else if (filePath.includes('recent_doc.txt')) {
                return { mtimeMs: now - (5 * 24 * 60 * 60 * 1000) }; // 5 days old
            } else if (filePath.includes('another_old.bak')) {
                return { mtimeMs: now - (50 * 24 * 60 * 60 * 1000) }; // 50 days old
            }
            return { mtimeMs: now };
        });

        // Ensure archiveDir exists for live run
        fs.existsSync.mockImplementation((p) => p === mockRootPath || p === mockArchiveDir);

        const results = sweepDirectory(mockRootPath, 30, [], false, mockArchiveDir);

        expect(results.sweptFiles).toEqual([
            path.join(mockRootPath, 'old_log.log'),
            path.join(mockRootPath, 'another_old.bak'),
        ]);
        expect(results.skippedFiles).toEqual([path.join(mockRootPath, 'recent_doc.txt')]);
        expect(fs.mkdirSync).toHaveBeenCalledWith(mockArchiveDir, { recursive: true });
        expect(fs.renameSync).toHaveBeenCalledWith(path.join(mockRootPath, 'old_log.log'), path.join(mockArchiveDir, 'old_log.log'));
        expect(fs.renameSync).toHaveBeenCalledWith(path.join(mockRootPath, 'another_old.bak'), path.join(mockArchiveDir, 'another_old.bak'));
        expect(fs.renameSync).toHaveBeenCalledTimes(2);
    });

    test('should sweep files with specified extensions and age', () => {
        fs.readdirSync.mockReturnValueOnce([
            createDirent('old_log.log'),
            createDirent('old_txt.txt'),
            createDirent('recent_log.log'),
            createDirent('old_json.json'),
        ]);
        fs.statSync.mockImplementation((filePath) => {
            if (filePath.includes('old_log.log')) {
                return { mtimeMs: now - (40 * 24 * 60 * 60 * 1000) }; // 40 days old
            } else if (filePath.includes('old_txt.txt')) {
                return { mtimeMs: now - (40 * 24 * 60 * 60 * 1000) }; // 40 days old
            } else if (filePath.includes('recent_log.log')) {
                return { mtimeMs: now - (5 * 24 * 60 * 60 * 1000) }; // 5 days old
            } else if (filePath.includes('old_json.json')) {
                return { mtimeMs: now - (40 * 24 * 60 * 60 * 1000) }; // 40 days old
            }
            return { mtimeMs: now };
        });

        fs.existsSync.mockImplementation((p) => p === mockRootPath || p === mockArchiveDir);

        const results = sweepDirectory(mockRootPath, 30, ['.log', '.txt'], false, mockArchiveDir);

        expect(results.sweptFiles).toEqual([
            path.join(mockRootPath, 'old_log.log'),
            path.join(mockRootPath, 'old_txt.txt'),
        ]);
        expect(results.skippedFiles).toEqual([
            path.join(mockRootPath, 'recent_log.log'),
            path.join(mockRootPath, 'old_json.json'), // Skipped because extension not targeted
        ]);
        expect(fs.renameSync).toHaveBeenCalledTimes(2);
    });

    test('should create default .dustbunnies directory if archive-dir is not specified', () => {
        fs.readdirSync.mockReturnValueOnce([
            createDirent('old_file.txt'),
        ]);
        fs.statSync.mockReturnValueOnce({ mtimeMs: now - (60 * 24 * 60 * 60 * 1000) });

        // Mock existsSync: rootPath exists, defaultArchiveDir does NOT exist initially
        fs.existsSync.mockImplementation((p) => p === mockRootPath);

        const results = sweepDirectory(mockRootPath, 30, [], false, defaultArchiveDir);

        expect(results.sweptFiles).toEqual([path.join(mockRootPath, 'old_file.txt')]);
        expect(fs.mkdirSync).toHaveBeenCalledWith(defaultArchiveDir, { recursive: true });
        expect(fs.renameSync).toHaveBeenCalledWith(path.join(mockRootPath, 'old_file.txt'), path.join(defaultArchiveDir, 'old_file.txt'));
    });

    test('should handle subdirectories and skip archive directory', () => {
        const subDir1 = path.join(mockRootPath, 'sub1');
        const subDir2 = path.join(mockRootPath, 'sub2');
        const archiveSubDir = path.join(mockRootPath, '.dustbunnies'); // Default archive dir

        fs.readdirSync.mockImplementation((p) => {
            if (p === mockRootPath) {
                return [
                    createDirent('file_in_root.txt'),
                    createDirent('sub1', true),
                    createDirent('sub2', true),
                    createDirent('.dustbunnies', true), // Archive dir itself
                ];
            } else if (p === subDir1) {
                return [createDirent('file_in_sub1.log')];
            } else if (p === subDir2) {
                return [createDirent('file_in_sub2.tmp')];
            }
            return [];
        });

        fs.statSync.mockImplementation((filePath) => {
            // All files are old enough
            return { mtimeMs: now - (60 * 24 * 60 * 60 * 1000) };
        });

        // Mock existsSync to ensure all paths are considered existing
        fs.existsSync.mockImplementation((p) => {
            return [mockRootPath, subDir1, subDir2, archiveSubDir, path.join(mockRootPath, 'file_in_root.txt'), path.join(subDir1, 'file_in_sub1.log'), path.join(subDir2, 'file_in_sub2.tmp')].includes(p);
        });

        const results = sweepDirectory(mockRootPath, 30, [], false, archiveSubDir);

        expect(results.sweptFiles).toEqual([
            path.join(mockRootPath, 'file_in_root.txt'),
            path.join(subDir1, 'file_in_sub1.log'),
            path.join(subDir2, 'file_in_sub2.tmp'),
        ]);
        expect(results.skippedFiles).toEqual([]);
        expect(fs.renameSync).toHaveBeenCalledTimes(3);
        // Ensure the archive directory itself is not scanned or swept
        expect(fs.readdirSync).not.toHaveBeenCalledWith(archiveSubDir, expect.any(Object));
    });

    test('should return empty arrays if rootPath does not exist', () => {
        fs.existsSync.mockReturnValueOnce(false); // Root path does not exist

        const results = sweepDirectory('/nonexistent/path', 30, [], false, mockArchiveDir);

        expect(results.sweptFiles).toEqual([]);
        expect(results.skippedFiles).toEqual([]);
        expect(fs.readdirSync).not.toHaveBeenCalled();
        expect(fs.mkdirSync).not.toHaveBeenCalled();
        expect(fs.renameSync).not.toHaveBeenCalled();
    });
});
