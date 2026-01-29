const fs = require('fs');
const path = require('path');

// Exported for testing purposes
function getFileAgeInDays(filePath) {
    const stats = fs.statSync(filePath);
    const mtimeMs = stats.mtimeMs; // Modification time in milliseconds
    const nowMs = Date.now();
    const ageMs = nowMs - mtimeMs;
    return ageMs / (1000 * 60 * 60 * 24); // Convert milliseconds to days
}

// Exported for testing purposes
function findDustBunnies(directoryPath, minAgeDays) {
    const dustBunnies = [];
    let filesAndDirs;
    try {
        filesAndDirs = fs.readdirSync(directoryPath, { withFileTypes: true });
    } catch (error) {
        // If directory cannot be read (e.g., permissions), treat as empty
        // console.warn(`Could not read directory ${directoryPath}: ${error.message}`);
        return [];
    }


    for (const entry of filesAndDirs) {
        const fullPath = path.join(directoryPath, entry.name);
        try {
            if (entry.isDirectory()) {
                dustBunnies.push(...findDustBunnies(fullPath, minAgeDays));
            } else if (entry.isFile()) {
                const age = getFileAgeInDays(fullPath);
                if (age > minAgeDays) {
                    dustBunnies.push({ path: fullPath, age: age });
                }
            }
        } catch (error) {
            // Ignore permission errors or other file system issues for robustness
            // console.warn(`Could not process ${fullPath}: ${error.message}`);
        }
    }
    return dustBunnies;
}

// Main function to run the CLI
function runCLI(argv) {
    const args = argv.slice(2);
    if (args.length !== 2) {
        console.error('Usage: node src/index.js <directory_path> <age_in_days>');
        return 1; // Return exit code for testing
    }

    const directoryPath = args[0];
    const minAgeDays = parseFloat(args[1]);

    if (isNaN(minAgeDays) || minAgeDays < 0) {
        console.error('Error: <age_in_days> must be a non-negative number.');
        return 1;
    }

    if (!fs.existsSync(directoryPath)) {
        console.error(`Error: Directory not found: ${directoryPath}`);
        return 1;
    }

    console.log(`\n--- Initiating Digital Dust Bunny Sweep in '${directoryPath}' ---\n`);
    console.log(`Searching for files older than ${minAgeDays.toFixed(2)} days...\n`);

    const dustBunnies = findDustBunnies(directoryPath, minAgeDays);

    if (dustBunnies.length === 0) {
        console.log('✨ The digital realm is pristine! No dust bunnies found. ✨');
    } else {
        console.log(`Found ${dustBunnies.length} digital dust bunnies:\n`);
        dustBunnies.sort((a, b) => b.age - a.age).forEach(bunny => {
            console.log(`  - ${bunny.path} (forgotten for ${bunny.age.toFixed(2)} days)`);
        });
        console.log('\n--- End of Sweep. Consider their fate, digital caretaker. ---');
    }
    return 0; // Success
}

// Only run if this script is executed directly
if (require.main === module) {
    const exitCode = runCLI(process.argv);
    process.exit(exitCode);
}

// Export for testing
module.exports = { findDustBunnies, getFileAgeInDays, runCLI };
