const COSMIC_CONSTANT = 7; // A mystical number for our cosmic transmissions

function getCosmicPulses(message) {
    const pulses = [];
    const messageLength = message.length;
    for (let i = 0; i < message.length; i++) {
        const charCode = message.charCodeAt(i);
        // Whimsical modulation: add a value based on message length and cosmic constant
        const modulatedCode = charCode + (messageLength % COSMIC_CONSTANT) + (i % COSMIC_CONSTANT);
        pulses.push(modulatedCode);
    }
    return pulses.join(',');
}

function decodeCosmicPulses(pulsesString) {
    const pulses = pulsesString.split(',').map(Number);
    let decodedMessage = '';
    const messageLength = pulses.length; // Use pulse count as proxy for original message length

    for (let i = 0; i < pulses.length; i++) {
        const modulatedCode = pulses[i];
        // Reverse the whimsical modulation
        const originalCode = modulatedCode - (messageLength % COSMIC_CONSTANT) - (i % COSMIC_CONSTANT);
        decodedMessage += String.fromCharCode(originalCode);
    }
    return decodedMessage;
}

function main() {
    const args = process.argv.slice(2);
    if (args.length < 2) {
        console.error('Usage: node src/main.js <encode|decode> <message_or_pulses>');
        process.exit(1);
    }

    const command = args[0];
    const input = args.slice(1).join(' ');

    if (command === 'encode') {
        const cosmicPulses = getCosmicPulses(input);
        console.log(`Cosmic Pulses: ${cosmicPulses}`);
    } else if (command === 'decode') {
        const decodedMessage = decodeCosmicPulses(input);
        console.log(`Decoded Message: ${decodedMessage}`);
    } else {
        console.error(`Unknown command: ${command}. Use 'encode' or 'decode'.`);
        process.exit(1);
    }
}

main();
