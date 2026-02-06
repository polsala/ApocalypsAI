#!/usr/bin/env node

const fs = require('fs').promises;
const path = require('path');

/**
 * Cleanses text content by removing digital dust.
 * - Trims leading/trailing whitespace from each line.
 * - Reduces multiple consecutive empty lines to a single empty line.
 * - Removes non-printable ASCII characters (0x00-0x1F and 0x7F-0x9F).
 * @param {string} content - The input text content.
 * @returns {string} The purified text content.
 */
function purifyText(content) {
    const lines = content.split(/\r?\n/); // Handle both \n and \r\n
    const purifiedLines = [];
    let lastLineWasEmpty = false;

    for (const line of lines) {
        const trimmedLine = line.trim();
        // Remove non-printable ASCII characters
        const cleanedLine = trimmedLine.replace(/[\x00-\x1F\x7F-\x9F]/g, '');

        if (cleanedLine === '') {
            if (!lastLineWasEmpty) {
                purifiedLines.push('');
                lastLineWasEmpty = true;
            }
        } else {
            purifiedLines.push(cleanedLine);
            lastLineWasEmpty = false;
        }
    }

    // The logic above correctly handles leading/trailing empty lines by reducing them to a single one.
    // If the input is entirely empty lines, it will result in a single empty line.
    return purifiedLines.join('\n');
}

async function main() {
    const args = process.argv.slice(2);

    if (args.length < 1 || args.length > 2) {
        console.error('Usage: node src/index.js <input_file_path> [output_file_path]');
        process.exit(1);
    }

    const inputFilePath = args[0];
    const outputFilePath = args[1];

    try {
        const rawContent = await fs.readFile(inputFilePath, 'utf8');
        const purifiedContent = purifyText(rawContent);

        if (outputFilePath) {
            await fs.writeFile(outputFilePath, purifiedContent, 'utf8');
            console.log(`Purified content saved to: ${outputFilePath}`);
        } else {
            console.log(purifiedContent);
        }
    } catch (error) {
        console.error(`Error purifying file: ${error.message}`);
        process.exit(1);
    }
}

// Only run main if this script is executed directly
if (require.main === module) {
    main();
}

// Export for testing
module.exports = { purifyText, main };
