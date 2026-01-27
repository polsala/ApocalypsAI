const fs = require('fs').promises;
const path = require('path');

async function getFileStats(filePath) {
    try {
        return await fs.stat(filePath);
    } catch (error) {
        // Ignore files we can't access
        return null;
    }
}

function classifyDustiness(mtimeMs, thresholdDays) {
    const now = Date.now();
    const ageMs = now - mtimeMs;
    const ageDays = ageMs / (1000 * 60 * 60 * 24);

    if (ageDays > thresholdDays * 3) {
        return 'Ancient Relic (very dusty)';
    } else if (ageDays > thresholdDays) {
        return 'Very Dusty';
    } else if (ageDays > thresholdDays / 2) {
        return 'Mildly Dusty';
    }
    return 'Fresh (not dusty)';
}

async function sweepDustBunnies(directoryPath, thresholdDays) {
    const dustBunnies = [];
    const filesToScan = [directoryPath];

    while (filesToScan.length > 0) {
        const currentPath = filesToScan.shift();
        let entries;
        try {
            entries = await fs.readdir(currentPath, { withFileTypes: true });
        } catch (error) {
            console.warn(`Warning: Could not read directory ${currentPath}. Skipping.`);
            continue;
        }

        for (const entry of entries) {
            const fullPath = path.join(currentPath, entry.name);
            if (entry.isDirectory()) {
                filesToScan.push(fullPath);
            } else if (entry.isFile()) {
                const stats = await getFileStats(fullPath);
                if (stats) {
                    const dustiness = classifyDustiness(stats.mtimeMs, thresholdDays);
                    if (dustiness !== 'Fresh (not dusty)') {
                        dustBunnies.push({
                            path: fullPath,
                            mtime: new Date(stats.mtimeMs).toISOString().split('T')[0],
                            dustiness: dustiness
                        });
                    }
                }
            }
        }
    }
    return dustBunnies;
}

async function runCli() {
    const args = process.argv.slice(2);
    const directoryPath = args[0] || '.';
    const thresholdDays = parseInt(args[1], 10) || 90; // Default to 90 days

    console.log(`\nSweeping for Temporal Dust Bunnies in: ${directoryPath}`);
    console.log(`Threshold for 'Mildly Dusty': ${thresholdDays / 2} days`);
    console.log(`Threshold for 'Very Dusty': ${thresholdDays} days`);
    console.log(`Threshold for 'Ancient Relic': ${thresholdDays * 3} days\n`);

    const bunnies = await sweepDustBunnies(directoryPath, thresholdDays);

    if (bunnies.length === 0) {
        console.log('✨ No temporal dust bunnies found! Your directory is sparkling clean. ✨');
    } else {
        console.log('Found these temporal dust bunnies:');
        bunnies.sort((a, b) => {
            // Sort by dustiness (Ancient Relic first) then path
            const dustinessOrder = {
                'Ancient Relic (very dusty)': 3,
                'Very Dusty': 2,
                'Mildly Dusty': 1,
                'Fresh (not dusty)': 0
            };
            const orderDiff = dustinessOrder[b.dustiness] - dustinessOrder[a.dustiness];
            if (orderDiff !== 0) return orderDiff;
            return a.path.localeCompare(b.path);
        }).forEach(bunny => {
            console.log(`- [${bunny.dustiness}] ${bunny.path} (Last Modified: ${bunny.mtime})`);
        });
        console.log('\nConsider tidying these forgotten files!');
    }
}

// If run directly, execute the CLI function
if (require.main === module) {
    runCli().catch(console.error);
}

module.exports = { sweepDustBunnies, classifyDustiness };
