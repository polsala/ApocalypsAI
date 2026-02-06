const yargs = require('yargs');

/**
 * Applies distortion to a message based on truncation and word replacements.
 * @param {string} message - The input message.
 * @param {number} truncationFactor - Factor (0-1) to reduce message length.
 * @param {Object.<string, string>} replacements - Map of words to replace.
 * @returns {string} The distorted message.
 */
function applyDistortion(message, truncationFactor, replacements) {
    let words = message.split(/\s+/);

    // 1. Apply truncation
    const newLength = Math.max(1, Math.floor(words.length * truncationFactor));
    words = words.slice(0, newLength);

    // 2. Apply word replacements
    const processedWords = words.map(word => {
        // Strip trailing punctuation for matching, but keep original word for replacement if no match
        const cleanedWord = word.replace(/[.,!?;:]+$/, '').toLowerCase();
        for (const key in replacements) {
            if (cleanedWord === key.toLowerCase()) {
                // Simple replacement. Original punctuation on the word is lost.
                return replacements[key];
            }
        }
        return word;
    });

    return processedWords.join(' ');
}

/**
 * Simulates a message passing through a whisper network.
 * @param {string} initialMessage - The starting message.
 * @param {number} hops - Number of times the message is processed.
 * @param {number} truncationFactor - Factor (0-1) to reduce message length at each hop.
 * @param {Object.<string, string>} replacements - Map of words to replace.
 */
function simulateWhisper(initialMessage, hops, truncationFactor, replacements) {
    let currentMessage = initialMessage;
    console.log(`--- Initial Message ---\n${currentMessage}\n`);

    for (let i = 1; i <= hops; i++) {
        currentMessage = applyDistortion(currentMessage, truncationFactor, replacements);
        console.log(`--- Hop ${i} ---\n${currentMessage}\n`);
    }
}

// CLI setup
if (require.main === module) {
    const argv = yargs
        .option('message', {
            alias: 'm',
            description: 'The initial message to propagate.',
            type: 'string',
            demandOption: true,
        })
        .option('hops', {
            alias: 'h',
            description: 'The number of times the message will be processed.',
            type: 'number',
            default: 5,
        })
        .option('truncationFactor', {
            alias: 't',
            description: 'A decimal between 0 and 1. At each hop, the message\'s word count will be multiplied by this factor.',
            type: 'number',
            default: 0.9,
            check: (num) => {
                if (num >= 0 && num <= 1) return true;
                throw new Error('truncationFactor must be between 0 and 1.');
            },
        })
        .option('replacements', {
            alias: 'r',
            description: 'A JSON string representing a map of words to replace. E.g., \'{\"old\":\"ancient\", \"city\":\"town\"}\'.',
            type: 'string',
            default: '{}',
            coerce: (jsonString) => {
                try {
                    return JSON.parse(jsonString);
                } catch (e) {
                    throw new Error('replacements must be a valid JSON string.');
                }
            },
        })
        .help()
        .alias('help', 'H')
        .argv;

    simulateWhisper(argv.message, argv.hops, argv.truncationFactor, argv.replacements);
}

// Export for testing
module.exports = {
    applyDistortion,
    simulateWhisper
};
