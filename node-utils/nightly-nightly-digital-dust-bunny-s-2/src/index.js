const fs = require('fs').promises;
const path = require('path');
const process = require('process');

async function sweepDigitalDustBunnies(targetPath, ageDays, dryRun, quarantineDir) {
    console.log(`\n🧹 Starting Digital Dust Bunny Sweep in: ${targetPath}`);
    console.log(`Files older than ${ageDays} days will be considered dust bunnies.`);
    if (dryRun) {
        console.log("DRY RUN mode: No files will be moved or deleted.");
    }

    const now = Date.now();
    const thresholdMs = ageDays * 24 * 60 * 60 * 1000;
    const sweptFiles = [];
    const quarantinePath = path.join(targetPath, quarantineDir);

    try {
        await fs.mkdir(quarantinePath, { recursive: true });
        console.log(`Digital Compost Bin (quarantine) created/ensured at: ${quarantinePath}`);
    } catch (error) {
        console.error(`Error creating quarantine directory: ${error.message}`);
        return;
    }

    try {
        const files = await fs.readdir(targetPath, { withFileTypes: true });

        for (const file of files) {
            if (file.isDirectory()) {
                // For simplicity, we skip directories and only sweep files in the targetPath.
                continue;
            }

            const filePath = path.join(targetPath, file.name);
            try {
                const stats = await fs.stat(filePath);
                const fileAgeMs = now - stats.mtimeMs;

                if (fileAgeMs > thresholdMs) {
                    console.log(`Found dust bunny: ${file.name} (last modified ${new Date(stats.mtimeMs).toLocaleDateString()})`);
                    if (!dryRun) {
                        const newPath = path.join(quarantinePath, file.name);
                        await fs.rename(filePath, newPath);
                        sweptFiles.push(file.name);
                        console.log(`  -> Swept to Digital Compost Bin: ${newPath}`);
                    } else {
                        sweptFiles.push(file.name); // Still count in dry run for reporting
                    }
                }
            } catch (statError) {
                console.warn(`Could not stat file ${file.name}: ${statError.message}`);
            }
        }

        console.log("\n--- Sweep Summary ---");
        if (sweptFiles.length > 0) {
            console.log(`Successfully swept ${sweptFiles.length} digital dust bunnies.`);
            if (dryRun) {
                console.log("These files *would have been* moved (dry run):");
            } else {
                console.log("These files were moved to the Digital Compost Bin:");
            }
            sweptFiles.forEach(f => console.log(`- ${f}`));
            console.log(`Review them in: ${quarantinePath}`);
        } else {
            console.log("No digital dust bunnies found. Your digital space is sparkling clean!");
        }

    } catch (error) {
        console.error(`Error during sweep: ${error.message}`);
    }
}

// CLI Argument Parsing (only if this file is executed directly)
if (require.main === module) {
    const args = process.argv.slice(2);
    const options = {
        path: '.', // default current directory
        age: 90,   // default 90 days
        dryRun: false,
        quarantineDir: '.digital_compost_bin'
    };

    for (let i = 0; i < args.length; i++) {
        const arg = args[i];
        if (arg === '--path' && args[i + 1]) {
            options.path = args[++i];
        } else if (arg === '--age' && args[i + 1]) {
            options.age = parseInt(args[++i], 10);
            if (isNaN(options.age) || options.age <= 0) {
                console.error("Error: --age must be a positive number.");
                process.exit(1);
            }
        } else if (arg === '--dry-run') {
            options.dryRun = true;
        } else if (arg === '--quarantine-dir' && args[i + 1]) {
            options.quarantineDir = args[++i];
        } else if (arg === '--help' || arg === '-h') {
            console.log(`\nUsage: node src/index.js [options]\n\nOptions:\n  --path <directory>      The directory to sweep. Defaults to current directory.\n  --age <days>            Files older than this many days will be swept. Defaults to 90.\n  --dry-run               Simulate the sweep without moving any files.\n  --quarantine-dir <name> Name of the quarantine directory. Defaults to '.digital_compost_bin'.\n  --help, -h              Show this help message.\n        `);
            process.exit(0);
        }
    }

    if (!options.path) {
        console.error("Error: --path is required.");
        process.exit(1);
    }

    sweepDigitalDustBunnies(options.path, options.age, options.dryRun, options.quarantineDir);
}

module.exports = { sweepDigitalDustBunnies };
