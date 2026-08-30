// src/parser.js

/**
 * Parses a string content of an .env file into a key-value object.
 * Handles basic key=value pairs, ignoring comments and empty lines.
 * @param {string} content The content of the .env file.
 * @returns {Object.<string, string>} A dictionary of environment variables.
 */
function parseEnvContent(content) {
    const env = {};
    const lines = content.split('\n');

    for (const line of lines) {
        const trimmedLine = line.trim();
        if (trimmedLine.length === 0 || trimmedLine.startsWith('#')) {
            continue; // Skip empty lines and comments
        }

        const parts = trimmedLine.split('=');
        if (parts.length >= 2) {
            const key = parts[0].trim();
            // Join the rest of the parts in case the value contains '='
            const value = parts.slice(1).join('=').trim();
            env[key] = value;
        }
    }
    return env;
}

module.exports = { parseEnvContent };
