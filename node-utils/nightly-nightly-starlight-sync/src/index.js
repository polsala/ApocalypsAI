const fs = require('fs');
const path = require('path');

function parseDuration(durationStr) {
    const match = durationStr.match(/^(\d+)([hmd])$/);
    if (!match) {
        throw new Error('Invalid duration format. Use e.g., "24h", "7d", "30m".');
    }
    const value = parseInt(match[1], 10);
    const unit = match[2];

    switch (unit) {
        case 'm': return value * 60 * 1000; // milliseconds
        case 'h': return value * 60 * 60 * 1000;
        case 'd': return value * 24 * 60 * 60 * 1000;
        default: throw new Error('Unknown duration unit.');
    }
}

function getRandomDateInRange(baseDate, rangeMs) {
    const baseTime = baseDate.getTime();
    const randomOffset = Math.random() * rangeMs; // Offset from 0 to rangeMs
    return new Date(baseTime - randomOffset); // Subtract to go into the past
}

function synchronizeTimestamps(targetPath, baseDate, randomRangeMs, dryRun = false) {
    if (!fs.existsSync(targetPath)) {
        console.error(`Error: Path does not exist: ${targetPath}`);
        process.exit(1);
    }

    const filesToProcess = [];

    function walk(currentDir) {
        const entries = fs.readdirSync(currentDir, { withFileTypes: true });
        for (const entry of entries) {
            const fullPath = path.join(currentDir, entry.name);
            filesToProcess.push(fullPath);
            if (entry.isDirectory()) {
                walk(fullPath);
            }
        }
    }

    // Add the targetPath itself to the list to update its timestamp too
    filesToProcess.push(targetPath);
    walk(targetPath);

    console.log(`Starlight Synchronizer initiated for: ${targetPath}`);
    if (dryRun) {
        console.log("--- DRY RUN MODE --- No files will be modified.");
    }

    for (const filePath of filesToProcess) {
        let newDate;
        if (randomRangeMs > 0) {
            newDate = getRandomDateInRange(baseDate, randomRangeMs);
        } else {
            newDate = baseDate;
        }

        if (dryRun) {
            console.log(`[DRY RUN] Would set ${filePath} to ${newDate.toISOString()}`);
        } else {
            try {
                // Node.js fs.utimesSync expects Date objects or milliseconds since epoch for atime and mtime
                fs.utimesSync(filePath, newDate, newDate);
                console.log(`Synchronized ${filePath} to ${newDate.toISOString()}`);
            } catch (error) {
                console.error(`Failed to synchronize ${filePath}: ${error.message}`);
            }
        }
    }

    console.log("Starlight Synchronization complete.");
}

function main(args) {
    const targetPath = args[0];
    if (!targetPath) {
        console.error('Usage: node src/index.js <path> [--date <YYYY-MM-DDTHH:MM:SSZ>] [--random-range <duration>] [--dry-run]');
        process.exit(1);
    }

    let baseDate = new Date(); // Default to current time
    let randomRangeMs = 0;
    let dryRun = false;

    for (let i = 1; i < args.length; i++) {
        const arg = args[i];
        if (arg === '--date') {
            const dateStr = args[++i];
            if (!dateStr) {
                console.error('Error: --date requires a value.');
                process.exit(1);
            }
            try {
                baseDate = new Date(dateStr);
                if (isNaN(baseDate.getTime())) {
                    throw new Error('Invalid date format.');
                }
            } catch (e) {
                console.error(`Error: Invalid date format for --date: ${dateStr}. Please use ISO 8601.`);
                process.exit(1);
            }
        } else if (arg === '--random-range') {
            const rangeStr = args[++i];
            if (!rangeStr) {
                console.error('Error: --random-range requires a value.');
                process.exit(1);
            }
            try {
                randomRangeMs = parseDuration(rangeStr);
            } catch (e) {
                console.error(`Error: ${e.message}`);
                process.exit(1);
            }
        } else if (arg === '--dry-run') {
            dryRun = true;
        } else {
            console.error(`Error: Unknown argument: ${arg}`);
            process.exit(1);
        }
    }

    synchronizeTimestamps(targetPath, baseDate, randomRangeMs, dryRun);
}

// Only run main if this script is executed directly
if (require.main === module) {
    main(process.argv.slice(2));
}

// Export for testing
module.exports = {
    synchronizeTimestamps,
    parseDuration,
    getRandomDateInRange,
    main // Export main for testing argument parsing
};
