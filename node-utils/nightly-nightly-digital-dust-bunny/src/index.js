const fs = require('fs').promises;
const path = require('path');
const minimist = require('minimist');
const prompts = require('prompts');

async function findDustBunnies(directory, ageInDays) {
    const now = Date.now();
    const thresholdMs = ageInDays * 24 * 60 * 60 * 1000;
    const dustBunnies = [];

    async function scanDir(currentPath) {
        let entries;
        try {
            entries = await fs.readdir(currentPath, { withFileTypes: true });
        } catch (error) {
            console.error(`Error reading directory ${currentPath}: ${error.message}`);
            return;
        }

        for (const entry of entries) {
            const fullPath = path.join(currentPath, entry.name);
            if (entry.isDirectory()) {
                // Skip node_modules and other common ignored directories
                if (entry.name === 'node_modules' || entry.name === '.git' || entry.name === 'dist' || entry.name === 'build') {
                    continue;
                }
                await scanDir(fullPath);
            } else if (entry.isFile()) {
                let stats;
                try {
                    stats = await fs.stat(fullPath);
                } catch (error) {
                    console.error(`Error getting stats for file ${fullPath}: ${error.message}`);
                    continue;
                }

                if (now - stats.mtimeMs > thresholdMs) {
                    dustBunnies.push({
                        path: fullPath,
                        mtime: new Date(stats.mtimeMs).toLocaleString()
                    });
                }
            }
        }
    }

    await scanDir(directory);
    return dustBunnies;
}

async function sweepDustBunnies(dustBunnies, dryRun, autoYes) {
    if (dustBunnies.length === 0) {
        console.log('No digital dust bunnies found. Your space is sparkling clean!');
        return;
    }

    console.log(`Found ${dustBunnies.length} digital dust bunnies:`);
    dustBunnies.forEach(bunny => {
        console.log(`- ${bunny.path} (Last modified: ${bunny.mtime})`);
    });

    if (dryRun) {
        console.log('\nThis was a dry run. No files were deleted.');
        return;
    }

    if (!autoYes) {
        const response = await prompts({
            type: 'confirm',
            name: 'value',
            message: 'Do you want to sweep these dust bunnies away?',
            initial: false
        });

        if (!response.value) {
            console.log('Sweeping cancelled. The dust bunnies live to see another day.');
            return;
        }
    }

    console.log('\nSweeping away digital dust bunnies...');
    for (const bunny of dustBunnies) {
        try {
            await fs.unlink(bunny.path);
            console.log(`- Swept: ${bunny.path}`);
        } catch (error) {
            console.error(`- Failed to sweep ${bunny.path}: ${error.message}`);
        }
    }
    console.log('Digital dust bunnies swept! Your space is cleaner.');
}

async function main() {
    const argv = minimist(process.argv.slice(2));

    const directory = argv._[0];
    const ageInDays = parseInt(argv.a || argv.age || 30, 10);
    const dryRun = argv.d || argv['dry-run'] || false;
    const autoYes = argv.y || argv.yes || false;
    const showHelp = argv.h || argv.help || false;

    if (showHelp || !directory) {
        console.log(`\nUsage: node src/index.js <directory_path> [options]\n\nA Node.js CLI utility to sweep digital dust bunnies (old, unused files).\n\nOptions:\n  -a, --age <days>   Files older than this many days will be considered "dust bunnies". Default: 30.\n  -d, --dry-run      List files that would be deleted without actually deleting them.\n  -y, --yes          Automatically confirm deletion for all identified files (use with caution!).\n  -h, --help         Display this help message.\n        `);
        process.exit(0);
    }

    if (isNaN(ageInDays) || ageInDays <= 0) {
        console.error('Error: --age must be a positive number.');
        process.exit(1);
    }

    try {
        const dustBunnies = await findDustBunnies(directory, ageInDays);
        await sweepDustBunnies(dustBunnies, dryRun, autoYes);
    } catch (error) {
        console.error('An unexpected error occurred:', error.message);
        process.exit(1);
    }
}

if (require.main === module) {
    main();
}

// Export for testing
module.exports = { findDustBunnies, sweepDustBunnies };
