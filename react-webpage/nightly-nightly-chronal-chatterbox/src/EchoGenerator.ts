export interface TemporalEcho {
  id: string;
  message: string;
  frequency: string;
  timestamp: number;
}

const echoPools: { [key: string]: string[] } = {
  'Whimsical Wisdom': [
    "A forgotten giggle echoes from the 3rd Tuesday of last month.",
    "The secret to eternal youth was briefly whispered in 1888, then lost.",
    "Beware the sentient dust bunnies of Sector Gamma-7.",
    "Did you remember to feed the time-traveling goldfish?",
    "The universe hums a lullaby, if you listen closely enough.",
    "Yesterday's coffee tasted of tomorrow's regrets."
  ],
  'Temporal Trivia': [
    "The first recorded instance of a 'Monday feeling' was in 1452.",
    "Butterflies in the year 2042 will have iridescent wings.",
    "The average human spends 3.7 years waiting for progress bars.",
    "Before clocks, time was measured in 'how many naps until dinner'.",
    "The concept of 'soon' varies wildly across parallel dimensions.",
    "A sock went missing in the dryer. It's now a sentient entity in another timeline."
  ],
  'Void Whispers': [
    "The silence between thoughts holds infinite possibilities.",
    "A faint hum from the edge of existence... or is it just the fridge?",
    "What if the void whispers back?",
    "The shadows know more than they let on.",
    "Existence is but a fleeting spark in the cosmic dark.",
    "Listen closely. The universe is trying to tell you something."
  ]
};

export const frequencies = Object.keys(echoPools);

export function generateEcho(frequency: string): TemporalEcho {
  const pool = echoPools[frequency] || echoPools['Whimsical Wisdom'];
  const message = pool[Math.floor(Math.random() * pool.length)];
  return {
    id: `echo-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`,
    message,
    frequency,
    timestamp: Date.now()
  };
}
