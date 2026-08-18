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

async function ensureDirectoryExists(dirPath) {
    await fs.mkdir(dirPath, { recursive: true });
}

async function sweepDigitalDustBunnies(targetDir, sanctuaryDir, ageThresholdDays) {
    const now = Date.now();
    const thresholdMs = ageThresholdDays * 24 * 60 * 60 * 1000;
    let sweptCount = 0;
    let sweptSize = 0;
    const processedDirs = new Set(); // To track directories that might become empty

    await ensureDirectoryExists(sanctuaryDir);

    async function processDirectory(currentDir) {
        let entries;
        try {
            entries = await fs.readdir(currentDir, { withFileTypes: true });
        } catch (error) {
            if (error.code === 'ENOENT') {
                console.warn(`Target directory not found: ${currentDir}. Skipping.`);
                return;
            }
            console.error(`Error reading directory ${currentDir}: ${error.message}`);
            return;
        }

        for (const entry of entries) {
            const fullPath = path.join(currentDir, entry.name);
            if (entry.isDirectory()) {
                await processDirectory(fullPath);
                processedDirs.add(fullPath); // Mark for potential cleanup
            } else if (entry.isFile()) {
                const stats = await getFileStats(fullPath);
                if (stats && (now - stats.mtimeMs > thresholdMs)) { // Using mtime for modification time
                    const newPath = path.join(sanctuaryDir, entry.name);
                    try {
                        await fs.rename(fullPath, newPath);
                        sweptCount++;
                        sweptSize += stats.size;
                        console.log(`Swept: ${fullPath} -> ${newPath}`);
                    } catch (error) {
                        console.error(`Failed to sweep ${fullPath}: ${error.message}`);
                    }
                }
            }
        }
    }

    await processDirectory(targetDir);

    // Clean up empty directories, starting from deepest
    const sortedProcessedDirs = Array.from(processedDirs).sort((a, b) => b.length - a.length);
    for (const dirPath of sortedProcessedDirs) {
        try {
            const entries = await fs.readdir(dirPath);
            if (entries.length === 0) {
                await fs.rmdir(dirPath);
                console.log(`Removed empty directory: ${dirPath}`);
            }
        } catch (error) {
            if (error.code !== 'ENOENT') { // Ignore if dir was already removed
                console.error(`Failed to remove empty directory ${dirPath}: ${error.message}`);
            }
        }
    }

    return { sweptCount, sweptSize };
}

// CLI execution
if (require.main === module) {
    const args = process.argv.slice(2);
    const targetDir = args[0];
    const sanctuaryDir = args[1];
    const ageThresholdDays = parseInt(args[2], 10);

    if (!targetDir || !sanctuaryDir || isNaN(ageThresholdDays)) {
        console.error('Usage: node src/index.js <target_directory> <sanctuary_directory> <age_threshold_days>');
        process.exit(1);
    }

    sweepDigitalDustBunnies(targetDir, sanctuaryDir, ageThresholdDays)
        .then(({ sweptCount, sweptSize }) => {
            console.log('\n--- Digital Dust Bunny Sweeper Report ---');
            console.log(`Swept ${sweptCount} digital dust bunnies, totaling ${sweptSize} bytes, into the sanctuary!`);
            console.log('----------------------------------------');
        })
        .catch(error => {
            console.error('An error occurred during sweeping:', error);
            process.exit(1);
        });
}

module.exports = { sweepDigitalDustBunnies };
