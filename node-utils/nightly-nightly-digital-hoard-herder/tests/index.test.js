const { analyzeHoard } = require('../src/index');
const path = require('path');

// Mock fs.promises to prevent actual file system operations during tests.
jest.mock('fs', () => ({
  promises: {
    readdir: jest.fn(),
    stat: jest.fn(),
  },
}));

// Mock whimsical-names to ensure deterministic suffixes for testing renaming suggestions.
jest.mock('../src/whimsy-names', () => ({
  getRandomWhimsySuffix: jest.fn(() => '_of_yore'), // Mock rationale: Ensure deterministic renaming for tests.
}));

const fs = require('fs').promises;
const { getRandomWhimsySuffix } = require('../src/whimsy-names');

describe('nightly-digital-hoard-herder', () => {
  const MOCK_DIR = '/mock/hoard';
  const ONE_YEAR_MS = 365 * 24 * 60 * 60 * 1000;
  const now = Date.now();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('should identify forgotten relics and space gobblers', async () => {
    // Mock rationale: Simulate a directory with various files for testing analysis logic.
    fs.readdir.mockImplementation(async (dirPath) => {
      if (dirPath === MOCK_DIR) {
        return [
          { name: 'old_small.txt', isDirectory: () => false, isFile: () => true },
          { name: 'new_large.zip', isDirectory: () => false, isFile: () => true },
          { name: 'old_large.mp4', isDirectory: () => false, isFile: () => true },
          { name: 'new_small.pdf', isDirectory: () => false, isFile: () => true },
          { name: 'subdir', isDirectory: () => true, isFile: () => false },
        ];
      } else if (dirPath === path.join(MOCK_DIR, 'subdir')) {
        return [
          { name: 'sub_old_small.doc', isDirectory: () => false, isFile: () => true },
        ];
      }
      return [];
    });

    // Mock rationale: Simulate file stats (modification time, size) for testing age and size thresholds.
    fs.stat.mockImplementation(async (filePath) => {
      if (filePath === path.join(MOCK_DIR, 'old_small.txt')) {
        return {
          mtimeMs: now - (ONE_YEAR_MS + 1000), // Older than 1 year
          size: 50 * 1024, // 50 KB (small)
        };
      } else if (filePath === path.join(MOCK_DIR, 'new_large.zip')) {
        return {
          mtimeMs: now - (ONE_YEAR_MS / 2), // Newer than 1 year
          size: 150 * 1024 * 1024, // 150 MB (large)
        };
      } else if (filePath === path.join(MOCK_DIR, 'old_large.mp4')) {
        return {
          mtimeMs: now - (ONE_YEAR_MS + 5000), // Older than 1 year
          size: 200 * 1024 * 1024, // 200 MB (large)
        };
      } else if (filePath === path.join(MOCK_DIR, 'new_small.pdf')) {
        return {
          mtimeMs: now - (ONE_YEAR_MS / 4), // Newer than 1 year
          size: 2 * 1024 * 1024, // 2 MB (small)
        };
      } else if (filePath === path.join(MOCK_DIR, 'subdir', 'sub_old_small.doc')) {
        return {
          mtimeMs: now - (ONE_YEAR_MS + 2000), // Older than 1 year
          size: 10 * 1024, // 10 KB (small)
        };
      }
      throw new Error('File not found in mock');
    });

    const results = await analyzeHoard(MOCK_DIR, {
      ageThresholdDays: 365,
      sizeThresholdBytes: 100 * 1024 * 1024, // 100 MB
    });

    expect(results.forgottenRelics).toHaveLength(3);
    expect(results.forgottenRelics[0].path).toBe(path.join(MOCK_DIR, 'old_small.txt'));
    expect(results.forgottenRelics[1].path).toBe(path.join(MOCK_DIR, 'old_large.mp4'));
    expect(results.forgottenRelics[2].path).toBe(path.join(MOCK_DIR, 'subdir', 'sub_old_small.doc'));

    expect(results.spaceGobblers).toHaveLength(2);
    expect(results.spaceGobblers[0].path).toBe(path.join(MOCK_DIR, 'new_large.zip'));
    expect(results.spaceGobblers[1].path).toBe(path.join(MOCK_DIR, 'old_large.mp4'));

    expect(results.renamedFiles).toHaveLength(0); // No whimsical rename option enabled
  });

  test('should suggest whimsical renames for old files when enabled', async () => {
    // Mock rationale: Simulate a directory with an old file to test the whimsical rename feature.
    fs.readdir.mockImplementation(async (dirPath) => {
      if (dirPath === MOCK_DIR) {
        return [{ name: 'very_old_report.pdf', isDirectory: () => false, isFile: () => true }];
      }
      return [];
    });

    // Mock rationale: Simulate file stats for an old file.
    fs.stat.mockImplementation(async (filePath) => {
      if (filePath === path.join(MOCK_DIR, 'very_old_report.pdf')) {
        return {
          mtimeMs: now - (ONE_YEAR_MS * 2), // 2 years old
          size: 5 * 1024 * 1024, // 5 MB
        };
      }
      throw new Error('File not found in mock');
    });

    const results = await analyzeHoard(MOCK_DIR, {
      ageThresholdDays: 365,
      sizeThresholdBytes: 100 * 1024 * 1024,
      whimsicalRename: true,
    });

    expect(results.forgottenRelics).toHaveLength(1);
    expect(results.forgottenRelics[0].path).toBe(path.join(MOCK_DIR, 'very_old_report.pdf'));

    expect(results.spaceGobblers).toHaveLength(0);

    expect(results.renamedFiles).toHaveLength(1);
    expect(results.renamedFiles[0].oldPath).toBe(path.join(MOCK_DIR, 'very_old_report.pdf'));
    expect(results.renamedFiles[0].newPath).toBe(path.join(MOCK_DIR, 'very_old_report_of_yore.pdf'));
    expect(getRandomWhimsySuffix).toHaveBeenCalled();
  });

  test('should handle empty directory gracefully', async () => {
    // Mock rationale: Simulate an empty directory to ensure the utility handles it without errors.
    fs.readdir.mockResolvedValue([]);
    fs.stat.mockRejectedValue(new Error('File not found')); // Should not be called for empty dir

    const results = await analyzeHoard(MOCK_DIR);

    expect(results.forgottenRelics).toHaveLength(0);
    expect(results.spaceGobblers).toHaveLength(0);
    expect(results.renamedFiles).toHaveLength(0);
  });

  test('should handle directory read errors', async () => {
    // Mock rationale: Simulate a directory that cannot be read to test error handling.
    fs.readdir.mockRejectedValue(new Error('Permission denied'));
    const consoleWarnSpy = jest.spyOn(console, 'warn').mockImplementation(() => {}); // Mock rationale: Suppress console warnings during test.

    const results = await analyzeHoard(MOCK_DIR);

    expect(consoleWarnSpy).toHaveBeenCalledWith(expect.stringContaining(`Could not read directory ${MOCK_DIR}: Permission denied`));
    expect(results.forgottenRelics).toHaveLength(0);
    expect(results.spaceGobblers).toHaveLength(0);
    expect(results.renamedFiles).toHaveLength(0);

    consoleWarnSpy.mockRestore();
  });

  test('should handle file stat errors', async () => {
    // Mock rationale: Simulate a file whose stats cannot be retrieved to test error handling.
    fs.readdir.mockResolvedValue([
      { name: 'unreadable.txt', isDirectory: () => false, isFile: () => true },
    ]);
    fs.stat.mockRejectedValue(new Error('File system error'));
    const consoleWarnSpy = jest.spyOn(console, 'warn').mockImplementation(() => {}); // Mock rationale: Suppress console warnings during test.

    const results = await analyzeHoard(MOCK_DIR);

    expect(consoleWarnSpy).toHaveBeenCalledWith(expect.stringContaining(`Could not stat file ${path.join(MOCK_DIR, 'unreadable.txt')}: File system error`));
    expect(results.forgottenRelics).toHaveLength(0);
    expect(results.spaceGobblers).toHaveLength(0);
    expect(results.renamedFiles).toHaveLength(0);

    consoleWarnSpy.mockRestore();
  });
});
