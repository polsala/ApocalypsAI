const readline = require('readline');

// --- Configuration ---
const TRANSMISSION_DELAY_MIN = 1000; // Minimum delay in ms for transmission
const TRANSMISSION_DELAY_MAX = 5000; // Maximum delay in ms for transmission
const SIGNAL_DEGRADATION_CHANCE_DEFAULT = 0; // Default chance of signal degradation (0-100)

// --- Helper Functions ---

/**
 * Generates a random integer between min (inclusive) and max (inclusive).
 * @param {number} min - The minimum value.
 * @param {number} max - The maximum value.
 * @returns {number} A random integer.
 */
function getRandomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

/**
 * Simulates signal degradation for a message.
 * @param {string} message - The message to potentially degrade.
 * @param {number} degradationChance - The percentage chance of degradation (0-100).
 * @returns {string} The potentially degraded message.
 */
function degradeSignal(message, degradationChance) {
    if (Math.random() * 100 < degradationChance) {
        const corruptionType = getRandomInt(0, 2);
        switch (corruptionType) {
            case 0: // Character swap
                if (message.length > 1) {
                    const idx1 = getRandomInt(0, message.length - 1);
                    let idx2 = getRandomInt(0, message.length - 1);
                    while (idx1 === idx2) {
                        idx2 = getRandomInt(0, message.length - 1);
                    }
                    const chars = message.split('');
                    [chars[idx1], chars[idx2]] = [chars[idx2], chars[idx1]];
                    return chars.join('') + " (Signal Scrambled!)";
                }
                break;
            case 1: // Character deletion
                if (message.length > 0) {
                    const idx = getRandomInt(0, message.length - 1);
                    return message.slice(0, idx) + message.slice(idx + 1) + " (Signal Lost a Bit!)";
                }
                break;
            case 2: // Gibberish insertion
                const gibberish = ['blip', 'bloop', 'zzzt', 'whirr'];
                const insertPos = getRandomInt(0, message.length);
                return message.slice(0, insertPos) + gibberish[getRandomInt(0, gibberish.length - 1)] + message.slice(insertPos) + " (Cosmic Static!)";
        }
    }
    return message;
}

/**
 * Simulates sending a message across the cosmos.
 * @param {string} message - The message to send.
 * @param {number} degradationChance - The percentage chance of signal degradation.
 * @returns {Promise<string>} A promise that resolves with the received message.
 */
function sendMessage(message, degradationChance) {
    return new Promise((resolve, reject) => {
        const delay = getRandomInt(TRANSMISSION_DELAY_MIN, TRANSMISSION_DELAY_MAX);
        console.log(`\n🚀 Transmitting message: "${message}" (ETA: ${delay / 1000} light-seconds)...`);

        setTimeout(() => {
            const receivedMessage = degradeSignal(message, degradationChance);
            if (receivedMessage.includes('Lost a Bit') || receivedMessage.includes('Static')) {
                console.log(`📡 Received garbled transmission: "${receivedMessage}"`);
                resolve(`Received garbled: "${receivedMessage}"`);
            } else if (receivedMessage.includes('Scrambled')) {
                console.log(`📡 Received scrambled transmission: "${receivedMessage}"`);
                resolve(`Received scrambled: "${receivedMessage}"`);
            } else {
                console.log(`✨ Successfully received message: "${receivedMessage}"`);
                resolve(`Received: "${receivedMessage}"`);
            }
        }, delay);
    });
}

/**
 * Simulates listening for incoming cosmic transmissions.
 * @param {number} degradationChance - The percentage chance of signal degradation.
 */
async function listenForTransmissions(degradationChance) {
    console.log(`
🌌 Listening for cosmic transmissions... (Signal degradation: ${degradationChance}%)
`);
    const sampleMessages = [
        "Greetings, Earthlings!",
        "Is anyone out there?",
        "We come in peace... mostly.",
        "Your planet has excellent Wi-Fi.",
        "Send more snacks.",
        "The nebula is singing tonight.",
        "Beware the sentient dust bunnies."
    ];

    // Simulate receiving a few random messages over time
    for (let i = 0; i < 3; i++) {
        const randomMessage = sampleMessages[getRandomInt(0, sampleMessages.length - 1)];
        await sendMessage(randomMessage, degradationChance);
    }
    console.log("\n🌠 No more transmissions detected for now. The void is quiet...");
}

// --- Main Execution ---

function parseArgs() {
    const args = process.argv.slice(2);
    let degradationChance = SIGNAL_DEGRADATION_CHANCE_DEFAULT;

    for (let i = 0; i < args.length; i++) {
        if (args[i] === '--degrade' && args[i+1]) {
            const percentage = parseInt(args[i+1], 10);
            if (!isNaN(percentage) && percentage >= 0 && percentage <= 100) {
                degradationChance = percentage;
            } else {
                console.warn(`Warning: Invalid degradation percentage '${args[i+1]}'. Using default ${SIGNAL_DEGRADATION_CHANCE_DEFAULT}%.`);
            }
            i++; // Skip the next argument as it's the value
        }
    }
    return { degradationChance };
}

async function main() {
    const { degradationChance } = parseArgs();
    await listenForTransmissions(degradationChance);
}

main().catch(err => {
    console.error("\n💥 An unexpected cosmic anomaly occurred:", err);
});
