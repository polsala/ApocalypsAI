const path = require('path');
const fs = require('fs');

const STATE_FILE_NAME = '.garden_state.json';

/**
 * Recursively scans a directory and returns a map of file paths to their stats.
 * @param {string} dirPath The directory to scan.
 * @param {object} fsModule The fs module (or mock fs module) to use.
 * @param {string} [basePath=''] The base path for relative file paths.
 * @returns {Map<string, {mtimeMs: number, size: number}>} A map of file paths to their stats.
 */
function scanDirectory(dirPath, fsModule, basePath = '') {
    const files = new Map();
    let entries;
    try {
        entries = fsModule.readdirSync(dirPath, { withFileTypes: true });
    } catch (error) {
        if (error.code === 'ENOENT') {
            console.error(`Error: Directory not found: ${dirPath}`);
            return files;
        } else if (error.code === 'EACCES') {
            console.error(`Error: Permission denied for directory: ${dirPath}`);
            return files;
        } else {
            throw error;
        }
    }

    for (const entry of entries) {
        const fullPath = path.join(dirPath, entry.name);
        const relativePath = path.join(basePath, entry.name);

        if (entry.name === STATE_FILE_NAME) {
            continue; // Skip the state file itself
        }

        let stats;
        try {
            stats = fsModule.statSync(fullPath);
        } catch (error) {
            if (error.code === 'ENOENT') {
                // File might have been deleted between readdir and stat
                continue;
            } else {
                throw error;
            }
        }

        if (stats.isDirectory()) {
            const subFiles = scanDirectory(fullPath, fsModule, relativePath);
            subFiles.forEach((value, key) => files.set(key, value));
        } else if (stats.isFile()) {
            files.set(relativePath, { mtimeMs: stats.mtimeMs, size: stats.size });
        }
    }
    return files;
}

/**
 * Loads the previous state from the .garden_state.json file.
 * @param {string} stateFilePath The path to the state file.
 * @param {object} fsModule The fs module (or mock fs module) to use.
 * @returns {Map<string, {mtimeMs: number, size: number}>} The previous state map.
 */
function loadState(stateFilePath, fsModule) {
    if (fsModule.existsSync(stateFilePath)) {
        try {
            const content = fsModule.readFileSync(stateFilePath, 'utf8');
            const parsed = JSON.parse(content);
            return new Map(parsed.map(item => [item.path, { mtimeMs: item.mtimeMs, size: item.size }]));
        } catch (error) {
            console.warn(`Warning: Could not read or parse state file: ${stateFilePath}. Starting fresh.`, error.message);
            return new Map();
        }
    }
    return new Map();
}

/**
 * Saves the current state to the .garden_state.json file.
 * @param {Map<string, {mtimeMs: number, size: number}>} currentState The current state map.
 * @param {string} stateFilePath The path to the state file.
 * @param {object} fsModule The fs module (or mock fs module) to use.
 */
function saveState(currentState, stateFilePath, fsModule) {
    const serializableState = Array.from(currentState.entries()).map(([path, stats]) => ({ path, ...stats }));
    fsModule.writeFileSync(stateFilePath, JSON.stringify(serializableState, null, 2), 'utf8');
}

/**
 * Compares previous and current states to find changes.
 * @param {Map<string, {mtimeMs: number, size: number}>} previousState
 * @param {Map<string, {mtimeMs: number, size: number}>} currentState
 * @returns {{newFiles: string[], modifiedFiles: string[], deletedFiles: string[]}}
 */
function compareStates(previousState, currentState) {
    const newFiles = [];
    const modifiedFiles = [];
    const deletedFiles = [];

    // Check for new and modified files
    for (const [filePath, currentStats] of currentState.entries()) {
        if (!previousState.has(filePath)) {
            newFiles.push(filePath);
        } else {
            const prevStats = previousState.get(filePath);
            if (prevStats.mtimeMs !== currentStats.mtimeMs || prevStats.size !== currentStats.size) {
                modifiedFiles.push(filePath);
            }
        }
    }

    // Check for deleted files
    for (const [filePath] of previousState.entries()) {
        if (!currentState.has(filePath)) {
            deletedFiles.push(filePath);
        }
    }

    return { newFiles, modifiedFiles, deletedFiles };
}

/**
 * Generates and prints a whimsical garden report.
 * @param {{newFiles: string[], modifiedFiles: string[], deletedFiles: string[]}} changes
 */
function generateReport({ newFiles, modifiedFiles, deletedFiles }) {
    const date = new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
    console.log(`\n🌿 The Digital Garden Report for ${date} 🌸\n`);
    console.log('--- A New Day in the Garden ---\n');

    if (newFiles.length > 0) {
        console.log('🌱 New Sprouts (Freshly Planted):');
        newFiles.forEach(file => console.log(`  - ${file}`));
        console.log('');
    }

    if (modifiedFiles.length > 0) {
        console.log('🌼 Blooming Beauties (Flourishing & Changed):');
        modifiedFiles.forEach(file => console.log(`  - ${file}`));
        console.log('');
    }

    if (deletedFiles.length > 0) {
        console.log('🍂 Wilted Wonders (Faded Away):');
        deletedFiles.forEach(file => console.log(`  - ${file}`));
        console.log('');
    }

    if (newFiles.length === 0 && modifiedFiles.length === 0 && deletedFiles.length === 0) {
        console.log('✨ Quiet Corners (No Major Changes Detected). The garden rests peacefully.\n');
    }

    console.log('--- Garden is Thriving! ---\n');
}

/**
 * Main function to run the Digital Garden Guard.
 * @param {string} targetDir The directory to monitor.
 * @param {object} [fsModule=fs] The fs module (or mock fs module) to use. Defaults to real fs.
 */
function run(targetDir, fsModule = fs) {
    const stateFilePath = path.join(targetDir, STATE_FILE_NAME);

    const previousState = loadState(stateFilePath, fsModule);
    const currentState = scanDirectory(targetDir, fsModule);

    const changes = compareStates(previousState, currentState);

    generateReport(changes);

    saveState(currentState, stateFilePath, fsModule);
}

// If run directly from CLI
if (require.main === module) {
    const targetDir = process.argv[2];
    if (!targetDir) {
        console.error('Usage: node src/index.js <directory_to_monitor>');
        process.exit(1);
    }
    run(targetDir);
}

module.exports = { run, scanDirectory, loadState, saveState, compareStates, generateReport };
