#!/usr/bin/env node
const { findDigitalEchoes, archiveEcho } = require('./index');
const path = require('path');

async function main() {
    const args = process.argv.slice(2);
    let targetDirectory = process.cwd();
    let thresholdDays = 90; // Default to 90 days
    let archiveMode = false;
    let archivePath = path.join(targetDirectory, '_digital_echoes_archive'); // Default relative to targetDirectory

    for (let i = 0; i < args.length; i++) {
        const arg = args[i];
        if (arg === '--dir' || arg === '-d') {
            targetDirectory = path.resolve(args[++i]); // Resolve target directory
        } else if (arg === '--age' || arg === '-a') {
            thresholdDays = parseInt(args[++i], 10);
            if (isNaN(thresholdDays) || thresholdDays <= 0) {
                console.error('Error: --age must be a positive number of days.');
                process.exit(1);
            }
        } else if (arg === '--archive' || arg === '-r') {
            archiveMode = true;
            if (args[i+1] && !args[i+1].startsWith('-')) { // Check if next arg is a path, not another flag
                archivePath = path.resolve(args[++i]); // Resolve provided archive path
            } else {
                // If --archive is present without a path, use the default relative to targetDirectory
                archivePath = path.join(targetDirectory, '_digital_echoes_archive');
            }
        } else if (arg === '--help' || arg === '-h') {
            console.log(`\nNightly Digital Echo Purifier\n\nUsage:\n  nightly-echo-purifier [options]\n\nOptions:\n  -d, --dir <path>      Directory to scan (default: current working directory)\n  -a, --age <days>      Files older than this many days are considered echoes (default: 90)\n  -r, --archive [path]  Move echoes to an archive directory. If path is not provided,\n                        defaults to '_digital_echoes_archive' in the target directory.\n  -h, --help            Show this help message\n            `);
            process.exit(0);
        } else {
            console.warn(`Unknown argument: ${arg}. Use --help for usage.`);
        }
    }

    console.log(`\nScanning for digital echoes in "${targetDirectory}" older than ${thresholdDays} days...`);

    const echoes = await findDigitalEchoes(targetDirectory, thresholdDays);

    if (echoes.length === 0) {
        console.log('No digital echoes found. Your digital space is pristine!');
        return;
    }

    console.log(`\nFound ${echoes.length} digital echoes:`);
    echoes.forEach(echo => console.log(`  - ${path.relative(targetDirectory, echo)}`));

    if (archiveMode) {
        console.log(`\nInitiating archive protocol to "${archivePath}"...`);
        let archivedCount = 0;
        for (const echo of echoes) {
            const success = await archiveEcho(echo, archivePath, targetDirectory);
            if (success) {
                archivedCount++;
            }
        }
        console.log(`\nSuccessfully archived ${archivedCount} of ${echoes.length} digital echoes.`);
        if (archivedCount < echoes.length) {
            console.log('Some echoes could not be archived. Check the logs for details.');
        }
    } else {
        console.log('\nTo archive these echoes, run with the --archive flag.');
    }
}

if (require.main === module) {
    main().catch(console.error);
}
