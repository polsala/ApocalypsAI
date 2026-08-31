const fs = require('fs').promises;
const path = require('path');

async function getFileStats(filePath) {
    try {
        return await fs.stat(filePath);
    } catch (error) {
        if (error.code === 'ENOENT') {
            return null; // File/directory does not exist
        }
        throw error;
    }
}

async function isDirectoryEmpty(dirPath) {
    try {
        const files = await fs.readdir(dirPath);
        return files.length === 0;
    } catch (error) {
        if (error.code === 'ENOENT' || error.code === 'ENOTDIR') {
            return false; // Not a directory or doesn't exist
        }
        throw error;
    }
}

async function findDustBunnies(targetPath, options) {
    const { maxAgeDays = 30, sweep = false } = options;
    const dustBunnies = { emptyDirs: [], oldFiles: [] };
    const now = Date.now();
    const ageThresholdMs = maxAgeDays * 24 * 60 * 60 * 1000;

    async function scan(currentPath) {
        let entries;
        try {
            entries = await fs.readdir(currentPath, { withFileTypes: true });
        } catch (error) {
            console.warn(`ApocalypsAI: Cannot access ${currentPath}: ${error.message}`);
            return;
        }

        for (const entry of entries) {
            const fullPath = path.join(currentPath, entry.name);
            if (entry.isDirectory()) {
                await scan(fullPath); // Recurse first to check if it becomes empty
                if (await isDirectoryEmpty(fullPath)) {
                    dustBunnies.emptyDirs.push(fullPath);
                }
            } else if (entry.isFile()) {
                const stats = await getFileStats(fullPath);
                if (stats && (now - stats.mtime.getTime()) > ageThresholdMs) {
                    dustBunnies.oldFiles.push(fullPath);
                }
            }
        }
    }

    const initialStats = await getFileStats(targetPath);
    if (!initialStats || !initialStats.isDirectory()) {
        console.error(`ApocalypsAI: Target path "${targetPath}" is not a valid directory.`);
        return { emptyDirs: [], oldFiles: [] };
    }

    await scan(targetPath);

    if (sweep) {
        console.log("ApocalypsAI: Sweeping digital dust bunnies...");
        for (const dir of dustBunnies.emptyDirs) {
            try {
                await fs.rmdir(dir);
                console.log(`ApocalypsAI: Swept empty directory: ${dir}`);
            } catch (error) {
                console.error(`ApocalypsAI: Failed to sweep empty directory ${dir}: ${error.message}`);
            }
        }
        for (const file of dustBunnies.oldFiles) {
            try {
                await fs.unlink(file);
                console.log(`ApocalypsAI: Swept ancient file: ${file}`);
            } catch (error) {
                console.error(`ApocalypsAI: Failed to sweep ancient file ${file}: ${error.message}`);
            }
        }
    }

    return dustBunnies;
}

// CLI entry point
if (require.main === module) {
    const args = process.argv.slice(2);
    const targetPath = args[0];
    const sweep = args.includes('--sweep');
    const maxAgeIndex = args.indexOf('--max-age');
    const maxAgeDays = maxAgeIndex !== -1 && args[maxAgeIndex + 1] ? parseInt(args[maxAgeIndex + 1], 10) : 30;

    if (!targetPath) {
        console.error('Usage: node src/index.js <path> [--sweep] [--max-age <days>]');
        process.exit(1);
    }

    findDustBunnies(targetPath, { sweep, maxAgeDays })
        .then(result => {
            if (!sweep) {
                console.log('\n--- ApocalypsAI Digital Dust Bunny Report ---');
                console.log(`Scanning "${targetPath}" for digital dust bunnies older than ${maxAgeDays} days.`);
                console.log(`Found ${result.emptyDirs.length} empty directories:`);
                result.emptyDirs.forEach(dir => console.log(`  - ${dir}`));
                console.log(`Found ${result.oldFiles.length} ancient files:`);
                result.oldFiles.forEach(file => console.log(`  - ${file}`));
                if (result.emptyDirs.length === 0 && result.oldFiles.length === 0) {
                    console.log('No digital dust bunnies found. Your digital space is pristine!');
                } else {
                    console.log('\nTo sweep these dust bunnies away, run with the --sweep flag.');
                }
            }
        })
        .catch(error => {
            console.error('ApocalypsAI: An error occurred:', error.message);
            process.exit(1);
        });
}

module.exports = { findDustBunnies };
