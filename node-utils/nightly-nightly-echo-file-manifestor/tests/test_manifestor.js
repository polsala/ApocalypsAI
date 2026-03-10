const { manifestGhost, cleanGhosts, listGhosts } = require('../src/manifestor');
const path = require('path');

// Mock rationale: fs operations are non-deterministic and interact with the actual file system.
// Mocking fs allows tests to run quickly, deterministically, and without side effects on the user's machine.
// It ensures the logic of creating/deleting/listing files is correct without needing to create/delete real files.
const mockFs = {
    _files: new Map(), // Map<filePath, content>
    _dirs: new Set(),  // Set<dirPath>

    async mkdir(dirPath, options) {
        this._dirs.add(dirPath);
    },
    async writeFile(filePath, content) {
        const dir = path.dirname(filePath);
        if (!this._dirs.has(dir)) {
            // In a real scenario, this would throw if recursive is false.
            // For simplicity in mock, we assume parent dir is implicitly created or mkdir was called.
            this._dirs.add(dir); 
        }
        this._files.set(filePath, content);
    },
    async unlink(filePath) {
        if (!this._files.delete(filePath)) {
            const error = new Error(`ENOENT: no such file or directory, unlink '${filePath}'`);
            error.code = 'ENOENT';
            throw error;
        }
    },
    async readdir(dirPath) {
        if (!this._dirs.has(dirPath)) {
            const error = new Error(`ENOENT: no such file or directory, scandir '${dirPath}'`);
            error.code = 'ENOENT';
            throw error;
        }
        const filesInDir = Array.from(this._files.keys())
            .filter(filePath => path.dirname(filePath) === dirPath)
            .map(filePath => path.basename(filePath));
        return filesInDir;
    },
    reset() {
        this._files.clear();
        this._dirs.clear();
    }
};

// Temporarily replace fs.promises with our mock
const originalFsPromises = require('fs').promises;
require('fs').promises = mockFs;

describe('Nightly Echo File Manifestor', () => {
    const GHOST_DIR = '/tmp/ghosts';

    beforeEach(() => {
        mockFs.reset();
        mockFs._dirs.add(GHOST_DIR); // Ensure ghost directory exists for tests
    });

    test('should manifest a ghost file with default content', async () => {
        const originalPath = 'project/src/file.js';
        const expectedGhostPath = path.join(GHOST_DIR, 'file.js.ghost');
        const ghostPath = await manifestGhost(originalPath, GHOST_DIR);

        expect(ghostPath).toBe(expectedGhostPath);
        expect(mockFs._files.has(expectedGhostPath)).toBe(true);
        expect(mockFs._files.get(expectedGhostPath)).toContain('Echo of a forgotten file: project/src/file.js');
    });

    test('should manifest a ghost file with custom content', async () => {
        const originalPath = 'another/path/document.txt';
        const customContent = 'This document was important once.';
        const expectedGhostPath = path.join(GHOST_DIR, 'document.txt.ghost');
        const ghostPath = await manifestGhost(originalPath, GHOST_DIR, customContent);

        expect(ghostPath).toBe(expectedGhostPath);
        expect(mockFs._files.has(expectedGhostPath)).toBe(true);
        expect(mockFs._files.get(expectedGhostPath)).toContain(`// ${customContent}`);
    });

    test('should list manifested ghost files', async () => {
        await manifestGhost('file1.js', GHOST_DIR);
        await manifestGhost('file2.txt', GHOST_DIR);
        // Add a non-ghost file to ensure filtering works
        mockFs.writeFile(path.join(GHOST_DIR, 'regular_file.log'), 'log content');

        const ghosts = await listGhosts(GHOST_DIR);
        expect(ghosts).toEqual(expect.arrayContaining([
            path.join(GHOST_DIR, 'file1.js.ghost'),
            path.join(GHOST_DIR, 'file2.txt.ghost')
        ]));
        expect(ghosts).not.toContain(path.join(GHOST_DIR, 'regular_file.log'));
        expect(ghosts.length).toBe(2);
    });

    test('should return empty array if no ghosts exist', async () => {
        const ghosts = await listGhosts(GHOST_DIR);
        expect(ghosts).toEqual([]);
    });

    test('should return empty array if ghost directory does not exist for listing', async () => {
        mockFs.reset(); // Ensure no directories exist
        const ghosts = await listGhosts('/nonexistent/dir');
        expect(ghosts).toEqual([]);
    });

    test('should clean all ghost files', async () => {
        await manifestGhost('fileA.js', GHOST_DIR);
        await manifestGhost('fileB.txt', GHOST_DIR);
        mockFs.writeFile(path.join(GHOST_DIR, 'important.log'), 'keep this'); // Non-ghost file

        let ghostsBeforeClean = await listGhosts(GHOST_DIR);
        expect(ghostsBeforeClean.length).toBe(2);

        const cleanedPaths = await cleanGhosts(GHOST_DIR);
        expect(cleanedPaths).toEqual(expect.arrayContaining([
            path.join(GHOST_DIR, 'fileA.js.ghost'),
            path.join(GHOST_DIR, 'fileB.txt.ghost')
        ]));
        expect(cleanedPaths.length).toBe(2);

        let ghostsAfterClean = await listGhosts(GHOST_DIR);
        expect(ghostsAfterClean).toEqual([]);
        expect(mockFs._files.has(path.join(GHOST_DIR, 'important.log'))).toBe(true); // Non-ghost file should remain
    });

    test('should handle cleaning when ghost directory does not exist', async () => {
        mockFs.reset(); // Ensure no directories exist
        const cleaned = await cleanGhosts('/nonexistent/dir');
        expect(cleaned).toEqual([]);
    });

    test('should ensure ghost directory is created if it does not exist during manifest', async () => {
        mockFs.reset(); // Start with no directories
        const newGhostDir = '/new/ghost/location';
        await manifestGhost('new_file.js', newGhostDir);
        expect(mockFs._dirs.has(newGhostDir)).toBe(true);
        expect(mockFs._files.has(path.join(newGhostDir, 'new_file.js.ghost'))).toBe(true);
    });
});

// Restore original fs.promises after tests
afterAll(() => {
    require('fs').promises = originalFsPromises;
});
