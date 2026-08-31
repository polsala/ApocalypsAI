const fs = require('fs').promises;
const path = require('path');

async function getFileDustScore(filePath) {
    try {
        const stats = await fs.stat(filePath);
        if (stats.isFile()) {
            const now = Date.now();
            const mtimeMs = stats.mtimeMs; // Modification time
            const atimeMs = stats.atimeMs; // Access time

            // Calculate days since modification and access
            const daysSinceModified = Math.floor((now - mtimeMs) / (1000 * 60 * 60 * 24));
            const daysSinceAccessed = Math.floor((now - atimeMs) / (1000 * 60 * 60 * 24));

            // A simple dust score: the maximum of days since modified or accessed.
            // This ensures a file is considered 'dusty' if either its content or its last use is old.
            const dustScore = Math.max(daysSinceModified, daysSinceAccessed);

            return {
                filePath: filePath,
                dustScore: dustScore,
                mtime: new Date(mtimeMs).toISOString(),
                atime: new Date(atimeMs).toISOString()
            };
        }
    } catch (error) {
        // Ignore errors for files we can't access (e.g., permissions, broken symlinks)
        // console.warn(`Could not process file ${filePath}: ${error.message}`);
    }
    return null;
}

async function scanDirectory(dirPath, minDustDays = 90) {
    let forgottenFiles = [];
    try {
        const entries = await fs.readdir(dirPath, { withFileTypes: true });

        for (const entry of entries) {
            const fullPath = path.join(dirPath, entry.name);
            if (entry.isDirectory()) {
                forgottenFiles = forgottenFiles.concat(await scanDirectory(fullPath, minDustDays));
            } else if (entry.isFile()) {
                const fileInfo = await getFileDustScore(fullPath);
                if (fileInfo && fileInfo.dustScore >= minDustDays) {
                    forgottenFiles.push(fileInfo);
                }
            }
        }
    } catch (error) {
        // console.error(`Error scanning directory ${dirPath}: ${error.message}`);
    }
    return forgottenFiles;
}

async function main() {
    const args = process.argv.slice(2);
    let targetPath = args[0];
    let minDustDays = parseInt(args[1], 10);

    if (!targetPath) {
        console.error("Usage: node src/index.js <directory_to_scan> [minimum_dust_days (default: 90)]");
        process.exit(1);
    }

    if (isNaN(minDustDays) || minDustDays < 0) {
        minDustDays = 90; // Default to 90 days
    }

    console.log(`\nScanning '${targetPath}' for files with at least ${minDustDays} days of digital dust...\n`);

    const forgottenFiles = await scanDirectory(targetPath, minDustDays);

    if (forgottenFiles.length === 0) {
        console.log("The Byte-Breeze finds no truly forgotten files here. All is well!");
        return;
    }

    forgottenFiles.sort((a, b) => b.dustScore - a.dustScore); // Sort by highest dust score first

    console.log("The Byte-Breeze whispers about these forgotten files:\n");
    for (const file of forgottenFiles) {
        console.log(`[Digital Dust: ${file.dustScore} days] ${file.filePath}`);
    }
    console.log("\nConsider reviewing or archiving these digital relics.");
}

// Only run main if this script is executed directly
if (require.main === module) {
    main();
}

module.exports = { getFileDustScore, scanDirectory, main }; // Export for testing
