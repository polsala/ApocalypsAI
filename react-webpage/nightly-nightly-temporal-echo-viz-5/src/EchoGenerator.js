// src/EchoGenerator.js

/**
 * Generates a deterministic "echo" of a phrase based on a given timeline.
 * This module is designed to be pure and easily testable.
 */
const EchoGenerator = {
  /**
   * Generates a hash from a string for deterministic randomness.
   * @param {string} str The input string.
   * @returns {number} A simple numeric hash.
   */
  _stringHash(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      const char = str.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash |= 0; // Convert to 32bit integer
    }
    return Math.abs(hash);
  },

  /**
   * Applies a wasteland-themed distortion to the text.
   * @param {string} text The input text.
   * @param {number} seed A numeric seed for deterministic results.
   * @returns {string} The distorted text.
   */
  wastelandWhisper(text, seed) {
    if (!text) return '';
    let result = '';
    const words = text.split(/\s+/);
    const rng = (s) => () => {
      s = (s * 9301 + 49297) % 233280;
      return s / 233280;
    };
    const random = rng(seed);

    for (let i = 0; i < words.length; i++) {
      let word = words[i];
      if (word.length > 0) {
        if (random() < 0.3) { // 30% chance to drop a word
          continue;
        }
        if (random() < 0.4) { // 40% chance to shorten/scramble
          word = word.slice(0, Math.max(1, Math.floor(word.length * (0.5 + random() * 0.5))));
          if (word.length > 2 && random() < 0.5) {
            word = word.split('').sort(() => 0.5 - random()).join(''); // Scramble
          }
        }
        if (random() < 0.2) { // 20% chance to add grit
          word += (random() < 0.5 ? '.' : '*');
        }
        result += word + ' ';
      }
    }
    return result.trim().replace(/\s+/g, ' ').replace(/(\w)\./g, '$1.').replace(/(\w)\*/g, '$1*') || '...dust...';
  },

  /**
   * Applies a verdant-themed distortion to the text.
   * @param {string} text The input text.
   * @param {number} seed A numeric seed for deterministic results.
   * @returns {string} The distorted text.
   */
  verdantResonance(text, seed) {
    if (!text) return '';
    const natureWords = ['bloom', 'leaf', 'root', 'vine', 'petal', 'moss', 'dew', 'grove', 'sprout', 'tendril'];
    const rng = (s) => () => {
      s = (s * 9301 + 49297) % 233280;
      return s / 233280;
    };
    const random = rng(seed);

    let result = text.split('').map(char => {
      if (char.match(/[a-zA-Z]/) && random() < 0.15) { // 15% chance to replace with a flowery char
        const replacements = ['🌿', '🍃', '🌸', '🌼', '🌱', '🌳'];
        return replacements[Math.floor(random() * replacements.length)];
      }
      return char;
    }).join('');

    const words = result.split(/\s+/);
    let finalWords = [];
    for (let i = 0; i < words.length; i++) {
      finalWords.push(words[i]);
      if (random() < 0.25) { // 25% chance to insert a nature word
        finalWords.push(natureWords[Math.floor(random() * natureWords.length)]);
      }
    }
    return finalWords.join(' ').replace(/\s+/g, ' ').trim() || '...nature\'s embrace...';
  },

  /**
   * Applies a cybernetic-themed distortion to the text.
   * @param {string} text The input text.
   * @param {number} seed A numeric seed for deterministic results.
   * @returns {string} The distorted text.
   */
  cyberneticGlitch(text, seed) {
    if (!text) return '';
    const glitchChars = ['#', '$', '%', '&', '*', '!', '?', '/', '\\', '0', '1'];
    const rng = (s) => () => {
      s = (s * 9301 + 49297) % 233280;
      return s / 233280;
    };
    const random = rng(seed);

    let result = text.split('').map(char => {
      if (char.match(/[a-zA-Z0-9]/) && random() < 0.2) { // 20% chance to glitch a char
        return glitchChars[Math.floor(random() * glitchChars.length)];
      }
      if (random() < 0.05) { // 5% chance to insert a binary fragment
        return (random() < 0.5 ? '0' : '1');
      }
      return char;
    }).join('');

    if (random() < 0.3) { // 30% chance to add a prefix/suffix glitch
      result = (random() < 0.5 ? '[[ERROR]] ' : '>>> ') + result + (random() < 0.5 ? ' [[/END]]' : ' <<<');
    }

    return result.replace(/\s+/g, ' ').trim() || '...[SYSTEM_CORRUPT]...';
  },

  /**
   * Main function to generate echoes for all timelines.
   * @param {string} phrase The input phrase.
   * @returns {{wasteland: string, verdant: string, cybernetic: string}} An object with echoes for each timeline.
   */
  generateEchoes(phrase) {
    const baseSeed = this._stringHash(phrase);
    return {
      wasteland: this.wastelandWhisper(phrase, baseSeed + 1),
      verdant: this.verdantResonance(phrase, baseSeed + 2),
      cybernetic: this.cyberneticGlitch(phrase, baseSeed + 3),
    };
  }
};

export default EchoGenerator;
