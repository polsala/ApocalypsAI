const fs = require('fs');
const path = require('path');

/**
 * Scrubs a file's content based on provided options.
 * @param {string} filePath - Path to the input file.
 * @param {object} options - Scrubbing options.
 * @param {string} [options.outputFile] - Path to the output file. If not provided, prints to stdout.
 * @param {boolean} [options.removeComments=true] - Whether to remove lines starting with # or //. Default: true.
 * @param {boolean} [options.removeEmptyLines=true] - Whether to remove empty lines. Default: true.
 * @param {Array<string>} [options.redactPatterns=[]] - Array of regex strings to redact.
 * @param {string} [options.redactionPlaceholder='[REDACTED]'] - Placeholder for redacted content. Default: '[REDACTED]'.
 * @returns {string} The scrubbed content.
 */
function scrubFileContent(filePath, options = {}) {
    const {
        removeComments = true,
        removeEmptyLines = true,
        redactPatterns = [],
        redactionPlaceholder = '[REDACTED]'
    } = options;

    let content;
    try {
        content = fs.readFileSync(filePath, 'utf8');
    } catch (error) {
        throw new Error(`Failed to read file ${filePath}: ${error.message}`);
    }

    let lines = content.split(/\r?\n/);

    // Apply scrubbing rules
    lines = lines.map(line => {
        let processedLine = line;

        // Redact patterns first
        for (const pattern of redactPatterns) {
            try {
                const regex = new RegExp(pattern, 'g');
                processedLine = processedLine.replace(regex, redactionPlaceholder);
            } catch (e) {
                console.warn(`Warning: Invalid regex pattern '${pattern}' skipped. Error: ${e.message}`);
            }
        }

        return processedLine;
    });

    if (removeComments) {
        lines = lines.filter(line => {
            const trimmedLine = line.trim();
            return !(trimmedLine.startsWith('#') || trimmedLine.startsWith('//'));
        });
    }

    if (removeEmptyLines) {
        lines = lines.filter(line => line.trim() !== '');
    }

    const scrubbedContent = lines.join('\n');

    if (options.outputFile) {
        try {
            fs.writeFileSync(options.outputFile, scrubbedContent, 'utf8');
        } catch (error) {
            throw new Error(`Failed to write to output file ${options.outputFile}: ${error.message}`);
        }
    }

    return scrubbedContent;
}

module.exports = { scrubFileContent };
