const crypto = require('crypto');

// In a real scenario, this would be a secure, shared secret.
// For this whimsical utility, it's hardcoded.
const SECRET_PASSPHRASE = 'apocalypse_is_a_cosmic_joke';

// Simulate a simple in-memory message queue
const messageQueue = [];

/**
 * Generates a consistent encryption key based on recipient ID and passphrase.
 * @param {string} recipientId - The ID of the recipient.
 * @returns {string} The derived encryption key.
 */
function deriveKey(recipientId) {
    const combined = recipientId + SECRET_PASSPHRASE;
    return crypto.createHash('sha256').update(combined).digest('hex').substring(0, 32); // 256-bit key
}

/**
 * Encrypts a message using AES-256-CBC.
 * @param {string} message - The plaintext message.
 * @param {string} key - The encryption key.
 * @returns {{iv: string, encryptedData: string}}
 */
function encryptMessage(message, key) {
    const iv = crypto.randomBytes(16);
    const cipher = crypto.createCipheriv('aes-256-cbc', Buffer.from(key, 'hex'), iv);
    let encrypted = cipher.update(message, 'utf8', 'hex');
    encrypted += cipher.final('hex');
    return { iv: iv.toString('hex'), encryptedData: encrypted };
}

/**
 * Decrypts a message using AES-256-CBC.
 * @param {string} encryptedData - The hex-encoded encrypted data.
 * @param {string} key - The encryption key.
 * @param {string} iv - The hex-encoded initialization vector.
 * @returns {string} The decrypted plaintext message.
 */
function decryptMessage(encryptedData, key, iv) {
    const decipher = crypto.createDecipheriv('aes-256-cbc', Buffer.from(key, 'hex'), Buffer.from(iv, 'hex'));
    let decrypted = decipher.update(encryptedData, 'hex', 'utf8');
    decrypted += decipher.final('utf8');
    return decrypted;
}

/**
 * Simulates signal degradation by flipping bits and dropping characters.
 * @param {string} message - The message to degrade.
 * @returns {string} The degraded message.
 */
function simulateSignalDegradation(message) {
    let degradedMessage = message;
    const degradationChance = Math.random(); // 0-1

    // Simulate character dropping
    if (degradationChance > 0.7) {
        const dropRate = Math.random() * 0.2; // Drop up to 20% of characters
        const charsToDrop = Math.floor(degradedMessage.length * dropRate);
        for (let i = 0; i < charsToDrop; i++) {
            const randomIndex = Math.floor(Math.random() * degradedMessage.length);
            degradedMessage = degradedMessage.slice(0, randomIndex) + degradedMessage.slice(randomIndex + 1);
        }
    }

    // Simulate bit flipping (represented by character substitution for simplicity)
    if (degradationChance > 0.5) {
        const flipRate = Math.random() * 0.1; // Flip up to 10% of characters
        const charsToFlip = Math.floor(degradedMessage.length * flipRate);
        let tempMessageArray = degradedMessage.split('');
        for (let i = 0; i < charsToFlip; i++) {
            const randomIndex = Math.floor(Math.random() * tempMessageArray.length);
            // Replace with a random character (simple substitution)
            const randomChar = String.fromCharCode(Math.floor(Math.random() * 95) + 32); // Printable ASCII range
            tempMessageArray[randomIndex] = randomChar;
        }
        degradedMessage = tempMessageArray.join('');
    }

    return degradedMessage;
}

/**
 * Sends a message to a recipient.
 * @param {string} recipientId - The ID of the recipient.
 * @param {string} message - The plaintext message.
 */
function sendMessage(recipientId, message) {
    const key = deriveKey(recipientId);
    const { iv, encryptedData } = encryptMessage(message, key);

    // Simulate transmission with degradation
    const transmittedData = simulateSignalDegradation(encryptedData);

    // Store the message in the queue for the recipient
    messageQueue.push({ recipientId, iv, encryptedData: transmittedData });
    console.log(`
🚀 Transmission initiated to ${recipientId}. Signal strength: ${Math.random().toFixed(2)}/1.00. Message encoded and sent!
`);
}

/**
 * Receives and decrypts messages for a given ID.
 * @param {string} myId - Your ID.
 */
function receiveMessages(myId) {
    console.log(`
📡 Scanning subspace for messages addressed to ${myId}...
`);
    const messagesForMe = messageQueue.filter(msg => msg.recipientId === myId);

    if (messagesForMe.length === 0) {
        console.log('🌌 No new transmissions detected. The void remains silent...
');
        return;
    }

    const key = deriveKey(myId);
    messagesForMe.forEach(msg => {
        try {
            const decryptedMessage = decryptMessage(msg.encryptedData, key, msg.iv);
            console.log(`✨ Incoming transmission from unknown source (via ${msg.recipientId}):`);
            console.log(`   Decrypted Payload: "${decryptedMessage}"
`);
            // Remove message from queue after processing
            const index = messageQueue.indexOf(msg);
            if (index > -1) {
                messageQueue.splice(index, 1);
            }
        } catch (error) {
            console.error(`❌ Transmission corrupted or invalid for ${myId}. Unable to decrypt.
`);
            // Optionally, keep corrupted messages or log them differently
        }
    });
}

module.exports = {
    sendMessage,
    receiveMessages,
    // For testing purposes
    _deriveKey: deriveKey,
    _encryptMessage: encryptMessage,
    _decryptMessage: decryptMessage,
    _simulateSignalDegradation: simulateSignalDegradation,
    _messageQueue: messageQueue // Expose for testing
};
