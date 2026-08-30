interface DecipherResult {
  chime: string;
  advice: string;
}

const CHIMES: string[] = [
  "The Whispering Sands Hum",
  "A Glimmer in the Temporal Fog",
  "The Echo of a Forgotten Dawn",
  "Starlight Sings a Silent Tune",
  "The Void's Gentle Murmur",
  "Chronos's Clock Ticks Softly",
  "A Ripple in the Aether Stream",
  "The Cosmic Loom Weaves",
  "Moonbeam's Secret Message",
  "The Sunken City's Bell Tolls",
];

const ADVICE: string[] = [
  "Seek wisdom in the smallest grain of truth, or perhaps a well-preserved pickle.",
  "The path ahead is clear, if you only remember where you left your spectacles.",
  "Embrace the unexpected; it often hides the best snacks.",
  "A stitch in time saves nine, but a well-timed nap saves your sanity.",
  "Listen to the void, but double-check if it's just your stomach rumbling.",
  "Your destiny awaits, probably behind that dusty old bookshelf.",
  "Plant a seed of kindness, or a really robust potato.",
  "The answer lies within, or possibly under the couch cushions.",
  "Don't forget your towel, for the journey is long and spills are inevitable.",
  "Today's mystery is tomorrow's anecdote. Or a really good excuse.",
];

/**
 * Generates a simple numeric hash from a string input.
 * This ensures deterministic selection from the lists.
 */
function generateDeterministicHash(input: string): number {
  let hash = 0;
  for (let i = 0; i < input.length; i++) {
    const char = input.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash |= 0; // Convert to 32bit integer
  }
  return Math.abs(hash); // Ensure positive
}

export function decipherChronoChime(input: string): DecipherResult {
  if (!input || input.trim() === '') {
    return {
      chime: "The Silent Void",
      advice: "No input, no prophecy. Perhaps the universe is just shy today.",
    };
  }

  const hash = generateDeterministicHash(input);

  const chimeIndex = hash % CHIMES.length;
  const adviceIndex = (hash + 7) % ADVICE.length; // Offset to get different advice

  return {
    chime: CHIMES[chimeIndex],
    advice: ADVICE[adviceIndex],
  };
}
