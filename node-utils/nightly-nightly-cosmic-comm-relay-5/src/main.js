const MIN_DELAY_MS = 500;
const MAX_DELAY_MS = 5000;
const CORRUPTION_CHANCE = 0.3; // 30% chance of corruption
const MESSAGES_TO_SEND = 5;

/**
 * Simulates a random delay.
 * @returns {Promise<void>}
 */
function simulateDelay() {
  const delay = Math.floor(Math.random() * (MAX_DELAY_MS - MIN_DELAY_MS + 1)) + MIN_DELAY_MS;
  return new Promise(resolve => setTimeout(resolve, delay));
}

/**
 * Simulates cosmic message corruption.
 * @param {string} message - The original message.
 * @returns {string} The potentially corrupted message.
 */
function corruptMessage(message) {
  if (Math.random() < CORRUPTION_CHANCE) {
    let corrupted = '';
    for (let i = 0; i < message.length; i++) {
      if (Math.random() < 0.1) { // 10% chance to alter a character
        const charCode = message.charCodeAt(i);
        // Simple alteration: shift character code slightly
        const alteredCharCode = charCode + (Math.random() < 0.5 ? 1 : -1);
        corrupted += String.fromCharCode(alteredCharCode);
      } else {
        corrupted += message[i];
      }
    }
    return corrupted;
  }
  return message;
}

/**
 * Simulates sending and receiving a message with cosmic effects.
 * @param {string} message - The message to send.
 * @returns {Promise<void>}
 */
async function relayMessage(message) {
  console.log(`Sending message: "${message}"`);
  await simulateDelay();
  const receivedMessage = corruptMessage(message);
  const delay = Math.floor(Math.random() * (MAX_DELAY_MS - MIN_DELAY_MS + 1)) + MIN_DELAY_MS; // Re-simulate delay for reporting
  console.log(`Received message: "${receivedMessage}" after ${delay}ms delay.`);
  console.log(''); // Add a blank line for readability
}

/**
 * Main function to run the cosmic communication simulation.
 */
async function runSimulation() {
  const sampleMessages = [
    "Greetings from Sector 7G!",
    "Report status: All clear.",
    "Encountered anomaly in Nebula X.",
    "Requesting warp core diagnostics.",
    "Is anyone out there?",
    "The void whispers secrets."
  ];

  console.log("--- Initiating Cosmic Communication Relay ---");
  console.log("\n");

  for (let i = 0; i < MESSAGES_TO_SEND; i++) {
    const message = sampleMessages[i % sampleMessages.length];
    await relayMessage(message);
  }

  console.log("--- Cosmic Communication Relay Complete ---");
}

runSimulation();
