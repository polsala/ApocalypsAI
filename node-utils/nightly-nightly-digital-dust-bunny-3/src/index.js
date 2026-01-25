const fs = require('fs');
const path = require('path');

// Helper to parse command line arguments
function parseArgs(args) {
    const options = {
        recursive: true, // Default to recursive
        action: 'list'   // Default action
    };
    let dirToScan = null;

    for (let i = 2; i < args.length; i++) {
        const arg = args[i];
        const nextArg = args[i + 1];

        switch (arg) {
            case '-a':
            case '--age':
                options.ageDays = parseInt(nextArg, 10);
                i++;
                break;
            case '-s':
            case '--size-gt':
                options.sizeGtBytes = parseInt(nextArg, 10);
                i++;
                break;
            case '-p':
            case '--pattern':
                options.pattern = new RegExp(nextArg);
                i++;
                break;
            case '-q':
            case '--quarantine':
                options.quarantinePath = nextArg;
                options.action = 'quarantine';
                i++;
                break;
            case '-d':
            case '--delete':
                options.action = 'delete';
                break;
            case '-r':
            case '--recursive':
                options.recursive = true;
                break;
            case '-h':
            case '--help':
                printHelp();
                process.exit(0);
            default:
                if (!dirToScan) {
                    dirToScan = arg;
                } else {
                    console.warn(`Unknown argument or multiple directories specified: ${arg}. Ignoring.`);
                }
                break;
        }
    }

    if (!dirToScan) {
        console.error('Error: No directory to scan specified.');
        printHelp();
        process.exit(1);
    }

    if (options.quarantinePath && !fs.existsSync(options.quarantinePath)) {
        console.error(`Error: Quarantine path does not exist: ${options.quarantinePath}`);
        process.exit(1);
    }

    return { dirToScan, options };
}

function printHelp() {
    console.log(`\nUsage: node src/index.js <directory_to_scan> [options]\n\nA Node.js utility to sweep and manage old, unused 'digital dust bunny' files.\n\nArguments:\n  <directory_to_scan>  The root directory to start scanning from. Required.\n\nOptions:\n  -a, --age <days>       Files older than <days> will be considered dust bunnies.\n  -s, --size-gt <bytes>  Files larger than <bytes> will be considered dust bunnies.\n  -p, --pattern <regex>  Files whose names match the <regex> will be considered dust bunnies.\n  -q, --quarantine <path> Move identified dust bunnies to the specified <path>.\n                         The path must exist. Implies --action quarantine.\n  -d, --delete           Permanently delete identified dust bunnies. Use with caution!\n                         Implies --action delete.\n  -r, --recursive        Scan directories recursively. (Default: true)\n  -h, --help             Display help information.\n\nExamples:\n  node src/index.js . --age 7 --pattern "\\.tmp$"\n  node src/index.js /var/log --age 90 --pattern "\\.log$" --quarantine /tmp/dust-bunnies\n  node src/index.js ~/Downloads --size-gt 524288000 --age 180 --delete\n`);
}

/**
 * Scans a directory for files matching the given criteria.
 * @param {string} currentDir The directory to scan.
 * @param {object} options Scanning options (ageDays, sizeGtBytes, pattern, recursive).
 * @param {Array<string>} dustBunnies Accumulator for identified files.
 */
function scanDirectory(currentDir, options, dustBunnies = []) {
    if (!fs.existsSync(currentDir)) {
        console.warn(`Warning: Directory not found: ${currentDir}. Skipping.`);
        return dustBunnies;
    }

    const files = fs.readdirSync(currentDir);
    const now = Date.now();

    for (const file of files) {
        const filePath = path.join(currentDir, file);
        let stats;
        try {
            stats = fs.statSync(filePath);
        } catch (e) {
            console.warn(`Warning: Could not stat file ${filePath}. Skipping. Error: ${e.message}`);
            continue;
        }

        if (stats.isDirectory()) {
            if (options.recursive) {
                scanDirectory(filePath, options, dustBunnies);
            }
        } else if (stats.isFile()) {
            let isDustBunny = true;

            // Check age
            if (options.ageDays !== undefined) {
                const fileAgeMs = now - stats.mtimeMs;
                const ageThresholdMs = options.ageDays * 24 * 60 * 60 * 1000;
                if (fileAgeMs < ageThresholdMs) {
                    isDustBunny = false;
                }
            }

            // Check size
            if (isDustBunny && options.sizeGtBytes !== undefined) {
                if (stats.size <= options.sizeGtBytes) {
                    isDustBunny = false;
                }
            }

            // Check pattern
            if (isDustBunny && options.pattern) {
                if (!options.pattern.test(file)) {
                    isDustBunny = false;
                }
            }

            if (isDustBunny) {
                dustBunnies.push(filePath);
            }
        }
    }
    return dustBunnies;
}

/**
 * Processes the identified dust bunnies based on the action.
 * @param {Array<string>} files The list of file paths to process.
 * @param {string} action The action to perform ('list', 'quarantine', 'delete').
 * @param {string} [quarantinePath] The path to move files to if action is 'quarantine'.
 */
function processDustBunnies(files, action, quarantinePath) {
    console.log(`\n--- Digital Lint Trap Report (${action.toUpperCase()}) ---\n`);

    if (files.length === 0) {
        console.log('No digital dust bunnies found. Your system is sparkling clean!');
        return;
    }

    console.log(`Found ${files.length} digital dust bunnies:\n`);

    for (const filePath of files) {
        const fileName = path.basename(filePath);
        switch (action) {
            case 'list':
                console.log(`  - ${filePath}`);
                break;
            case 'quarantine':
                const newPath = path.join(quarantinePath, fileName);
                try {
                    fs.renameSync(filePath, newPath);
                    console.log(`  - Moved '${filePath}' to '${newPath}'`);
                } catch (e) {
                    console.error(`  - Failed to move '${filePath}': ${e.message}`);
                }
                break;
            case 'delete':
                try {
                    fs.unlinkSync(filePath);
                    console.log(`  - Deleted '${filePath}'`);
                } catch (e) {
                    console.error(`  - Failed to delete '${filePath}': ${e.message}`);
                }
                break;
        }
    }
    console.log('\n--- Report End ---');
}

// Main execution
if (require.main === module) {
    const { dirToScan, options } = parseArgs(process.argv);

    console.log(`Scanning '${dirToScan}' for digital dust bunnies...`);
    const dustBunnies = scanDirectory(dirToScan, options);

    processDustBunnies(dustBunnies, options.action, options.quarantinePath);
}

// Export for testing
module.exports = {
    parseArgs,
    scanDirectory,
    processDustBunnies,
    printHelp // Export for testing help output
};
