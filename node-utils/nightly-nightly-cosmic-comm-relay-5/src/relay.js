const crypto = require('crypto');
const process = require('process');

// --- Configuration ---
const MAX_SIMULATED_DISTANCE = 100; // Light-years
const MIN_SIMULATED_DISTANCE = 1;   // Light-years
const DEFAULT_DEGRADATION_RATE = 0.01; // 1% chance of bit flip per character
const DEFAULT_DELAY_MULTIPLIER = 500; // ms per light-year for travel time

// --- Encryption/Decryption --- 
function encrypt(text, key) {
    const iv = crypto.randomBytes(16);
    const cipher = crypto.createCipheriv('aes-256-cbc', Buffer.from(key, 'utf8'), iv);
    let encrypted = cipher.update(text, 'utf8', 'hex');
    encrypted += cipher.final('hex');
    return `${iv.toString('hex')}:${encrypted}`;
}

function decrypt(text, key) {
    const parts = text.split(':');
    const iv = Buffer.from(parts.shift(), 'hex');
    const encryptedText = parts.join(':');
    const decipher = crypto.createDecipheriv('aes-256-cbc', Buffer.from(key, 'utf8'), iv);
    let decrypted = decipher.update(encryptedText, 'hex', 'utf8');
    decrypted += decipher.final('utf8');
    return decrypted;
}

// --- Signal Degradation ---
function degradeSignal(encryptedMessage, degradationRate) {
    if (degradationRate <= 0) return encryptedMessage;

    const messageBuffer = Buffer.from(encryptedMessage, 'hex');
    const degradedBuffer = Buffer.from(messageBuffer);

    for (let i = 0; i < degradedBuffer.length; i++) {
        for (let bit = 0; bit < 8; bit++) {
            if (Math.random() < degradationRate) {
                degradedBuffer[i] ^= (1 << bit); // Flip a random bit
            }
        }
    }
    return degradedBuffer.toString('hex');
}

// --- Message Storage (simulated) ---
// In a real scenario, this would be a database or persistent storage.
// For this utility, we'll use a simple in-memory array, keyed by arrival time.
const messageQueue = [];

// --- Command Line Argument Parsing ---
function parseArgs(args) {
    const result = {};
    for (let i = 0; i < args.length; i++) {
        if (args[i].startsWith('--')) {
            const key = args[i].substring(2);
            const value = (i + 1 < args.length && !args[i+1].startsWith('--')) ? args[++i] : true;
            result[key] = value;
        }
    }
    return result;
}

// --- Core Logic ---
async function sendMessage(options) {
    const { message, recipient, key, distance, degradationRate } = options;

    if (!message || !key) {
        console.error("Error: Message and key are required for sending.");
        process.exit(1);
    }

    const effectiveDistance = Math.max(MIN_SIMULATED_DISTANCE, Math.min(MAX_SIMULATED_DISTANCE, parseInt(distance || MIN_SIMULATED_DISTANCE)));
    const effectiveDegradationRate = Math.max(0, Math.min(1, parseFloat(degradationRate || DEFAULT_DEGRADATION_RATE)));

    const encryptedMessage = encrypt(message, key);
    const degradedEncryptedMessage = degradeSignal(encryptedMessage, effectiveDegradationRate);

    const travelTime = effectiveDistance * DEFAULT_DELAY_MULTIPLIER;
    const arrivalTime = Date.now() + travelTime;

    messageQueue.push({
        id: Date.now() + Math.random(), // Simple unique ID
        recipient: recipient || "Unknown Destination",
        encryptedMessage: degradedEncryptedMessage,
        arrivalTime: arrivalTime,
        originalDistance: effectiveDistance,
        degradationRate: effectiveDegradationRate
    });

    console.log(`Message sent to ${recipient || 'Unknown Destination'}!`);
    console.log(`  - Simulated Distance: ${effectiveDistance} light-years`);
    console.log(`  - Signal Degradation: ${effectiveDegradationRate * 100}%`);
    console.log(`  - Estimated Arrival: ${new Date(arrivalTime).toLocaleString()}`);
}

async function receiveMessage(options) {
    const { key } = options;

    if (!key) {
        console.error("Error: Key is required for receiving.");
        process.exit(1);
    }

    const currentTime = Date.now();
    const arrivedMessages = messageQueue.filter(msg => msg.arrivalTime <= currentTime);

    if (arrivedMessages.length === 0) {
        console.log("No messages have arrived yet. Keep waiting for cosmic signals...");
        return;
    }

    console.log(`\n--- Incoming Cosmic Transmissions (${arrivedMessages.length}) ---
`);

    arrivedMessages.forEach(msg => {
        try {
            const decryptedMessage = decrypt(msg.encryptedMessage, key);
            console.log(`From: ${msg.recipient} (Distance: ${msg.originalDistance} ly, Degradation: ${msg.degradationRate * 100}%)`);
            console.log(`  Message: ${decryptedMessage}`);
        } catch (e) {
            console.log(`From: ${msg.recipient} (Distance: ${msg.originalDistance} ly, Degradation: ${msg.degradationRate * 100}%)`);
            console.log(`  Message: [DEGRADED/UNREADABLE] - Could not decrypt. The cosmic winds may have scrambled it too much!`);
        }
        // Remove processed message from queue
        const index = messageQueue.indexOf(msg);
        if (index > -1) {
            messageQueue.splice(index, 1);
        }
    });
    console.log("\n--- End of Transmissions ---");
}

// --- Main Execution ---
async function main() {
    const args = parseArgs(process.argv.slice(2));
    const command = args._[0]; // Assuming the first argument is the command

    if (command === 'send') {
        await sendMessage(args);
    } else if (command === 'receive') {
        await receiveMessage(args);
    } else {
        console.log("Cosmic Comm Relay Usage:");
        console.log("  node src/relay.js send --message <msg> --recipient <dest> --key <key> [--distance <ly>] [--degradationRate <rate>] ");
        console.log("  node src/relay.js receive --key <key>");
        process.exit(1);
    }
}

main().catch(err => {
    console.error("A cosmic anomaly occurred:", err);
    process.exit(1);
});
