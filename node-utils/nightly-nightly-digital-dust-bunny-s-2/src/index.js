const fs = require('fs').promises;
const path = require('path');

/**
 * Scans a directory recursively to find files not modified within the given threshold.
 * @param {string} dirPath - The path to the directory to scan.
 * @param {number} thresholdDays - The number of days. Files modified before this threshold are considered 'dust bunnies'.
 * @returns {Promise<Array<{path: string, modified: string}>>} A promise that resolves to an array of old file objects.
 */
async function getDustBunnies(dirPath, thresholdDays) {
    const now = new Date();
    // Mock rationale: In tests, global.Date is mocked to return a fixed 'now'.
    // This ensures thresholdDate is consistent and tests are deterministic.
    const thresholdDate = new Date(now.setDate(now.getDate() - thresholdDays));
    const dustBunnies = [];

    async function scan(currentPath) {
        let entries;
        try {
            // Mock rationale: fs.readdir is mocked in tests to simulate directory contents
            // without actual file system access, ensuring offline and deterministic behavior.
            entries = await fs.readdir(currentPath, { withFileTypes: true });
        } catch (error) {
            console.error(`ApocalypsAI Sentry: Cannot access path "${currentPath}". Skipping. Error: ${error.message}`);
            return;
        }

        for (const entry of entries) {
            const fullPath = path.join(currentPath, entry.name);
            try {
                // Mock rationale: fs.stat is mocked in tests to provide controlled file metadata
                // (like mtime and isFile/isDirectory) without actual file system access.
                const stats = await fs.stat(fullPath);
                if (stats.isFile()) {
                    if (stats.mtime < thresholdDate) {
                        dustBunnies.push({
                            path: fullPath,
                            modified: stats.mtime.toISOString().split('T')[0] // YYYY-MM-DD
                        });
                    }
                } else if (stats.isDirectory()) {
                    await scan(fullPath); // Recurse into subdirectories
                }
            } catch (error) {
                console.error(`ApocalypsAI Sentry: Cannot stat "${fullPath}". Skipping. Error: ${error.message}`);
            }
        }
    }

    await scan(dirPath);
    return dustBunnies;
}

/**
 * Main function to parse arguments and run the dust bunny sweeper.
 */
async function main() {
    const args = process.argv.slice(2);
    const dirPath = args[0];
    const thresholdDays = parseInt(args[1], 10);

    if (!dirPath || isNaN(thresholdDays) || thresholdDays <= 0) {
        console.log("Usage: node src/index.js <directory_path> <threshold_days>");
        console.log("Example: node src/index.js ./my_project 90");
        console.log("Identifies files not modified in the last <threshold_days> days.");
        process.exit(1);
    }

    console.log(`\nScanning "${dirPath}" for digital dust bunnies older than ${thresholdDays} days...\n`);

    const bunnies = await getDustBunnies(dirPath, thresholdDays);

    if (bunnies.length === 0) {
        console.log("✨ All clear! No digital dust bunnies found. Your digital sanctuary is pristine.");
    } else {
        console.log("🚨 Digital Dust Bunnies Detected! These files are gathering virtual dust:");
        bunnies.forEach(bunny => {
            console.log(`- ${bunny.path} (Last modified: ${bunny.modified})`);
        });
        console.log(`\nConsider sweeping these relics into the void or quarantining them for later inspection.`);
    }
}

// Export for testing purposes, run main if executed directly
if (require.main === module) {
    main();
} else {
    module.exports = { getDustBunnies };
}
