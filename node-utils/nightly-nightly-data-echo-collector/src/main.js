const fs = require('fs');
const path = require('path');

const STATE_FILE_NAME = 'echo_state.json';
const REPORT_FILE_NAME = 'echo_report.txt';

/**
 * Scans a directory and collects file metadata.
 * @param {string} dirPath - The directory to scan.
 * @returns {Object<string, {size: number, mtimeMs: number}>} - Map of file paths to metadata.
 */
function scanDirectory(dirPath) {
    const files = {};
    if (!fs.existsSync(dirPath)) {
        console.warn(`Warning: Directory not found: ${dirPath}`);
        return files;
    }

    const entries = fs.readdirSync(dirPath, { withFileTypes: true });
    for (const entry of entries) {
        const fullPath = path.join(dirPath, entry.name);
        try {
            const stats = fs.statSync(fullPath);
            if (stats.isFile()) {
                files[fullPath] = {
                    size: stats.size,
                    mtimeMs: stats.mtimeMs
                };
            } else if (stats.isDirectory()) {
                // Recursively scan subdirectories
                Object.assign(files, scanDirectory(fullPath));
            }
        } catch (error) {
            console.error(`Error accessing ${fullPath}: ${error.message}`);
        }
    }
    return files;
}

/**
 * Loads the previous state from a JSON file.
 * @param {string} stateFilePath - Path to the state file.
 * @returns {Object<string, {size: number, mtimeMs: number}>} - Previous state.
 */
function loadState(stateFilePath) {
    if (fs.existsSync(stateFilePath)) {
        try {
            const data = fs.readFileSync(stateFilePath, 'utf8');
            return JSON.parse(data);
        } catch (error) {
            console.error(`Error loading state from ${stateFilePath}: ${error.message}`);
            return {};
        }
    }
    return {};
}

/**
 * Saves the current state to a JSON file.
 * @param {string} stateFilePath - Path to the state file.
 * @param {Object} currentState - The current state to save.
 */
function saveState(stateFilePath, currentState) {
    try {
        fs.writeFileSync(stateFilePath, JSON.stringify(currentState, null, 2), 'utf8');
    } catch (error) {
        console.error(`Error saving state to ${stateFilePath}: ${error.message}`);
    }
}

/**
 * Generates a report based on current and previous states.
 * @param {Object} previousState - The state from the last run.
 * @param {Object} currentState - The current scanned state.
 * @returns {string} - The generated report.
 */
function generateReport(previousState, currentState) {
    const reportLines = [`--- Data Echo Report - ${new Date().toISOString()} ---`];
    reportLines.push('');

    const allPaths = new Set([...Object.keys(previousState), ...Object.keys(currentState)]);

    let newFiles = 0;
    let modifiedFiles = 0;
    let deletedFiles = 0;

    for (const filePath of allPaths) {
        const prev = previousState[filePath];
        const curr = currentState[filePath];

        if (!prev && curr) {
            reportLines.push(`[NEW] ${filePath} (Size: ${curr.size} bytes)`);
            newFiles++;
        } else if (prev && !curr) {
            reportLines.push(`[DELETED] ${filePath}`);
            deletedFiles++;
        } else if (prev && curr) {
            if (prev.size !== curr.size || prev.mtimeMs !== curr.mtimeMs) {
                reportLines.push(`[MODIFIED] ${filePath} (Old Size: ${prev.size}, New Size: ${curr.size})`);
                modifiedFiles++;
            }
        }
    }

    reportLines.push('');
    reportLines.push('--- Summary ---');
    reportLines.push(`New Files: ${newFiles}`);
    reportLines.push(`Modified Files: ${modifiedFiles}`);
    reportLines.push(`Deleted Files: ${deletedFiles}`);
    reportLines.push('-----------------');

    return reportLines.join('\n');
}

/**
 * Main function to run the data echo collector.
 * @param {string[]} monitorDirs - Array of directories to monitor.
 * @param {string} outputDir - Directory to save state and report files.
 */
function run(monitorDirs, outputDir) {
    const stateFilePath = path.join(outputDir, STATE_FILE_NAME);
    const reportFilePath = path.join(outputDir, REPORT_FILE_NAME);

    console.log(`Monitoring directories: ${monitorDirs.join(', ')}`);
    console.log(`State file: ${stateFilePath}`);
    console.log(`Report file: ${reportFilePath}`);

    // Ensure output directory exists
    if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir, { recursive: true });
    }

    const previousState = loadState(stateFilePath);
    let currentState = {};

    for (const dir of monitorDirs) {
        Object.assign(currentState, scanDirectory(dir));
    }

    const report = generateReport(previousState, currentState);
    fs.writeFileSync(reportFilePath, report, 'utf8');

    saveState(stateFilePath, currentState);

    console.log(`Report generated and saved to ${reportFilePath}`);
    console.log(`State updated in ${stateFilePath}`);
}

// CLI entry point
if (require.main === module) {
    const args = process.argv.slice(2);
    if (args.length < 2) {
        console.error('Usage: node src/main.js <output_directory> <directory_to_monitor_1> [directory_to_monitor_2 ...]');
        process.exit(1);
    }

    const outputDir = args[0];
    const monitorDirs = args.slice(1);

    run(monitorDirs, outputDir);
}

module.exports = {
    scanDirectory,
    loadState,
    saveState,
    generateReport,
    run
};
