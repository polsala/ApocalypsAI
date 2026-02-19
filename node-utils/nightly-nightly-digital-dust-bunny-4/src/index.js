#!/usr/bin/env node
const { program } = require('commander');
const { readdir, stat } = require('fs/promises');
const { join, extname } = require('path');

async function findDustBunnies(dir, options) {
    const { ageDays, minSizeKB, whimsyPatterns } = options;
    
    // Only set cutoffTime if ageDays is provided and valid
    const cutoffTime = ageDays && !isNaN(ageDays) ? Date.now() - ageDays * 24 * 60 * 60 * 1000 : null;
    // Only set minSizeBytes if minSizeKB is provided and valid
    const minSizeBytes = minSizeKB && !isNaN(minSizeKB) ? minSizeKB * 1024 : null;
    const patterns = whimsyPatterns ? whimsyPatterns.split(',').map(p => new RegExp(p.trim(), 'i')) : [];

    let dustBunnies = [];

    async function scanDirectory(currentPath) {
        try {
            const entries = await readdir(currentPath, { withFileTypes: true });
            for (const entry of entries) {
                const fullPath = join(currentPath, entry.name);
                if (entry.isDirectory()) {
                    await scanDirectory(fullPath);
                } else if (entry.isFile()) {
                    const stats = await stat(fullPath);
                    
                    const isOld = cutoffTime !== null && stats.mtimeMs < cutoffTime;
                    const isLarge = minSizeBytes !== null && stats.size >= minSizeBytes;
                    const isWhimsical = patterns.length > 0 && patterns.some(pattern => pattern.test(entry.name) || pattern.test(extname(entry.name)));

                    if (isOld || isLarge || isWhimsical) {
                        dustBunnies.push({
                            path: fullPath,
                            size: stats.size,
                            mtime: new Date(stats.mtimeMs),
                            isOld,
                            isLarge,
                            isWhimsical
                        });
                    }
                }
            }
        } catch (error) {
            // In a real CLI, this would log to console. For testability, we might want to capture it.
            // For this self-contained utility, direct console.error is acceptable.
            // console.error(`Error scanning ${currentPath}: ${error.message}`);
        }
    }

    await scanDirectory(dir);
    return dustBunnies;
}

// Commander setup for CLI
program
    .name('dust-bunny')
    .description('A Node.js CLI tool to sweep digital dust bunnies (old, large, or whimsical files).')
    .argument('<directory>', 'The directory to scan for digital clutter.')
    .option('-a, --age <days>', 'Files older than this many days (based on modification time).', parseInt)
    .option('-s, --min-size <kb>', 'Files larger than this many kilobytes.', parseInt)
    .option('-w, --whimsy-patterns <patterns>', 'Comma-separated regex patterns for whimsical file names/extensions (e.g., "log,tmp,bak,DS_Store").')
    .option('-d, --dry-run', 'Perform a dry run without suggesting deletion, just list files.')
    .action(async (directory, options) => {
        console.log(`\nScanning "${directory}" for digital dust bunnies...`);
        console.log('Options:', options);

        const dustBunnies = await findDustBunnies(directory, options);

        if (dustBunnies.length === 0) {
            console.log('\n✨ No digital dust bunnies found! Your directory is sparkling clean. ✨');
            return;
        }

        console.log(`\nFound ${dustBunnies.length} potential dust bunnies:\n`);
        dustBunnies.forEach(bunny => {
            let reasons = [];
            if (bunny.isOld) reasons.push('OLD');
            if (bunny.isLarge) reasons.push('LARGE');
            if (bunny.isWhimsical) reasons.push('WHIMSICAL');
            console.log(`- ${bunny.path}`);
            console.log(`  Size: ${(bunny.size / 1024 / 1024).toFixed(2)} MB, Modified: ${bunny.mtime.toLocaleDateString()} ${bunny.mtime.toLocaleTimeString()}`);
            console.log(`  Reasons: [${reasons.join(', ')}]\n`);
        });

        if (!options.dryRun) {
            console.log('\nTo remove these files, consider using `rm` or `git clean -fdx` with caution.');
            console.log('Always review files before deletion!');
        } else {
            console.log('\n(Dry run complete. No files were suggested for deletion.)');
        }
    });

// Export for testing, but only run CLI when executed directly
if (require.main === module) {
    program.parse(process.argv);
} else {
    module.exports = { findDustBunnies };
}
