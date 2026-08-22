const fs = require('fs');
const path = require('path');

const defaultPatterns = [
    'node_modules',
    'dist',
    'build',
    'target',
    '.cache',
    '.tmp',
    'tmp',
    '.DS_Store',
    'Thumbs.db',
    '*.log',
    '*.bak',
    '*.swp',
    'coverage',
    '.nyc_output'
];

/**
 * Recursively finds files and directories matching specified patterns.
 * @param {string} startPath The path to start scanning from.
 * @param {string[]} patterns List of file/directory names or glob patterns to match.
 * @param {string[]} foundBunnies Accumulator for found items.
 * @returns {string[]} List of paths to "dust bunnies".
 */
function findDustBunnies(startPath, patterns = defaultPatterns, foundBunnies = []) {
    if (!fs.existsSync(startPath)) {
        return foundBunnies;
    }

    const entries = fs.readdirSync(startPath, { withFileTypes: true });

    for (const entry of entries) {
        const fullPath = path.join(startPath, entry.name);

        // Skip symbolic links to prevent infinite loops or unintended deletions
        if (entry.isSymbolicLink()) {
            continue;
        }

        const isMatch = patterns.some(pattern => {
            if (pattern.startsWith('*.')) { // Simple glob for file extensions
                return entry.isFile() && entry.name.endsWith(pattern.substring(1));
            }
            return entry.name === pattern; // Exact match for file/directory names
        });

        if (isMatch) {
            foundBunnies.push(fullPath);
            // If it's a directory, we don't need to scan inside it further
            // as the whole directory is a dust bunny.
            continue;
        }

        if (entry.isDirectory()) {
            // Prevent scanning into node_modules or other large known dust bunnies
            // if they are not the target match themselves, but a parent directory.
            // This optimization avoids deep dives into directories that will be deleted anyway.
            if (!patterns.includes(entry.name)) {
                findDustBunnies(fullPath, patterns, foundBunnies);
            }
        }
    }
    return foundBunnies;
}

/**
 * Deletes a list of files and directories.
 * @param {string[]} bunnyPaths Paths to delete.
 * @returns {object} An object containing counts of deleted files/dirs and errors.
 */
function deleteDustBunnies(bunnyPaths) {
    let deletedCount = 0;
    let errorCount = 0;
    const errors = [];

    for (const bunnyPath of bunnyPaths) {
        try {
            const stats = fs.statSync(bunnyPath);
            if (stats.isDirectory()) {
                fs.rmSync(bunnyPath, { recursive: true, force: true });
                deletedCount++;
            } else if (stats.isFile()) {
                fs.unlinkSync(bunnyPath);
                deletedCount++;
            }
        } catch (error) {
            errorCount++;
            errors.push({ path: bunnyPath, error: error.message });
        }
    }
    return { deletedCount, errorCount, errors };
}

module.exports = {
    findDustBunnies,
    deleteDustBunnies,
    defaultPatterns
};
