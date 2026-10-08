#!/usr/bin/env node

const { promises: fs } = require('fs');
const path = require('path');
const { program } = require('commander');

/**
 * Recursively finds files in a directory that are older than a specified age.
 * @param {string} directory The root directory to scan.
 * @param {number} ageDays The minimum age in days for a file to be considered old.
 * @returns {Promise<Array<{path: string, mtime: Date}>>} A promise that resolves to an array of old file objects.
 */
async function getFilesOlderThan(directory, ageDays) {
    const now = Date.now();
    const thresholdMs = ageDays * 24 * 60 * 60 * 1000;
    const oldFiles = [];

    async function traverse(currentPath) {
        let entries;
        try {
            entries = await fs.readdir(currentPath, { withFileTypes: true });
        } catch (error) {
            console.error(`ApocalypsAI: Cannot access directory ${currentPath}. Skipping.`, error.message);
            return;
        }

        for (const entry of entries) {
            const fullPath = path.join(currentPath, entry.name);
            if (entry.isDirectory()) {
                await traverse(fullPath);
            } else if (entry.isFile()) {
                let stats;
                try {
                    stats = await fs.stat(fullPath);
                } catch (error) {
                    console.error(`ApocalypsAI: Cannot stat file ${fullPath}. Skipping.`, error.message);
                    continue;
                }

                if (now - stats.mtimeMs > thresholdMs) {
                    oldFiles.push({
                        path: fullPath,
                        mtime: new Date(stats.mtimeMs)
                    });
                }
            }
        }
    }

    await traverse(directory);
    return oldFiles;
}

/**
 * Moves a file from a source path to a destination directory.
 * @param {string} sourcePath The full path of the file to move.
 * @param {string} destinationDir The target directory for the file.
 * @returns {Promise<string>} A promise that resolves to a status message.
 */
async function moveFile(sourcePath, destinationDir) {
    const fileName = path.basename(sourcePath);
    const destinationPath = path.join(destinationDir, fileName);
    try {
        await fs.mkdir(destinationDir, { recursive: true });
        await fs.rename(sourcePath, destinationPath);
        return `Rehomed digital echo: ${sourcePath} -> ${destinationPath}`;
    } catch (error) {
        return `Failed to rehome digital echo ${sourcePath}: ${error.message}`;
    }
}

/**
 * Main function to parse CLI arguments and run the sweeper logic.
 */
async function main() {
    program
        .name('nightly-digital-echo-sweeper')
        .description('Scans specified directories for old, unused files (digital echoes) and suggests archiving them to a designated "temporal stasis" folder.')
        .version('1.0.0')
        .option('-s, --source <path>', 'Source directory to scan for digital echoes', process.cwd())
        .option('-a, --age <days>', 'Minimum age in days for a file to be considered an echo', '30')
        .option('-t, --target <path>', 'Target directory for temporal stasis (archiving)', path.join(process.cwd(), 'temporal_stasis_archive'))
        .option('-m, --move', 'Execute the rehoming (move files) instead of just listing suggestions', false)
        .parse(process.argv);

    const options = program.opts();
    const sourceDir = path.resolve(options.source);
    const ageDays = parseInt(options.age, 10);
    const targetDir = path.resolve(options.target);
    const executeMove = options.move;

    if (isNaN(ageDays) || ageDays < 0) {
        console.error('Error: Age must be a non-negative number of days.');
        process.exit(1);
    }

    console.log(`ApocalypsAI Digital Echo Sweeper initiated.`);
    console.log(`Scanning for digital echoes older than ${ageDays} days in: ${sourceDir}`);
    console.log(`Temporal stasis target: ${targetDir}`);
    if (executeMove) {
        console.log(`Rehoming mode: ACTIVATED. Files will be moved.`);
    } else {
        console.log(`Suggestion mode: ACTIVATED. Files will NOT be moved.`);
    }

    const oldFiles = await getFilesOlderThan(sourceDir, ageDays);

    if (oldFiles.length === 0) {
        console.log('No digital echoes detected. Your digital realm is pristine!');
        return;
    }

    console.log(`\nDetected ${oldFiles.length} digital echoes:`);
    for (const file of oldFiles) {
        console.log(`- ${file.path} (Last modified: ${file.mtime.toISOString().split('T')[0]})`);
    }

    if (executeMove) {
        console.log('\nInitiating rehoming sequence...');
        const results = await Promise.all(oldFiles.map(file => moveFile(file.path, targetDir)));
        results.forEach(result => console.log(result));
        console.log('Rehoming sequence complete.');
    } else {
        console.log(`\nTo rehome these digital echoes to temporal stasis, run with the --move flag.`);
    }
}

// Only run main if this script is executed directly
if (require.main === module) {
    main().catch(error => {
        console.error('An unexpected temporal anomaly occurred:', error);
        process.exit(1);
    });
}

// Export for testing purposes
module.exports = { getFilesOlderThan, moveFile };
