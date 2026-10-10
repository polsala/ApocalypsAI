/**
 * @typedef {object} RelayOptions
 * @property {[number, number]} delayRange - The range of possible delays in milliseconds.
 * @property {number} corruptionChance - The probability (0-1) of message corruption.
 */

/**
 * Simulates message corruption by randomly altering characters.
 * @param {string} message - The message to corrupt.
 * @param {number} corruptionChance - The probability of corruption.
 * @returns {string} The potentially corrupted message.
 */
function corruptMessage(message, corruptionChance) {
  if (Math.random() > corruptionChance) {
    return message;
  }

  let corrupted = message.split('');
  const corruptionType = Math.floor(Math.random() * 3);

  switch (corruptionType) {
    case 0: // Character substitution
      if (corrupted.length > 0) {
        const index = Math.floor(Math.random() * corrupted.length);
        const randomChar = String.fromCharCode(Math.floor(Math.random() * 95) + 32); // Printable ASCII
        corrupted[index] = randomChar;
      }
      break;
    case 1: // Character deletion
      if (corrupted.length > 1) {
        const index = Math.floor(Math.random() * corrupted.length);
        corrupted.splice(index, 1);
      }
      break;
    case 2: // Character insertion
      const index = Math.floor(Math.random() * (corrupted.length + 1));
      const randomChar = String.fromCharCode(Math.floor(Math.random() * 95) + 32); // Printable ASCII
      corrupted.splice(index, 0, randomChar);
      break;
  }

  return corrupted.join('');
}

/**
 * Simulates sending a message through a cosmic communication relay.
 * @param {string} message - The message to send.
 * @param {RelayOptions} [options] - Configuration options for the relay.
 * @returns {Promise<string>} A promise that resolves with the received message.
 */
async function send(message, options = {}) {
  const defaultOptions = {
    delayRange: [100, 2000],
    corruptionChance: 0.1
  };
  const mergedOptions = { ...defaultOptions, ...options };

  const [minDelay, maxDelay] = mergedOptions.delayRange;
  const delay = Math.floor(Math.random() * (maxDelay - minDelay + 1)) + minDelay;

  return new Promise(resolve => {
    setTimeout(() => {
      const finalMessage = corruptMessage(message, mergedOptions.corruptionChance);
      resolve(finalMessage);
    }, delay);
  });
}

module.exports = {
  send
};
