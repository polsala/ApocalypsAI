const { program } = require('commander');

/**
 * Simulates a random delay.
 * @param {number} ms - The delay in milliseconds.
 * @returns {Promise<void>}
 */
function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Corrupts a message based on the specified type and probability.
 * @param {string} message - The message to corrupt.
 * @param {object} options - Corruption options.
 * @param {number} options.corruptionProbability - The probability of corruption (0.0 to 1.0).
 * @param {'substitute' | 'delete' | 'insert'} options.corruptionType - The type of corruption.
 * @returns {string} The potentially corrupted message.
 */
function corruptMessage(message, options) {
    if (Math.random() > options.corruptionProbability) {
        return message;
    }

    let corrupted = message.split('');
    const alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+';

    switch (options.corruptionType) {
        case 'substitute':
            if (corrupted.length === 0) return message;
            const subIndex = Math.floor(Math.random() * corrupted.length);
            corrupted[subIndex] = alphabet[Math.floor(Math.random() * alphabet.length)];
            break;
        case 'delete':
            if (corrupted.length === 0) return message;
            const delIndex = Math.floor(Math.random() * corrupted.length);
            corrupted.splice(delIndex, 1);
            break;
        case 'insert':
            const insIndex = Math.floor(Math.random() * (corrupted.length + 1));
            corrupted.splice(insIndex, 0, alphabet[Math.floor(Math.random() * alphabet.length)]);
            break;
        default:
            // No corruption if type is unknown
            return message;
    }

    return corrupted.join('');
}

/**
 * Sends a message with simulated cosmic delays and corruption.
 * @param {string} message - The message to send.
 * @param {object} [options] - Optional configuration.
 * @param {number} [options.delay=100] - Base delay in milliseconds.
 * @param {number} [options.corruptionProbability=0.05] - Probability of corruption (0.0 to 1.0).
 * @param {'substitute' | 'delete' | 'insert'} [options.corruptionType='substitute'] - Type of corruption.
 * @returns {Promise<string>} The received message.
 */
async function sendCosmicMessage(message, options = {}) {
    const defaultOptions = {
        delay: 100,
        corruptionProbability: 0.05,
        corruptionType: 'substitute'
    };
    const mergedOptions = { ...defaultOptions, ...options };

    // Simulate travel time
    await delay(mergedOptions.delay + Math.random() * 500); // Add some jitter

    // Simulate potential signal degradation
    const receivedMessage = corruptMessage(message, mergedOptions);

    return receivedMessage;
}

// CLI setup
program
    .argument('<message>', 'The message to send')
    .option('-d, --delay <ms>', 'Base delay in milliseconds', '100')
    .option('-c, --corruption <prob>', 'Probability of message corruption (0.0 to 1.0)', '0.05')
    .option('-t, --type <type>', 'Type of corruption (substitute, delete, insert)', 'substitute')
    .action(async (message, opts) => {
        const options = {
            delay: parseInt(opts.delay, 10),
            corruptionProbability: parseFloat(opts.corruption),
            corruptionType: opts.type
        };

        if (isNaN(options.delay) || options.delay < 0) {
            console.error('Invalid delay value. Must be a non-negative number.');
            process.exit(1);
        }
        if (isNaN(options.corruptionProbability) || options.corruptionProbability < 0 || options.corruptionProbability > 1) {
            console.error('Invalid corruption probability. Must be between 0.0 and 1.0.');
            process.exit(1);
        }
        if (!['substitute', 'delete', 'insert'].includes(options.corruptionType)) {
            console.error('Invalid corruption type. Must be "substitute", "delete", or "insert".');
            process.exit(1);
        }

        try {
            console.log(`Sending: "${message}"`);
            const received = await sendCosmicMessage(message, options);
            console.log(`Received: "${received}"`);
        } catch (error) {
            console.error(`Error sending message: ${error.message}`);
            process.exit(1);
        }
    });

if (process.argv.length === 2) {
    // If no arguments are provided, show help
    program.help();
} else {
    program.parse(process.argv);
}

module.exports = { sendCosmicMessage };
