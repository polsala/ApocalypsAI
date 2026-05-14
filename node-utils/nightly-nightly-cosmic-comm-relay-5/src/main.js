/**
 * @typedef {object} CommunicationResult
 * @property {string} originalMessage - The message sent.
 * @property {string} receivedMessage - The message received after simulation.
 * @property {number} delayMs - The simulated communication delay in milliseconds.
 * @property {boolean} corrupted - Whether the message was corrupted.
 */

/**
 * Simulates cosmic communication delay and interference.
 * @param {string} message - The message to send.
 * @param {number} distance - The simulated distance in light-years.
 * @returns {CommunicationResult}
 */
function simulateCosmicCommunication(message, distance) {
  const MAX_DELAY_PER_LIGHT_YEAR_MS = 50;
  const CORRUPTION_CHANCE_PER_LIGHT_YEAR = 0.005;

  const delayMs = Math.min(distance * MAX_DELAY_PER_LIGHT_YEAR_MS, 5000); // Cap delay
  const corruptionChance = Math.min(distance * CORRUPTION_CHANCE_PER_LIGHT_YEAR, 0.5); // Cap corruption chance

  let receivedMessage = message;
  let corrupted = false;

  // Simulate corruption
  if (Math.random() < corruptionChance) {
    corrupted = true;
    let corruptedMessageArray = message.split('');
    const numCharsToCorrupt = Math.floor(Math.random() * (corruptedMessageArray.length / 2)) + 1;

    for (let i = 0; i < numCharsToCorrupt; i++) {
      const randomIndex = Math.floor(Math.random() * corruptedMessageArray.length);
      const corruptionType = Math.floor(Math.random() * 3);

      switch (corruptionType) {
        case 0: // Replace character
          const randomChar = String.fromCharCode(97 + Math.floor(Math.random() * 26)); // lowercase a-z
          corruptedMessageArray[randomIndex] = randomChar;
          break;
        case 1: // Delete character
          corruptedMessageArray.splice(randomIndex, 1);
          break;
        case 2: // Swap characters (if possible)
          if (randomIndex + 1 < corruptedMessageArray.length) {
            [corruptedMessageArray[randomIndex], corruptedMessageArray[randomIndex + 1]] = [corruptedMessageArray[randomIndex + 1], corruptedMessageArray[randomIndex]];
          } else if (randomIndex - 1 >= 0) {
            [corruptedMessageArray[randomIndex], corruptedMessageArray[randomIndex - 1]] = [corruptedMessageArray[randomIndex - 1], corruptedMessageArray[randomIndex]];
          }
          break;
      }
    }
    receivedMessage = corruptedMessageArray.join('');
  }

  return {
    originalMessage: message,
    receivedMessage: receivedMessage,
    delayMs: delayMs,
    corrupted: corrupted
  };
}

// Example Usage:
if (process.argv.length > 3) {
  const message = process.argv[2];
  const distance = parseInt(process.argv[3], 10);

  if (!isNaN(distance)) {
    const result = simulateCosmicCommunication(message, distance);
    console.log("--- Cosmic Communication Relay ---");
    console.log(`Original Message: "${result.originalMessage}"`);
    console.log(`Simulated Distance: ${distance} light-years`);
    console.log(`Simulated Delay: ${result.delayMs} ms`);
    console.log(`Message Corrupted: ${result.corrupted ? 'Yes' : 'No'}`);
    console.log(`Received Message: "${result.receivedMessage}"`);
    console.log("----------------------------------");
  } else {
    console.error("Error: Distance must be a valid number.");
    process.exit(1);
  }
} else {
  console.error("Usage: node src/main.js <message> <distance_in_light_years>");
  process.exit(1);
}

module.exports = { simulateCosmicCommunication };
