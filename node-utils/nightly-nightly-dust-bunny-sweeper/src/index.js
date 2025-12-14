const fs = require('fs');
const path = require('path');

function sweepDirectory(dirPath, ageThresholdMs, isCleaning, foundDustBunnies) {
    const files = fs.readdirSync(dirPath); // # Mock rationale: `fs.readdirSync` is mocked to simulate directory contents without actual file system access, ensuring deterministic test environments.
    const now = Date.now(); // # Mock rationale: `Date.now()` is used to determine file age. In tests, this will be implicitly controlled by the mocked `mtimeMs` values relative to a fixed `now` in the test setup, ensuring deterministic age calculation.

    for (const file of files) {
        const fullPath = path.join(dirPath, file);
        const stats = fs.statSync(fullPath); // # Mock rationale: `fs.statSync` is mocked to return predefined file stats (isDirectory, isFile, mtimeMs) for deterministic testing of file type and age without actual file system access.

        if (stats.isDirectory()) {
            sweepDirectory(fullPath, ageThresholdMs, isCleaning, foundDustBunnies);
        } else if (stats.isFile()) {
            if (now - stats.mtimeMs > ageThresholdMs) {
                foundDustBunnies.push(fullPath);
                if (isCleaning) {
                    fs.unlinkSync(fullPath); // # Mock rationale: `fs.unlinkSync` is mocked to verify that deletion attempts are made for the correct files without performing actual file deletion during tests.
                }
            }
        }
    }
}

function main() {
    const args = process.argv.slice(2);
    const dir = args[0];
    const days = parseInt(args[1], 10);
    const clean = args.includes('--clean');

    if (!dir || isNaN(days)) {
        console.log('Usage: node src/index.js <directory> <age_in_days> [--clean]'); // # Mock rationale: `console.log` is mocked to capture and assert on CLI output, ensuring the utility provides correct user feedback.
        return;
    }

    const ageThresholdMs = days * 24 * 60 * 60 * 1000;
    const foundDustBunnies = [];

    try {
        if (!fs.existsSync(dir)) { // # Mock rationale: `fs.existsSync` is mocked to simulate a directory not existing, allowing testing of error handling for invalid paths.
            throw new Error(`Directory not found: ${dir}`);
        }
        sweepDirectory(dir, ageThresholdMs, clean, foundDustBunnies);

        if (foundDustBunnies.length === 0) {
            console.log(`No digital dust bunnies found older than ${days} days in ${dir}.`);
        } else {
            console.log(`Found ${foundDustBunnies.length} digital dust bunnies older than ${days} days:`);
            foundDustBunnies.forEach(bunny => console.log(`- ${bunny}`));
            if (clean) {
                console.log('Swept them away!');
            } else {
                console.log('Run with --clean to sweep them away.');
            }
        }
    } catch (error) {
        console.error(`Error sweeping directory: ${error.message}`); // # Mock rationale: `console.error` is mocked to capture and assert on error messages, ensuring robust error handling.
    }
}

// Export main for testing
module.exports = { main };

// If run directly, execute main
if (require.main === module) {
    main();
}
