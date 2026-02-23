const fs = require('fs').promises;
const path = require('path');

async function findStaleFiles(dir, daysOld, currentTimestamp) {
    const thresholdMs = daysOld * 24 * 60 * 60 * 1000;
    const staleFiles = [];

    async function traverse(currentPath) {
        let entries;
        try {
            entries = await fs.readdir(currentPath, { withFileTypes: true });
        } catch (error) {
            // Ignore directories we can't read, but log for debugging if needed
            // console.error(`Could not read directory ${currentPath}: ${error.message}`);
            return;
        }

        for (const entry of entries) {
            const fullPath = path.join(currentPath, entry.name);
            try {
                const stats = await fs.stat(fullPath);
                if (stats.isDirectory()) {
                    await traverse(fullPath);
                } else if (stats.isFile()) {
                    // Use mtimeMs for modification time in milliseconds
                    if (currentTimestamp - stats.mtimeMs > thresholdMs) {
                        staleFiles.push(fullPath);
                    }
                }
            } catch (error) {
                // Ignore files/directories we can't stat, e.g., broken symlinks or permission issues
                // console.error(`Could not stat ${fullPath}: ${error.message}`);
            }
        }
    }

    await traverse(dir);
    return staleFiles;
}

async function run() {
    const args = process.argv.slice(2);
    const directory = args[0];
    const days = parseInt(args[1], 10);

    if (!directory || isNaN(days) || days <= 0) {
        console.log("Usage: node src/index.js <directory_path> <days_old>");
        console.log("Example: node src/index.js ./my_project 30");
        console.log("Finds files in ./my_project that haven't been modified in 30 days.");
        process.exit(1);
    }

    const currentTimestamp = Date.now();
    console.log(`Sweeping for digital dust bunnies older than ${days} days in: ${directory}\n`);

    const staleFiles = await findStaleFiles(directory, days, currentTimestamp);

    if (staleFiles.length === 0) {
        console.log("✨ No digital dust bunnies found! Your directory is sparkling clean.");
    } else {
        console.log("🗑️ Found these digital dust bunnies:");
        staleFiles.forEach(file => console.log(`- ${file}`));
        console.log(`\nConsider archiving or deleting these ${staleFiles.length} files.`);
    }
}

// Only run if called directly
if (require.main === module) {
    run().catch(err => {
        console.error("An error occurred:", err);
        process.exit(1);
    });
}

module.exports = { findStaleFiles }; // Export for testing
