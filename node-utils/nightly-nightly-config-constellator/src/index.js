// src/index.js
const fs = require('fs');
const path = require('path');
const { parseEnvContent } = require('./parser');

/**
 * Compares environment variables across multiple parsed config objects.
 * @param {Object.<string, Object.<string, string>>} configs An object where keys are file paths
 *                                                           and values are parsed env objects.
 * @returns {{missing: Object, drifting: Object, harmonized: string[]}} Comparison results.
 */
function compareConfigs(configs) {
    const allKeys = new Set();
    for (const filePath in configs) {
        for (const key in configs[filePath]) {
            allKeys.add(key);
        }
    }

    const missing = {}; // { filePath: [key1, key2], ... }
    const drifting = {}; // { key: { filePath: value, ... }, ... }
    const harmonized = []; // [key1, key2, ...]

    for (const key of allKeys) {
        let firstValue = null;
        let isDrifting = false;
        const valuesPerFile = {};
        const filesHavingKey = [];

        for (const filePath in configs) {
            if (configs[filePath].hasOwnProperty(key)) {
                const currentValue = configs[filePath][key];
                valuesPerFile[filePath] = currentValue;
                filesHavingKey.push(filePath);

                if (firstValue === null) {
                    firstValue = currentValue;
                } else if (firstValue !== currentValue) {
                    isDrifting = true;
                }
            } else {
                // Key is missing in this file
                if (!missing[filePath]) {
                    missing[filePath] = [];
                }
                missing[filePath].push(key);
            }
        }

        if (filesHavingKey.length === Object.keys(configs).length) { // Key is in all files
            if (isDrifting) {
                drifting[key] = valuesPerFile;
            } else {
                harmonized.push(key);
            }
        }
    }

    return { missing, drifting, harmonized };
}

/**
 * Prints the comparison report to the console.
 * @param {string[]} filePaths The paths of the files being compared.
 * @param {{missing: Object, drifting: Object, harmonized: string[]}} results Comparison results.
 */
function printReport(filePaths, results) {
    console.log('\n🌌 Aligning Config Constellations 🌌\n');
    console.log(`Comparing: ${filePaths.map(p => path.basename(p)).join(', ')}\n`);

    console.log('--- Missing Stars ---');
    if (Object.keys(results.missing).length === 0) {
        console.log('  All keys present in all files (no missing stars).\n');
    } else {
        for (const filePath in results.missing) {
            console.log(`[${path.basename(filePath)}] is missing:`);
            results.missing[filePath].forEach(key => console.log(`  - ${key}`));
        }
        console.log('');
    }

    console.log('--- Drifting Stars ---');
    if (Object.keys(results.drifting).length === 0) {
        console.log('  All common keys have identical values (no drifting stars).\n');
    } else {
        for (const key in results.drifting) {
            console.log(`${key}:`);
            for (const filePath in results.drifting[key]) {
                console.log(`  - ${path.basename(filePath)}: ${results.drifting[key][filePath]}`);
            }
        }
        console.log('');
    }

    console.log('--- Harmonized Stars ---');
    if (results.harmonized.length === 0) {
        console.log('  No perfectly aligned stars found.\n');
    } else {
        results.harmonized.forEach(key => console.log(`  - ${key}`));
        console.log('');
    }

    console.log('✨ Constellations checked. May your configurations be ever aligned! ✨\n');
}

async function main(args) {
    if (args.length < 2) {
        console.error('Usage: node src/index.js <path/to/env1> <path/to/env2> [path/to/env3 ...]');
        process.exit(1);
    }

    const filePaths = args;
    const configs = {};

    for (const filePath of filePaths) {
        try {
            const content = fs.readFileSync(filePath, 'utf8');
            configs[filePath] = parseEnvContent(content);
        } catch (error) {
            console.error(`Error reading file ${filePath}: ${error.message}`);
            process.exit(1);
        }
    }

    const results = compareConfigs(configs);
    printReport(filePaths, results);
}

// Only run main if this script is executed directly
if (require.main === module) {
    main(process.argv.slice(2));
}

module.exports = {
    parseEnvContent, // Export for testing
    compareConfigs,
    printReport, // Export for testing, though it prints to console
    main // Export main for testing CLI behavior
};
