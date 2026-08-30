/**
 * @typedef {object} CosmicCommRelayOptions
 * @property {number} [baseDelayMs=500] - The base delay for messages in milliseconds.
 * @property {number} [delayVariance=200] - The maximum additional random delay in milliseconds.
 * @property {number} [corruptionChance=0.1] - The probability (0.0 to 1.0) that any given character will be corrupted.
 */

/**
 * Simulates intergalactic communication delays and message corruption.
 */
class CosmicCommRelay {
  /**
   * @param {CosmicCommRelayOptions} [options={}]
   */
  constructor(options = {}) {
    this.baseDelayMs = options.baseDelayMs ?? 500;
    this.delayVariance = options.delayVariance ?? 200;
    this.corruptionChance = options.corruptionChance ?? 0.1;
  }

  /**
   * Simulates sending a message through the cosmic relay.
   * @param {string} message - The message to send.
   * @returns {Promise<string>} A promise that resolves with the received (potentially corrupted) message.
   */
  async send(message) {
    const delay = this.baseDelayMs + Math.random() * this.delayVariance;
    await new Promise(resolve => setTimeout(resolve, delay));

    let corruptedMessage = '';
    for (const char of message) {
      if (Math.random() < this.corruptionChance) {
        // Corrupt the character: replace with a random printable ASCII character
        const randomCharCode = Math.floor(Math.random() * 95) + 32; // ASCII 32-126
        corruptedMessage += String.fromCharCode(randomCharCode);
      } else {
        corruptedMessage += char;
      }
    }
    return corruptedMessage;
  }
}

module.exports = { CosmicCommRelay };
