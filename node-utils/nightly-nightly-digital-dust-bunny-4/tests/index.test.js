const assert = require('assert');
const { findDustBunnies } = require('../src/index');

// Mock rationale: We need to simulate file system interactions without actually touching the disk.
// This allows for deterministic and fast tests.
const mockFiles = {
    '/mock/dir/old_small.txt': {
        isDirectory: () => false,
        isFile: () => true,
        mtimeMs: Date.now() - (30 * 24 * 60 * 60 * 1000) - 1000, // 30 days + 1 second ago
        size: 100 // bytes
    },
    '/mock/dir/recent_large.log': {
        isDirectory: () => false,
        isFile: () => true,
        mtimeMs: Date.now() - (5 * 24 * 60 * 60 * 1000), // 5 days ago
        size: 2 * 1024 * 1024 // 2 MB
    },
    '/mock/dir/temp/whimsical.tmp': {
        isDirectory: () => false,
        isFile: () => true,
        mtimeMs: Date.now() - (10 * 24 * 60 * 60 * 1000), // 10 days ago
        size: 500 // bytes
    },
    '/mock/dir/temp/important.js': {
        isDirectory: () => false,
        isFile: () => true,
        mtimeMs: Date.now() - (1 * 24 * 60 * 60 * 1000), // 1 day ago
        size: 10 * 1024 // 10 KB
    },
    '/mock/dir/nested/another_old.bak': {
        isDirectory: () => false,
        isFile: () => true,
        mtimeMs: Date.now() - (60 * 24 * 60 * 60 * 1000), // 60 days ago
        size: 200 // bytes
    },
    '/mock/dir/nested/sub/recent_small.txt': {
        isDirectory: () => false,
        isFile: () => true,
        mtimeMs: Date.now() - (2 * 24 * 60 * 60 * 1000), // 2 days ago
        size: 50 // bytes
    }
};

const mockDirStructure = {
    '/mock/dir': [
        { name: 'old_small.txt', isDirectory: () => false, isFile: () => true },
        { name: 'recent_large.log', isDirectory: () => false, isFile: () => true },
        { name: 'temp', isDirectory: () => true, isFile: () => false },
        { name: 'nested', isDirectory: () => true, isFile: () => false }
    ],
    '/mock/dir/temp': [
        { name: 'whimsical.tmp', isDirectory: () => false, isFile: () => true },
        { name: 'important.js', isDirectory: () => false, isFile: () => true }
    ],
    '/mock/dir/nested': [
        { name: 'another_old.bak', isDirectory: () => false, isFile: () => true },
        { name: 'sub', isDirectory: () => true, isFile: () => false }
    ],
    '/mock/dir/nested/sub': [
        { name: 'recent_small.txt', isDirectory: () => false, isFile: () => true }
    ]
};

// Mock fs/promises module
const fsPromises = require('fs/promises');
fsPromises.readdir = async (path, options) => { // Mock rationale: Simulate directory listing
    const entries = mockDirStructure[path];
    if (!entries) throw new Error(`Path not found in mock: ${path}`);
    return entries;
};
fsPromises.stat = async (path) => { // Mock rationale: Simulate file stats retrieval
    const stats = mockFiles[path];
    if (!stats) throw new Error(`File not found in mock: ${path}`);
    return stats;
};

async function runTests() {
    console.log('Running tests for Nightly Digital Dust Bunny Sweeper...');

    // Test 1: Find old files (older than 29 days)
    console.log('\nTest 1: Find files older than 29 days...');
    let options1 = { ageDays: 29 };
    let result1 = await findDustBunnies('/mock/dir', options1);
    assert.strictEqual(result1.length, 2, `Test 1 Failed: Expected 2 old files, got ${result1.length}`);
    assert(result1.some(f => f.path === '/mock/dir/old_small.txt'), 'Test 1 Failed: old_small.txt should be found');
    assert(result1.some(f => f.path === '/mock/dir/nested/another_old.bak'), 'Test 1 Failed: another_old.bak should be found');
    console.log('Test 1 Passed.');

    // Test 2: Find large files (larger than 1 MB)
    console.log('\nTest 2: Find files larger than 1 MB...');
    let options2 = { minSizeKB: 1024 }; // 1 MB
    let result2 = await findDustBunnies('/mock/dir', options2);
    assert.strictEqual(result2.length, 1, `Test 2 Failed: Expected 1 large file, got ${result2.length}`);
    assert(result2.some(f => f.path === '/mock/dir/recent_large.log'), 'Test 2 Failed: recent_large.log should be found');
    console.log('Test 2 Passed.');

    // Test 3: Find whimsical files (log, tmp, bak)
    console.log('\nTest 3: Find files matching whimsy patterns (log, tmp, bak)...');
    let options3 = { whimsyPatterns: 'log,tmp,bak' };
    let result3 = await findDustBunnies('/mock/dir', options3);
    assert.strictEqual(result3.length, 3, `Test 3 Failed: Expected 3 whimsical files, got ${result3.length}`);
    assert(result3.some(f => f.path === '/mock/dir/recent_large.log'), 'Test 3 Failed: recent_large.log should be found');
    assert(result3.some(f => f.path === '/mock/dir/temp/whimsical.tmp'), 'Test 3 Failed: whimsical.tmp should be found');
    assert(result3.some(f => f.path === '/mock/dir/nested/another_old.bak'), 'Test 3 Failed: another_old.bak should be found');
    console.log('Test 3 Passed.');

    // Test 4: Combined criteria (old OR large OR whimsical)
    console.log('\nTest 4: Combined criteria (old, large, whimsical)...');
    let options4 = { ageDays: 29, minSizeKB: 1024, whimsyPatterns: 'tmp' };
    let result4 = await findDustBunnies('/mock/dir', options4);
    // Expected: old_small.txt (old), recent_large.log (large), whimsical.tmp (whimsical), another_old.bak (old)
    assert.strictEqual(result4.length, 4, `Test 4 Failed: Expected 4 files with combined criteria, got ${result4.length}`);
    console.log('Test 4 Passed.');

    // Test 5: No criteria, expect no files
    console.log('\nTest 5: No criteria, expect no files...');
    let options5 = {};
    let result5 = await findDustBunnies('/mock/dir', options5);
    assert.strictEqual(result5.length, 0, `Test 5 Failed: Expected 0 files with no criteria, got ${result5.length}`);
    console.log('Test 5 Passed.');

    // Test 6: Specific age and size that matches nothing
    console.log('\nTest 6: Specific criteria that matches nothing...');
    let options6 = { ageDays: 1, minSizeKB: 10000 }; // Very recent, very large (no match in mock data)
    let result6 = await findDustBunnies('/mock/dir', options6);
    assert.strictEqual(result6.length, 0, `Test 6 Failed: Expected 0 files with specific non-matching criteria, got ${result6.length}`);
    console.log('Test 6 Passed.');

    console.log('\nAll tests passed! ✨');
}

runTests().catch(err => {
    console.error('\nTests failed:', err.message);
    process.exit(1);
});
