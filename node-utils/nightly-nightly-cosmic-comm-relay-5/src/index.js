#!/usr/bin/env node

const { program } = require('commander');

// --- Constants ---
const MESSAGE_PROBABILITY = 0.7; // Chance a message is successfully sent/received
const INTERFERENCE_CHANCE = 0.3; // Chance of cosmic interference when enabled
const MAX_MESSAGE_LENGTH = 100;
const GREETINGS = [
    "Hello from Sector 7G!",
    "Is anyone out there?",
    "Transmission received, over.",
    "Cosmic dust storm approaching.",
    "Starlight is fading.",
    "We are not alone."
];

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
 * Simulates a random cosmic event.
 * @returns {string|null} A simulated message or null if no event.
 */
function simulateCosmicEvent() {
    if (Math.random() < MESSAGE_PROBABILITY) {
        const randomIndex = getRandomInt(0, GREETINGS.length - 1);
        return GREETINGS[randomIndex];
    }
    return null;
}

/**
 * Simulates cosmic interference on a message.
 * @param {string} message - The original message.
 * @returns {string} The potentially garbled message.
 */
function introduceInterference(message) {
    if (Math.random() < INTERFERENCE_CHANCE) {
        const interferenceType = getRandomInt(0, 2);
        switch (interferenceType) {
            case 0: // Garble characters
                let garbled = '';
                for (let i = 0; i < message.length; i++) {
                    if (Math.random() < 0.5) {
                        garbled += String.fromCharCode(message.charCodeAt(i) + getRandomInt(-5, 5));
                    } else {
                        garbled += message[i];
                    }
                }
                return garbled.substring(0, MAX_MESSAGE_LENGTH);
            case 1: // Repeat message
                return `${message} ... ${message.substring(0, MAX_MESSAGE_LENGTH / 2)}`;
            case 2: // Add random noise
                const noise = "!@#$%^&*()_+=";
                let noisyMessage = '';
                for (let i = 0; i < message.length; i++) {
                    noisyMessage += message[i];
                    if (Math.random() < 0.2) {
                        noisyMessage += noise[getRandomInt(0, noise.length - 1)];
                    }
                }
                return noisyMessage.substring(0, MAX_MESSAGE_LENGTH);
            default:
                return message;
        }
    }
    return message;
}

// --- Commands ---

program
    .name('cosmic-relay')
    .description('A whimsical utility for interstellar communication.')
    .version('1.0.0');

program
    .command('send <message>')
    .description('Send a message into the cosmic void.')
    .action((message) => {
        console.log(`Attempting to send message: "${message}"`);
        if (Math.random() < MESSAGE_PROBABILITY) {
            console.log(`Message successfully transmitted to the void!`);
        } else {
            console.log(`Transmission failed. The void is silent... for now.`);
        }
    });

program
    .command('receive')
    .description('Listen for incoming cosmic transmissions.')
    .option('--interfere', 'Enable cosmic interference for unpredictable results.')
    .action((options) => {
        console.log("Listening for cosmic transmissions...");
        if (options.interfere) {
            console.log("Cosmic interference is active. Expect the unexpected!");
        }

        const intervalId = setInterval(() => {
            let receivedMessage = null;
            if (options.interfere && Math.random() < INTERFERENCE_CHANCE) {
                // Simulate a new, potentially garbled message due to interference
                const potentialMessage = simulateCosmicEvent();
                if (potentialMessage) {
                    receivedMessage = introduceInterference(potentialMessage);
                    console.log(`[INTERFERENCE DETECTED] Garbled transmission: "${receivedMessage}"`);
                } else {
                    // Interference might also cause silence or a false alarm
                    console.log("[INTERFERENCE DETECTED] Static crackles...");
                }
            } else {
                // Normal reception attempt
                receivedMessage = simulateCosmicEvent();
                if (receivedMessage) {
                    console.log(`Incoming transmission: "${receivedMessage}"`);
                }
            }
        }, getRandomInt(1000, 5000)); // Listen every 1-5 seconds

        // Handle interruption (Ctrl+C)
        process.on('SIGINT', () => {
            clearInterval(intervalId);
            console.log("\nCeasing cosmic listening. Until next time...");
            process.exit(0);
        });
    });

program.parse(process.argv);
