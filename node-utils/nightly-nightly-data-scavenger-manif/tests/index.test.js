const assert = require('assert');
const path = require('path');
// Import the module, not just the functions, so we can modify its exports for mocking
const mainModule = require('../src/index');

// Mock rationale: We need to simulate a file system for deterministic, offline testing.
// This avoids actual file system operations which are non-deterministic and slow.
const mockFs = {
    '/mock_data': {
        'file1.txt': { isFile: true, isDirectory: false, size: 100 },
        'file2.json': { isFile: true, isDirectory: false, size: 250 },
        'image.png': { isFile: true, isDirectory: false, size: 1024 },
        'subdir': {
            'nested_file.txt': { isFile: true, isDirectory: false, size: 50 },
            'another_dir': {
                'deep_file.md': { isFile: true, isDirectory: false, size: 300 }
            },
            'temp.log': { isFile: true, isDirectory: false, size: 120 }
        }
    },
    '/empty_data': {},
    '/non_existent': null // Represents a directory that doesn't exist
};

// Store original fs and path methods to restore after tests
const originalFs = Object.assign({}, require('fs'));
const originalPath = Object.assign({}, require('path'));

// Override fs methods for testing
require('fs').existsSync = (p) => {
    const normalizedPath = path.normalize(p);
    return mockFs[normalizedPath] !== undefined;
};

require('fs').readdirSync = (p) => {
    const normalizedPath = path.normalize(p);
    const dirContent = mockFs[normalizedPath];
    if (dirContent) {
        return Object.keys(dirContent);
    }
    throw new Error(`ENOENT: no such file or directory, scandir '${p}'`);
};

require('fs').statSync = (p) => {
    const normalizedPath = path.normalize(p);
    const parts = normalizedPath.split(path.sep).filter(Boolean); // Split and remove empty strings
    let current = mockFs;
    let found = null;

    // Traverse the mockFs object to find the item
    let tempPath = '';
    for (let i = 0; i < parts.length; i++) {
        const part = parts[i];
        tempPath = path.join(tempPath, part);
        if (current[part]) {
            if (i === parts.length - 1) { // Last part, it's the target file/dir
                found = current[part];
            } else { // Not last part, must be a directory
                current = current[part];
            }
        } else {
            found = null; // Path not found
            break;
        }
    }

    if (found) {
        return {
            isFile: () => found.isFile,
            isDirectory: () => found.isDirectory,
            size: found.size || 0
        };
    }
    throw new Error(`ENOENT: no such file or directory, stat '${p}'`);
};

// Mock path.join to ensure consistent paths regardless of OS
require('path').join = (...args) => {
    return args.join('/').replace(/\/\//g, '/'); // Simple join for mock paths
};

// Mock generateIntegrityScore to be deterministic for tests
const mockGenerateIntegrityScore = (filePath) => {
    // Mock rationale: Ensure deterministic integrity scores for consistent test results.
    // In production, this might be truly random or based on content.
    if (filePath.includes('file1.txt')) return 75;
    if (filePath.includes('file2.json')) return 80;
    if (filePath.includes('nested_file.txt')) return 60;
    if (filePath.includes('deep_file.md')) return 90;
    return 50; // Default for any other file
};

// Temporarily replace the function in the imported module for testing
const originalGenerateIntegrityScore = mainModule.generateIntegrityScore;
mainModule.generateIntegrityScore = mockGenerateIntegrityScore;

// Get the generateManifest function after the mock has been applied
const generateManifest = mainModule.generateManifest;

console.log('Running tests for Nightly Data Scavenger\'s Manifest...');

function runTest(name, testFunction) {
    try {
        testFunction();
        console.log(`✅ ${name}`);
    } catch (error) {
        console.error(`❌ ${name}`);
        console.error(error);
        process.exit(1);
    }
}

runTest('should find files with specified extensions in a flat directory', () => {
    const manifest = generateManifest('/mock_data', ['.txt', '.json']);
    assert.strictEqual(manifest.length, 2, 'Expected 2 files');
    assert.deepStrictEqual(manifest.map(f => f.path).sort(), ['/mock_data/file1.txt', '/mock_data/file2.json'].sort());
    assert.strictEqual(manifest.find(f => f.path === '/mock_data/file1.txt').size, 100);
    assert.strictEqual(manifest.find(f => f.path === '/mock_data/file1.txt').integrityScore, 75);
    assert.strictEqual(manifest.find(f => f.path === '/mock_data/file2.json').size, 250);
    assert.strictEqual(manifest.find(f => f.path === '/mock_data/file2.json').integrityScore, 80);
});

runTest('should find files in nested directories', () => {
    const manifest = generateManifest('/mock_data', ['.txt', '.md']);
    assert.strictEqual(manifest.length, 3, 'Expected 3 files including nested ones');
    assert.deepStrictEqual(manifest.map(f => f.path).sort(), [
        '/mock_data/file1.txt',
        '/mock_data/subdir/nested_file.txt',
        '/mock_data/subdir/another_dir/deep_file.md'
    ].sort());
    assert.strictEqual(manifest.find(f => f.path === '/mock_data/subdir/nested_file.txt').size, 50);
    assert.strictEqual(manifest.find(f => f.path === '/mock_data/subdir/nested_file.txt').integrityScore, 60);
    assert.strictEqual(manifest.find(f => f.path === '/mock_data/subdir/another_dir/deep_file.md').size, 300);
    assert.strictEqual(manifest.find(f => f.path === '/mock_data/subdir/another_dir/deep_file.md').integrityScore, 90);
});

runTest('should return an empty manifest if no files match extensions', () => {
    const manifest = generateManifest('/mock_data', ['.jpg', '.gif']);
    assert.strictEqual(manifest.length, 0, 'Expected 0 files');
});

runTest('should return an empty manifest for an empty directory', () => {
    const manifest = generateManifest('/empty_data', ['.txt', '.json']);
    assert.strictEqual(manifest.length, 0, 'Expected 0 files');
});

runTest('should handle non-existent directory gracefully', () => {
    const manifest = generateManifest('/non_existent', ['.txt']);
    assert.strictEqual(manifest.length, 0, 'Expected 0 files for non-existent directory');
});

runTest('should handle extensions with and without leading dot', () => {
    const manifest = generateManifest('/mock_data', ['txt', '.json']); // Mix of formats
    assert.strictEqual(manifest.length, 2, 'Expected 2 files with mixed extension formats');
    assert.deepStrictEqual(manifest.map(f => f.path).sort(), ['/mock_data/file1.txt', '/mock_data/file2.json'].sort());
});

console.log('All tests passed!');

// Restore original fs and path methods after tests
Object.assign(require('fs'), originalFs);
Object.assign(require('path'), originalPath);
// Restore original generateIntegrityScore function
mainModule.generateIntegrityScore = originalGenerateIntegrityScore;
