const path = require('path');

function createDustSweeper(fsModule) {
    const fs = fsModule || require('fs'); // Use provided fs or default

    /**
     * Calculates the age of a file in days based on its modification time.
     * @param {string} filePath - The path to the file.
     * @returns {number} The age of the file in days, or -1 if an error occurs.
     */
    function getFileAgeInDays(filePath) {
        try {
            const stats = fs.statSync(filePath);
            const now = new Date();
            const mtime = stats.mtime;
            const diffTime = Math.abs(now.getTime() - mtime.getTime());
            return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        } catch (error) {
            // File might not exist, or permissions issue
            return -1;
        }
    }

    /**
     * Scans a directory for files older than a specified age threshold.
     * @param {string} dirPath - The directory to scan.
     * @param {number} ageThresholdDays - The minimum age in days for a file to be considered 'dusty'.
     * @param {boolean} recursive - Whether to scan subdirectories recursively.
     * @returns {Array<Object>} An array of dusty files, each with its path and age.
     */
    function scanDirectory(dirPath, ageThresholdDays, recursive = false) {
        let dustyFiles = [];
        try {
            const entries = fs.readdirSync(dirPath, { withFileTypes: true });
            for (const entry of entries) {
                const fullPath = path.join(dirPath, entry.name);
                if (entry.isDirectory()) {
                    if (recursive) {
                        dustyFiles = dustyFiles.concat(scanDirectory(fullPath, ageThresholdDays, recursive));
                    }
                } else {
                    const age = getFileAgeInDays(fullPath);
                    if (age >= ageThresholdDays) {
                        dustyFiles.push({ path: fullPath, age: age });
                    }
                }
            }
        } catch (error) {
            console.error(`Error scanning directory ${dirPath}: ${error.message}`);
        }
        return dustyFiles;
    }

    /**
     * Moves a file to a specified 'digital attic' directory.
     * @param {string} filePath - The path to the file to move.
     * @param {string} atticPath - The destination directory for the file.
     * @returns {string} A message indicating the result of the move operation.
     */
    function moveFile(filePath, atticPath) {
        const fileName = path.basename(filePath);
        const destinationPath = path.join(atticPath, fileName);
        try {
            fs.mkdirSync(atticPath, { recursive: true });
            fs.renameSync(filePath, destinationPath);
            return `Moved '${filePath}' to '${destinationPath}' (the Digital Attic).`;
        } catch (error) {
            return `Failed to move '${filePath}': ${error.message}`;
        }
    }

    /**
     * Generates a whimsical suggestion for a dusty file.
     * @param {string} filePath - The path to the dusty file.
     * @returns {string} A whimsical suggestion.
     */
    function suggestAction(filePath) {
        const suggestions = [
            `Consider renaming '${filePath}' to '${path.basename(filePath)}.forgotten_by_time'`,
            `Perhaps archive '${filePath}' into a 'digital_dust_bunnies.zip'`, // This would require more complex logic to actually zip
            `Maybe give '${filePath}' a new purpose, or let it drift into the void.`, 
            `This file, '${filePath}', has achieved peak temporal resonance.`, 
            `The whispers of '${filePath}' suggest it's ready for a new home.`,
            `It seems '${filePath}' has been gathering digital dust. A new adventure awaits it?`
        ];
        return suggestions[Math.floor(Math.random() * suggestions.length)];
    }

    return {
        scanDirectory,
        moveFile,
        suggestAction,
        getFileAgeInDays // Export for testing
    };
}

// CLI entry point
if (require.main === module) {
    const { scanDirectory, moveFile, suggestAction } = createDustSweeper();
    const args = process.argv.slice(2);

    let targetDir = '.';
    let ageThreshold = 30; // Default 30 days
    let recursive = false;
    let atticDir = null;
    let dryRun = true;

    for (let i = 0; i < args.length; i++) {
        const arg = args[i];
        if (arg === '--dir' || arg === '-d') {
            targetDir = args[++i];
        } else if (arg === '--age' || arg === '-a') {
            ageThreshold = parseInt(args[++i], 10);
            if (isNaN(ageThreshold) || ageThreshold <= 0) {
                console.error('Error: --age must be a positive number.');
                process.exit(1);
            }
        } else if (arg === '--recursive' || arg === '-r') {
            recursive = true;
        } else if (arg === '--attic' || arg === '-t') {
            atticDir = args[++i];
            dryRun = false; // If attic is specified, it's not a dry run by default
        } else if (arg === '--execute' || arg === '-e') {
            dryRun = false; // Explicitly execute actions
        } else if (arg === '--help' || arg === '-h') {
            console.log(`\nNightly Digital Dust Sweeper\n\nUsage: node src/index.js [options]\n\nOptions:\n  -d, --dir <path>       Directory to scan (default: current directory)\n  -a, --age <days>       Minimum age in days for a file to be considered 'dusty' (default: 30)\n  -r, --recursive        Scan directories recursively\n  -t, --attic <path>     Move dusty files to this 'digital attic' directory. Implies --execute.\n  -e, --execute          Execute file operations (move to attic). By default, it's a dry run.\n  -h, --help             Display this help message\n            `);
            process.exit(0);
        }
    }

    if (!targetDir) {
        console.error('Error: Target directory must be specified with --dir.');
        process.exit(1);
    }

    console.log(`\nScanning '${targetDir}' for files older than ${ageThreshold} days (recursive: ${recursive})...\n`);

    const dustyFiles = scanDirectory(targetDir, ageThreshold, recursive);

    if (dustyFiles.length === 0) {
        console.log('No digital dust bunnies found! Your directories are sparkling clean.');
    } else {
        console.log(`Found ${dustyFiles.length} dusty files:\n`);
        for (const file of dustyFiles) {
            console.log(`- '${file.path}' (last modified ${file.age} days ago)`);
            if (atticDir && !dryRun) {
                console.log(`  ${moveFile(file.path, atticDir)}`);
            } else if (!dryRun) {
                // If --execute but no attic, just suggest
                console.log(`  Suggestion: ${suggestAction(file.path)}`);
            } else {
                console.log(`  (Dry run) Suggestion: ${suggestAction(file.path)}`);
            }
        }

        if (dryRun) {
            console.log('\nThis was a dry run. Use --execute or --attic <path> to perform actions.');
        } else if (atticDir) {
            console.log(`\nAll identified digital dust bunnies have been swept into the Digital Attic at '${atticDir}'.`);
        } else {
            console.log('\nActions suggested for identified digital dust bunnies.');
        }
    }
}
