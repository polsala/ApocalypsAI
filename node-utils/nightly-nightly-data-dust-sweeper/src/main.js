const fs = require('fs');
const path = require('path');

/**
 * Identifies and optionally removes files older than a specified number of days in a given directory.
 * @param {string} directory - The path to the directory to scan.
 * @param {number} days - The age threshold in days. Files older than this will be considered 'data-dust'.
 * @param {boolean} dryRun - If true, only lists files. If false, actually deletes them.
 * @returns {Array<Object>} An array of objects, each containing the path and modification time of an identified old file.
 */
function getFilesOlderThan(directory, days, dryRun = true) {
    const now = Date.now();
    const thresholdMs = days * 24 * 60 * 60 * 1000;
    const oldFiles = [];

    if (!fs.existsSync(directory)) {
        console.error(`Error: Digital cache not found: ${directory}`);
        return [];
    }

    let files;
    try {
        files = fs.readdirSync(directory);
    } catch (error) {
        console.error(`Error reading digital cache ${directory}: ${error.message}`);
        return [];
    }

    for (const file of files) {
        const filePath = path.join(directory, file);
        try {
            const stats = fs.statSync(filePath);
            // Only consider files, not directories
            if (stats.isFile() && (now - stats.mtimeMs) > thresholdMs) {
                oldFiles.push({ path: filePath, mtime: new Date(stats.mtimeMs) });
            }
        } catch (error) {
            console.warn(`Warning: Could not access temporal residue ${filePath}: ${error.message}`);
        }
    }

    if (dryRun) {
        console.log(`\n--- Dry Run: Found ${oldFiles.length} data-dust files older than ${days} days in ${directory} ---`);
        oldFiles.forEach(f => console.log(`  - ${f.path} (Modified: ${f.mtime.toISOString()})`));
        console.log('--- End Dry Run ---');
    } else {
        console.log(`\n--- Sweeping ${oldFiles.length} data-dust files older than ${days} days in ${directory} ---`);
        for (const file of oldFiles) {
            try {
                fs.unlinkSync(file.path);
                console.log(`  - Swept: ${file.path}`);
            } catch (error) {
                console.error(`  - Failed to sweep ${file.path}: ${error.message}`);
            }
        }
        console.log('--- Sweep Complete ---');
    }

    return oldFiles;
}

// CLI entry point
if (require.main === module) {
    const args = process.argv.slice(2);
    const directory = args[0];
    const days = parseInt(args[1], 10);
    const dryRun = !args.includes('--sweep');

    if (!directory || isNaN(days)) {
        console.log('Usage: node src/main.js <directory_path> <days_old> [--sweep]');
        console.log('Example: node src/main.js ./temp_cache 30 --sweep');
        console.log('  --sweep: Actually delete files. Without it, performs a dry run.');
        process.exit(1);
    }

    getFilesOlderThan(directory, days, dryRun);
}

module.exports = { getFilesOlderThan }; // Export for testing
