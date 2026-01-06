const { findDustBunnies, categorizeDustBunnies, generateReport } = require('../src/index');
const path = require('path'); // Original path module

// # Mock rationale:
// We need to simulate file system operations (readdir, stat) without actually touching the disk
// to ensure deterministic and offline tests. The 'path' module is also mocked to ensure
// consistent path separators across different operating systems for test stability.

// Mock fs.promises and path module
const mockFs = {
    readdir: jest.fn(),
    stat: jest.fn(),
};

const mockPath = {
    join: jest.fn((...args) => args.join('/')), // Use '/' for consistent path joining
    extname: jest.fn((p) => path.extname(p)), // Keep original extname logic
    relative: jest.fn((from, to) => {
        const relativePath = path.relative(from, to);
        return relativePath.replace(/\\/g, '/'); // Ensure '/' for relative paths
    }),
    basename: jest.fn((p) => path.basename(p)),
};

// Replace the actual modules with mocks for testing
jest.mock('fs/promises', () => mockFs);
jest.mock('path', () => mockPath);

describe('Nightly Digital Dust Bunny Collector', () => {
    beforeEach(() => {
        jest.clearAllMocks();
        // Reset path.join to use '/' for consistency in tests
        mockPath.join.mockImplementation((...args) => args.join('/'));
        mockPath.relative.mockImplementation((from, to) => {
            const relativePath = path.relative(from, to);
            return relativePath.replace(/\\/g, '/'); // Ensure '/' for relative paths
        });
    });

    describe('findDustBunnies', () => {
        test('should find small files in a flat directory', async () => {
            const mockDir = '/test/dir';
            mockFs.readdir.mockResolvedValueOnce([
                { name: 'file1.txt', isDirectory: () => false, isFile: () => true },
                { name: 'file2.log', isDirectory: () => false, isFile: () => true },
                { name: 'large.img', isDirectory: () => false, isFile: () => true },
            ]);
            mockFs.stat
                .mockResolvedValueOnce({ size: 500 }) // file1.txt
                .mockResolvedValueOnce({ size: 1024 }) // file2.log
                .mockResolvedValueOnce({ size: 20 * 1024 }); // large.img (too big)

            const bunnies = await findDustBunnies(mockDir, 10); // Max 10KB

            expect(bunnies).toHaveLength(2);
            expect(bunnies[0]).toEqual({
                path: '/test/dir/file1.txt',
                size: 500,
                extension: '.txt',
                name: 'file1.txt'
            });
            expect(bunnies[1]).toEqual({
                path: '/test/dir/file2.log',
                size: 1024,
                extension: '.log',
                name: 'file2.log'
            });
            expect(mockFs.readdir).toHaveBeenCalledWith(mockDir, { withFileTypes: true });
            expect(mockFs.stat).toHaveBeenCalledTimes(3);
        });

        test('should handle nested directories and filter by size', async () => {
            const mockDir = '/test/root';
            mockFs.readdir
                .mockResolvedValueOnce([ // /test/root
                    { name: 'sub1', isDirectory: () => true, isFile: () => false },
                    { name: 'fileA.js', isDirectory: () => false, isFile: () => true },
                ])
                .mockResolvedValueOnce([ // /test/root/sub1
                    { name: 'fileB.json', isDirectory: () => false, isFile: () => true },
                    { name: 'sub2', isDirectory: () => true, isFile: () => false },
                ])
                .mockResolvedValueOnce([ // /test/root/sub1/sub2
                    { name: 'fileC.txt', isDirectory: () => false, isFile: () => true },
                    { name: 'bigfile.data', isDirectory: () => false, isFile: () => true },
                ]);

            mockFs.stat
                .mockResolvedValueOnce({ size: 2000 }) // fileA.js
                .mockResolvedValueOnce({ size: 500 })  // fileB.json
                .mockResolvedValueOnce({ size: 100 })  // fileC.txt
                .mockResolvedValueOnce({ size: 15 * 1024 }); // bigfile.data (too big)

            const bunnies = await findDustBunnies(mockDir, 5); // Max 5KB

            expect(bunnies).toHaveLength(3);
            expect(bunnies.map(b => b.name)).toEqual(['fileA.js', 'fileB.json', 'fileC.txt']);
            expect(bunnies.map(b => b.size)).toEqual([2000, 500, 100]);
            expect(mockFs.readdir).toHaveBeenCalledTimes(3);
            expect(mockFs.stat).toHaveBeenCalledTimes(4);
        });

        test('should skip node_modules and .git directories', async () => {
            const mockDir = '/project';
            mockFs.readdir
                .mockResolvedValueOnce([
                    { name: 'src', isDirectory: () => true, isFile: () => false },
                    { name: 'node_modules', isDirectory: () => true, isFile: () => false },
                    { name: '.git', isDirectory: () => true, isFile: () => false },
                    { name: 'package.json', isDirectory: () => false, isFile: () => true },
                ])
                .mockResolvedValueOnce([ // /project/src
                    { name: 'main.js', isDirectory: () => false, isFile: () => true },
                ]);

            mockFs.stat
                .mockResolvedValueOnce({ size: 1000 }) // package.json
                .mockResolvedValueOnce({ size: 500 }); // main.js

            const bunnies = await findDustBunnies(mockDir, 10);

            expect(bunnies).toHaveLength(2);
            expect(bunnies.map(b => b.name)).toEqual(['package.json', 'main.js']);
            expect(mockFs.readdir).toHaveBeenCalledTimes(2); // Should not read node_modules or .git
        });

        test('should handle empty directories', async () => {
            const mockDir = '/empty';
            mockFs.readdir.mockResolvedValueOnce([]);
            const bunnies = await findDustBunnies(mockDir, 10);
            expect(bunnies).toHaveLength(0);
            expect(mockFs.readdir).toHaveBeenCalledWith(mockDir, { withFileTypes: true });
        });

        test('should handle unreadable directories gracefully', async () => {
            const mockDir = '/unreadable';
            mockFs.readdir.mockRejectedValueOnce(new Error('Permission denied'));
            const bunnies = await findDustBunnies(mockDir, 10);
            expect(bunnies).toHaveLength(0);
            expect(mockFs.readdir).toHaveBeenCalledWith(mockDir, { withFileTypes: true });
        });

        test('should handle unreadable files gracefully', async () => {
            const mockDir = '/test/dir';
            mockFs.readdir.mockResolvedValueOnce([
                { name: 'file1.txt', isDirectory: () => false, isFile: () => true },
            ]);
            mockFs.stat.mockRejectedValueOnce(new Error('Permission denied')); // file1.txt
            const bunnies = await findDustBunnies(mockDir, 10);
            expect(bunnies).toHaveLength(0);
            expect(mockFs.readdir).toHaveBeenCalledWith(mockDir, { withFileTypes: true });
            expect(mockFs.stat).toHaveBeenCalledTimes(1);
        });

        test('should exclude files with size 0', async () => {
            const mockDir = '/test/dir';
            mockFs.readdir.mockResolvedValueOnce([
                { name: 'empty.txt', isDirectory: () => false, isFile: () => true },
                { name: 'small.txt', isDirectory: () => false, isFile: () => true },
            ]);
            mockFs.stat
                .mockResolvedValueOnce({ size: 0 }) // empty.txt
                .mockResolvedValueOnce({ size: 100 }); // small.txt

            const bunnies = await findDustBunnies(mockDir, 10);
            expect(bunnies).toHaveLength(1);
            expect(bunnies[0].name).toBe('small.txt');
        });
    });

    describe('categorizeDustBunnies', () => {
        const mockBunnies = [
            { path: '/a/b/log.txt', size: 100, extension: '.txt', name: 'log.txt' },
            { path: '/a/b/temp.tmp', size: 200, extension: '.tmp', name: 'temp.tmp' },
            { path: '/a/b/image.png', size: 300, extension: '.png', name: 'image.png' },
            { path: '/a/b/script.js', size: 400, extension: '.js', name: 'script.js' },
            { path: '/a/b/report.pdf', size: 500, extension: '.pdf', name: 'report.pdf' },
            { path: '/a/b/archive.zip', size: 600, extension: '.zip', name: 'archive.zip' },
            { path: '/a/b/unknown.xyz', size: 700, extension: '.xyz', name: 'unknown.xyz' },
            { path: '/a/b/another.log', size: 150, extension: '.log', name: 'another.log' },
        ];

        test('should correctly categorize files based on extension', () => {
            const categorized = categorizeDustBunnies(mockBunnies);

            expect(categorized.logs).toHaveLength(2);
            expect(categorized.logs.map(b => b.name)).toEqual(['log.txt', 'another.log']);

            expect(categorized.temp).toHaveLength(1);
            expect(categorized.temp[0].name).toBe('temp.tmp');

            expect(categorized.images).toHaveLength(1);
            expect(categorized.images[0].name).toBe('image.png');

            expect(categorized.code).toHaveLength(1);
            expect(categorized.code[0].name).toBe('script.js');

            expect(categorized.documents).toHaveLength(1);
            expect(categorized.documents[0].name).toBe('report.pdf');

            expect(categorized.archives).toHaveLength(1);
            expect(categorized.archives[0].name).toBe('archive.zip');

            expect(categorized.other).toHaveLength(1);
            expect(categorized.other[0].name).toBe('unknown.xyz');

            // Ensure no other categories were created unexpectedly
            expect(Object.keys(categorized).sort()).toEqual([
                'archives', 'code', 'documents', 'images', 'logs', 'other', 'temp'
            ].sort());
        });

        test('should handle empty input array', () => {
            const categorized = categorizeDustBunnies([]);
            for (const category in categorized) {
                expect(categorized[category]).toHaveLength(0);
            }
        });
    });

    describe('generateReport', () => {
        const mockBaseDir = '/project/root';
        const mockCategorized = {
            logs: [
                { path: '/project/root/logs/app.log', size: 1024, extension: '.log', name: 'app.log' },
                { path: '/project/root/temp/error.txt', size: 512, extension: '.txt', name: 'error.txt' },
            ],
            images: [
                { path: '/project/root/assets/icon.png', size: 2048, extension: '.png', name: 'icon.png' },
            ],
            other: [
                { path: '/project/root/data/config.dat', size: 256, extension: '.dat', name: 'config.dat' },
            ],
            temp: [], // Empty category
            code: [],
            documents: [],
            archives: [],
        };

        test('should generate a well-formatted report', () => {
            const report = generateReport(mockCategorized, mockBaseDir);

            expect(report).toContain('Digital Dust Bunny Report for: /project/root');
            expect(report).toContain('Category: LOGS (2 files)');
            expect(report).toContain('  Total Size: 1.50 KB'); // 1024 + 512 = 1536 bytes = 1.5 KB
            expect(report).toContain('    - logs/app.log (1.00 KB)');
            expect(report).toContain('    - temp/error.txt (0.50 KB)');

            expect(report).toContain('Category: IMAGES (1 files)');
            expect(report).toContain('  Total Size: 2.00 KB'); // 2048 bytes = 2 KB
            expect(report).toContain('    - assets/icon.png (2.00 KB)');

            expect(report).toContain('Category: OTHER (1 files)');
            expect(report).toContain('  Total Size: 0.25 KB'); // 256 bytes = 0.25 KB
            expect(report).toContain('    - data/config.dat (0.25 KB)');

            expect(report).toContain('Summary:');
            expect(report).toContain('  Total Dust Bunnies Found: 4');
            expect(report).toContain('  Total Size: 3.75 KB'); // 1.5 + 2 + 0.25 = 3.75 KB

            // Ensure empty categories are not reported
            expect(report).not.toContain('Category: TEMP');
            expect(report).not.toContain('Category: CODE');
        });

        test('should generate an empty report if no bunnies are found', () => {
            const emptyCategorized = {
                logs: [], temp: [], images: [], code: [], documents: [], archives: [], other: []
            };
            const report = generateReport(emptyCategorized, mockBaseDir);

            expect(report).toContain('Digital Dust Bunny Report for: /project/root');
            expect(report).toContain('Summary:');
            expect(report).toContain('  Total Dust Bunnies Found: 0');
            expect(report).toContain('  Total Size: 0.00 KB');
            expect(report.split('\n').filter(line => line.startsWith('Category:')).length).toBe(0);
        });
    });
});
