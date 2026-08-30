const fs = require('fs');
const path = require('path');

/**
 * Recursively finds files in a directory that are older than a specified number of days.
 * These are affectionately referred to as 'digital dust bunnies'.
 *
 * @param {string} directory The path to the directory to scan.
 * @param {number} daysOld The minimum age in days for a file to be considered a dust bunny.
 * @returns {Array<Object>} An array of objects, each containing the path and modification time of a dust bunny.
 */
function findDustBunnies(directory, daysOld) {
    const dustBunnies = [];
    const cutoffTime = Date.now() - (daysOld * 24 * 60 * 60 * 1000);

    function traverse(currentPath) {
        let entries;
        try {
            entries = fs.readdirSync(currentPath, { withFileTypes: true });
        } catch (error) {
            if (error.code === 'ENOENT') {
                // console.error(`Directory not found: ${currentPath}`); // Suppress for cleaner CLI output on error
                return;
            }
            console.warn(`Warning: Could not read directory ${currentPath}: ${error.message}`);
            return;
        }

        for (const entry of entries) {
            const fullPath = path.join(currentPath, entry.name);
            try {
                const stats = fs.statSync(fullPath);
                if (entry.isDirectory()) {
                    traverse(fullPath);
                } else if (stats.isFile() && stats.mtimeMs < cutoffTime) {
                    dustBunnies.push({
                        path: fullPath,
                        modified: new Date(stats.mtimeMs).toISOString()
                    });
                }
            } catch (error) {
                console.warn(`Warning: Could not stat ${fullPath}: ${error.message}`);
            }
        }
    }

    traverse(directory);
    return dustBunnies;
}

// CLI execution logic
if (require.main === module) {
    const args = process.argv.slice(2);
    const directory = args[0];
    const days = parseInt(args[1], 10);

    if (!directory || isNaN(days) || days < 0) {
        console.log('Usage: node src/index.js <directory_path> <days_old>');
        console.log('Example: node src/index.js ./my_project 365');
        process.exit(1);
    }

    console.log(`\nSweeping for digital dust bunnies older than ${days} days in: ${directory}\n`);
    const bunnies = findDustBunnies(directory, days);

    if (bunnies.length > 0) {
        console.log('Found these forgotten digital dust bunnies:');
        bunnies.forEach(bunny => {
            console.log(`- ${bunny.path} (Last modified: ${bunny.modified})`);
        });
        console.log('\nConsider giving them a new home in the archive, or perhaps a gentle sweep into the void!');
    } else {
        console.log('No digital dust bunnies found! Your digital space is sparkling clean.');
    }
}

module.exports = { findDustBunnies };
