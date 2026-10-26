#!/usr/bin/env node

const fs = require('fs/promises');
const path = require('path');

/**
 * Parses command-line arguments.
 * @param {string[]} args - The arguments array (e.g., process.argv).
 * @returns {object} An object containing parsed options.
 * @throws {Error} If an invalid argument or option is provided.
 */
function parseArgs(args) {
    const options = {
        dir: process.cwd(), // Default to current working directory
        ageDays: 90,        // Default age threshold
        action: 'list',     // Default action
        quarantineDir: path.join(process.cwd(), '.digital_attic'), // Default quarantine dir
        force: false        // Default force to false
    };

    for (let i = 2; i < args.length; i++) {
        const arg = args[i];
        switch (arg) {
            case '--dir':
                options.dir = args[++i];
                if (!options.dir) throw new Error('Missing value for --dir.');
                break;
            case '--age':
                options.ageDays = parseInt(args[++i], 10);
                if (isNaN(options.ageDays) || options.ageDays <= 0) {
                    throw new Error('Invalid --age. Must be a positive number of days.');
                }
                break;
            case '--action':
                const action = args[++i];
                if (!['list', 'quarantine', 'delete'].includes(action)) {
                    throw new Error('Invalid --action. Must be one of: list, quarantine, delete.');
                }
                options.action = action;
                break;
            case '--quarantine-dir':
                options.quarantineDir = args[++i];
                if (!options.quarantineDir) throw new Error('Missing value for --quarantine-dir.');
                break;
            case '--force':
                options.force = true;
                break;
            case '-h':
            case '--help':
                console.log(`
Digital Dust Bunny Sweeper - Sweep away old, unused files!

Usage:
  node src/index.js [options]

Options:
  --dir <path>             Directory to scan (default: current working directory)
  --age <days>             Files older than this many days are considered dust bunnies (default: 90)
  --action <list|quarantine|delete>
                           Action to perform:
                           - list: Just list the dust bunnies (default)
                           - quarantine: Move them to a digital attic
                           - delete: Permanently delete them (use with caution!)
  --quarantine-dir <path>  Directory for quarantining files (default: ./.digital_attic)
  --force                  Skip confirmation for 'delete' action.
  -h, --help               Display this help message.

Examples:
  node src/index.js --dir ~/Downloads --age 180 --action list
  node src/index.js --dir ~/Projects/old --action quarantine
  node src/index.js --dir /tmp --age 7 --action delete --force
                `);
                process.exit(0);
            default:
                throw new Error(`Unknown argument: ${arg}`);
        }
    }

    if (options.action === 'delete' && !options.force) {
        throw new Error("Deletion requires --force flag for safety. No digital dust bunnies will be deleted without explicit confirmation.");
    }

    return options;
}

/**
 * Main function to execute the Digital Dust Bunny Sweeper.
 */
async function main() {
    let options;
    try {
        options = parseArgs(process.argv);
    } catch (err) {
        console.error('Argument Error:', err.message);
        console.log('Use --help for usage information.');
        process.exit(1);
    }

    const { dir, ageDays, action, quarantineDir, force } = options;

    const now = Date.now();
    const thresholdMs = ageDays * 24 * 60 * 60 * 1000;

    const filesToProcess = [];

    /**
     * Recursively scans a directory for old files.
     * @param {string} currentDir - The directory to scan.
     */
    async function scanDirectory(currentDir) {
        try {
            const entries = await fs.readdir(currentDir, { withFileTypes: true });

            for (const entry of entries) {
                const fullPath = path.join(currentDir, entry.name);
                if (entry.isDirectory()) {
                    // Skip the quarantine directory if it's within the scanned path
                    if (fullPath === quarantineDir) {
                        continue;
                    }
                    await scanDirectory(fullPath);
                } else if (entry.isFile()) {
                    const stats = await fs.stat(fullPath);
                    if (now - stats.mtimeMs > thresholdMs) {
                        filesToProcess.push({
                            path: fullPath,
                            size: stats.size,
                            mtimeMs: stats.mtimeMs
                        });
                    }
                }
            }
        } catch (err) {
            if (err.code === 'ENOENT') {
                console.error(`Warning: Directory not found or accessible: '${currentDir}'. Skipping.`);
            } else if (err.code === 'EACCES') {
                console.error(`Warning: Permission denied for directory: '${currentDir}'. Skipping.`);
            } else {
                throw err; // Re-throw other errors
            }
        }
    }

    console.log(`
Starting digital dust bunny sweep in '${dir}' for files older than ${ageDays} days...`);
    await scanDirectory(dir);

    if (filesToProcess.length === 0) {
        console.log(`
✨ Your digital space is sparkling! No dust bunnies found older than ${ageDays} days in '${dir}'.`);
        return;
    }

    console.log(`
Found ${filesToProcess.length} digital dust bunnies older than ${ageDays} days:`);
    filesToProcess.forEach(file => {
        console.log(`- ${file.path} (Size: ${file.size} bytes, Last Modified: ${new Date(file.mtimeMs).toLocaleDateString()})`);
    });

    if (action === 'list') {
        console.log('\n🧹 Use --action quarantine or --action delete to sweep them away!');
    } else if (action === 'quarantine') {
        console.log(`\nMoving ${filesToProcess.length} dust bunnies to digital attic: '${quarantineDir}'...`);
        try {
            await fs.mkdir(quarantineDir, { recursive: true });
            let movedCount = 0;
            for (const file of filesToProcess) {
                const newPath = path.join(quarantineDir, path.basename(file.path));
                await fs.rename(file.path, newPath);
                movedCount++;
            }
            console.log(`Moved ${movedCount} dust bunny(ies) to digital attic. They're safe there!`);
        } catch (err) {
            console.error('Failed to quarantine files:', err.message);
            process.exit(1);
        }
    } else if (action === 'delete') {
        console.log(`\nPermanently sweeping away ${filesToProcess.length} dust bunnies...`);
        try {
            let deletedCount = 0;
            for (const file of filesToProcess) {
                await fs.unlink(file.path);
                deletedCount++;
            }
            console.log(`Swept away ${deletedCount} dust bunny(ies) forever! Your digital space is cleaner.`);
        } catch (err) {
            console.error('Failed to delete files:', err.message);
            process.exit(1);
        }
    }
}

// Only run main if this script is executed directly
if (require.main === module) {
    main().catch(err => {
        console.error('An apocalyptic error occurred:', err.message);
        process.exit(1);
    });
}

// Export for testing
module.exports = { main, parseArgs };
