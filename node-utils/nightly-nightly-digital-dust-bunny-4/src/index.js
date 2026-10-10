#!/usr/bin/env node

const { readdir, stat } = require('node:fs/promises');
const path = require('node:path');
const { program } = require('commander');

async function findDigitalDustBunnies(directoryPath, ageThresholdMs) {
    const dustBunnies = [];
    const now = Date.now();

    async function scan(currentPath) {
        let entries;
        try {
            entries = await readdir(currentPath, { withFileTypes: true });
        } catch (error) {
            console.error(`Error accessing directory ${currentPath}: ${error.message}`);
            return;
        }

        for (const entry of entries) {
            const fullPath = path.join(currentPath, entry.name);
            try {
                const fileStat = await stat(fullPath);
                if (entry.isDirectory()) {
                    await scan(fullPath); // Recurse into subdirectories
                } else if (entry.isFile()) {
                    // Use mtimeMs (modification time) as it's generally more indicative of "use" than atimeMs (access time)
                    // atimeMs can be updated by system processes without user interaction.
                    if (now - fileStat.mtimeMs > ageThresholdMs) {
                        dustBunnies.push({
                            path: fullPath,
                            modified: new Date(fileStat.mtimeMs).toISOString().split('T')[0]
                        });
                    }
                }
            } catch (error) {
                // Ignore errors for individual files/directories (e.g., permission denied)
                // console.warn(`Could not stat ${fullPath}: ${error.message}`);
            }
        }
    }

    await scan(directoryPath);
    return dustBunnies;
}

function parseAgeThreshold(age, unit) {
    const ageNum = parseInt(age, 10);
    if (isNaN(ageNum) || ageNum <= 0) {
        throw new Error('Age must be a positive number.');
    }

    let multiplier;
    switch (unit.toLowerCase()) {
        case 'days':
            multiplier = 24 * 60 * 60 * 1000; // milliseconds in a day
            break;
        case 'months':
            multiplier = 30 * 24 * 60 * 60 * 1000; // approximate milliseconds in a month
            break;
        case 'years':
            multiplier = 365 * 24 * 60 * 60 * 1000; // approximate milliseconds in a year
            break;
        default:
            throw new Error('Unit must be "days", "months", or "years".');
    }
    return ageNum * multiplier;
}

async function main() {
    program
        .name('nightly-digital-dust-bunny')
        .description('Sweeps directories for old, unused files (digital dust bunnies).')
        .requiredOption('-p, --path <directory>', 'The directory to scan for digital dust bunnies.')
        .option('-a, --age <number>', 'The age threshold (number). Files older than this will be reported.', '90')
        .option('-u, --unit <unit>', 'The unit for the age argument (days, months, years).', 'days')
        .parse(process.argv);

    const options = program.opts();
    const directoryPath = path.resolve(options.path); // Resolve to absolute path

    let ageThresholdMs;
    try {
        ageThresholdMs = parseAgeThreshold(options.age, options.unit);
    } catch (error) {
        console.error(`Error: ${error.message}`);
        program.help();
        process.exit(1);
    }

    console.log(`\n🔍 Sweeping for digital dust bunnies in: ${directoryPath}`);
    console.log(`   Threshold: older than ${options.age} ${options.unit}\n`);

    const dustBunnies = await findDigitalDustBunnies(directoryPath, ageThresholdMs);

    if (dustBunnies.length === 0) {
        console.log('✨ No digital dust bunnies found! Your digital space is sparkling clean.');
    } else {
        console.log('Found these digital dust bunnies:');
        dustBunnies.forEach(bunny => {
            console.log(`- ${bunny.path} (Last modified: ${bunny.modified})`);
        });
        console.log(`\nTotal: ${dustBunnies.length} digital dust bunnies found.`);
        console.log('Consider archiving or deleting these forgotten files to reclaim your digital space!');
    }
}

if (require.main === module) {
    main();
}

// Export for testing
module.exports = { findDigitalDustBunnies, parseAgeThreshold };
