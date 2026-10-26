const { program } = require('commander');

/**
 * Simulates a delay with a random variation.
 * @param {number} baseDelay - The base delay in milliseconds.
 * @returns {Promise<void>}
 */
function simulateDelay(baseDelay) {
    const variation = Math.random() * baseDelay * 0.5; // +/- 25% variation
    const actualDelay = baseDelay + variation;
    return new Promise(resolve => setTimeout(resolve, actualDelay));
}

/**
 * Simulates potential message corruption or loss.
 * @param {number} errorRate - The probability of an error (0.0 to 1.0).
 * @returns {boolean} - True if an error occurred, false otherwise.
 */
function simulateCosmicInterference(errorRate) {
    return Math.random() < errorRate;
}

/**
 * Transmits a message with simulated intergalactic conditions.
 * @param {string} message - The message to transmit.
 * @param {number} baseDelay - The base delay in milliseconds.
 * @param {number} errorRate - The probability of an error.
 */
async function transmitMessage(message, baseDelay, errorRate) {
    console.log(`\n🚀 Initiating transmission of: "${message}"`);
    console.log(`  - Base delay set to: ${baseDelay}ms`);
    console.log(`  - Cosmic interference rate: ${errorRate * 100}%`);

    await simulateDelay(baseDelay);

    if (simulateCosmicInterference(errorRate)) {
        const interferenceType = Math.random() < 0.5 ? "corrupted" : "lost";
        console.log(`✨ Cosmic interference detected! Message was ${interferenceType}.`);
        if (interferenceType === "corrupted") {
            // Simple corruption: swap some characters
            let corruptedMessage = message.split('');
            if (corruptedMessage.length > 2) {
                const idx1 = Math.floor(Math.random() * corruptedMessage.length);
                let idx2 = Math.floor(Math.random() * corruptedMessage.length);
                while (idx2 === idx1) {
                    idx2 = Math.floor(Math.random() * corruptedMessage.length);
                }
                [corruptedMessage[idx1], corruptedMessage[idx2]] = [corruptedMessage[idx2], corruptedMessage[idx1]];
            }
            console.log(`  - Received garbled transmission: "${corruptedMessage.join('')}"`);
        } else {
            console.log("  - Transmission failed to arrive.");
        }
    } else {
        console.log(`✅ Transmission successful! Received: "${message}"`);
    }
    console.log("🌌 Transmission cycle complete.");
}

program
    .argument('<message>', 'The message to transmit')
    .option('-d, --delay <ms>', 'Base delay in milliseconds', '1000')
    .option('-e, --error-rate <rate>', 'Probability of message corruption/loss (0.0-1.0)', '0.05')
    .action((message, options) => {
        const baseDelay = parseInt(options.delay, 10);
        const errorRate = parseFloat(options.errorRate);

        if (isNaN(baseDelay) || baseDelay < 0) {
            console.error('Error: Invalid delay value. Must be a non-negative number.');
            process.exit(1);
        }
        if (isNaN(errorRate) || errorRate < 0 || errorRate > 1) {
            console.error('Error: Invalid error rate. Must be between 0.0 and 1.0.');
            process.exit(1);
        }

        transmitMessage(message, baseDelay, errorRate);
    });

program.parse(process.argv);
