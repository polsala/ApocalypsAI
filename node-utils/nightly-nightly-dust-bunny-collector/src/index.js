const fs = require('fs');
const path = require('path');

/**
 * Calculates the age of a file in days based on its last modification time.
 * @param {string} filePath - The path to the file.
 * @returns {number} The age of the file in days, or -1 if an error occurs.
 */
function getFileAgeInDays(filePath) {
    try {
        const stats = fs.statSync(filePath);
        const now = new Date();
        const mtime = new Date(stats.mtime);
        const diffTime = Math.abs(now.getTime() - mtime.getTime());
        return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    } catch (error) {
        console.error(`Error getting stats for ${filePath}: ${error.message}`);
        return -1; // Indicate error
    }
}

/**
 * Recursively finds files older than a specified age threshold in a directory.
 * Skips the '.dust-bunnies-archive' directory to prevent re-processing archived files.
 * @param {string} dirPath - The directory to scan.
 * @param {number} ageThresholdDays - The minimum age in days for a file to be considered.
 * @param {Array<Object>} [filesFound=[]] - Accumulator for found files.
 * @returns {Array<Object>} A list of objects, each with { path: string, age: number }.
 */
function findDustBunnies(dirPath, ageThresholdDays, filesFound = []) {
    if (!fs.existsSync(dirPath)) {
        console.warn(`Directory not found: ${dirPath}`);
        return filesFound;
    }
    if (!fs.statSync(dirPath).isDirectory()) {
        console.warn(`Path is not a directory: ${dirPath}`);
        return filesFound;
    }

    const items = fs.readdirSync(dirPath);

    for (const item of items) {
        const itemPath = path.join(dirPath, item);
        try {
            const stats = fs.statSync(itemPath);
            if (stats.isDirectory()) {
                // Skip the archive directory itself
                if (path.basename(itemPath) === '.dust-bunnies-archive') {
                    continue;
                }
                findDustBunnies(itemPath, ageThresholdDays, filesFound);
            } else if (stats.isFile()) {
                const age = getFileAgeInDays(itemPath);
                if (age >= ageThresholdDays) {
                    filesFound.push({ path: itemPath, age: age });
                }
            }
        } catch (error) {
            console.error(`Error processing ${itemPath}: ${error.message}`);
        }
    }
    return filesFound;
}

/**
 * Archives a single file by moving it to a '.dust-bunnies-archive' subfolder.
 * Creates the archive folder if it doesn't exist.
 * @param {string} filePath - The path to the file to archive.
 * @param {string} baseDir - The base directory where the archive folder should be created.
 * @returns {boolean} True if archiving was successful, false otherwise.
 */
function archiveFile(filePath, baseDir) {
    const archiveDir = path.join(baseDir, '.dust-bunnies-archive');
    if (!fs.existsSync(archiveDir)) {
        fs.mkdirSync(archiveDir, { recursive: true });
    }
    const fileName = path.basename(filePath);
    const newPath = path.join(archiveDir, fileName);
    try {
        fs.renameSync(filePath, newPath);
        console.log(`Archived: ${filePath} -> ${newPath}`);
        return true;
    } catch (error) {
        console.error(`Error archiving ${filePath}: ${error.message}`);
        return false;
    }
}

/**
 * Main function to parse command-line arguments and execute the utility logic.
 * @param {string[]} args - Command-line arguments (e.g., process.argv.slice(2)).
 */
function main(args) {
    let targetPath = '.';
    let ageThreshold = 90; // Default 90 days
    let action = 'list';

    for (let i = 0; i < args.length; i++) {
        if (args[i] === '--path' && args[i + 1]) {
            targetPath = args[++i];
        } else if (args[i] === '--age' && args[i + 1]) {
            ageThreshold = parseInt(args[++i], 10);
            if (isNaN(ageThreshold) || ageThreshold < 0) {
                console.error('Error: --age must be a positive number.');
                process.exit(1);
            }
        } else if (args[i] === '--action' && args[i + 1]) {
            const requestedAction = args[++i];
            if (['list', 'archive'].includes(requestedAction)) {
                action = requestedAction;
            } else {
                console.error('Error: --action must be "list" or "archive".');
                process.exit(1);
            }
        }
    }

    console.log(`Scanning '${targetPath}' for digital dust bunnies older than ${ageThreshold} days...`);
    const dustBunnies = findDustBunnies(targetPath, ageThreshold);

    if (dustBunnies.length === 0) {
        console.log('No digital dust bunnies found! Your directories are sparkling clean.');
        return;
    }

    console.log(`Found ${dustBunnies.length} digital dust bunnies:`);
    dustBunnies.forEach(bunny => {
        console.log(`- ${bunny.path} (age: ${bunny.age} days)`);
    });

    if (action === 'archive') {
        console.log('\nArchiving found dust bunnies...');
        dustBunnies.forEach(bunny => {
            archiveFile(bunny.path, targetPath);
        });
        console.log('Archiving complete.');
    }
}

// Allow running directly from CLI or importing as a module for testing
if (require.main === module) {
    main(process.argv.slice(2));
}

module.exports = {
    getFileAgeInDays,
    findDustBunnies,
    archiveFile,
    main
};
