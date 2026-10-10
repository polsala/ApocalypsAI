const process = require('process');

/**
 * Simulates a cosmic delay for a message.
 * @param {string} message - The message to send.
 * @param {number} minDelay - Minimum delay in milliseconds.
 * @param {number} maxDelay - Maximum delay in milliseconds.
 * @param {number} interferenceChance - Probability of interference (0-100).
 * @returns {Promise<string>} A promise that resolves with the processed message.
 */
async function relayMessage(message, minDelay = 1000, maxDelay = 5000, interferenceChance = 20) {
    const delay = Math.floor(Math.random() * (maxDelay - minDelay + 1)) + minDelay;
    console.log(`\n🚀 Initiating cosmic transmission...`);
    console.log(`   Original Message: "${message}"`);
    console.log(`   Estimated travel time: ${delay}ms`);

    await new Promise(resolve => setTimeout(resolve, delay));

    let finalMessage = message;
    const interferenceRoll = Math.random() * 100;

    if (interferenceRoll < interferenceChance) {
        console.log(`   ⚠️ Cosmic interference detected! Signal is a bit fuzzy...`);
        // Simulate interference by randomly changing a character or adding/removing one
        const interferenceType = Math.floor(Math.random() * 3);
        if (interferenceType === 0 && finalMessage.length > 0) {
            // Replace a random character
            const index = Math.floor(Math.random() * finalMessage.length);
            const randomChar = String.fromCharCode(97 + Math.floor(Math.random() * 26)); // lowercase a-z
            finalMessage = finalMessage.substring(0, index) + randomChar + finalMessage.substring(index + 1);
        } else if (interferenceType === 1) {
            // Add a random character
            const index = Math.floor(Math.random() * (finalMessage.length + 1));
            const randomChar = String.fromCharCode(97 + Math.floor(Math.random() * 26));
            finalMessage = finalMessage.substring(0, index) + randomChar + finalMessage.substring(index);
        } else if (interferenceType === 2 && finalMessage.length > 1) {
            // Remove a random character
            const index = Math.floor(Math.random() * finalMessage.length);
            finalMessage = finalMessage.substring(0, index) + finalMessage.substring(index + 1);
        }
    }

    console.log(`✨ Message received at destination!`);
    console.log(`   Final Message: "${finalMessage}"`);
    return finalMessage;
}

function parseArgs() {
    const args = process.argv.slice(2);
    let message = "";
    let minDelay = 1000;
    let maxDelay = 5000;
    let interferenceChance = 20;

    for (let i = 0; i < args.length; i++) {
        if (args[i] === '--delay-range' && i + 1 < args.length) {
            const range = args[++i].split(',');
            if (range.length === 2) {
                minDelay = parseInt(range[0], 10);
                maxDelay = parseInt(range[1], 10);
            }
        } else if (args[i] === '--interference-chance' && i + 1 < args.length) {
            interferenceChance = parseInt(args[++i], 10);
        } else {
            message = args[i];
        }
    }

    if (!message) {
        console.error("Error: Message is required.");
        console.log("Usage: node src/main.js <message> [--delay-range <min>,<max>] [--interference-chance <percentage>]");
        process.exit(1);
    }

    return { message, minDelay, maxDelay, interferenceChance };
}

async function main() {
    const { message, minDelay, maxDelay, interferenceChance } = parseArgs();
    await relayMessage(message, minDelay, maxDelay, interferenceChance);
}

main().catch(err => {
    console.error("An unexpected cosmic anomaly occurred:", err);
    process.exit(1);
});
