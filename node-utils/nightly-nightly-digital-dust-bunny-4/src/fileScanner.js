const fs = require('fs');
const path = require('path');

/**
 * Scans a directory for files older than a specified age.
 * @param {string} rootPath - The path to start scanning from.
 * @param {number} minAgeDays - Minimum age in days for a file to be considered "old".
 * @param {string[]} excludePatterns - Array of regex patterns for paths to exclude.
 * @returns {Array<{path: string, ageDays: number, mtime: Date}>} - List of old files found.
 */
function scan(rootPath, minAgeDays, excludePatterns = []) {
    const oldFiles = [];
    const now = Date.now();
    const minAgeMs = minAgeDays * 24 * 60 * 60 * 1000; // Convert days to milliseconds

    if (!fs.existsSync(rootPath)) {
        console.error(`Error: Path does not exist: ${rootPath}`);
        return [];
    }

    const excludeRegexes = excludePatterns.map(pattern => new RegExp(pattern));

    function traverse(currentPath) {
        try {
            const entries = fs.readdirSync(currentPath, { withFileTypes: true });

            for (const entry of entries) {
                const fullPath = path.join(currentPath, entry.name);

                // Check against exclude patterns
                if (excludeRegexes.some(regex => regex.test(fullPath))) {
                    continue;
                }

                if (entry.isDirectory()) {
                    traverse(fullPath); // Recurse into subdirectories
                } else if (entry.isFile()) {
                    const stats = fs.statSync(fullPath);
                    const fileAgeMs = now - stats.mtime.getTime();
                    const fileAgeDays = fileAgeMs / (24 * 60 * 60 * 1000);

                    if (fileAgeDays >= minAgeDays) {
                        oldFiles.push({
                            path: fullPath,
                            ageDays: parseFloat(fileAgeDays.toFixed(2)),
                            mtime: stats.mtime
                        });
                    }
                }
            }
        } catch (error) {
            // Ignore permission errors or other read errors for robustness
            // console.warn(`Warning: Could not read ${currentPath}: ${error.message}`);
        }
    }

    traverse(rootPath);
    return oldFiles;
}

module.exports = { scan };
