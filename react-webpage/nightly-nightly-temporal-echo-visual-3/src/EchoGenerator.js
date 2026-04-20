const whimsicalPrefixes = [
  "Whisper of", "Echo from", "Temporal Ripple of", "Distortion of",
  "Phantom of", "Glimmer of", "Resonance of", "Flicker of",
  "Shadow of", "Aura of", "Vibration of"
];

const whimsicalSuffixes = [
  "past", "future", "void", "ether", "dream", "memory", "oblivion", "stardust",
  "chronos", "aether", "the beyond"
];

const wordReplacements = {
  "time": ["chronos", "epoch", "era", "moment"],
  "space": ["void", "cosmos", "expanse", "infinity"],
  "world": ["realm", "dimension", "plane", "sphere"],
  "life": ["essence", "spark", "existence", "vitality"],
  "death": ["oblivion", "cessation", "terminus", "fade"]
};

/**
 * Generates a set of whimsical temporal echoes from a given phrase.
 * @param {string} phrase The input phrase.
 * @param {number} count The number of echoes to generate.
 * @returns {string[]} An array of generated echo phrases.
 */
export const generateEchoes = (phrase, count = 5) => {
  if (!phrase || phrase.trim() === "") {
    return [];
  }

  const basePhrase = phrase.trim();
  const echoes = new Set(); // Use a Set to avoid duplicates

  // Add the original phrase as one of the echoes (or a slightly modified version)
  echoes.add(`The Original: "${basePhrase}"`);

  while (echoes.size < count) {
    let currentEcho = basePhrase;
    const randomizer = Math.random();

    if (randomizer < 0.3) {
      // 30% chance: Add a whimsical prefix
      const prefix = whimsicalPrefixes[Math.floor(Math.random() * whimsicalPrefixes.length)];
      currentEcho = `${prefix} the "${basePhrase}"`;
    } else if (randomizer < 0.6) {
      // 30% chance: Add a whimsical suffix
      const suffix = whimsicalSuffixes[Math.floor(Math.random() * whimsicalSuffixes.length)];
      currentEcho = `"${basePhrase}" from the ${suffix}`;
    } else if (randomizer < 0.8) {
      // 20% chance: Replace a word
      const words = basePhrase.split(/\s+/);
      const replaceableWords = words.filter(word => Object.keys(wordReplacements).includes(word.toLowerCase()));
      if (replaceableWords.length > 0) {
        const wordToReplace = replaceableWords[Math.floor(Math.random() * replaceableWords.length)];
        const replacements = wordReplacements[wordToReplace.toLowerCase()];
        const replacement = replacements[Math.floor(Math.random() * replacements.length)];
        currentEcho = words.map(word => word.toLowerCase() === wordToReplace.toLowerCase() ? replacement : word).join(" ");
        currentEcho = `Shifted: "${currentEcho}"`;
      } else {
        // Fallback if no replaceable words
        currentEcho = `Faint echo of "${basePhrase}"`;
      }
    } else {
      // 20% chance: Simple distortion (e.g., reversing a word, adding a slight alteration)
      const words = basePhrase.split(/\s+/);
      if (words.length > 0) {
        const wordIndex = Math.floor(Math.random() * words.length);
        const word = words[wordIndex];
        const distortedWord = word.split('').reverse().join(''); // Simple reverse
        words[wordIndex] = distortedWord;
        currentEcho = `Distorted: "${words.join(" ")}"`;
      } else {
        currentEcho = `Whisper: "${basePhrase}"`;
      }
    }
    echoes.add(currentEcho);
  }

  return Array.from(echoes).slice(0, count); // Ensure we return exactly 'count' items
};
