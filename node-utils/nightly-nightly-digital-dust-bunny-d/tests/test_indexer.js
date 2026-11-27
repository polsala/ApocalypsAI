const assert = require('assert');
const path = require('path');
const { indexDirectory, searchIndex, extractKeywords, isStopWord } = require('../src/index');

// # Mock rationale:
// We need to mock the 'fs' module to ensure tests are deterministic and offline.
// This prevents actual file system operations, making tests fast and reliable,
// and allowing us to control the "state" of the file system for different scenarios.
const mockFs = {
  _files: {},
  _dirs: {},

  // Helper to set up mock files and directories
  __setMockFilesAndDirs: function(files, dirs) {
    this._files = files;
    this._dirs = dirs;
  },

  readdirSync: function(dirPath, options) {
    const normalizedPath = path.normalize(dirPath);
    if (this._dirs[normalizedPath]) {
      const entries = this._dirs[normalizedPath].map(name => {
        const fullPath = path.join(normalizedPath, name);
        return {
          name: name,
          isDirectory: () => !!this._dirs[fullPath],
          isFile: () => !!this._files[fullPath]
        };
      });
      return entries;
    }
    throw new Error(`ENOENT: no such file or directory, scandir '${dirPath}'`);
  },

  readFileSync: function(filePath, encoding) {
    const normalizedPath = path.normalize(filePath);
    if (this._files[normalizedPath]) {
      return this._files[normalizedPath];
    }
    throw new Error(`ENOENT: no such file or directory, open '${filePath}'`);
  },

  writeFileSync: function(filePath, content, encoding) {
    const normalizedPath = path.normalize(filePath);
    this._files[normalizedPath] = content; // Store written content
  }
};

// Replace the actual 'fs' module with our mock
const fs = require('fs');
Object.assign(fs, mockFs);

// --- Test Cases ---

async function runTests() {
  console.log('Running tests for Nightly Digital Dust Bunny Duster...');

  // Test 1: Keyword extraction
  console.log('\nTest 1: Keyword extraction');
  const text1 = "The quick brown fox jumps over the lazy dog. It's a good day!";
  const keywords1 = extractKeywords(text1);
  assert.deepStrictEqual(keywords1.sort(), ['brown', 'day', 'dog', 'fox', 'good', 'jumps', 'lazy', 'quick', 'over'].sort(), 'Test 1.1 Failed: Basic keyword extraction');
  console.log('  Test 1.1 Passed: Basic keyword extraction');

  const text2 = "A-B-C, 123. Hello World! Node.js is awesome.";
  const keywords2 = extractKeywords(text2);
  assert.deepStrictEqual(keywords2.sort(), ['awesome', 'hello', 'node', 'world'].sort(), 'Test 1.2 Failed: Special characters and numbers');
  console.log('  Test 1.2 Passed: Special characters and numbers');

  // Test 2: Stop word filtering
  console.log('\nTest 2: Stop word filtering');
  assert.strictEqual(isStopWord('the'), true, 'Test 2.1 Failed: "the" should be a stop word');
  assert.strictEqual(isStopWord('awesome'), false, 'Test 2.2 Failed: "awesome" should not be a stop word');
  console.log('  Test 2.1 & 2.2 Passed: Stop word filtering');

  // Test 3: Indexing a directory
  console.log('\nTest 3: Indexing a directory');
  const mockDir = path.resolve('/mock/data');
  const mockSubDir = path.resolve('/mock/data/sub');
  const mockOutputPath = path.resolve('./test-index.json');

  mockFs.__setMockFilesAndDirs(
    {
      [path.join(mockDir, 'file1.txt')]: 'This is a test file with important data.',
      [path.join(mockDir, 'ignore.log')]: 'This log file should be indexed.',
      [path.join(mockSubDir, 'file2.md')]: 'Another file. Markdown content about survival.',
      [path.join(mockSubDir, 'image.jpg')]: 'Binary content, should be ignored.' // Should be ignored
    },
    {
      [mockDir]: ['file1.txt', 'ignore.log', 'sub'],
      [mockSubDir]: ['file2.md', 'image.jpg']
    }
  );

  await indexDirectory(mockDir, mockOutputPath);

  const generatedIndexContent = mockFs.readFileSync(mockOutputPath, 'utf8');
  const generatedIndex = JSON.parse(generatedIndexContent);

  assert.strictEqual(generatedIndex.length, 3, 'Test 3.1 Failed: Should index 3 files');
  console.log('  Test 3.1 Passed: Correct number of files indexed');

  const file1Entry = generatedIndex.find(e => e.path === path.join(mockDir, 'file1.txt'));
  assert.ok(file1Entry, 'Test 3.2 Failed: file1.txt entry missing');
  assert.ok(file1Entry.keywords.includes('test'), 'Test 3.3 Failed: file1.txt keywords incorrect');
  assert.ok(file1Entry.keywords.includes('data'), 'Test 3.4 Failed: file1.txt keywords incorrect');
  assert.strictEqual(file1Entry.snippet, 'This is a test file with important data.', 'Test 3.5 Failed: file1.txt snippet incorrect');
  console.log('  Test 3.2-3.5 Passed: file1.txt indexed correctly');

  const file2Entry = generatedIndex.find(e => e.path === path.join(mockSubDir, 'file2.md'));
  assert.ok(file2Entry, 'Test 3.6 Failed: file2.md entry missing');
  assert.ok(file2Entry.keywords.includes('survival'), 'Test 3.7 Failed: file2.md keywords incorrect');
  assert.ok(file2Entry.keywords.includes('markdown'), 'Test 3.8 Failed: file2.md keywords incorrect');
  console.log('  Test 3.6-3.8 Passed: file2.md indexed correctly');

  const logFileEntry = generatedIndex.find(e => e.path === path.join(mockDir, 'ignore.log'));
  assert.ok(logFileEntry, 'Test 3.9 Failed: log file entry missing');
  assert.ok(logFileEntry.keywords.includes('log'), 'Test 3.10 Failed: log file keywords incorrect');
  console.log('  Test 3.9-3.10 Passed: log file indexed correctly');

  // Test 4: Searching the index
  console.log('\nTest 4: Searching the index');
  const mockIndexContent = JSON.stringify([
    { path: '/data/notes/recipe.txt', snippet: 'Recipe for delicious mutated berry pie.', keywords: ['recipe', 'mutated', 'berry', 'pie'] },
    { path: '/data/maps/wasteland.md', snippet: 'Map of the northern wasteland sector.', keywords: ['map', 'wasteland', 'northern', 'sector'] },
    { path: '/data/logs/anomaly.log', snippet: 'Anomaly detected near sector 7.', keywords: ['anomaly', 'detected', 'sector'] }
  ], null, 2);

  const mockSearchIndexPath = path.resolve('./search-index.json');
  mockFs.__setMockFilesAndDirs(
    {
      [mockSearchIndexPath]: mockIndexContent
    },
    {} // No directories needed for search
  );

  // Capture console output for search results
  let consoleOutput = [];
  const originalConsoleLog = console.log;
  console.log = (...args) => consoleOutput.push(args.join(' '));

  await searchIndex('recipe', mockSearchIndexPath);
  const recipeResults = consoleOutput.join('\n');
  assert.ok(recipeResults.includes('Found 1 results for "recipe"'), 'Test 4.1 Failed: Search for "recipe" count incorrect');
  assert.ok(recipeResults.includes('/data/notes/recipe.txt'), 'Test 4.2 Failed: Search for "recipe" path incorrect');
  console.log('  Test 4.1 & 4.2 Passed: Search for "recipe"');

  consoleOutput = []; // Clear output
  await searchIndex('wasteland', mockSearchIndexPath);
  const wastelandResults = consoleOutput.join('\n');
  assert.ok(wastelandResults.includes('Found 1 results for "wasteland"'), 'Test 4.3 Failed: Search for "wasteland" count incorrect');
  assert.ok(wastelandResults.includes('/data/maps/wasteland.md'), 'Test 4.4 Failed: Search for "wasteland" path incorrect');
  console.log('  Test 4.3 & 4.4 Passed: Search for "wasteland"');

  consoleOutput = []; // Clear output
  await searchIndex('sector', mockSearchIndexPath);
  const sectorResults = consoleOutput.join('\n');
  assert.ok(sectorResults.includes('Found 2 results for "sector"'), 'Test 4.5 Failed: Search for "sector" count incorrect');
  assert.ok(sectorResults.includes('/data/maps/wasteland.md'), 'Test 4.6 Failed: Search for "sector" path incorrect');
  assert.ok(sectorResults.includes('/data/logs/anomaly.log'), 'Test 4.7 Failed: Search for "sector" path incorrect');
  console.log('  Test 4.5-4.7 Passed: Search for "sector"');

  consoleOutput = []; // Clear output
  await searchIndex('nonexistent', mockSearchIndexPath);
  const noResults = consoleOutput.join('\n');
  assert.ok(noResults.includes('No results found for "nonexistent".'), 'Test 4.8 Failed: No results message incorrect');
  console.log('  Test 4.8 Passed: Search for nonexistent keyword');

  console.log = originalConsoleLog; // Restore original console.log

  console.log('\nAll tests passed!');
}

runTests().catch(err => {
  console.error('Tests failed:', err);
  process.exit(1);
});
