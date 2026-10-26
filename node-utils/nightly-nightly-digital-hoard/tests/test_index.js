const assert = require('assert');
const path = require('path');
const { Writable } = require('stream');

// Mock fs/promises and path modules
const mockFs = {
    readdir: async (dirPath, options) => {
        // # Mock rationale: To ensure deterministic and offline testing, the file system operations (reading directories and file stats) are mocked.
        // This allows simulating various directory structures and file properties without actual disk access, making tests fast and reliable.
        const mockStructure = {
            '/mock/bunker': [
                { name: 'large_video.mp4', isDirectory: () => false, isFile: () => true },
                { name: 'small_doc.txt', isDirectory: () => false, isFile: () => true },
                { name: 'old_report.pdf', isDirectory: () => false, isFile: () => true },
                { name: 'current_project', isDirectory: () => true, isFile: () => false },
                { name: 'inaccessible_dir', isDirectory: () => true, isFile: () => false } // Simulate inaccessible dir
            ],
            '/mock/bunker/current_project': [
                { name: 'recent_code.js', isDirectory: () => false, isFile: () => true },
                { name: 'ancient_config.json', isDirectory: () => false, isFile: () => true }
            ],
            '/mock/bunker/inaccessible_dir': [] // Will cause an error in scanDirectory's inner catch
        };
        if (mockStructure[dirPath]) {
            return mockStructure[dirPath];
        }
        throw new Error(`ENOENT: no such file or directory, scandir '${dirPath}'`);
    },
    stat: async (filePath) => {
        // # Mock rationale: See readdir mock rationale.
        const now = Date.now();
        const oneYearAgo = new Date(now - (365 * 24 * 60 * 60 * 1000));
        const twoYearsAgo = new Date(now - (2 * 365 * 24 * 60 * 60 * 1000));
        const sixMonthsAgo = new Date(now - (180 * 24 * 60 * 60 * 1000));

        const mockStats = {
            '/mock/bunker/large_video.mp4': { size: 150 * 1024 * 1024, mtime: sixMonthsAgo }, // 150MB, 6 months old
            '/mock/bunker/small_doc.txt': { size: 10 * 1024, mtime: new Date() }, // 10KB, current
            '/mock/bunker/old_report.pdf': { size: 5 * 1024 * 1024, mtime: twoYearsAgo }, // 5MB, 2 years old
            '/mock/bunker/current_project/recent_code.js': { size: 20 * 1024, mtime: new Date() }, // 20KB, current
            '/mock/bunker/current_project/ancient_config.json': { size: 1 * 1024, mtime: oneYearAgo } // 1KB, 1 year old
        };

        if (filePath.includes('inaccessible_dir')) {
            throw new Error(`EACCES: permission denied, stat '${filePath}'`);
        }

        if (mockStats[filePath]) {
            return mockStats[filePath];
        }
        throw new Error(`ENOENT: no such file or directory, stat '${filePath}'`);
    }
};

// Store original built-in modules for restoration
const originalFsPromises = require('fs/promises');
const originalPath = require('path');

// Override built-in modules for testing
Object.assign(require('fs/promises'), mockFs);
Object.assign(require('path'), {
    join: originalPath.join,
    isAbsolute: originalPath.isAbsolute,
    normalize: originalPath.normalize,
    resolve: (...args) => {
        // Simulate path.resolve behavior relative to a fixed mock CWD for tests
        const mockCwd = '/mock/bunker';
        let resolvedPath = mockCwd;
        for (const arg of args) {
            if (originalPath.isAbsolute(arg)) {
                resolvedPath = arg;
            } else {
                resolvedPath = originalPath.join(resolvedPath, arg);
            }
        }
        return originalPath.normalize(resolvedPath);
    }
});

// Import the main script AFTER mocking
const mainScript = require('../src/index');

// Helper to capture console output
class ConsoleCapture extends Writable {
    constructor(options) {
        super(options);
        this.buffer = [];
    }
    _write(chunk, encoding, callback) {
        this.buffer.push(chunk.toString());
        callback();
    }
    getOutput() {
        return this.buffer.join('');
    }
    clear() {
        this.buffer = [];
    }
}

let capturedOutput = new ConsoleCapture();
let originalConsoleLog;
let originalConsoleError;
let originalProcessExit;
let exitCode = null;

function setupConsoleCapture() {
    originalConsoleLog = console.log;
    originalConsoleError = console.error;
    originalProcessExit = process.exit;

    console.log = (...args) => capturedOutput.write(args.join(' ') + '\n');
    console.error = (...args) => capturedOutput.write(args.join(' ') + '\n');
    process.exit = (code) => { exitCode = code; }; // Mock process.exit
    exitCode = null; // Reset exit code for each test
}

function restoreConsole() {
    console.log = originalConsoleLog;
    console.error = originalConsoleError;
    process.exit = originalProcessExit;
    capturedOutput.clear();
}

// Basic test runner structure for self-contained tests
function describe(name, fn) {
    console.log(`\nRunning test suite: ${name}`);
    fn();
}

async function it(name, fn) {
    try {
        await beforeEachFn();
        await fn();
        console.log(`  ✓ ${name}`);
    } catch (error) {
        console.error(`  ✗ ${name}`);
        console.error(error);
        process.exit(1); // Exit on first test failure
    } finally {
        await afterEachFn();
    }
}

let beforeEachFn = async () => {};
let afterEachFn = async () => {};

function beforeEach(fn) {
    beforeEachFn = fn;
}

function afterEach(fn) {
    afterEachFn = fn;
}

describe('Nightly Digital Hoard Organizer', () => {
    beforeEach(() => {
        setupConsoleCapture();
    });

    afterEach(() => {
        restoreConsole();
    });

    it('should report large and old files with default thresholds', async () => {
        process.argv = ['node', 'src/index.js', '/mock/bunker'];
        await mainScript.main();
        const output = capturedOutput.getOutput();

        assert.ok(output.includes('Scanning your digital bunker at: /mock/bunker'), 'Should indicate scanning path');
        assert.ok(output.includes('Thresholds: Max Size = 100 MB, Max Age = 365 days'), 'Should show default thresholds');
        assert.ok(output.includes('### Bulky Cargo Containers (Files > 100 MB):'), 'Should list bulky files section');
        assert.ok(output.includes('/mock/bunker/large_video.mp4 (150.0 MB)'), 'Should identify large_video.mp4 as bulky');
        assert.ok(output.includes('### Ancient Data Scrolls (Files > 365 days old):'), 'Should list ancient files section');
        assert.ok(output.includes('/mock/bunker/old_report.pdf (Last modified:'), 'Should identify old_report.pdf as ancient');
        assert.ok(output.includes('/mock/bunker/current_project/ancient_config.json (Last modified:'), 'Should identify ancient_config.json as ancient');
        assert.ok(output.includes('Found 1 Bulky Cargo Containers.'), 'Should count bulky files correctly');
        assert.ok(output.includes('Found 2 Ancient Data Scrolls.'), 'Should count ancient files correctly');
        assert.ok(output.includes('Recommendation: Review these items.'), 'Should provide recommendation');
        assert.strictEqual(exitCode, null, 'Should not exit with an error code');
    });

    it('should report no files if thresholds are very high', async () => {
        process.argv = ['node', 'src/index.js', '/mock/bunker', '--max-size', '1000', '--max-age', '10000']; // 1GB, ~27 years
        await mainScript.main();
        const output = capturedOutput.getOutput();

        assert.ok(output.includes('Your digital bunker is remarkably clean! No bulky cargo or ancient scrolls found exceeding thresholds.'), 'Should report clean bunker');
        assert.ok(!output.includes('Bulky Cargo Containers'), 'Should not list bulky files section');
        assert.ok(!output.includes('Ancient Data Scrolls'), 'Should not list ancient files section');
        assert.strictEqual(exitCode, null, 'Should not exit with an error code');
    });

    it('should handle custom thresholds correctly', async () => {
        // Set thresholds to catch small_doc (10KB) if max-size is 0.005MB (5KB) and recent_code (current) if max-age is 1 day
        process.argv = ['node', 'src/index.js', '/mock/bunker', '--max-size', '0.005', '--max-age', '1']; // 5KB, 1 day
        await mainScript.main();
        const output = capturedOutput.getOutput();

        assert.ok(output.includes('Thresholds: Max Size = 0.005 MB, Max Age = 1 days'), 'Should show custom thresholds');
        assert.ok(output.includes('/mock/bunker/large_video.mp4'), 'large_video should still be bulky');
        assert.ok(output.includes('/mock/bunker/old_report.pdf'), 'old_report should still be ancient');
        assert.ok(output.includes('/mock/bunker/small_doc.txt (10.0 KB)'), 'small_doc should now be bulky'); // 10KB > 5KB
        assert.ok(output.includes('/mock/bunker/current_project/recent_code.js (Last modified:'), 'recent_code should now be ancient'); // current > 1 day old (relative to now)
        assert.ok(output.includes('Found 2 Bulky Cargo Containers.'), 'Should count bulky files correctly with custom size');
        assert.ok(output.includes('Found 3 Ancient Data Scrolls.'), 'Should count ancient files correctly with custom age');
        assert.strictEqual(exitCode, null, 'Should not exit with an error code');
    });

    it('should exit with error if no path is provided', async () => {
        process.argv = ['node', 'src/index.js'];
        await mainScript.main();
        const output = capturedOutput.getOutput();

        assert.ok(output.includes('Usage: node src/index.js <path_to_bunker>'), 'Should print usage error');
        assert.strictEqual(exitCode, 1, 'Should exit with code 1');
    });

    it('should handle inaccessible directories gracefully', async () => {
        process.argv = ['node', 'src/index.js', '/mock/bunker'];
        await mainScript.main();
        const output = capturedOutput.getOutput();

        assert.ok(output.includes("Error scanning /mock/bunker/inaccessible_dir: EACCES: permission denied, stat '/mock/bunker/inaccessible_dir'"), 'Should log error for inaccessible directory');
        // Ensure the scan still completes for other files
        assert.ok(output.includes('/mock/bunker/large_video.mp4'), 'Should still report other files');
        assert.strictEqual(exitCode, null, 'Should not exit with an error code');
    });

    it('should handle invalid --max-size argument', async () => {
        process.argv = ['node', 'src/index.js', '/mock/bunker', '--max-size', 'invalid'];
        await mainScript.main();
        const output = capturedOutput.getOutput();

        assert.ok(output.includes('Error: --max-size must be a positive number.'), 'Should print error for invalid max-size');
        assert.strictEqual(exitCode, 1, 'Should exit with code 1');
    });

    it('should handle invalid --max-age argument', async () => {
        process.argv = ['node', 'src/index.js', '/mock/bunker', '--max-age', 'invalid'];
        await mainScript.main();
        const output = capturedOutput.getOutput();

        assert.ok(output.includes('Error: --max-age must be a positive integer.'), 'Should print error for invalid max-age');
        assert.strictEqual(exitCode, 1, 'Should exit with code 1');
    });
});
