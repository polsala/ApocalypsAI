const fs = require('fs');
const path = require('path');

/**
 * Calculates the age of a file in full days since its last modification.
 * @param {string} filePath - The path to the file.
 * @returns {number} The age of the file in days.
 */
function getFileAgeInDays(filePath) {
    const stats = fs.statSync(filePath);
    const now = new Date();
    const mtime = stats.mtime;
    const diffTime = Math.abs(now.getTime() - mtime.getTime());
    return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
}

/**
 * Recursively scans a directory for files older than a specified age.
 * @param {string} dirPath - The directory to scan.
 * @param {number} minAgeDays - The minimum age in days for a file to be considered old.
 * @param {Array<Object>} results - Accumulator for findings.
 * @returns {Array<Object>} A list of old files with their age and category.
 */
function scanDirectory(dirPath, minAgeDays, results = []) {
    const entries = fs.readdirSync(dirPath, { withFileTypes: true });

    for (const entry of entries) {
        const fullPath = path.join(dirPath, entry.name);
        if (entry.isDirectory()) {
            scanDirectory(fullPath, minAgeDays, results);
        } else if (entry.isFile()) {
            const age = getFileAgeInDays(fullPath);
            if (age >= minAgeDays) {
                let category;
                if (age >= 365) {
                    category = "Ancient Relic";
                } else if (age >= 180) {
                    category = "Forgotten Scroll";
                } else {
                    category = "Digital Dust Bunny";
                }
                results.push({
                    path: fullPath,
                    age: age,
                    category: category,
                    size: fs.statSync(fullPath).size
                });
            }
        }
    }
    return results;
}

/**
 * Runs the Digital Dust Bunny Sweeper, scanning a target path and reporting old files.
 * @param {string} targetPath - The path to the directory to scan.
 * @param {number} minAgeDays - The minimum age in days for a file to be considered old.
 * @returns {Array<Object>} The list of detected digital dust bunnies.
 */
function runSweeper(targetPath, minAgeDays) {
    if (!fs.existsSync(targetPath)) {
        throw new Error(`Path not found: ${targetPath}`);
    }
    if (!fs.statSync(targetPath).isDirectory()) {
        throw new Error(`Target path must be a directory: ${targetPath}`);
    }

    console.log(`\n🔍 Initiating Digital Dust Bunny Sweep in: ${targetPath}`);
    console.log(`🧹 Searching for files older than ${minAgeDays} days...\n`);

    const findings = scanDirectory(targetPath, minAgeDays);

    if (findings.length === 0) {
        console.log("✨ All clear! No digital dust bunnies found. Your directory is sparkling clean.");
    } else {
        console.log("Found the following digital dust bunnies:");
        findings.sort((a, b) => b.age - a.age); // Sort by age, oldest first
        findings.forEach(file => {
            console.log(`  [${file.category}] ${file.path} (Age: ${file.age} days, Size: ${file.size} bytes)`);
        });
        console.log(`\nTotal ${findings.length} digital dust bunnies detected. Time for a cleanup!`);
    }
    return findings; // Return findings for testing
}

// CLI entry point
if (require.main === module) {
    const args = process.argv.slice(2);
    let targetPath = '.';
    let minAgeDays = 90;

    if (args.length > 0) {
        targetPath = args[0];
    }
    if (args.length > 1 && !isNaN(parseInt(args[1]))) {
        minAgeDays = parseInt(args[1]);
    }

    try {
        runSweeper(targetPath, minAgeDays);
    } catch (error) {
        console.error(`\n🚨 Sweep Aborted: ${error.message}`);
        process.exit(1);
    }
}

module.exports = { runSweeper, getFileAgeInDays, scanDirectory };
