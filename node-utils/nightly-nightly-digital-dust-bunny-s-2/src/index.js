const fs = require('fs').promises;
const path = require('path');
const minimist = require('minimist');

const MS_PER_DAY = 1000 * 60 * 60 * 24;

async function getFileAgeInDays(filePath) {
    try {
        const stats = await fs.stat(filePath);
        if (stats.isFile()) {
            const now = new Date();
            const modifiedDate = stats.mtime; // Last modified date
            const ageMs = now.getTime() - modifiedDate.getTime();
            return Math.floor(ageMs / MS_PER_DAY);
        }
    } catch (error) {
        // Ignore errors for non-existent files or permission issues
        return -1;
    }
    return -1; // Not a file or error
}

async function findDustBunnies(directoryPath, minAgeDays, recursive) {
    const dustBunnies = [];
    let totalSize = 0;

    async function scanDirectory(currentPath) {
        try {
            const entries = await fs.readdir(currentPath, { withFileTypes: true });

            for (const entry of entries) {
                const fullPath = path.join(currentPath, entry.name);

                if (entry.isFile()) {
                    const age = await getFileAgeInDays(fullPath);
                    if (age >= minAgeDays) {
                        const stats = await fs.stat(fullPath);
                        dustBunnies.push({
                            path: fullPath,
                            age: age,
                            size: stats.size
                        });
                        totalSize += stats.size;
                    }
                } else if (entry.isDirectory() && recursive) {
                    await scanDirectory(fullPath);
                }
            }
        } catch (error) {
            // console.warn(`Warning: Could not read directory ${currentPath}: ${error.message}`);
            // Silently ignore directories we can't read, or log a warning if desired.
        }
    }

    await scanDirectory(directoryPath);
    return { dustBunnies, totalSize };
}

function formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

async function main() {
    const argv = minimist(process.argv.slice(2), {
        alias: {
            a: 'age',
            r: 'recursive',
            o: 'output',
            h: 'help'
        },
        default: {
            age: 90,
            recursive: false
        },
        boolean: ['recursive', 'help']
    });

    if (argv.help || !argv._[0]) {
        console.log(`\nNightly Digital Dust Bunny Sweeper\n\nUsage: node src/index.js <directory_path> [options]\n\nArguments:\n  <directory_path>    The path to the directory to scan.\n\nOptions:\n  -a, --age <days>    Minimum age in days for a file to be considered a "dust bunny".\n                      Defaults to 90 days.\n  -r, --recursive     Scan subdirectories recursively.\n  -o, --output <file> Output the report to a specified file instead of the console.\n  -h, --help          Display this help message.\n\nExamples:\n  node src/index.js . --age 180 --recursive\n  node src/index.js /path/to/my/old/files -o dust_report.txt\n        `);
        process.exit(0);
    }

    const directoryPath = argv._[0];
    const minAgeDays = parseInt(argv.age, 10);
    const recursive = argv.recursive;
    const outputPath = argv.output;

    if (isNaN(minAgeDays) || minAgeDays < 0) {
        console.error("Error: --age must be a non-negative number.");
        process.exit(1);
    }

    try {
        const stats = await fs.stat(directoryPath);
        if (!stats.isDirectory()) {
            console.error(`Error: "${directoryPath}" is not a valid directory.`);
            process.exit(1);
        }
    } catch (error) {
        console.error(`Error: Directory "${directoryPath}" not found or accessible. ${error.message}`);
        process.exit(1);
    }

    console.log(`\nSweeping for digital dust bunnies in "${directoryPath}" (older than ${minAgeDays} days, recursive: ${recursive ? 'yes' : 'no'})...\n`);

    const { dustBunnies, totalSize } = await findDustBunnies(directoryPath, minAgeDays, recursive);

    let reportContent = '';
    if (dustBunnies.length === 0) {
        reportContent = `✨ All clear! No digital dust bunnies found in "${directoryPath}". Your digital space is sparkling!\n`;
    } else {
        reportContent += `Found ${dustBunnies.length} digital dust bunnies, totaling ${formatBytes(totalSize)}:\n\n`;
        dustBunnies.sort((a, b) => b.age - a.age); // Sort by age, oldest first
        for (const bunny of dustBunnies) {
            reportContent += `- ${bunny.path} (Age: ${bunny.age} days, Size: ${formatBytes(bunny.size)})\n`;
        }
        reportContent += `\nConsider giving these old files a new purpose, archiving them, or letting them float away into the digital ether.\n`;
    }

    if (outputPath) {
        try {
            await fs.writeFile(outputPath, reportContent);
            console.log(`Report saved to "${outputPath}"`);
        } catch (error) {
            console.error(`Error: Could not write report to "${outputPath}": ${error.message}`);
            process.exit(1);
        }
    } else {
        console.log(reportContent);
    }
}

if (require.main === module) {
    main();
}

// Export for testing
module.exports = {
    findDustBunnies,
    getFileAgeInDays,
    formatBytes,
    main
};
