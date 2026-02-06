const process = require('process');
const { program } = require('commander');

/**
 * Simulates cosmic static by randomly corrupting characters in a string.
 * @param {string} message The message to corrupt.
 * @param {number} chance The probability (0-1) of a character being corrupted.
 * @returns {string} The corrupted message.
 */
function introduceCosmicStatic(message, chance) {
    let corruptedMessage = '';
    for (let i = 0; i < message.length; i++) {
        const char = message[i];
        if (Math.random() < chance) {
            // Replace with a random printable ASCII character (excluding space for simplicity)
            const randomCharCode = Math.floor(Math.random() * 94) + 33;
            corruptedMessage += String.fromCharCode(randomCharCode);
        } else {
            corruptedMessage += char;
        }
    }
    return corruptedMessage;
}

/**
 * Simulates signal degradation, potentially returning a degraded version of the message.
 * @param {string} message The message to potentially degrade.
 * @param {number} chance The probability (0-1) of degradation occurring.
 * @returns {string} The potentially degraded message.
 */
function simulateSignalDegradation(message, chance) {
    if (Math.random() < chance) {
        // Simulate degradation by replacing some characters with '?' or similar
        let degradedMessage = '';
        for (let i = 0; i < message.length; i++) {
            if (Math.random() < 0.3) { // 30% chance of a character being replaced
                degradedMessage += '?';
            } else {
                degradedMessage += message[i];
            }
        }
        return degradedMessage;
    }
    return message;
}

/**
 * Relays a message with simulated cosmic effects and delay.
 * @param {string} message The message to relay.
 * @param {object} options Configuration options.
 */
async function relayMessage(message, options) {
    const { delay, staticChance, degradation } = options;
    const prefix = options.prefix || '[Galactic Dispatch] ';
    const suffix = options.suffix || ' [End Transmission]';

    console.log(`${prefix}Transmitting...`);

    let processedMessage = message;
    processedMessage = introduceCosmicStatic(processedMessage, staticChance);
    processedMessage = simulateSignalDegradation(processedMessage, degradation);

    await new Promise(resolve => setTimeout(resolve, delay));

    console.log(`${prefix}Received: ${processedMessage}${suffix}`);
}

program
    .argument('<message>', 'The message to relay')
    .option('-d, --delay <ms>', 'Transmission delay in milliseconds', '500')
    .option('-s, --static-chance <0-1>', 'Probability of character corruption by static', '0.05')
    .option('-g, --degradation <0-1>', 'Probability of signal degradation', '0.1')
    .option('-p, --prefix <string>', 'Custom message prefix', '[Galactic Dispatch] ')
    .option('-x, --suffix <string>', 'Custom message suffix', ' [End Transmission]')
    .action((message, options) => {
        // Ensure numeric options are parsed correctly
        options.delay = parseInt(options.delay, 10);
        options.staticChance = parseFloat(options.staticChance);
        options.degradation = parseFloat(options.degradation);

        // Basic validation for probability ranges
        if (options.staticChance < 0 || options.staticChance > 1) {
            console.error('Error: --static-chance must be between 0 and 1.');
            process.exit(1);
        }
        if (options.degradation < 0 || options.degradation > 1) {
            console.error('Error: --degradation must be between 0 and 1.');
            process.exit(1);
        }

        relayMessage(message, options).catch(err => {
            console.error('An error occurred during transmission:', err);
            process.exit(1);
        });
    });

program.parse(process.argv);

// If no arguments are provided, show help
if (process.argv.length <= 2) {
    program.help();
}
