const fs = require('fs');
const path = require('path');

function getFilesAndDirs(dirPath) {
    let files = [];
    let dirs = [];
    try {
        const entries = fs.readdirSync(dirPath, { withFileTypes: true });
        for (const entry of entries) {
            const fullPath = path.join(dirPath, entry.name);
            if (entry.isFile()) {
                files.push(fullPath);
            } else if (entry.isDirectory()) {
                dirs.push(fullPath);
                const subContent = getFilesAndDirs(fullPath);
                files = files.concat(subContent.files);
                dirs = dirs.concat(subContent.dirs);
            }
        }
    } catch (error) {
        // Ignore permission errors or non-existent paths for robustness
        if (error.code !== 'ENOENT' && error.code !== 'EACCES') {
            console.error(`Warning: Could not fully scan ${dirPath}: ${error.message}`);
        }
    }
    return { files, dirs };
}

function isDirectoryEmpty(dirPath) {
    try {
        const files = fs.readdirSync(dirPath);
        return files.length === 0;
    } catch (error) {
        // Ignore permission errors or non-existent paths.
        // If we can't read it, we can't confirm it's empty, so treat as not empty.
        if (error.code !== 'ENOENT' && error.code !== 'EACCES') {
            console.error(`Warning: Could not check if directory is empty ${dirPath}: ${error.message}`);
        }
        return false;
    }
}

function findDigitalDustBunnies(targetPath, ageThresholdDays) {
    const now = Date.now();
    const thresholdMs = ageThresholdDays * 24 * 60 * 60 * 1000;

    const staleFiles = [];
    const emptyDirs = [];

    const { files, dirs } = getFilesAndDirs(targetPath);

    for (const filePath of files) {
        try {
            const stats = fs.statSync(filePath);
            if (now - stats.mtimeMs > thresholdMs) {
                staleFiles.push({ path: filePath, mtime: new Date(stats.mtimeMs).toISOString() });
            }
        } catch (error) {
            // Ignore files that might have been deleted during scan or permission issues
            if (error.code !== 'ENOENT' && error.code !== 'EACCES') {
                console.error(`Error stating file ${filePath}: ${error.message}`);
            }
        }
    }

    // Check directories from deepest to shallowest to catch newly empty ones
    dirs.sort((a, b) => b.length - a.length);

    for (const dirPath of dirs) {
        if (isDirectoryEmpty(dirPath)) {
            emptyDirs.push(dirPath);
        }
    }

    return { staleFiles, emptyDirs };
}

function run() {
    const args = process.argv.slice(2);
    let targetPath = process.cwd();
    let ageThresholdDays = 365; // Default to 1 year

    if (args.length > 0) {
        targetPath = path.resolve(args[0]);
    }
    if (args.length > 1 && !isNaN(parseInt(args[1]))) {
        ageThresholdDays = parseInt(args[1]);
    }

    console.log(`\n🔍 Sweeping for digital dust bunnies in: ${targetPath}`);
    console.log(`⏳ Considering files untouched for over ${ageThresholdDays} days.`);

    const { staleFiles, emptyDirs } = findDigitalDustBunnies(targetPath, ageThresholdDays);

    console.log('\n--- Digital Dust Bunnies Report ---');

    if (staleFiles.length > 0) {
        console.log(`\n👻 Stale Files (${staleFiles.length}):`);
        staleFiles.forEach(file => console.log(`  - ${file.path} (Last modified: ${file.mtime})`));
    } else {
        console.log('\n✨ No stale files found. Your digital garden is well-tended!');
    }

    if (emptyDirs.length > 0) {
        console.log(`\n🗑️ Empty Directories (${emptyDirs.length}):`);
        emptyDirs.forEach(dir => console.log(`  - ${dir}`));
    } else {
        console.log('\n🌳 No empty directories found. Your digital landscape is lush!');
    }

    if (staleFiles.length === 0 && emptyDirs.length === 0) {
        console.log('\n🎉 Your system is sparkling clean! No digital dust bunnies in sight.');
    } else {
        console.log('\n🧹 Time to grab your digital broom and sweep these away!');
    }
}

if (require.main === module) {
    run();
}

module.exports = { findDigitalDustBunnies, getFilesAndDirs, isDirectoryEmpty }; // Export for testing
