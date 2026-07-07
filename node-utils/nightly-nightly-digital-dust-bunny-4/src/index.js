const fs = require('fs');
const path = require('path');

/**
 * Recursively finds files in a directory that are older than a specified number of days.
 * @param {string} dirPath - The path to the directory to scan.
 * @param {number} daysOldThreshold - The minimum age in days for a file to be considered old.
 * @returns {Array<Object>} An array of objects, each representing an old file.
 */
function findOldFiles(dirPath, daysOldThreshold) {
    const oldFiles = [];
    const now = new Date();
    const thresholdMs = daysOldThreshold * 24 * 60 * 60 * 1000; // Convert days to milliseconds

    try {
        const entries = fs.readdirSync(dirPath, { withFileTypes: true });

        for (const entry of entries) {
            const fullPath = path.join(dirPath, entry.name);
            let stats;
            try {
                stats = fs.statSync(fullPath);
            } catch (statErr) {
                // Ignore files/directories we can't stat (e.g., permission errors, broken symlinks)
                continue;
            }

            if (entry.isDirectory()) {
                oldFiles.push(...findOldFiles(fullPath, daysOldThreshold));
            } else if (entry.isFile()) {
                const mtimeMs = stats.mtime.getTime();
                const ageMs = now.getTime() - mtimeMs;

                if (ageMs > thresholdMs) {
                    oldFiles.push({
                        path: fullPath,
                        mtime: stats.mtime,
                        size: stats.size
                    });
                }
            }
        }
    } catch (readDirErr) {
        // Ignore directories we can't read (e.g., permission errors)
        console.warn(`⚠️ Could not read directory: ${dirPath} - ${readDirErr.message}`);
    }

    return oldFiles;
}

/**
 * Formats file size into a human-readable string.
 * @param {number} bytes - The file size in bytes.
 * @returns {string} Human-readable file size.
 */
function formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

/**
 * Main execution logic for the CLI.
 */
function main() {
    const args = process.argv.slice(2);
    const directoryPath = args[0];
    const daysOld = parseInt(args[1], 10) || 90; // Default to 90 days

    if (!directoryPath) {
        console.error('Usage: node src/index.js <directory_path> [days_old]');
        process.exit(1);
    }

    console.log(`🧹 Sweeping for digital dust bunnies in ${directoryPath} (older than ${daysOld} days)...`);

    const oldFiles = findOldFiles(directoryPath, daysOld);

    if (oldFiles.length === 0) {
        console.log('\n🎉 No digital dust bunnies found! Your digital space is sparkling clean.');
    } else {
        console.log(`\nFound ${oldFiles.length} digital dust bunnies:`);
        oldFiles.forEach(file => {
            const ageDays = Math.floor((new Date().getTime() - file.mtime.getTime()) / (1000 * 60 * 60 * 24));
            console.log(
                `✨ ${file.path} (Modified: ${file.mtime.toISOString().split('T')[0]}, Size: ${formatBytes(file.size)}) - ${ageDays} days old!`
            );
        });
        console.log(`\nTotal dust bunnies found: ${oldFiles.length}. Time to consider a digital spring cleaning! 🧺`);
    }
}

// Only run main if this script is executed directly
if (require.main === module) {
    main();
}

// Export for testing
module.exports = { findOldFiles, formatBytes, main };
