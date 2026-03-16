const assert = require('assert');
const path = require('path');
const fs = require('fs');
const { loadResources, saveResources, calculateResourceValue, suggestTrade } = require('../src/barterCalculator');

// Mock rationale: We need to test file operations (load/save) without actually touching the filesystem
// or relying on a pre-existing file. This ensures deterministic and isolated tests.
const mockFs = {
  _files: {},
  readFileSync: (filePath, encoding) => {
    if (mockFs._files[filePath]) {
      return mockFs._files[filePath];
    } else if (filePath.includes('resources.json')) {
      // If it's the default resources file and not explicitly mocked, simulate ENOENT
      const error = new Error(`ENOENT: no such file or directory, open '${filePath}'`);
      error.code = 'ENOENT';
      throw error;
    }
    throw new Error(`File not found: ${filePath}`);
  },
  writeFileSync: (filePath, data, encoding) => {
    mockFs._files[filePath] = data;
  },
  reset: () => {
    mockFs._files = {};
  }
};

// Temporarily override fs methods for testing
const originalFsReadFileSync = fs.readFileSync;
const originalFsWriteFileSync = fs.writeFileSync;

fs.readFileSync = mockFs.readFileSync;
fs.writeFileSync = mockFs.writeFileSync;

const TEST_RESOURCES_FILE = path.join(__dirname, 'test_resources.json');

describe('Barter Calculator', () => {
  beforeEach(() => {
    mockFs.reset();
    // Populate with some initial data for tests
    mockFs._files[TEST_RESOURCES_FILE] = JSON.stringify([
      { name: 'A', baseValue: 10, scarcity: 1, desirability: 1 },
      { name: 'B', baseValue: 20, scarcity: 0.5, desirability: 1.5 },
      { name: 'C', baseValue: 5, scarcity: 2, desirability: 0.8 }
    ], null, 2);
  });

  after(() => {
    // Restore original fs methods after all tests
    fs.readFileSync = originalFsReadFileSync;
    fs.writeFileSync = originalFsWriteFileSync;
  });

  it('should load resources correctly from a file', () => {
    const resources = loadResources(TEST_RESOURCES_FILE);
    assert.strictEqual(Object.keys(resources).length, 3);
    assert.strictEqual(resources['A'].baseValue, 10);
    assert.strictEqual(resources['B'].scarcity, 0.5);
  });

  it('should create default resources if file not found', () => {
    mockFs.reset(); // Ensure no file exists
    // The actual code looks for 'src/resources.json' relative to its own path
    const defaultFilePath = path.join(process.cwd(), 'src', 'resources.json'); 
    const resources = loadResources(defaultFilePath);
    assert.strictEqual(Object.keys(resources).length, 5); // Default resources count
    assert.ok(resources['Water']);
    assert.ok(mockFs._files[defaultFilePath]); // Check if default file was written
  });

  it('should save resources correctly to a file', () => {
    const initialResources = loadResources(TEST_RESOURCES_FILE);
    initialResources['D'] = { name: 'D', baseValue: 100, scarcity: 0.1, desirability: 2.0 };
    saveResources(TEST_RESOURCES_FILE, initialResources);
    const savedData = JSON.parse(mockFs._files[TEST_RESOURCES_FILE]);
    assert.strictEqual(savedData.length, 4);
    assert.strictEqual(savedData.find(r => r.name === 'D').baseValue, 100);
  });

  it('should calculate resource value correctly', () => {
    const resources = loadResources(TEST_RESOURCES_FILE);
    // A: 10 * (1 / 1) = 10
    assert.strictEqual(calculateResourceValue('A', resources), 10);
    // B: 20 * (1.5 / 0.5) = 20 * 3 = 60
    assert.strictEqual(calculateResourceValue('B', resources), 60);
    // C: 5 * (0.8 / 2) = 5 * 0.4 = 2
    assert.strictEqual(calculateResourceValue('C', resources), 2);
  });

  it('should handle zero scarcity by using a minimum factor', () => {
    const resources = loadResources(TEST_RESOURCES_FILE);
    resources['ZeroScarcity'] = { name: 'ZeroScarcity', baseValue: 10, scarcity: 0, desirability: 1 };
    // Should use 0.01 for scarcity
    assert.strictEqual(calculateResourceValue('ZeroScarcity', resources), 10 * (1 / 0.01));
  });

  it('should throw error for non-existent resource during value calculation', () => {
    const resources = loadResources(TEST_RESOURCES_FILE);
    assert.throws(() => calculateResourceValue('NonExistent', resources), /Resource 'NonExistent' not found./);
  });

  it('should suggest trade amount correctly', () => {
    const resources = loadResources(TEST_RESOURCES_FILE);
    // Have A (value 10), want B (value 60). Have 6 A.
    // (10 * 6) / 60 = 60 / 60 = 1 B
    assert.strictEqual(suggestTrade('A', 'B', 6, resources), 1);

    // Have B (value 60), want A (value 10). Have 1 B.
    // (60 * 1) / 10 = 60 / 10 = 6 A
    assert.strictEqual(suggestTrade('B', 'A', 1, resources), 6);

    // Have C (value 2), want A (value 10). Have 5 C.
    // (2 * 5) / 10 = 10 / 10 = 1 A
    assert.strictEqual(suggestTrade('C', 'A', 5, resources), 1);
  });

  it('should return 0 if wanted resource has no effective value (to avoid division by zero)', () => {
    const resources = loadResources(TEST_RESOURCES_FILE);
    resources['Worthless'] = { name: 'Worthless', baseValue: 0, scarcity: 1, desirability: 0 };
    // Value of Worthless will be 0 * (0/1) = 0
    assert.strictEqual(suggestTrade('A', 'Worthless', 1, resources), 0);
  });
});

// Simple describe/it for Node.js built-in assert
function describe(name, fn) {
  console.log(`\n${name}`);
  fn();
}

function it(name, fn) {
  try {
    fn();
    console.log(`  ${name} ${chalk.green('✓')}`);
  } catch (error) {
    console.error(`  ${name} ${chalk.red('✗')}`);
    console.error(error.stack);
    process.exit(1);
  }
}

// Add chalk for test output coloring
const chalk = require('chalk');
