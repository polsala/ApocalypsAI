const fs = require('fs');
const path = require('path');

/**
 * Generates a simulated data integrity score for a file.
 * In a real scenario, this might involve checksums or content analysis.
 * For this whimsical utility, it's a simple mock.
 * @param {string} filePath - The path to the file.
 * @returns {number} A simulated integrity score between 0 and 100.
 */
function generateIntegrityScore(filePath) {
    // Mock rationale: For a whimsical utility, a simple simulated score is sufficient.
    // In a real-world scenario, this would involve actual data integrity checks (e.g., checksums).
    // For deterministic testing, this function will be mocked or its output controlled.
    const baseScore = filePath.length % 100; // Simple deterministic base
    return Math.min(100, baseScore + 50); // Ensure it's somewhat high for "valuable" data
}

/**
 * Recursively scans a directory for files matching specified extensions
 * and generates a manifest with file details and a simulated integrity score.
 * @param {string} directoryPath - The path to the directory to scan.
 * @param {string[]} extensions - An array of file extensions to include (e.g., ['.txt', '.json']).
 * @returns {Array<Object>} An array of manifest entries.
 */
function generateManifest(directoryPath, extensions) {
    const manifest = [];
    const normalizedExtensions = new Set(extensions.map(ext => ext.toLowerCase()));

    if (!fs.existsSync(directoryPath)) {
        console.error(`Error: Directory not found at ${directoryPath}`);
        return manifest;
    }

    function scanDirectory(currentPath) {
        const items = fs.readdirSync(currentPath);

        for (const item of items) {
            const itemPath = path.join(currentPath, item);
            const stats = fs.statSync(itemPath);

            if (stats.isDirectory()) {
                scanDirectory(itemPath);
            } else if (stats.isFile()) {
                const fileExtension = path.extname(item).toLowerCase();
                if (normalizedExtensions.has(fileExtension)) {
                    manifest.push({
                        path: itemPath,
                        size: stats.size,
                        integrityScore: generateIntegrityScore(itemPath)
                    });
                }
            }
        }
    }

    scanDirectory(directoryPath);
    return manifest;
}

// CLI execution
if (require.main === module) {
    const args = process.argv.slice(2);
    const directory = args[0];
    const extensions = args.slice(1).map(ext => ext.startsWith('.') ? ext : `.${ext}`);

    if (!directory || extensions.length === 0) {
        console.log('Usage: node src/index.js <directory_path> <extension1> [extension2 ...]');
        console.log('Example: node src/index.js ./data txt json md');
        process.exit(1);
    }

    const manifest = generateManifest(directory, extensions);

    if (manifest.length > 0) {
        console.log('--- Nightly Data Scavenger\'s Manifest ---');
        manifest.forEach(entry => {
            console.log(`Path: ${entry.path}`);
            console.log(`  Size: ${entry.size} bytes`);
            console.log(`  Integrity Score: ${entry.integrityScore}/100`);
            console.log('-----------------------------------------');
        });
        console.log(`Total valuable fragments found: ${manifest.length}`);
    } else {
        console.log('No valuable data fragments found matching criteria.');
    }
}

module.exports = { generateManifest, generateIntegrityScore };
