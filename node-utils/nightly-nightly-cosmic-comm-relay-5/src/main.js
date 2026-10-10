const readline = require('readline');

// --- Configuration ---
const DEFAULT_DELAY_MS = 1000;
const COSMIC_DESTINATION = "Galactic Core";

// --- Helper Functions ---

/**
 * Simulates cosmic interference by randomly altering messages.
 * @param {string} message - The message to potentially interfere with.
 * @returns {string} The (possibly altered) message.
 */
function introduceCosmicInterference(message) {
    if (Math.random() < 0.3) { // 30% chance of interference
        const interferenceType = Math.floor(Math.random() * 3);
        switch (interferenceType) {
            case 0: // Garble characters
                return message.split('').map(char => String.fromCharCode(char.charCodeAt(0) + Math.floor(Math.random() * 5) - 2)).join('');
            case 1: // Add random noise
                return message + " [STATIC] " + Math.random().toString(36).substring(2, 7);
            case 2: // Reverse part of the message
                const splitPoint = Math.floor(message.length / 2);
                return message.substring(splitPoint) + "..." + message.substring(0, splitPoint);
        }
    }
    return message;
}

/**
 * Simulates sending a message to a cosmic destination.
 * @param {string} message - The message to send.
 * @param {number} delay - The delay before sending.
 * @param {boolean} interference - Whether to apply interference.
 * @returns {Promise<string>} A promise that resolves with the sent message.
 */
function sendMessage(message, delay, interference) {
    return new Promise((resolve) => {
        const processedMessage = interference ? introduceCosmicInterference(message) : message;
        console.log(`\u{1F680} Transmitting to ${COSMIC_DESTINATION}: "${processedMessage}" (ETA: ${delay}ms)`);
        setTimeout(() => {
            console.log(`\u{2708} Message arrived at ${COSMIC_DESTINATION}!`);
            resolve(processedMessage);
        }, delay);
    });
}

/**
 * Simulates receiving a message from the cosmos.
 * @param {number} delay - The delay before receiving.
 * @param {boolean} interference - Whether interference might have occurred.
 * @returns {Promise<string>} A promise that resolves with a received message.
 */
function receiveMessage(delay, interference) {
    return new Promise((resolve) => {
        console.log(`\u{1F30C} Listening for signals... (ETA: ${delay}ms)`);
        setTimeout(() => {
            const possibleMessages = [
                "All systems nominal.",
                "We are receiving your transmission.",
                "Unknown anomaly detected.",
                "The void whispers secrets.",
                "Is anyone out there?",
                "Cosmic dust is settling."
            ];
            let received = possibleMessages[Math.floor(Math.random() * possibleMessages.length)];
            if (interference) {
                received = introduceCosmicInterference(received);
            }
            console.log(`\u{1F4E1} Signal received: "${received}"`);
            resolve(received);
        }, delay);
    });
}

// --- Main Logic ---

async function runCosmicRelay(options) {
    const delay = options.delay || DEFAULT_DELAY_MS;
    const interference = options.interference || false;

    if (options.send) {
        await sendMessage(options.send, delay, interference);
        console.log("\u{1F504} Transmission complete. Exiting.");
        process.exit(0);
    }

    if (options.listen) {
        console.log("\u{1F30C} Cosmic Communication Relay initialized. Listening mode active.");
        while (true) {
            await receiveMessage(delay, interference);
        }
    }

    // Default behavior: send a greeting and then listen
    console.log("\u{1F30C} Cosmic Communication Relay initialized. Sending initial greeting...");
    await sendMessage("Hello from Earth! This is ApocalypsAI.", delay, interference);
    console.log("\u{1F30C} Relay is now listening for incoming signals.");
    while (true) {
        await receiveMessage(delay, interference);
    }
}

// --- Argument Parsing ---

function parseArgs() {
    const args = process.argv.slice(2);
    const options = {};

    for (let i = 0; i < args.length; i++) {
        const arg = args[i];
        if (arg === '--interference' || arg === '-i') {
            options.interference = true;
        } else if (arg === '--delay' && args[i + 1]) {
            options.delay = parseInt(args[i + 1], 10);
            i++; // Skip the next argument as it's the value
        } else if (arg === '--listen') {
            options.listen = true;
        } else if (arg === '--send' && args[i + 1]) {
            options.send = args[i + 1];
            i++; // Skip the next argument as it's the value
        }
    }
    return options;
}

const programOptions = parseArgs();

// --- Start the Relay ---

process.on('SIGINT', () => {
    console.log('\n\u{1F680} Cosmic transmission interrupted. Shutting down relay gracefully...');
    process.exit(0);
});

runCosmicRelay(programOptions).catch(err => {
    console.error("\u{1F525} A cosmic anomaly occurred:", err);
    process.exit(1);
});
