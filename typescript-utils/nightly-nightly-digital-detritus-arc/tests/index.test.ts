import * as fs from 'fs';
import * as path from 'path';
import { ArchivistConfig, Category, Rule } from '../src/types';

// Mock the entire fs module
jest.mock('fs', () => ({
    // Mock rationale: We need to control file system interactions for deterministic tests.
    // This includes reading directories, getting file stats, reading file content, and simulating file moves/creations.
    existsSync: jest.fn(),
    readdirSync: jest.fn(),
    statSync: jest.fn(),
    readFileSync: jest.fn(),
    mkdirSync: jest.fn(),
    renameSync: jest.fn(),
}));

// Mock console.log to capture output
const mockConsoleLog = jest.spyOn(console, 'log').mockImplementation(() => {});
const mockConsoleError = jest.spyOn(console, 'error').mockImplementation(() => {});
const mockConsoleWarn = jest.spyOn(console, 'warn').mockImplementation(() => {});

// Import the functions to be tested after mocking fs
const { default: mainModule } = require('../src/index'); // Use require to get the module after mocks
const { loadConfig, classifyFile, archiveFiles } = mainModule;

describe('Nightly Digital Detritus Archivist', () => {
    const mockSourceDir = '/mock/source';
    const mockDestDir = '/mock/destination';
    const mockConfigPath = '/mock/config.json';

    const mockConfig: ArchivistConfig = {
        defaultCategoryName: 'Unclassified Scraps',
        categories: [
            {
                name: 'Survival Blueprints',
                description: 'Critical schematics.',
                rules: [
                    { type: 'extension', pattern: '(.pdf|.doc|.txt)$' },
                    { type: 'content', pattern: '(blueprint|schematic)' }
                ],
                destinationSubdir: 'blueprints'
            },
            {
                name: 'Emergency Broadcast Logs',
                description: 'Vital communications.',
                rules: [
                    { type: 'name', pattern: '^(emergency|broadcast)' },
                    { type: 'extension', pattern: '.log$' }
                ],
                destinationSubdir: 'broadcasts'
            },
            {
                name: 'Pre-Collapse Mementos',
                description: 'Personal photos.',
                rules: [
                    { type: 'extension', pattern: '(.jpg|.png)$' },
                    { type: 'size', minSizeKB: 100, maxSizeKB: 5000 }
                ],
                destinationSubdir: 'mementos'
            }
        ]
    };

    const mockDefaultCategory: Category = {
        name: 'Unclassified Scraps',
        description: 'Files that did not match any specific archiving rules.',
        rules: [],
        destinationSubdir: 'unclassified'
    };

    beforeEach(() => {
        jest.clearAllMocks();
        // Reset process.argv for each test
        process.argv = ['node', 'index.js'];

        // Default mock for existsSync
        (fs.existsSync as jest.Mock).mockReturnValue(true);
        // Default mock for readFileSync for config
        (fs.readFileSync as jest.Mock).mockImplementation((p: string, encoding: string) => {
            if (p === mockConfigPath) {
                return JSON.stringify(mockConfig);
            }
            // For content rules, return dummy content
            if (p.includes('blueprint-file.txt')) return 'This is a blueprint.';
            if (p.includes('log-file.log')) return 'Emergency broadcast received.';
            return '';
        });
    });

    describe('loadConfig', () => {
        it('should load and parse a valid configuration file', () => {
            const config = loadConfig(mockConfigPath);
            expect(config).toEqual(mockConfig);
            expect(fs.readFileSync).toHaveBeenCalledWith(mockConfigPath, 'utf8');
        });

        it('should exit if config file is invalid JSON', () => {
            (fs.readFileSync as jest.Mock).mockReturnValueOnce('invalid json');
            const mockExit = jest.spyOn(process, 'exit').mockImplementation((() => {}) as any);
            loadConfig(mockConfigPath);
            expect(mockConsoleError).toHaveBeenCalled();
            expect(mockExit).toHaveBeenCalledWith(1);
            mockExit.mockRestore();
        });

        it('should exit if config structure is invalid', () => {
            (fs.readFileSync as jest.Mock).mockReturnValueOnce(JSON.stringify({ categories: [] })); // Missing defaultCategoryName
            const mockExit = jest.spyOn(process, 'exit').mockImplementation((() => {}) as any);
            loadConfig(mockConfigPath);
            expect(mockConsoleError).toHaveBeenCalled();
            expect(mockExit).toHaveBeenCalledWith(1);
            mockExit.mockRestore();
        });
    });

    describe('classifyFile', () => {
        const createFileStats = (size: number, isFile: boolean = true) => ({
            size: size,
            isFile: () => isFile,
            isDirectory: () => !isFile,
            // Add other fs.Stats properties if needed by matchesRule
            dev: 0, ino: 0, mode: 0, nlink: 0, uid: 0, gid: 0, rdev: 0, blksize: 0, blocks: 0,
            atimeMs: 0, mtimeMs: 0, ctimeMs: 0, birthtimeMs: 0,
            atime: new Date(), mtime: new Date(), ctime: new Date(), birthtime: new Date()
        });

        it('should classify a file by extension into Survival Blueprints', () => {
            const filePath = path.join(mockSourceDir, 'plan.pdf');
            const fileStats = createFileStats(1000);
            const category = classifyFile(filePath, fileStats, mockConfig);
            expect(category.name).toBe('Survival Blueprints');
        });

        it('should classify a file by content into Survival Blueprints', () => {
            const filePath = path.join(mockSourceDir, 'blueprint-file.txt');
            const fileStats = createFileStats(1000);
            const category = classifyFile(filePath, fileStats, mockConfig);
            expect(category.name).toBe('Survival Blueprints');
        });

        it('should classify a file by name into Emergency Broadcast Logs', () => {
            const filePath = path.join(mockSourceDir, 'emergency_alert.log');
            const fileStats = createFileStats(500);
            const category = classifyFile(filePath, fileStats, mockConfig);
            expect(category.name).toBe('Emergency Broadcast Logs');
        });

        it('should classify a file by size into Pre-Collapse Mementos', () => {
            const filePath = path.join(mockSourceDir, 'old_photo.jpg');
            const fileStats = createFileStats(200 * 1024); // 200KB
            const category = classifyFile(filePath, fileStats, mockConfig);
            expect(category.name).toBe('Pre-Collapse Mementos');
        });

        it('should classify a file into the default category if no rules match', () => {
            const filePath = path.join(mockSourceDir, 'random_note.md');
            const fileStats = createFileStats(50);
            const category = classifyFile(filePath, fileStats, mockConfig);
            expect(category.name).toBe('Unclassified Scraps');
            expect(category.destinationSubdir).toBe('unclassified');
        });

        it('should handle content rule for unreadable files gracefully', () => {
            (fs.readFileSync as jest.Mock).mockImplementationOnce(() => { throw new Error('Permission denied'); });
            const filePath = path.join(mockSourceDir, 'secret_binary.bin');
            const fileStats = createFileStats(1000);
            const category = classifyFile(filePath, fileStats, mockConfig);
            expect(category.name).toBe('Unclassified Scraps'); // Should fall back to default
        });
    });

    describe('archiveFiles', () => {
        const mockFileStats = (size: number) => ({
            size: size,
            isFile: () => true,
            isDirectory: () => false,
            dev: 0, ino: 0, mode: 0, nlink: 0, uid: 0, gid: 0, rdev: 0, blksize: 0, blocks: 0,
            atimeMs: 0, mtimeMs: 0, ctimeMs: 0, birthtimeMs: 0,
            atime: new Date(), mtime: new Date(), ctime: new Date(), birthtime: new Date()
        });

        beforeEach(() => {
            (fs.readdirSync as jest.Mock).mockReturnValue([
                'plan.pdf', // Blueprints (extension)
                'emergency_log.txt', // Broadcasts (name)
                'photo.jpg', // Mementos (size)
                'random.txt', // Unclassified
                'blueprint-doc.txt' // Blueprints (content)
            ]);
            (fs.statSync as jest.Mock).mockImplementation((p: string) => {
                if (p.includes('plan.pdf')) return mockFileStats(150 * 1024); // 150KB
                if (p.includes('emergency_log.txt')) return mockFileStats(50 * 1024); // 50KB
                if (p.includes('photo.jpg')) return mockFileStats(200 * 1024); // 200KB
                if (p.includes('random.txt')) return mockFileStats(10 * 1024); // 10KB
                if (p.includes('blueprint-doc.txt')) return mockFileStats(300 * 1024); // 300KB
                return mockFileStats(0); // Default for others
            });
            (fs.readFileSync as jest.Mock).mockImplementation((p: string) => {
                if (p.includes('blueprint-doc.txt')) return 'This is a blueprint document.';
                return '';
            });
        });

        it('should perform a dry run without moving files', async () => {
            await archiveFiles(mockSourceDir, mockDestDir, mockConfigPath, true);

            expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('--- Digital Detritus Archivist (DRY RUN) ---'));
            expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining("'plan.pdf' (150.00 KB) -> Category: 'Survival Blueprints' (Subdir: 'blueprints')"));
            expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining("'emergency_log.txt' (50.00 KB) -> Category: 'Emergency Broadcast Logs' (Subdir: 'broadcasts')"));
            expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining("'photo.jpg' (200.00 KB) -> Category: 'Pre-Collapse Mementos' (Subdir: 'mementos')"));
            expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining("'random.txt' (10.00 KB) -> Category: 'Unclassified Scraps' (Subdir: 'unclassified')"));
            expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining("'blueprint-doc.txt' (300.00 KB) -> Category: 'Survival Blueprints' (Subdir: 'blueprints')"));

            expect(fs.mkdirSync).not.toHaveBeenCalled();
            expect(fs.renameSync).not.toHaveBeenCalled();
        });

        it('should move files to correct destinations in actual run', async () => {
            await archiveFiles(mockSourceDir, mockDestDir, mockConfigPath, false);

            expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('--- Digital Detritus Archivist ---'));

            // Check mkdirSync calls
            expect(fs.mkdirSync).toHaveBeenCalledWith(path.join(mockDestDir, 'blueprints'), { recursive: true });
            expect(fs.mkdirSync).toHaveBeenCalledWith(path.join(mockDestDir, 'broadcasts'), { recursive: true });
            expect(fs.mkdirSync).toHaveBeenCalledWith(path.join(mockDestDir, 'mementos'), { recursive: true });
            expect(fs.mkdirSync).toHaveBeenCalledWith(path.join(mockDestDir, 'unclassified'), { recursive: true });

            // Check renameSync calls
            expect(fs.renameSync).toHaveBeenCalledWith(path.join(mockSourceDir, 'plan.pdf'), path.join(mockDestDir, 'blueprints', 'plan.pdf'));
            expect(fs.renameSync).toHaveBeenCalledWith(path.join(mockSourceDir, 'emergency_log.txt'), path.join(mockDestDir, 'broadcasts', 'emergency_log.txt'));
            expect(fs.renameSync).toHaveBeenCalledWith(path.join(mockSourceDir, 'photo.jpg'), path.join(mockDestDir, 'mementos', 'photo.jpg'));
            expect(fs.renameSync).toHaveBeenCalledWith(path.join(mockSourceDir, 'random.txt'), path.join(mockDestDir, 'unclassified', 'random.txt'));
            expect(fs.renameSync).toHaveBeenCalledWith(path.join(mockSourceDir, 'blueprint-doc.txt'), path.join(mockDestDir, 'blueprints', 'blueprint-doc.txt'));
        });

        it('should handle empty source directory', async () => {
            (fs.readdirSync as jest.Mock).mockReturnValueOnce([]);
            await archiveFiles(mockSourceDir, mockDestDir, mockConfigPath, false);
            expect(mockConsoleLog).toHaveBeenCalledWith('No files found in the source directory to archive.');
            expect(fs.renameSync).not.toHaveBeenCalled();
        });

        it('should exit if source directory does not exist', async () => {
            (fs.existsSync as jest.Mock).mockImplementation((p: string) => p !== mockSourceDir);
            const mockExit = jest.spyOn(process, 'exit').mockImplementation((() => {}) as any);
            await archiveFiles(mockSourceDir, mockDestDir, mockConfigPath, false);
            expect(mockConsoleError).toHaveBeenCalledWith(expect.stringContaining(`Error: Source directory '${mockSourceDir}' does not exist.`));
            expect(mockExit).toHaveBeenCalledWith(1);
            mockExit.mockRestore();
        });

        it('should exit if destination directory does not exist', async () => {
            (fs.existsSync as jest.Mock).mockImplementation((p: string) => p !== mockDestDir);
            const mockExit = jest.spyOn(process, 'exit').mockImplementation((() => {}) as any);
            await archiveFiles(mockSourceDir, mockDestDir, mockConfigPath, false);
            expect(mockConsoleError).toHaveBeenCalledWith(expect.stringContaining(`Error: Destination directory '${mockDestDir}' does not exist.`));
            expect(mockExit).toHaveBeenCalledWith(1);
            mockExit.mockRestore();
        });

        it('should warn and skip if file cannot be statted', async () => {
            (fs.readdirSync as jest.Mock).mockReturnValueOnce(['unreadable.txt']);
            (fs.statSync as jest.Mock).mockImplementationOnce(() => { throw new Error('Permission denied'); });
            await archiveFiles(mockSourceDir, mockDestDir, mockConfigPath, false);
            expect(mockConsoleWarn).toHaveBeenCalledWith(expect.stringContaining("Skipping 'unreadable.txt': Could not stat file."));
            expect(fs.renameSync).not.toHaveBeenCalled();
        });

        it('should skip directories', async () => {
            (fs.readdirSync as jest.Mock).mockReturnValueOnce(['my_dir']);
            (fs.statSync as jest.Mock).mockReturnValueOnce({
                isFile: () => false,
                isDirectory: () => true,
                size: 0, dev: 0, ino: 0, mode: 0, nlink: 0, uid: 0, gid: 0, rdev: 0, blksize: 0, blocks: 0,
                atimeMs: 0, mtimeMs: 0, ctimeMs: 0, birthtimeMs: 0,
                atime: new Date(), mtime: new Date(), ctime: new Date(), birthtime: new Date()
            });
            await archiveFiles(mockSourceDir, mockDestDir, mockConfigPath, false);
            expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining("Skipping 'my_dir': Not a file."));
            expect(fs.renameSync).not.toHaveBeenCalled();
        });

        it('should log error if file move fails', async () => {
            (fs.renameSync as jest.Mock).mockImplementationOnce(() => { throw new Error('Disk full'); });
            await archiveFiles(mockSourceDir, mockDestDir, mockConfigPath, false);
            expect(mockConsoleError).toHaveBeenCalledWith(expect.stringContaining("Error moving 'plan.pdf': Disk full"));
            // Other files should still attempt to move
            expect(fs.renameSync).toHaveBeenCalledWith(path.join(mockSourceDir, 'emergency_log.txt'), path.join(mockDestDir, 'broadcasts', 'emergency_log.txt'));
        });
    });

    describe('CLI Entry Point (main)', () => {
        it('should call archiveFiles with correct arguments', async () => {
            const mockArchiveFiles = jest.spyOn(mainModule, 'archiveFiles').mockResolvedValue(undefined);
            process.argv = ['node', 'index.js', '--source', mockSourceDir, '--dest', mockDestDir, '--config', mockConfigPath, '--dry-run'];
            await mainModule.main();
            expect(mockArchiveFiles).toHaveBeenCalledWith(mockSourceDir, mockDestDir, mockConfigPath, true);
            mockArchiveFiles.mockRestore();
        });

        it('should exit with error if required arguments are missing', async () => {
            const mockExit = jest.spyOn(process, 'exit').mockImplementation((() => {}) as any);
            process.argv = ['node', 'index.js', '--source', mockSourceDir]; // Missing dest and config
            await mainModule.main();
            expect(mockConsoleError).toHaveBeenCalledWith(expect.stringContaining('Error: Missing required arguments'));
            expect(mockExit).toHaveBeenCalledWith(1);
            mockExit.mockRestore();
        });

        it('should print help and exit for --help argument', async () => {
            const mockExit = jest.spyOn(process, 'exit').mockImplementation((() => {}) as any);
            process.argv = ['node', 'index.js', '--help'];
            await mainModule.main();
            expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Usage: nightly-digital-detritus-arch'));
            expect(mockExit).toHaveBeenCalledWith(0);
            mockExit.mockRestore();
        });

        it('should exit for unknown arguments', async () => {
            const mockExit = jest.spyOn(process, 'exit').mockImplementation((() => {}) as any);
            process.argv = ['node', 'index.js', '--unknown-arg'];
            await mainModule.main();
            expect(mockConsoleError).toHaveBeenCalledWith(expect.stringContaining('Unknown argument: --unknown-arg'));
            expect(mockExit).toHaveBeenCalledWith(1);
            mockExit.mockRestore();
        });
    });
});
