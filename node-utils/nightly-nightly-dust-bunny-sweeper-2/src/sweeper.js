const fs = require('fs');
const path = require('path');

/**
 * Parses command-line arguments.
 * @returns {object} An object containing parsed arguments.
 */
function parseArgs() {
    const args = {};
    for (let i = 2; i < process.argv.length; i++) {
        const arg = process.argv[i];
        if (arg.startsWith('--')) {
            const key = arg.substring(2);
            const nextArg = process.argv[i + 1];
            if (nextArg && !nextArg.startsWith('--')) {
                args[key] = nextArg;
                i++;
            } else {
                args[key] = true; // Flag argument
            }
        }
    }
    return args;
}

/**
 * Sweeps old files from a directory into an archive.
 * @param {string} rootPath The directory to sweep.
 * @param {number} ageDays Files older than this many days will be swept.
 * @param {string[]} targetExtensions Array of file extensions to target (e.g., ['.log', '.tmp']).
 * @param {boolean} dryRun If true, only reports actions without performing them.
 * @param {string} archiveDir The directory to move swept files to.
 * @returns {object} An object containing lists of swept and skipped files.
 */
function sweepDirectory(rootPath, ageDays, targetExtensions, dryRun, archiveDir) {
    const sweptFiles = [];
    const skippedFiles = [];
    const now = Date.now();
    const ageMillis = ageDays * 24 * 60 * 60 * 1000;

    if (!fs.existsSync(rootPath)) {
        console.error(`Error: Path does not exist: ${rootPath}`);
        return { sweptFiles, skippedFiles };
    }

    // Ensure archive directory exists
    if (!fs.existsSync(archiveDir)) {
        if (!dryRun) {
            fs.mkdirSync(archiveDir, { recursive: true });
            console.log(`Created archive directory: ${archiveDir}`);
        } else {
            console.log(`[DRY RUN] Would create archive directory: ${archiveDir}`);
        }
    }

    function scanDir(currentPath) {
        const entries = fs.readdirSync(currentPath, { withFileTypes: true });

        for (const entry of entries) {
            const fullPath = path.join(currentPath, entry.name);
            if (entry.isDirectory()) {
                // Skip the archive directory itself or any of its subdirectories
                if (fullPath === archiveDir || fullPath.startsWith(archiveDir + path.sep)) {
                    continue;
                }
                scanDir(fullPath);
            } else if (entry.isFile()) {
                try {
                    const stats = fs.statSync(fullPath);
                    const fileAge = now - stats.mtimeMs;
                    const fileExtension = path.extname(entry.name).toLowerCase();

                    const isOldEnough = fileAge > ageMillis;
                    const isTargetExtension = targetExtensions.length === 0 || targetExtensions.includes(fileExtension);

                    if (isOldEnough && isTargetExtension) {
                        const destPath = path.join(archiveDir, entry.name);
                        if (dryRun) {
                            console.log(`[DRY RUN] Would sweep: ${fullPath} -> ${destPath}`);
                            sweptFiles.push(fullPath);
                        } else {
                            fs.renameSync(fullPath, destPath);
                            console.log(`Swept: ${fullPath} -> ${destPath}`);
                            sweptFiles.push(fullPath);
                        }
                    } else {
                        skippedFiles.push(fullPath);
                    }
                } catch (error) {
                    console.error(`Error processing file ${fullPath}: ${error.message}`);
                    skippedFiles.push(fullPath);
                }
            }
        }
    }

    scanDir(rootPath);
    return { sweptFiles, skippedFiles };
}

// Main execution block
if (require.main === module) {
    const args = parseArgs();

    const rootPath = args.path;
    if (!rootPath) {
        console.error('Error: --path argument is required.');
        process.exit(1);
    }

    const ageDays = parseInt(args.age || '30', 10);
    if (isNaN(ageDays) || ageDays <= 0) {
        console.error('Error: --age must be a positive number.');
        process.exit(1);
    }

    const targetExtensions = args.extensions ? args.extensions.split(',').map(ext => `.${ext.trim().toLowerCase()}`) : [];
    const dryRun = !!args['dry-run'];
    const defaultArchiveDir = path.join(rootPath, '.dustbunnies');
    const archiveDir = args['archive-dir'] ? path.resolve(args['archive-dir']) : defaultArchiveDir;

    console.log(`\n--- Digital Dust Bunny Sweeper ---`);
    console.log(`Scanning: ${rootPath}`);
    console.log(`Age threshold: ${ageDays} days`);
    console.log(`Target extensions: ${targetExtensions.length > 0 ? targetExtensions.join(', ') : 'All'}`);
    console.log(`Archive directory: ${archiveDir}`);
    console.log(`Mode: ${dryRun ? 'Dry Run' : 'Live Sweep'}\n`);

    const results = sweepDirectory(rootPath, ageDays, targetExtensions, dryRun, archiveDir);

    console.log(`\n--- Sweep Summary ---`);
    console.log(`Swept ${results.sweptFiles.length} files.`);
    if (results.sweptFiles.length > 0) {
        console.log('Swept files:\n' + results.sweptFiles.join('\n'));
    }
    console.log(`Skipped ${results.skippedFiles.length} files.`);
    if (results.skippedFiles.length > 0) {
        console.log('Skipped files:\n' + results.skippedFiles.join('\n'));
    }
    console.log(`\n--- Sweep Complete ---`);
}

// Export for testing
module.exports = { sweepDirectory };
