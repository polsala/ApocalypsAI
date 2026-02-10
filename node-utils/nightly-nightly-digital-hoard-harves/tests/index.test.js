const { collectDigitalArtifacts, program } = require('../src/index');
const fs = require('fs').promises;
const path = require('path');
const chalk = require('chalk');

// Mock rationale:
// fs.promises.readdir: To control the directory structure and file names returned,
//                      ensuring deterministic test results without actual file system access.
// fs.promises.stat: To control file metadata (size, modification time),
//                   allowing precise testing of filtering logic without relying on real file properties.
// console.log: To capture and assert the output of the CLI tool,
//              verifying that the correct messages are printed.
// process.exit: To prevent the test runner from exiting when the CLI tool finishes,
//               allowing assertions to be made after its execution.

jest.mock('fs', () => ({
    promises: {
        readdir: jest.fn(),
        stat: jest.fn(),
    },
}));

// Mock console.log to capture output
let consoleOutput = [];
const mockedLog = (output) => consoleOutput.push(output);
const originalLog = console.log;

// Mock process.exit to prevent tests from terminating
const mockExit = jest.spyOn(process, 'exit').mockImplementation(() => {});

describe('nightly-digital-hoard-harvester', () => {
    beforeEach(() => {
        jest.clearAllMocks();
        console.log = mockedLog; // Redirect console.log
        consoleOutput = [];
    });

    afterAll(() => {
        console.log = originalLog; // Restore console.log
        mockExit.mockRestore(); // Restore process.exit
    });

    // Helper to create mock stat objects
    const mockStat = (size, mtimeMs) => ({
        isFile: () => true,
        isDirectory: () => false,
        size: size,
        mtimeMs: mtimeMs,
    });

    // Helper to create mock directory entry objects
    const mockDirEntry = (name, isDirectory) => ({
        name,
        isDirectory: () => isDirectory,
        isFile: () => !isDirectory,
    });

    describe('collectDigitalArtifacts', () => {
        test('should find no files if directory is empty', async () => {
            fs.readdir.mockResolvedValue([]);
            const artifacts = await collectDigitalArtifacts('/test/dir', 0, 0);
            expect(artifacts).toEqual([]);
        });

        test('should find all files if no filters are applied', async () => {
            const now = Date.now();
            fs.readdir.mockResolvedValue([
                mockDirEntry('file1.txt', false),
                mockDirEntry('file2.log', false),
            ]);
            fs.stat.mockImplementation((p) => {
                if (p.includes('file1.txt')) return mockStat(100, now - 1000);
                if (p.includes('file2.log')) return mockStat(200, now - 2000);
                return Promise.reject(new Error('Not found'));
            });

            const artifacts = await collectDigitalArtifacts('/test/dir', undefined, undefined);
            expect(artifacts.length).toBe(2);
            expect(artifacts[0].path).toContain('file1.txt');
            expect(artifacts[1].path).toContain('file2.log');
        });

        test('should filter files older than specified days', async () => {
            const now = Date.now();
            const oneDayMs = 24 * 60 * 60 * 1000;
            fs.readdir.mockResolvedValue([
                mockDirEntry('recent.txt', false),
                mockDirEntry('old.log', false),
            ]);
            fs.stat.mockImplementation((p) => {
                if (p.includes('recent.txt')) return mockStat(100, now - (0.5 * oneDayMs)); // 0.5 days old
                if (p.includes('old.log')) return mockStat(200, now - (2 * oneDayMs)); // 2 days old
                return Promise.reject(new Error('Not found'));
            });

            const artifacts = await collectDigitalArtifacts('/test/dir', 1, undefined); // Older than 1 day
            expect(artifacts.length).toBe(1);
            expect(artifacts[0].path).toContain('old.log');
            expect(artifacts[0].isOld).toBe(true);
            expect(artifacts[0].isLarge).toBe(false);
        });

        test('should filter files larger than specified MB', async () => {
            const now = Date.now();
            fs.readdir.mockResolvedValue([
                mockDirEntry('small.txt', false),
                mockDirEntry('large.log', false),
            ]);
            fs.stat.mockImplementation((p) => {
                if (p.includes('small.txt')) return mockStat(5 * 1024 * 1024, now - 1000); // 5 MB
                if (p.includes('large.log')) return mockStat(15 * 1024 * 1024, now - 2000); // 15 MB
                return Promise.reject(new Error('Not found'));
            });

            const artifacts = await collectDigitalArtifacts('/test/dir', undefined, 10); // Larger than 10 MB
            expect(artifacts.length).toBe(1);
            expect(artifacts[0].path).toContain('large.log');
            expect(artifacts[0].isOld).toBe(false);
            expect(artifacts[0].isLarge).toBe(true);
        });

        test('should filter files by both age and size', async () => {
            const now = Date.now();
            const oneDayMs = 24 * 60 * 60 * 1000;
            fs.readdir.mockResolvedValue([
                mockDirEntry('old_small.txt', false),
                mockDirEntry('recent_large.log', false),
                mockDirEntry('old_large.zip', false),
            ]);
            fs.stat.mockImplementation((p) => {
                if (p.includes('old_small.txt')) return mockStat(5 * 1024 * 1024, now - (2 * oneDayMs)); // Old, small
                if (p.includes('recent_large.log')) return mockStat(15 * 1024 * 1024, now - (0.5 * oneDayMs)); // Recent, large
                if (p.includes('old_large.zip')) return mockStat(20 * 1024 * 1024, now - (3 * oneDayMs)); // Old, large
                return Promise.reject(new Error('Not found'));
            });

            const artifacts = await collectDigitalArtifacts('/test/dir', 1, 10); // Older than 1 day AND larger than 10 MB
            expect(artifacts.length).toBe(1);
            expect(artifacts[0].path).toContain('old_large.zip');
            expect(artifacts[0].isOld).toBe(true);
            expect(artifacts[0].isLarge).toBe(true);
        });

        test('should handle nested directories', async () => {
            const now = Date.now();
            const oneDayMs = 24 * 60 * 60 * 1000;

            fs.readdir.mockImplementation(async (p) => {
                if (p === '/test/dir') {
                    return [
                        mockDirEntry('subdir', true),
                        mockDirEntry('file_root.txt', false),
                    ];
                }
                if (p === '/test/dir/subdir') {
                    return [
                        mockDirEntry('file_nested.log', false),
                    ];
                }
                return [];
            });
            fs.stat.mockImplementation((p) => {
                if (p.includes('file_root.txt')) return mockStat(100, now - (2 * oneDayMs));
                if (p.includes('file_nested.log')) return mockStat(20 * 1024 * 1024, now - (3 * oneDayMs));
                return Promise.reject(new Error('Not found'));
            });

            const artifacts = await collectDigitalArtifacts('/test/dir', 1, 10);
            expect(artifacts.length).toBe(1);
            expect(artifacts[0].path).toContain('file_nested.log');
        });

        test('should gracefully handle permission errors for files', async () => {
            const now = Date.now();
            fs.readdir.mockResolvedValue([
                mockDirEntry('good_file.txt', false),
                mockDirEntry('bad_file.txt', false),
            ]);
            fs.stat.mockImplementation((p) => {
                if (p.includes('good_file.txt')) return mockStat(100, now - 1000);
                if (p.includes('bad_file.txt')) return Promise.reject(new Error('EACCES: Permission denied'));
                return Promise.reject(new Error('Not found'));
            });

            const artifacts = await collectDigitalArtifacts('/test/dir', undefined, undefined);
            expect(artifacts.length).toBe(1);
            expect(artifacts[0].path).toContain('good_file.txt');
            // Expect no crash, just skip the bad file
        });

        test('should gracefully handle permission errors for directories', async () => {
            fs.readdir.mockImplementation(async (p) => {
                if (p === '/test/dir') {
                    return [
                        mockDirEntry('good_subdir', true),
                        mockDirEntry('bad_subdir', true),
                    ];
                }
                if (p === '/test/dir/good_subdir') {
                    return [mockDirEntry('file_in_good.txt', false)];
                }
                if (p === '/test/dir/bad_subdir') {
                    return Promise.reject(new Error('EACCES: Permission denied'));
                }
                return [];
            });
            fs.stat.mockImplementation((p) => {
                if (p.includes('file_in_good.txt')) return mockStat(100, Date.now() - 1000);
                return Promise.reject(new Error('Not found'));
            });

            const artifacts = await collectDigitalArtifacts('/test/dir', undefined, undefined);
            expect(artifacts.length).toBe(1);
            expect(artifacts[0].path).toContain('file_in_good.txt');
            // Expect no crash, just skip the bad directory
        });
    });

    describe('CLI Program', () => {
        test('should exit with error if --path is not provided', async () => {
            await program.parseAsync(['node', 'index.js']);
            expect(mockExit).toHaveBeenCalledWith(1);
            expect(consoleOutput.some(line => line.includes('error: required option \'-p, --path <path>\' not specified'))).toBe(true);
        });

        test('should log a warning if no filters are provided', async () => {
            fs.readdir.mockResolvedValue([]);
            await program.parseAsync(['node', 'index.js', '--path', '/test/dir']);
            expect(consoleOutput.some(line => line.includes('⚠️  No filters specified.'))).toBe(true);
            expect(mockExit).not.toHaveBeenCalled(); // Should not exit with error, just warn
        });

        test('should report no artifacts found', async () => {
            fs.readdir.mockResolvedValue([]);
            await program.parseAsync(['node', 'index.js', '--path', '/test/dir', '--older-than-days', '1']);
            expect(consoleOutput.some(line => line.includes('✨ The digital landscape is pristine! No matching artifacts found.'))).toBe(true);
            expect(mockExit).not.toHaveBeenCalled();
        });

        test('should report found artifacts with filters', async () => {
            const now = Date.now();
            const oneDayMs = 24 * 60 * 60 * 1000;
            fs.readdir.mockResolvedValue([
                mockDirEntry('old_large.zip', false),
            ]);
            fs.stat.mockResolvedValue(mockStat(20 * 1024 * 1024, now - (3 * oneDayMs))); // Old, large

            await program.parseAsync(['node', 'index.js', '--path', '/test/dir', '--older-than-days', '1', '--larger-than-mb', '10']);
            expect(consoleOutput.some(line => line.includes('📜 Found 1 digital artifacts matching your criteria:'))).toBe(true);
            expect(consoleOutput.some(line => line.includes('old_large.zip'))).toBe(true);
            expect(consoleOutput.some(line => line.includes('(Old:'))).toBe(true);
            expect(consoleOutput.some(line => line.includes('(Size:'))).toBe(true);
            expect(mockExit).not.toHaveBeenCalled();
        });

        test('should handle collection errors gracefully in CLI', async () => {
            fs.readdir.mockRejectedValue(new Error('Permission denied to root path'));
            await program.parseAsync(['node', 'index.js', '--path', '/nonexistent/dir', '--older-than-days', '1']);
            expect(consoleOutput.some(line => line.includes('❌ An anomaly occurred during the harvest: Permission denied to root path'))).toBe(true);
            expect(mockExit).toHaveBeenCalledWith(1);
        });
    });
});
