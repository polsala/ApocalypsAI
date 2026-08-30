import { promises as fs } from 'fs';
import * as path from 'path';
import { getFileInfo, scanDirectory, filterDustBunnies } from '../src/index';
import { FileInfo, ScanOptions } from '../src/types';

// Mock fs/promises to prevent actual file system interactions during tests.
jest.mock('fs', () => ({
    promises: {
        readdir: jest.fn(),
        stat: jest.fn(),
    },
}));

// Mock rationale: We need to simulate file system interactions (listing directory contents, getting file metadata)
// without actually touching the disk. This ensures tests are fast, deterministic, and isolated from the host system's file state.

describe('Temporal Dust Bunny Collector', () => {
    const mockReaddir = fs.readdir as jest.Mock;
    const mockStat = fs.stat as jest.Mock;

    beforeEach(() => {
        jest.clearAllMocks();
    });

    describe('getFileInfo', () => {
        it('should return file info for a valid file path', async () => {
            const mockDate = new Date();
            mockStat.mockResolvedValue({
                isDirectory: () => false,
                mtime: mockDate,
                size: 1234,
            });
            const info = await getFileInfo('/test/file.txt');
            expect(info).toEqual({
                name: 'file.txt',
                path: '/test/file.txt',
                isDirectory: false,
                modifiedAt: mockDate,
                size: 1234,
            });
            expect(mockStat).toHaveBeenCalledWith('/test/file.txt');
        });

        it('should return null for an inaccessible file path', async () => {
            mockStat.mockRejectedValue(new Error('Permission denied'));
            const info = await getFileInfo('/test/inaccessible.txt');
            expect(info).toBeNull();
            expect(mockStat).toHaveBeenCalledWith('/test/inaccessible.txt');
        });
    });

    describe('scanDirectory', () => {
        it('should scan a flat directory and return file info', async () => {
            mockReaddir.mockResolvedValueOnce([
                { name: 'file1.txt', isDirectory: () => false },
                { name: 'file2.log', isDirectory: () => false },
            ]);
            const mockDate = new Date();
            mockStat.mockResolvedValue({
                isDirectory: () => false,
                mtime: mockDate,
                size: 100,
            });

            const options: ScanOptions = { ageDays: 30, patterns: [], recursive: false, dryRun: true };
            const files = await scanDirectory('/test/dir', options);

            expect(files).toHaveLength(2);
            expect(files[0].name).toBe('file1.txt');
            expect(files[1].name).toBe('file2.log');
            expect(mockReaddir).toHaveBeenCalledWith('/test/dir', { withFileTypes: true });
            expect(mockStat).toHaveBeenCalledTimes(2);
        });

        it('should scan recursively if the recursive option is true', async () => {
            mockReaddir
                .mockResolvedValueOnce([
                    { name: 'file1.txt', isDirectory: () => false },
                    { name: 'subdir', isDirectory: () => true },
                ])
                .mockResolvedValueOnce([
                    { name: 'file2.log', isDirectory: () => false },
                ]);
            const mockDate = new Date();
            mockStat.mockResolvedValue({
                isDirectory: () => false,
                mtime: mockDate,
                size: 100,
            });

            const options: ScanOptions = { ageDays: 30, patterns: [], recursive: true, dryRun: true };
            const files = await scanDirectory('/test/dir', options);

            expect(files).toHaveLength(2);
            expect(files.map(f => f.name)).toEqual(expect.arrayContaining(['file1.txt', 'file2.log']));
            expect(mockReaddir).toHaveBeenCalledTimes(2);
            expect(mockReaddir).toHaveBeenCalledWith('/test/dir', { withFileTypes: true });
            expect(mockReaddir).toHaveBeenCalledWith('/test/dir/subdir', { withFileTypes: true });
            expect(mockStat).toHaveBeenCalledTimes(2); // Only for files, not directories
        });

        it('should handle an empty directory gracefully', async () => {
            mockReaddir.mockResolvedValue([]);
            const options: ScanOptions = { ageDays: 30, patterns: [], recursive: false, dryRun: true };
            const files = await scanDirectory('/test/empty', options);
            expect(files).toHaveLength(0);
            expect(mockReaddir).toHaveBeenCalledWith('/test/empty', { withFileTypes: true });
            expect(mockStat).not.toHaveBeenCalled();
        });

        it('should not scan recursively if the recursive option is false', async () => {
            mockReaddir.mockResolvedValueOnce([
                { name: 'file1.txt', isDirectory: () => false },
                { name: 'subdir', isDirectory: () => true },
            ]);
            const mockDate = new Date();
            mockStat.mockResolvedValue({
                isDirectory: () => false,
                mtime: mockDate,
                size: 100,
            });

            const options: ScanOptions = { ageDays: 30, patterns: [], recursive: false, dryRun: true };
            const files = await scanDirectory('/test/dir', options);

            expect(files).toHaveLength(1);
            expect(files[0].name).toBe('file1.txt');
            expect(mockReaddir).toHaveBeenCalledTimes(1);
            expect(mockReaddir).toHaveBeenCalledWith('/test/dir', { withFileTypes: true });
            expect(mockStat).toHaveBeenCalledTimes(1);
        });
    });

    describe('filterDustBunnies', () => {
        const now = new Date();
        const thirtyDaysAgo = new Date(now.getTime() - (30 * 24 * 60 * 60 * 1000));
        const twentyDaysAgo = new Date(now.getTime() - (20 * 24 * 60 * 60 * 1000));
        const fortyDaysAgo = new Date(now.getTime() - (40 * 24 * 60 * 60 * 1000));

        const mockFiles: FileInfo[] = [
            { name: 'old_log.log', path: '/a/old_log.log', isDirectory: false, modifiedAt: fortyDaysAgo, size: 100 },
            { name: 'recent_report.pdf', path: '/a/recent_report.pdf', isDirectory: false, modifiedAt: twentyDaysAgo, size: 200 },
            { name: 'temp_data.bak', path: '/a/temp_data.bak', isDirectory: false, modifiedAt: twentyDaysAgo, size: 50 }, // Matches pattern, not age
            { name: 'important.txt', path: '/a/important.txt', isDirectory: false, modifiedAt: fortyDaysAgo, size: 300 }, // Old, but no pattern
            { name: 'another_temp.tmp', path: '/a/another_temp.tmp', isDirectory: false, modifiedAt: twentyDaysAgo, size: 75 }, // Matches pattern, not age
            { name: 'very_old.log', path: '/a/very_old.log', isDirectory: false, modifiedAt: new Date(now.getTime() - (100 * 24 * 60 * 60 * 1000)), size: 150 } // Very old
        ];

        it('should filter files correctly based on age threshold', () => {
            const options: ScanOptions = { ageDays: 30, patterns: [], recursive: false, dryRun: true };
            const dustBunnies = filterDustBunnies(mockFiles, options);
            expect(dustBunnies).toHaveLength(3);
            expect(dustBunnies.map(f => f.name)).toEqual(expect.arrayContaining(['old_log.log', 'important.txt', 'very_old.log']));
        });

        it('should filter files correctly based on provided patterns', () => {
            const options: ScanOptions = { ageDays: 90, patterns: ['\\.bak$', 'temp_.*'], recursive: false, dryRun: true }; // High age to isolate pattern test
            const dustBunnies = filterDustBunnies(mockFiles, options);
            expect(dustBunnies).toHaveLength(2);
            expect(dustBunnies.map(f => f.name)).toEqual(expect.arrayContaining(['temp_data.bak', 'another_temp.tmp']));
        });

        it('should filter files correctly based on both age and patterns (OR logic)', () => {
            const options: ScanOptions = { ageDays: 30, patterns: ['\\.bak$', 'temp_.*'], recursive: false, dryRun: true };
            const dustBunnies = filterDustBunnies(mockFiles, options);
            expect(dustBunnies).toHaveLength(5);
            expect(dustBunnies.map(f => f.name)).toEqual(expect.arrayContaining([
                'old_log.log',      // Old
                'temp_data.bak',    // Pattern
                'important.txt',    // Old
                'another_temp.tmp', // Pattern
                'very_old.log'      // Old
            ]));
        });

        it('should return an empty array if no dust bunnies are found', () => {
            const options: ScanOptions = { ageDays: 1, patterns: ['nonexistent_pattern'], recursive: false, dryRun: true };
            const dustBunnies = filterDustBunnies(mockFiles, options);
            expect(dustBunnies).toHaveLength(0);
        });

        it('should handle empty file list', () => {
            const options: ScanOptions = { ageDays: 30, patterns: [], recursive: false, dryRun: true };
            const dustBunnies = filterDustBunnies([], options);
            expect(dustBunnies).toHaveLength(0);
        });
    });
});
