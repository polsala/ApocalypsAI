/**
 * Generates a pseudo-random sequence based on input length.
 * # Mock rationale: This function is deterministic and relies only on its input.
 * @param {number} length - The desired length of the sequence.
 * @returns {number[]} An array of numbers.
 */
function pseudoRandomSequence(length) {
  const sequence = [];
  let seed = length * 13 + 7;
  for (let i = 0; i < length; i++) {
    seed = (seed * 1664525 + 101390423) % 4294967296; // LCG parameters
    sequence.push(seed % 256);
  }
  return sequence;
}

/**
 * A simple prime number lookup for character mapping.
 * # Mock rationale: This is a fixed lookup table.
 */
const primes = [
  2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97,
  101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199,
  211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331,
  337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457,
  461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599,
  601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733,
  739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877,
  881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997
];

/**
 * Maps a character to a unique cosmic frequency pattern.
 * # Mock rationale: This function is deterministic and relies on fixed lookups.
 * @param {string} char - The character to map.
 * @param {number} index - The index of the character in the original message.
 * @returns {string} The cosmic frequency pattern.
 */
function charToCosmicFrequency(char, index) {
  const charCode = char.charCodeAt(0);
  const seq = pseudoRandomSequence(1);
  const primeIndex = (charCode + seq[0]) % primes.length;
  const prime = primes[primeIndex];
  const offset = (index * 3 + seq[0]) % 100; // Add some variation based on index
  return `${prime}-${offset}`;
}

/**
 * Encodes a message into a cosmic frequency string.
 * @param {string} message - The message to encode.
 * @returns {string} The encoded cosmic frequency string.
 */
function encodeMessage(message) {
  if (!message) return "";
  const encodedParts = [];
  for (let i = 0; i < message.length; i++) {
    encodedParts.push(charToCosmicFrequency(message[i], i));
  }
  return encodedParts.join('|');
}

/**
 * Decodes a cosmic frequency string back into a message.
 * @param {string} cosmicString - The cosmic frequency string to decode.
 * @returns {string} The decoded message.
 */
function decodeMessage(cosmicString) {
  if (!cosmicString) return "";
  const parts = cosmicString.split('|');
  let decodedMessage = "";

  for (let i = 0; i < parts.length; i++) {
    const [primeStr, offsetStr] = parts[i].split('-');
    const prime = parseInt(primeStr, 10);
    const offset = parseInt(offsetStr, 10);

    // Find the character code that maps to this prime and offset
    // This is a reverse lookup, which is computationally more intensive
    // but necessary for decoding.
    let foundCharCode = -1;
    for (let charCode = 0; charCode < 256; charCode++) {
      const seq = pseudoRandomSequence(1);
      const primeIndex = (charCode + seq[0]) % primes.length;
      const currentPrime = primes[primeIndex];
      const currentOffset = (i * 3 + seq[0]) % 100;

      if (currentPrime === prime && currentOffset === offset) {
        foundCharCode = charCode;
        break;
      }
    }

    if (foundCharCode !== -1) {
      decodedMessage += String.fromCharCode(foundCharCode);
    } else {
      // Handle cases where a character might not be found (e.g., corrupted data)
      // For simplicity, we'll use a placeholder.
      decodedMessage += '?';
    }
  }
  return decodedMessage;
}

module.exports = {
  encodeMessage,
  decodeMessage
};
