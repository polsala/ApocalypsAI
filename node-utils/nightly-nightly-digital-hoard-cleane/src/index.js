const fs = require('fs').promises;
const path = require('path');

async function getFilesOlderThan(directory, ageDays, recursive = false) {
    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - ageDays);

    let oldFiles = [];
    let entries;
    try {
        entries = await fs.readdir(directory, { withFileTypes: true });
    } catch (error) {
        console.error(`\n🚨 Error accessing directory "${directory}": ${error.message}`);
        return [];
    }

    for (const entry of entries) {
        const fullPath = path.join(directory, entry.name);
        try {
            const stats = await fs.stat(fullPath);
            if (stats.isFile() && stats.mtime < cutoffDate) {
                oldFiles.push({ path: fullPath, mtime: stats.mtime });
            } else if (recursive && stats.isDirectory()) {
                oldFiles = oldFiles.concat(await getFilesOlderThan(fullPath, ageDays, recursive));
            }
        } catch (error) {
            // Ignore files that might disappear during scan or permission issues
            // console.warn(`Skipping "${fullPath}": ${error.message}`);
        }
    }
    return oldFiles;
}

async function cleanHoard(directory, ageDays, dryRun, compostDir, recursive = false) {
    console.log(`\n🧹 Initiating Digital Hoard Cleanup in "${directory}"...`);
    console.log(`Looking for files older than ${ageDays} days${recursive ? ' (recursively)' : ''}.`);

    const oldFiles = await getFilesOlderThan(directory, ageDays, recursive);

    if (oldFiles.length === 0) {
        console.log(`✨ No digital dust bunnies found! Your hoard is sparkling clean.`);
        return { cleaned: 0, skipped: 0, errors: 0 };
    }

    console.log(`\nFound ${oldFiles.length} ancient digital artifacts:`);
    oldFiles.forEach(file => console.log(`  - ${file.path} (last modified: ${file.mtime.toLocaleDateString()})`));

    if (dryRun) {
        console.log(`\n🔍 Dry run complete. No files were moved or deleted.`);
        return { cleaned: 0, skipped: oldFiles.length, errors: 0 };
    }

    let cleanedCount = 0;
    let errorCount = 0;

    for (const file of oldFiles) {
        try {
            if (compostDir) {
                const compostPath = path.join(compostDir, path.basename(file.path));
                await fs.mkdir(compostDir, { recursive: true }); // Ensure compost directory exists
                await fs.rename(file.path, compostPath);
                console.log(`  ➡️ Moved "${file.path}" to compost pile: "${compostPath}"`);
            } else {
                await fs.unlink(file.path);
                console.log(`  🗑️ Deleted "${file.path}"`);
            }
            cleanedCount++;
        } catch (error) {
            console.error(`  ❌ Failed to process "${file.path}": ${error.message}`);
            errorCount++;
        }
    }

    console.log(`\n🎉 Cleanup complete!`);
    console.log(`  ${cleanedCount} files ${compostDir ? 'composted' : 'deleted'}.`);
    if (errorCount > 0) {
        console.log(`  ${errorCount} files encountered errors.`);
    }
    return { cleaned: cleanedCount, skipped: 0, errors: errorCount };
}

// CLI entry point
if (require.main === module) {
    const args = process.argv.slice(2);
    let directory = process.cwd();
    let ageDays = 30;
    let dryRun = false;
    let compostDir = null;
    let recursive = false;

    for (let i = 0; i < args.length; i++) {
        const arg = args[i];
        if (arg === '--dir' || arg === '-d') {
            directory = args[++i];
        } else if (arg === '--age' || arg === '-a') {
            ageDays = parseInt(args[++i], 10);
            if (isNaN(ageDays) || ageDays <= 0) {
                console.error('Error: --age must be a positive number.');
                process.exit(1);
            }
        } else if (arg === '--dry-run' || arg === '-n') {
            dryRun = true;
        } else if (arg === '--compost' || arg === '-c') {
            compostDir = args[++i];
        } else if (arg === '--recursive' || arg === '-r') {
            recursive = true;
        } else if (arg === '--help' || arg === '-h') {
            console.log(`\nUsage: node src/index.js [options]\n\nA whimsical utility to find and sweep away old, forgotten files (digital dust bunnies) from your directories.\n\nOptions:\n  -d, --dir <path>       Directory to clean (default: current working directory)\n  -a, --age <days>       Files older than this many days will be targeted (default: 30)\n  -n, --dry-run          Only list files, do not move or delete them\n  -c, --compost <path>   Move old files to this directory instead of deleting them\n  -r, --recursive        Scan subdirectories recursively\n  -h, --help             Display this help message\n            `);
            process.exit(0);
        } else {
            console.error(`Unknown argument: ${arg}`);
            process.exit(1);
        }
    }

    if (!directory) {
        console.error('Error: Directory not specified. Use --dir or -d.');
        process.exit(1);
    }

    cleanHoard(directory, ageDays, dryRun, compostDir, recursive)
        .catch(err => {
            console.error('\nAn unexpected error occurred:', err);
            process.exit(1);
        });
}

module.exports = { cleanHoard, getFilesOlderThan }; // Export for testing
