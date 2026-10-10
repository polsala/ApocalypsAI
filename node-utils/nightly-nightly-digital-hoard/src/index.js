const fs = require('fs/promises');
const path = require('path');

// Default thresholds
const DEFAULT_MAX_SIZE_MB = 100; // 100 MB
const DEFAULT_MAX_AGE_DAYS = 365; // 1 year

/**
 * Recursively scans a directory and collects file information.
 * @param {string} dirPath - The path to the directory to scan.
 * @returns {Promise<Array<{path: string, size: number, mtime: Date}>>} - A promise that resolves to an array of file objects.
 */
async function scanDirectory(dirPath) {
    let files = [];
    try {
        const entries = await fs.readdir(dirPath, { withFileTypes: true });

        for (const entry of entries) {
            const fullPath = path.join(dirPath, entry.name);
            try {
                if (entry.isDirectory()) {
                    files = files.concat(await scanDirectory(fullPath));
                } else if (entry.isFile()) {
                    const stats = await fs.stat(fullPath);
                    files.push({
                        path: fullPath,
                        size: stats.size, // bytes
                        mtime: stats.mtime // modification time
                    });
                }
            } catch (innerErr) {
                console.error(`Error scanning ${fullPath}: ${innerErr.message}`);
                // Silently skip inaccessible files/directories to continue scan
            }
        }
    } catch (outerErr) {
        console.error(`Error scanning directory ${dirPath}: ${outerErr.message}`);
    }
    return files;
}

/**
 * Analyzes a list of files against size and age thresholds.
 * @param {Array<{path: string, size: number, mtime: Date}>} allFiles - List of all files found.
 * @param {number} maxSizeMB - Maximum allowed file size in MB.
 * @param {number} maxAgeDays - Maximum allowed file age in days.
 * @returns {{bulkyFiles: Array<{path: string, size: number}>, ancientFiles: Array<{path: string, mtime: Date}>}}
 */
function analyzeFiles(allFiles, maxSizeMB, maxAgeDays) {
    const bulkyFiles = [];
    const ancientFiles = [];

    const maxSizeInBytes = maxSizeMB * 1024 * 1024;
    const minMtime = new Date(Date.now() - (maxAgeDays * 24 * 60 * 60 * 1000));

    for (const file of allFiles) {
        if (file.size > maxSizeInBytes) {
            bulkyFiles.push({ path: file.path, size: file.size });
        }
        if (file.mtime < minMtime) {
            ancientFiles.push({ path: file.path, mtime: file.mtime });
        }
    }

    return { bulkyFiles, ancientFiles };
}

/**
 * Formats file size for display.
 * @param {number} bytes - File size in bytes.
 * @returns {string}
 */
function formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
}

/**
 * Main function to run the utility.
 */
async function main() {
    const args = process.argv.slice(2);
    let targetPath = args[0];
    let maxSizeMB = DEFAULT_MAX_SIZE_MB;
    let maxAgeDays = DEFAULT_MAX_AGE_DAYS;

    if (!targetPath) {
        console.error('Usage: node src/index.js <path_to_bunker> [--max-size <MB>] [--max-age <days>]');
        process.exit(1);
    }

    // Parse optional arguments
    for (let i = 1; i < args.length; i++) {
        if (args[i] === '--max-size' && args[i + 1]) {
            maxSizeMB = parseFloat(args[++i]);
            if (isNaN(maxSizeMB) || maxSizeMB <= 0) {
                console.error('Error: --max-size must be a positive number.');
                process.exit(1);
            }
        } else if (args[i] === '--max-age' && args[i + 1]) {
            maxAgeDays = parseInt(args[++i], 10);
            if (isNaN(maxAgeDays) || maxAgeDays <= 0) {
                console.error('Error: --max-age must be a positive integer.');
                process.exit(1);
            }
        }
    }

    // Resolve targetPath to an absolute path for clarity and robustness
    targetPath = path.resolve(targetPath);

    console.log(`Scanning your digital bunker at: ${targetPath}`);
    console.log(`Thresholds: Max Size = ${maxSizeMB} MB, Max Age = ${maxAgeDays} days`);
    console.log('\n--- Digital Hoard Analysis ---\n');

    const allFiles = await scanDirectory(targetPath);
    const { bulkyFiles, ancientFiles } = analyzeFiles(allFiles, maxSizeMB, maxAgeDays);

    if (bulkyFiles.length > 0) {
        console.log('### Bulky Cargo Containers (Files > ' + maxSizeMB + ' MB):');
        bulkyFiles.forEach(file => {
            console.log(`  - ${file.path} (${formatBytes(file.size)})`);
        });
        console.log('');
    }

    if (ancientFiles.length > 0) {
        console.log('### Ancient Data Scrolls (Files > ' + maxAgeDays + ' days old):');
        ancientFiles.forEach(file => {
            console.log(`  - ${file.path} (Last modified: ${file.mtime.toISOString().split('T')[0]})`);
        });
        console.log('');
    }

    console.log('--- Hoard Summary ---');
    if (bulkyFiles.length === 0 && ancientFiles.length === 0) {
        console.log('Your digital bunker is remarkably clean! No bulky cargo or ancient scrolls found exceeding thresholds.');
    } else {
        console.log(`Found ${bulkyFiles.length} Bulky Cargo Containers.`);
        console.log(`Found ${ancientFiles.length} Ancient Data Scrolls.`);
        console.log('\nRecommendation: Review these items. Consider archiving, compressing, or purging them to free up valuable storage rations for the future!');
    }
}

if (require.main === module) {
    main();
}

// Export main for testing purposes
module.exports = { main };
