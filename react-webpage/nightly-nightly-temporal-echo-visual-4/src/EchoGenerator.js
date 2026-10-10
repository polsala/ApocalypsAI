/**
 * @typedef {Object} Echo
 * @property {string} type - The type of temporal distortion (e.g., "Glitched", "Poetic", "Absurd").
 * @property {string} text - The distorted text.
 */

/**
 * Generates various "echoes" of an input phrase, simulating temporal distortions.
 * @param {string} phrase - The input phrase to distort.
 * @returns {Echo[]} An array of generated echoes.
 */
export function generateEchoes(phrase) {
  const echoes = [];
  const lowerPhrase = phrase.toLowerCase();

  // Glitched Echo
  const glitchedText = phrase
    .split('')
    .map((char, i) => (Math.random() < 0.15 ? String.fromCharCode(char.charCodeAt(0) + Math.floor(Math.random() * 5) - 2) : char))
    .join('')
    .replace(/[aeiou]/g, (vowel) => (Math.random() < 0.3 ? vowel + '.' : vowel))
    .replace(/ /g, (space) => (Math.random() < 0.2 ? '_' : space));
  echoes.push({ type: 'Glitched Echo', text: `[STATIC] g.l.i.t.c.h.e.d... g.l.i.t.c.h.e.d... ${glitchedText}` });

  // Poetic Echo
  const poeticText = `The whispers of "${phrase}" drift through the cosmic dust, a forgotten melody in the void's embrace. It speaks of what was, what is, and what might yet be, a fragile truth held by the dying light of stars.`;
  echoes.push({ type: 'Poetic Echo', text: poeticText });

  // Absurd Echo
  const absurdModifiers = [
    'a sentient toaster once declared',
    'the last squirrel remembered',
    'etched on the moon cheese',
    'whispered by a rogue satellite',
    'found in a can of expired beans',
  ];
  const absurdText = `In the year 3042, ${absurdModifiers[Math.floor(Math.random() * absurdModifiers.length)]}: "${phrase}" became the sacred chant of the rubber duck cult.`;
  echoes.push({ type: 'Absurd Echo', text: absurdText });

  // Future History Echo
  const futureHistoryText = `Historical records from the Neo-Archivist Guild indicate that the phrase "${phrase}" was a pivotal pre-Collapse meme, often associated with the 'Great Internet Purge' of 2077. Its true meaning remains debated.`;
  echoes.push({ type: 'Future History Echo', text: futureHistoryText });

  // Distorted Meaning Echo (simple keyword replacement)
  let distortedMeaningText = phrase;
  const distortions = {
    'hope': 'illusion', 'future': 'void', 'peace': 'stasis', 'love': 'resource',
    'life': 'cycle', 'death': 'transition', 'survive': 'adapt', 'build': 'repurpose'
  };
  for (const [key, value] of Object.entries(distortions)) {
    distortedMeaningText = distortedMeaningText.replace(new RegExp(`\\b${key}\\b`, 'gi'), value);
  }
  if (distortedMeaningText !== phrase) {
    echoes.push({ type: 'Distorted Meaning Echo', text: `A fragmented transmission reveals: "${distortedMeaningText}"` });
  }

  return echoes;
}
