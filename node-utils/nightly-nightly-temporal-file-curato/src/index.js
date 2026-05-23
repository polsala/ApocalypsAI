const fs = require('fs').promises;
const path = require('path');

async function getFilesWithDecay(dirPath, now = Date.now()) {
    try {
        const entries = await fs.readdir(dirPath, { withFileTypes: true });
        const files = [];

        for (const entry of entries) {
            if (entry.isFile()) {
                const filePath = path.join(dirPath, entry.name);
                try {
                    const stats = await fs.stat(filePath);
                    const mtimeMs = stats.mtimeMs;
                    const ageInDays = (now - mtimeMs) / (1000 * 60 * 60 * 24);
                    files.push({
                        name: entry.name,
                        path: filePath,
                        mtime: new Date(mtimeMs).toISOString().split('T')[0],
                        ageInDays: ageInDays
                    });
                } catch (statErr) {
                    console.warn(`Warning: Could not stat file ${filePath}: ${statErr.message}`);
                }
            }
        }
        return files;
    } catch (err) {
        if (err.code === 'ENOENT') {
            throw new Error(`Directory not found: ${dirPath}`);
        }
        throw new Error(`Error reading directory ${dirPath}: ${err.message}`);
    }
}

function generateCuratorReport(files, thresholdDays) {
    let report = `\n--- Temporal File Curator Report ---\n`;
    report += `Scanning for files older than ${thresholdDays} days.\n`;
    report += `Current Temporal Epoch: ${new Date(Date.now()).toISOString().split('T')[0]}\n\n`;

    if (files.length === 0) {
        report += "No files found in the specified directory.\n";
        return report;
    }

    const decayedFiles = files.filter(f => f.ageInDays > thresholdDays);
    const moderatelyDecayedFiles = files.filter(f => f.ageInDays > thresholdDays && f.ageInDays <= thresholdDays * 2);
    const deeplyDecayedFiles = files.filter(f => f.ageInDays > thresholdDays * 2);
    const freshFiles = files.filter(f => f.ageInDays <= thresholdDays);

    if (deeplyDecayedFiles.length > 0) {
        report += "Deeply Decayed Artifacts (Older than " + (thresholdDays * 2) + " days):\n";
        deeplyDecayedFiles.forEach(file => {
            report += `  - ${file.name} (Last Modified: ${file.mtime}, Age: ${file.ageInDays.toFixed(1)} days)\n`;
            report += `    Recommendation: Immediate Archival to 'Temporal Vault' or 'Void Purge'.\n`;
        });
        report += "\n";
    }

    if (moderatelyDecayedFiles.length > 0) {
        report += "Moderately Decayed Artifacts (Older than " + thresholdDays + " days, but less than " + (thresholdDays * 2) + " days):\n";
        moderatelyDecayedFiles.forEach(file => {
            report += `  - ${file.name} (Last Modified: ${file.mtime}, Age: ${file.ageInDays.toFixed(1)} days)\n`;
            report += `    Recommendation: Review for 'Archive' to 'Stasis Chamber' or 'Re-evaluation'.\n`;
        });
        report += "\n";
    }

    if (freshFiles.length > 0) {
        report += "Freshly Manifested Artifacts (Within " + thresholdDays + " days):\n";
        freshFiles.forEach(file => {
            report += `  - ${file.name} (Last Modified: ${file.mtime}, Age: ${file.ageInDays.toFixed(1)} days)\n`;
            report += `    Recommendation: No immediate action. Continue monitoring temporal integrity.\n`;
        });
        report += "\n";
    }

    report += `Total files scanned: ${files.length}\n`;
    report += `Total decayed files: ${decayedFiles.length}\n`;
    report += `--- End Report ---\n`;

    return report;
}

async function main() {
    const args = process.argv.slice(2);
    const dirPath = args[0];
    const thresholdDays = parseInt(args[1], 10);

    if (!dirPath || isNaN(thresholdDays) || thresholdDays <= 0) {
        console.error("Usage: node src/index.js <directory_path> <age_threshold_in_days>");
        console.error("Example: node src/index.js ./my_data 90");
        process.exit(1);
    }

    try {
        const files = await getFilesWithDecay(dirPath);
        const report = generateCuratorReport(files, thresholdDays);
        console.log(report);
    } catch (error) {
        console.error(`Error: ${error.message}`);
        process.exit(1);
    }
}

if (require.main === module) {
    main();
}

module.exports = { getFilesWithDecay, generateCuratorReport, main };
