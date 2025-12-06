#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const yargs = require('yargs/yargs');
const { hideBin } = require('yargs/helpers');

// Function to parse age duration (e.g., "7d", "24h", "30m") into milliseconds
function parseDurationToMs(durationStr) {
    const match = durationStr.match(/^(\d+)([dhms])$/);
    if (!match) {
        throw new Error('Invalid age duration format. Use Nd (days), Nh (hours), Nm (minutes), Ns (seconds).');
    }
    const value = parseInt(match[1], 10);
    const unit = match[2];

    switch (unit) {
        case 'd': return value * 24 * 60 * 60 * 1000;
        case 'h': return value * 60 * 60 * 1000;
        case 'm': return value * 60 * 1000;
        case 's': return value * 1000;
        default: return 0; // Should not happen due to regex
    }
}

async function processFiles(directory, ageMs, action, archiveDir, verbose) {
    const now = Date.now();
    let processedCount = 0;
    const filesToProcess = [];

    if (!fs.existsSync(directory)) {
        console.error(`Error: Directory not found: ${directory}`);
        return;
    }

    if (action === 'archive' && !archiveDir) {
        console.error('Error: Archive directory (--output) is required for the archive command.');
        return;
    }

    if (action === 'archive' && !fs.existsSync(archiveDir)) {
        try {
            fs.mkdirSync(archiveDir, { recursive: true });
            console.log(`Created temporal archive directory: ${archiveDir}`);
        } catch (err) {
            console.error(`Error creating archive directory ${archiveDir}: ${err.message}`);
            return;
        }
    }

    try {
        const files = fs.readdirSync(directory);

        for (const file of files) {
            const filePath = path.join(directory, file);
            try {
                const stats = fs.statSync(filePath);
                if (stats.isFile()) {
                    const fileAge = now - stats.mtimeMs;
                    if (fileAge > ageMs) {
                        filesToProcess.push({ filePath, file });
                    }
                }
            } catch (err) {
                if (verbose) {
                    console.warn(`Warning: Could not stat file ${filePath}: ${err.message}`);
                }
            }
        }

        if (filesToProcess.length === 0) {
            console.log(`No temporal echoes found in '${directory}' older than the specified age.`);
            return;
        }

        console.log(`\nInitiating Chrono-Cleanse Protocol for '${directory}'...`);
        console.log(`Targeting files older than ${ageMs / (1000 * 60 * 60 * 24)} days (${ageMs}ms).`); // Simplified for display

        for (const { filePath, file } of filesToProcess) {
            switch (action) {
                case 'list':
                    console.log(`  [ECHO] ${filePath}`);
                    processedCount++; // Count listed files too
                    break;
                case 'archive':
                    const destPath = path.join(archiveDir, file);
                    try {
                        fs.renameSync(filePath, destPath);
                        console.log(`  [ARCHIVED] ${filePath} -> ${destPath}`);
                        processedCount++;
                    } catch (err) {
                        console.error(`  [ERROR] Failed to archive ${filePath}: ${err.message}`);
                    }
                    break;
                case 'delete':
                    try {
                        fs.unlinkSync(filePath);
                        console.log(`  [CLEANSED] ${filePath}`);
                        processedCount++;
                    } catch (err) {
                        console.error(`  [ERROR] Failed to delete ${filePath}: ${err.message}`);
                    }
                    break;
            }
        }

        console.log(`\nChrono-Cleanse complete. Total files ${action === 'list' ? 'identified' : 'processed'}: ${processedCount}.`);

    } catch (err) {
        console.error(`An error occurred during Chrono-Cleanse: ${err.message}`);
    }
}

// Export for testing
if (process.env.NODE_ENV === 'test') {
    module.exports = { parseDurationToMs, processFiles };
} else {
    yargs(hideBin(process.argv))
        .command('list <directory>', 'List files older than the specified age', (yargs) => {
            yargs.positional('directory', {
                describe: 'The directory to scan for temporal echoes.',
                type: 'string'
            });
        }, async (argv) => {
            try {
                const ageMs = parseDurationToMs(argv.age);
                await processFiles(argv.directory, ageMs, 'list', null, argv.verbose);
            } catch (e) {
                console.error(`Error: ${e.message}`);
            }
        })
        .command('archive <directory>', 'Archive files older than the specified age to an output directory', (yargs) => {
            yargs.positional('directory', {
                describe: 'The directory to scan for temporal echoes.',
                type: 'string'
            })
            .option('output', {
                alias: 'o',
                describe: 'The path to the temporal archive directory.',
                type: 'string',
                demandOption: true
            });
        }, async (argv) => {
            try {
                const ageMs = parseDurationToMs(argv.age);
                await processFiles(argv.directory, ageMs, 'archive', argv.output, argv.verbose);
            } catch (e) {
                console.error(`Error: ${e.message}`);
            }
        })
        .command('delete <directory>', 'Delete files older than the specified age', (yargs) => {
            yargs.positional('directory', {
                describe: 'The directory to scan for temporal echoes.',
                type: 'string'
            });
        }, async (argv) => {
            try {
                const ageMs = parseDurationToMs(argv.age);
                await processFiles(argv.directory, ageMs, 'delete', null, argv.verbose);
            } catch (e) {
                console.error(`Error: ${e.message}`);
            }
        })
        .option('age', {
            alias: 'a',
            describe: 'The age threshold for files. Format: Nd (days), Nh (hours), Nm (minutes), Ns (seconds).',
            type: 'string',
            demandOption: true
        })
        .option('verbose', {
            alias: 'v',
            describe: 'Show more detailed output.',
            type: 'boolean',
            default: false
        })
        .demandCommand(1, 'You need at least one command before moving on')
        .help()
        .argv;
}
