const fs = require('fs').promises;
const path = require('path');

async function findDustBunnies(dir, ageThresholdDays, excludeDirs = []) {
    const now = Date.now();
    const dustBunnies = [];

    async function scan(currentPath) {
        let entries;
        try {
            entries = await fs.readdir(currentPath, { withFileTypes: true });
        } catch (error) {
            console.warn(`Could not read directory ${currentPath}: ${error.message}`);
            return; // Skip this directory if it can't be read
        }

        for (const entry of entries) {
            const fullPath = path.join(currentPath, entry.name);
            
            // Check if the current entry itself is an excluded directory
            if (entry.isDirectory() && excludeDirs.includes(entry.name)) {
                continue; // Skip this excluded directory and its contents
            }

            try {
                const stats = await fs.stat(fullPath);
                const ageMs = now - stats.mtimeMs;
                const ageDays = ageMs / (1000 * 60 * 60 * 24);

                if (ageDays > ageThresholdDays) {
                    dustBunnies.push({
                        path: fullPath,
                        type: entry.isDirectory() ? 'directory' : 'file',
                        ageDays: Math.floor(ageDays)
                    });
                }

                if (entry.isDirectory()) {
                    await scan(fullPath); // Recurse into subdirectories
                }
            } catch (error) {
                console.warn(`Could not stat ${fullPath}: ${error.message}`);
            }
        }
    }

    await scan(dir);
    return dustBunnies;
}

async function compostDustBunnies(dustBunnies, compostPath) {
    if (dustBunnies.length === 0) {
        console.log("No dust bunnies to compost. Your digital space is sparkling!");
        return;
    }

    await fs.mkdir(compostPath, { recursive: true });
    console.log(`Composting ${dustBunnies.length} digital dust bunnies to: ${compostPath}`);

    for (const bunny of dustBunnies) {
        const newPath = path.join(compostPath, path.basename(bunny.path));
        try {
            await fs.rename(bunny.path, newPath);
            console.log(`  Moved: ${bunny.path} -> ${newPath}`);
        } catch (error) {
            console.error(`  Failed to compost ${bunny.path}: ${error.message}`);
        }
    }
    console.log("Composting complete!");
}

async function runCli() {
    const args = process.argv.slice(2);
    const targetDir = args[0];
    const ageThreshold = parseInt(args[1], 10);
    const compostDir = args[2];

    if (!targetDir || isNaN(ageThreshold) || !compostDir) {
        console.log("Usage: node src/index.js <target_directory> <age_threshold_days> <compost_directory>");
        console.log("Example: node src/index.js ./my_project 90 ./digital_compost");
        process.exit(1);
    }

    console.log(`Scanning \"${targetDir}\" for digital dust bunnies older than ${ageThreshold} days...`);
    const dustBunnies = await findDustBunnies(targetDir, ageThreshold, ['node_modules', '.git']);

    if (dustBunnies.length === 0) {
        console.log("No dust bunnies found. Your digital space is pristine!");
        return;
    }

    console.log("\nFound these digital dust bunnies:");
    dustBunnies.forEach(bunny => {
        console.log(`- ${bunny.path} (${bunny.type}, ${bunny.ageDays} days old)`);
    });

    await compostDustBunnies(dustBunnies, compostDir);
}

// Only run CLI if executed directly
if (require.main === module) {
    runCli().catch(console.error);
}

module.exports = { findDustBunnies, compostDustBunnies };
