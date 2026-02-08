/**
 * @file TemporalProcessor.js
 * @brief Core logic for generating temporal echoes and calculating stability.
 * This module provides deterministic functions for text manipulation to simulate
 * 'temporal distortions' and a simple heuristic for 'temporal stability'.
 */

/**
 * Applies a simple character shift to the text.
 * @param {string} text - The input text.
 * @param {number} shift - The amount to shift characters.
 * @returns {string} The shifted text.
 */
const charShift = (text, shift) => {
  return text.split('').map(char => {
    if (char.match(/[a-zA-Z]/)) {
      const base = char === char.toLowerCase() ? 'a'.charCodeAt(0) : 'A'.charCodeAt(0);
      return String.fromCharCode(((char.charCodeAt(0) - base + shift) % 26 + 26) % 26 + base);
    }
    return char;
  }).join('');
};

/**
 * Reverses words in the text based on an index.
 * @param {string} text - The input text.
 * @param {number} index - A deterministic index to decide which words to reverse.
 * @returns {string} The text with some words reversed.
 */
const wordReverse = (text, index) => {
  return text.split(' ').map((word, i) => {
    if (i % (index + 2) === 0 && word.length > 2) {
      return word.split('').reverse().join('');
    }
    return word;
  }).join(' ');
};

/**
 * Adds or removes 'void' characters (e.g., '~', '#', '@') to the text.
 * @param {string} text - The input text.
 * @param {number} density - A deterministic density factor.
 * @returns {string} The text with added/removed void characters.
 */
const voidInterference = (text, density) => {
  const voidChars = ['~', '#', '@', '%', '&', '$'];
  let result = '';
  for (let i = 0; i < text.length; i++) {
    result += text[i];
    if (i % (density + 3) === 0 && density < 3) { // Add void chars more for lower density
      result += voidChars[i % voidChars.length];
    } else if (i % (density + 5) === 0 && density >= 3) { // Occasionally remove for higher density
        // Skip adding the char
    }
  }
  return result;
};

/**
 * Generates a series of 'temporal echoes' from an original text.
 * Each echo applies a different, deterministic distortion.
 * @param {string} originalText - The initial text to echo.
 * @param {number} numEchoes - The number of echoes to generate.
 * @returns {Array<Object>} An array of echo objects, each with text and style properties.
 */
export const generateEchoes = (originalText, numEchoes) => {
  if (!originalText) return [];

  const echoes = [];
  let currentText = originalText;

  // Echo 0: Original, slightly faded
  echoes.push({
    text: currentText,
    style: { opacity: 0.8, filter: 'blur(0.5px)', transform: 'translateX(0px)' }
  });

  // Subsequent echoes apply increasing distortion
  for (let i = 1; i < numEchoes; i++) {
    let distortedText = currentText;
    let opacity = 0.8 - (i * 0.1);
    let blur = 0.5 + (i * 0.5);
    let translateX = i * 5;
    let scale = 1 - (i * 0.02);

    // Apply deterministic transformations based on echo index
    if (i % 3 === 1) {
      distortedText = charShift(distortedText, i);
    } else if (i % 3 === 2) {
      distortedText = wordReverse(distortedText, i);
    } else {
      distortedText = voidInterference(distortedText, i);
    }

    // Add some random casing for flavor, but deterministically based on index
    if (i % 2 === 0) {
      distortedText = distortedText.split('').map((char, idx) => idx % 2 === 0 ? char.toLowerCase() : char.toUpperCase()).join('');
    } else {
      distortedText = distortedText.split('').map((char, idx) => idx % 3 === 0 ? char.toUpperCase() : char.toLowerCase()).join('');
    }

    echoes.push({
      text: distortedText,
      style: {
        opacity: Math.max(0.1, opacity),
        filter: `blur(${blur}px)`,
        transform: `translateX(${translateX}px) scale(${scale})`,
        fontStyle: i % 2 === 0 ? 'italic' : 'normal',
        textShadow: `0 0 ${i * 2}px rgba(100, 200, 255, ${opacity})`
      }
    });
    currentText = distortedText; // Each echo builds on the previous one
  }

  return echoes;
};

/**
 * Calculates a 'temporal stability' score for the given text.
 * This is a whimsical heuristic: longer and more complex texts are less stable.
 * @param {string} text - The input text.
 * @returns {number} A stability score between 0 and 100.
 */
export const calculateStability = (text) => {
  if (!text) return 100;
  const lengthPenalty = text.length * 0.5; // Longer text, less stable
  const wordCountPenalty = (text.split(/\s+/).filter(word => word.length > 0).length - 1) * 2; // More words, less stable
  const uniqueCharPenalty = new Set(text.toLowerCase()).size * 0.5; // More unique chars, less stable

  let stability = 100 - lengthPenalty - wordCountPenalty - uniqueCharPenalty;
  return Math.max(0, Math.min(100, stability));
};
