const fs = require('fs').promises;
const path = require('path');

/**
 * Ensures a directory exists, creating it recursively if necessary.
 * @param {string} dirPath - The path to the directory.
 */
async function ensureDir(dirPath) {
    await fs.mkdir(dirPath, { recursive: true });
}

/**
 * Creates a 'ghost file' for a given path in a specified ghost directory.
 * The ghost file will have a '.ghost' suffix and contain a placeholder message.
 * @param {string} filePath - The original path for which to create a ghost.
 * @param {string} ghostDir - The directory where the ghost file will be created.
 * @param {string} [content=''] - Optional custom content for the ghost file.
 * @returns {Promise<string>} The full path to the created ghost file.
 */
async function manifestGhost(filePath, ghostDir, content = '') {
    await ensureDir(ghostDir);
    const ghostFileName = path.basename(filePath) + '.ghost';
    const ghostPath = path.join(ghostDir, ghostFileName);
    const fileContent = `// ${content || 'Echo of a forgotten file: ' + filePath}\n`;
    await fs.writeFile(ghostPath, fileContent);
    return ghostPath;
}

/**
 * Removes all '.ghost' files from a specified directory.
 * @param {string} ghostDir - The directory to clean.
 * @returns {Promise<string[]>} An array of paths to the deleted ghost files.
 */
async function cleanGhosts(ghostDir) {
    try {
        const files = await fs.readdir(ghostDir);
        const ghostFiles = files.filter(file => file.endsWith('.ghost'));
        const deletedPaths = [];
        for (const file of ghostFiles) {
            const filePath = path.join(ghostDir, file);
            await fs.unlink(filePath);
            deletedPaths.push(filePath);
        }
        return deletedPaths;
    } catch (error) {
        if (error.code === 'ENOENT') {
            return []; // Directory doesn't exist, nothing to clean
        }
        throw error;
    }
}

/**
 * Lists all '.ghost' files in a specified directory.
 * @param {string} ghostDir - The directory to list ghosts from.
 * @returns {Promise<string[]>} An array of full paths to the ghost files.
 */
async function listGhosts(ghostDir) {
    try {
        const files = await fs.readdir(ghostDir);
        return files.filter(file => file.endsWith('.ghost')).map(file => path.join(ghostDir, file));
    } catch (error) {
        if (error.code === 'ENOENT') {
            return []; // Directory doesn't exist, no ghosts
        }
        throw error;
    }
}

module.exports = {
    manifestGhost,
    cleanGhosts,
    listGhosts
};
